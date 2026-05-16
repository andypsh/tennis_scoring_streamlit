import { defineStore } from 'pinia'
import { hasSupabase } from '@/lib/supabase'
import {
  emptyScores,
  EVENT_KEYS,
  type BracketNode,
  type EventKey,
  type Group,
  type Match,
  type Player,
} from '@/types/domain'
import { generateKnockoutBracket, generateRoundRobin, evaluateBracketNode, propagateWinner } from '@/lib/bracket'
import { evaluateMatch } from '@/lib/scoring'
import {
  ensureTournament,
  pullSnapshot,
  pushGroups,
  pushMatches,
  pushPlayers,
  subscribeRealtime,
} from '@/lib/sync'

const STORAGE_KEY = 'cj_tennis_state_v1'

interface PersistedState {
  tournamentId: string
  tournamentName: string
  format: 'tournament' | 'friendly'
  groups: Group[]
  players: Player[]
  matches: Match[]
  bracket: BracketNode[]
  advancePerGroup: number
  online: boolean
  syncing: boolean
  lastSyncedAt: string | null
}

function emptyState(): PersistedState {
  return {
    tournamentId: 'local',
    tournamentName: 'CJ 테니스',
    format: 'tournament',
    groups: [],
    players: [],
    matches: [],
    bracket: [],
    advancePerGroup: 2,
    online: false,
    syncing: false,
    lastSyncedAt: null,
  }
}

let unsubscribeRealtime: (() => void) | null = null
let suppressRealtime = false

export const useTournamentStore = defineStore('tournament', {
  state: (): PersistedState => emptyState(),
  getters: {
    teams(): string[] {
      const set = new Set<string>()
      for (const p of this.players) set.add(p.team)
      for (const g of this.groups) for (const t of g.teams) set.add(t)
      return [...set].sort()
    },
    groupOf(): (team: string) => string | null {
      return (team: string) => {
        for (const g of this.groups) if (g.teams.includes(team)) return g.name
        return null
      }
    },
    poolForEvent(): (team: string, event: EventKey, exclude: string[]) => string[] {
      return (team, event, exclude) => {
        const gender = event === '여복' ? '여' : '남'
        return this.players
          .filter(p => p.team === team && p.gender === gender && !exclude.includes(p.name))
          .map(p => p.name)
      }
    },
  },
  actions: {
    async loadAll() {
      // 로컬 캐시 먼저 적용 (오프라인에서도 빠르게 시작)
      const raw = localStorage.getItem(STORAGE_KEY)
      if (raw) {
        try {
          this.$patch(JSON.parse(raw) as PersistedState)
        } catch {
          /* ignore */
        }
      }

      if (!hasSupabase) return

      try {
        this.syncing = true
        const id = await ensureTournament()
        this.tournamentId = id
        const snap = await pullSnapshot()
        if (snap) {
          suppressRealtime = true
          this.groups = snap.groups
          this.players = snap.players
          this.matches = snap.matches
          this.bracket = snap.bracket
          suppressRealtime = false
        }
        this.online = true
        this.lastSyncedAt = new Date().toISOString()
        this.persist()
        unsubscribeRealtime?.()
        unsubscribeRealtime = subscribeRealtime(this.tournamentId, {
          onChange: () => {
            if (suppressRealtime) return
            this.refreshFromRemote()
          },
        })
      } catch (e) {
        console.warn('[sync] pull failed, falling back to local cache', e)
        this.online = false
      } finally {
        this.syncing = false
      }
    },
    async refreshFromRemote() {
      if (!hasSupabase) return
      const snap = await pullSnapshot()
      if (!snap) return
      suppressRealtime = true
      this.tournamentId = snap.tournamentId
      this.groups = snap.groups
      this.players = snap.players
      this.matches = snap.matches
      this.bracket = snap.bracket
      this.lastSyncedAt = new Date().toISOString()
      suppressRealtime = false
      this.persist()
    },
    persist() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.$state))
    },
    reset() {
      unsubscribeRealtime?.()
      unsubscribeRealtime = null
      this.$patch(emptyState())
      this.persist()
    },
    importPlayers(rows: Array<Partial<Player> & { 이름?: string; 소속?: string; 성별?: string; 구력?: number; ntrp?: number }>) {
      const players: Player[] = rows
        .map((r, idx) => ({
          id: `p_${Date.now()}_${idx}`,
          name: (r.name ?? r.이름 ?? '').toString().trim(),
          team: (r.team ?? r.소속 ?? '').toString().trim(),
          gender: ((r.gender ?? r.성별 ?? '남').toString().trim().startsWith('여') ? '여' : '남') as '남' | '여',
          ntrp: typeof r.ntrp === 'number' ? r.ntrp : null,
          career_years: typeof r.구력 === 'number' ? r.구력 : (typeof r.career_years === 'number' ? r.career_years : null),
        }))
        .filter(p => p.name && p.team)
      this.players = players
      this.persist()
      void this.flushRemote('players')
    },
    setGroups(groups: Group[]) {
      this.groups = groups.filter(g => g.teams.length > 0)
      this.matches = generateRoundRobin(this.tournamentId, this.groups)
      this.bracket = []
      this.persist()
      void this.flushRemote('groups')
      void this.flushRemote('matches')
    },
    updateMatchScore(matchId: string, event: EventKey, payload: { home: number; away: number; homePlayers: string[]; awayPlayers: string[]; finalized: boolean }) {
      const m = this.matches.find(x => x.id === matchId)
      if (!m) return
      m.scores[event] = {
        home: payload.home,
        away: payload.away,
        homePlayers: payload.homePlayers,
        awayPlayers: payload.awayPlayers,
      }
      m.finalized = payload.finalized
      const { homeWonEvents, awayWonEvents } = evaluateMatch(m.scores)
      if (homeWonEvents >= 2) m.winner = m.home
      else if (awayWonEvents >= 2) m.winner = m.away
      else m.winner = null
      this.persist()
      void this.flushRemote('matches')
    },
    generateBracket(opts: { advancePerGroup?: number } = {}) {
      const advancePerGroup = opts.advancePerGroup ?? this.advancePerGroup
      this.advancePerGroup = advancePerGroup
      this.bracket = generateKnockoutBracket(this.tournamentId, this.groups, this.matches, { advancePerGroup })
      this.persist()
      void this.flushRemote('matches')
    },
    updateBracketScore(nodeId: string, event: EventKey, payload: { home: number; away: number; homePlayers: string[]; awayPlayers: string[]; finalized: boolean }) {
      const node = this.bracket.find(n => n.id === nodeId)
      if (!node) return
      node.scores[event] = { ...payload }
      node.finalized = payload.finalized
      const { homeWins, awayWins, winner } = evaluateBracketNode(node)
      node.homeWins = homeWins
      node.awayWins = awayWins
      node.winner = winner
      if (winner) propagateWinner(this.bracket, node)
      this.persist()
      void this.flushRemote('matches')
    },
    clearScores() {
      for (const m of this.matches) {
        m.scores = emptyScores()
        m.finalized = false
        m.winner = null
      }
      for (const n of this.bracket) {
        n.scores = emptyScores()
        n.finalized = false
        n.winner = null
        n.homeWins = 0
        n.awayWins = 0
      }
      this.persist()
      void this.flushRemote('matches')
    },
    async flushRemote(target: 'players' | 'groups' | 'matches') {
      if (!hasSupabase || !this.tournamentId || this.tournamentId === 'local') return
      try {
        this.syncing = true
        suppressRealtime = true
        if (target === 'players') await pushPlayers(this.tournamentId, this.players)
        if (target === 'groups') await pushGroups(this.tournamentId, this.groups)
        if (target === 'matches') await pushMatches(this.tournamentId, this.matches, this.bracket)
        this.online = true
        this.lastSyncedAt = new Date().toISOString()
      } catch (e) {
        console.warn(`[sync] push ${target} failed`, e)
        this.online = false
      } finally {
        suppressRealtime = false
        this.syncing = false
      }
    },
  },
})

export { EVENT_KEYS }

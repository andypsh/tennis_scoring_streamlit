import { defineStore } from 'pinia'
import { hasSupabase, supabase } from '@/lib/supabase'
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
  }
}

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
      if (hasSupabase && supabase) {
        // TODO: 서버 동기화 — 1차에서는 로컬만 사용
      }
      const raw = localStorage.getItem(STORAGE_KEY)
      if (raw) {
        try {
          const parsed = JSON.parse(raw) as PersistedState
          this.$patch(parsed)
        } catch {
          /* ignore */
        }
      }
    },
    persist() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.$state))
    },
    reset() {
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
    },
    setGroups(groups: Group[]) {
      this.groups = groups.filter(g => g.teams.length > 0)
      this.matches = generateRoundRobin(this.tournamentId, this.groups)
      this.bracket = []
      this.persist()
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
    },
    generateBracket(opts: { advancePerGroup?: number } = {}) {
      const advancePerGroup = opts.advancePerGroup ?? this.advancePerGroup
      this.advancePerGroup = advancePerGroup
      this.bracket = generateKnockoutBracket(this.tournamentId, this.groups, this.matches, { advancePerGroup })
      this.persist()
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
    },
  },
})

export { EVENT_KEYS }

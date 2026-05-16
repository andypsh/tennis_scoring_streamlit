import { hasSupabase, supabase } from './supabase'
import { emptyScores, type BracketNode, type Group, type Match, type Player } from '@/types/domain'

const DEFAULT_TOURNAMENT_ID = '00000000-0000-0000-0000-000000000001'

export interface SyncSnapshot {
  tournamentId: string
  groups: Group[]
  players: Player[]
  matches: Match[]
  bracket: BracketNode[]
}

/**
 * Supabase에서 현재 대회 상태를 불러온다.
 * 데이터가 없으면 빈 스냅샷을 반환.
 */
export async function pullSnapshot(): Promise<SyncSnapshot | null> {
  if (!hasSupabase || !supabase) return null

  let tournamentId = DEFAULT_TOURNAMENT_ID
  const { data: tourn } = await supabase
    .from('tournaments')
    .select('id')
    .order('created_at', { ascending: false })
    .limit(1)
    .maybeSingle()
  if (tourn?.id) tournamentId = tourn.id

  const [{ data: groups }, { data: players }, { data: matches }] = await Promise.all([
    supabase.from('groups').select('name, teams').eq('tournament_id', tournamentId).order('name'),
    supabase.from('players').select('*').eq('tournament_id', tournamentId).order('team'),
    supabase.from('matches').select('*').eq('tournament_id', tournamentId).order('created_at'),
  ])

  const allMatches: Match[] = (matches ?? []).map(rowToMatch)
  const bracket: BracketNode[] = (matches ?? [])
    .filter(m => m.stage === 'ko')
    .map(rowToBracketNode)

  return {
    tournamentId,
    groups: (groups ?? []).map(g => ({ name: g.name as string, teams: (g.teams as string[]) ?? [] })),
    players: (players ?? []).map(rowToPlayer),
    matches: allMatches.filter(m => m.stage === 'group'),
    bracket,
  }
}

export async function pushPlayers(tournamentId: string, players: Player[]) {
  if (!hasSupabase || !supabase) return
  await supabase.from('players').delete().eq('tournament_id', tournamentId)
  if (!players.length) return
  await supabase.from('players').insert(
    players.map(p => ({
      tournament_id: tournamentId,
      name: p.name,
      team: p.team,
      gender: p.gender,
      ntrp: p.ntrp,
      career_years: p.career_years,
    })),
  )
}

export async function pushGroups(tournamentId: string, groups: Group[]) {
  if (!hasSupabase || !supabase) return
  await supabase.from('groups').delete().eq('tournament_id', tournamentId)
  if (!groups.length) return
  await supabase
    .from('groups')
    .insert(groups.map(g => ({ tournament_id: tournamentId, name: g.name, teams: g.teams })))
}

export async function pushMatches(tournamentId: string, matches: Match[], bracket: BracketNode[]) {
  if (!hasSupabase || !supabase) return
  await supabase.from('matches').delete().eq('tournament_id', tournamentId)
  const rows: Record<string, unknown>[] = []
  for (const m of matches) {
    rows.push({
      id: m.id,
      tournament_id: tournamentId,
      stage: 'group',
      group_name: m.groupName,
      home: m.home,
      away: m.away,
      scores: m.scores,
      finalized: m.finalized,
      winner: m.winner,
    })
  }
  for (const n of bracket) {
    rows.push({
      id: n.id,
      tournament_id: tournamentId,
      stage: 'ko',
      ko_label: n.label,
      ko_round: n.round,
      ko_position: n.position,
      home: n.home,
      away: n.away,
      scores: n.scores,
      finalized: n.finalized,
      winner: n.winner,
      feeds_home_from: n.feedsHomeFrom ?? null,
      feeds_away_from: n.feedsAwayFrom ?? null,
    })
  }
  if (rows.length) await supabase.from('matches').insert(rows)
}

export async function ensureTournament(name = 'CJ Tennis'): Promise<string> {
  if (!hasSupabase || !supabase) return DEFAULT_TOURNAMENT_ID
  const { data: existing } = await supabase
    .from('tournaments')
    .select('id')
    .order('created_at', { ascending: false })
    .limit(1)
    .maybeSingle()
  if (existing?.id) return existing.id as string
  const { data: created, error } = await supabase
    .from('tournaments')
    .insert({ name, format: 'tournament' })
    .select('id')
    .single()
  if (error) throw error
  return created.id as string
}

export interface RealtimeHandlers {
  onChange: () => void
}

export function subscribeRealtime(tournamentId: string, handlers: RealtimeHandlers): () => void {
  if (!hasSupabase || !supabase) return () => undefined
  const channel = supabase
    .channel(`tournament:${tournamentId}`)
    .on('postgres_changes', { event: '*', schema: 'public', table: 'matches', filter: `tournament_id=eq.${tournamentId}` }, handlers.onChange)
    .on('postgres_changes', { event: '*', schema: 'public', table: 'players', filter: `tournament_id=eq.${tournamentId}` }, handlers.onChange)
    .on('postgres_changes', { event: '*', schema: 'public', table: 'groups', filter: `tournament_id=eq.${tournamentId}` }, handlers.onChange)
    .subscribe()
  return () => {
    if (supabase) supabase.removeChannel(channel)
  }
}

// --- row mappers -----------------------------------------------------

function rowToMatch(r: Record<string, unknown>): Match {
  return {
    id: r.id as string,
    tournamentId: r.tournament_id as string,
    stage: r.stage as 'group' | 'ko',
    groupName: (r.group_name as string) ?? null,
    koLabel: (r.ko_label as string) ?? null,
    home: r.home as string,
    away: r.away as string,
    scores: (r.scores as Match['scores']) ?? emptyScores(),
    finalized: Boolean(r.finalized),
    winner: (r.winner as string) ?? null,
  }
}

function rowToBracketNode(r: Record<string, unknown>): BracketNode {
  const scores = (r.scores as BracketNode['scores']) ?? emptyScores()
  let homeWins = 0
  let awayWins = 0
  for (const ev of Object.values(scores)) {
    if (ev.home > ev.away) homeWins += 1
    else if (ev.away > ev.home) awayWins += 1
  }
  return {
    id: r.id as string,
    label: (r.ko_label as string) ?? '',
    round: (r.ko_round as number) ?? 1,
    position: (r.ko_position as number) ?? 0,
    home: r.home as string,
    away: r.away as string,
    homeWins,
    awayWins,
    winner: (r.winner as string) ?? null,
    scores,
    finalized: Boolean(r.finalized),
    feedsHomeFrom: (r.feeds_home_from as string) ?? undefined,
    feedsAwayFrom: (r.feeds_away_from as string) ?? undefined,
  }
}

function rowToPlayer(r: Record<string, unknown>): Player {
  return {
    id: r.id as string,
    name: r.name as string,
    team: r.team as string,
    gender: (r.gender as Player['gender']) ?? '남',
    ntrp: (r.ntrp as number) ?? null,
    career_years: (r.career_years as number) ?? null,
  }
}

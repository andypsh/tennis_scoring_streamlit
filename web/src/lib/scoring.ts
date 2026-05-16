import {
  EVENT_KEYS,
  type EventScores,
  type Match,
  type Standing,
} from '@/types/domain'

export interface EventOutcome {
  homeWonEvents: number
  awayWonEvents: number
  goalDiff: number
}

export function evaluateMatch(scores: EventScores): EventOutcome {
  let homeWonEvents = 0
  let awayWonEvents = 0
  let goalDiff = 0
  for (const ev of EVENT_KEYS) {
    const s = scores[ev]
    if (s.home > s.away) homeWonEvents += 1
    else if (s.away > s.home) awayWonEvents += 1
    goalDiff += s.home - s.away
  }
  return { homeWonEvents, awayWonEvents, goalDiff }
}

export function matchWinner(home: string, away: string, scores: EventScores): string | null {
  const { homeWonEvents, awayWonEvents } = evaluateMatch(scores)
  if (homeWonEvents >= 2) return home
  if (awayWonEvents >= 2) return away
  return null
}

export function calculateStandings(teams: string[], matches: Match[]): Standing[] {
  const rows: Standing[] = teams.map(team => ({
    team,
    played: 0,
    wins: 0,
    draws: 0,
    losses: 0,
    points: 0,
    goalDiff: 0,
  }))
  const byTeam = new Map(rows.map(r => [r.team, r]))

  for (const m of matches) {
    if (!m.finalized) continue
    const home = byTeam.get(m.home)
    const away = byTeam.get(m.away)
    if (!home || !away) continue
    const { homeWonEvents, awayWonEvents, goalDiff } = evaluateMatch(m.scores)
    home.played += 1
    away.played += 1
    home.goalDiff += goalDiff
    away.goalDiff -= goalDiff
    if (homeWonEvents === awayWonEvents) {
      home.draws += 1
      away.draws += 1
      home.points += 1
      away.points += 1
    } else if (homeWonEvents > awayWonEvents) {
      home.wins += 1
      away.losses += 1
      home.points += 3
    } else {
      away.wins += 1
      home.losses += 1
      away.points += 3
    }
  }

  return rows.sort((a, b) => {
    if (b.points !== a.points) return b.points - a.points
    if (b.goalDiff !== a.goalDiff) return b.goalDiff - a.goalDiff
    if (b.wins !== a.wins) return b.wins - a.wins
    return a.team.localeCompare(b.team)
  })
}

export type Gender = '남' | '여'
export type EventKey = '남단' | '남복' | '여복'
export const EVENT_KEYS: EventKey[] = ['남단', '남복', '여복']

export const EVENT_PLAYER_COUNT: Record<EventKey, number> = {
  남단: 1,
  남복: 2,
  여복: 2,
}

export const EVENT_GENDER: Record<EventKey, Gender> = {
  남단: '남',
  남복: '남',
  여복: '여',
}

export interface Player {
  id: string
  name: string
  team: string
  gender: Gender
  ntrp: number | null
  career_years: number | null
}

export interface EventScore {
  home: number
  away: number
  homePlayers: string[]
  awayPlayers: string[]
}

export type EventScores = Record<EventKey, EventScore>

export interface Match {
  id: string
  tournamentId: string
  stage: 'group' | 'ko'
  groupName: string | null
  koLabel: string | null
  home: string
  away: string
  scores: EventScores
  finalized: boolean
  winner: string | null
}

export interface Group {
  name: string
  teams: string[]
}

export interface Standing {
  team: string
  played: number
  wins: number
  draws: number
  losses: number
  points: number
  goalDiff: number
}

export interface Tournament {
  id: string
  name: string
  format: 'tournament' | 'friendly'
  groups: Group[]
  createdAt: string
}

export interface BracketNode {
  id: string
  label: string
  round: number
  position: number
  home: string
  away: string
  homeWins: number
  awayWins: number
  winner: string | null
  scores: EventScores
  finalized: boolean
  feedsHomeFrom?: string
  feedsAwayFrom?: string
}

export const emptyScores = (): EventScores => ({
  남단: { home: 0, away: 0, homePlayers: [], awayPlayers: [] },
  남복: { home: 0, away: 0, homePlayers: [], awayPlayers: [] },
  여복: { home: 0, away: 0, homePlayers: [], awayPlayers: [] },
})

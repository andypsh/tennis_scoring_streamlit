import {
  emptyScores,
  type BracketNode,
  type Group,
  type Match,
  type Standing,
} from '@/types/domain'
import { calculateStandings } from './scoring'

const uid = () => Math.random().toString(36).slice(2, 10)

/**
 * 각 조 안에서 라운드로빈 대진을 생성.
 * 같은 조 안의 모든 팀쌍이 한 번씩 맞붙는다.
 */
export function generateRoundRobin(
  tournamentId: string,
  groups: Group[],
): Match[] {
  const matches: Match[] = []
  for (const g of groups) {
    for (let i = 0; i < g.teams.length; i++) {
      for (let j = i + 1; j < g.teams.length; j++) {
        matches.push({
          id: uid(),
          tournamentId,
          stage: 'group',
          groupName: g.name,
          koLabel: null,
          home: g.teams[i],
          away: g.teams[j],
          scores: emptyScores(),
          finalized: false,
          winner: null,
        })
      }
    }
  }
  return matches
}

export interface SeedingOptions {
  /** 각 조에서 몇 등까지 본선 진출시킬지 (기본 2) */
  advancePerGroup: number
}

/**
 * 조별 순위 → 본선 시드 배정 + 빈 브래킷 생성.
 *
 * - advancePerGroup × groupCount 가 2의 거듭제곱이 아니면 가장 가까운
 *   상위 거듭제곱으로 올리고 부족분은 BYE 처리한다.
 * - 1라운드 매칭은 표준 시드 인터리브 (1 vs N, 2 vs N-1 …)이되,
 *   같은 조 1라운드 충돌은 피한다.
 */
export function generateKnockoutBracket(
  tournamentId: string,
  groups: Group[],
  matches: Match[],
  opts: SeedingOptions = { advancePerGroup: 2 },
): BracketNode[] {
  if (groups.length === 0) return []

  const seeded: { team: string; group: string; rank: number; placeholder: boolean }[] = []
  for (const g of groups) {
    const standings = calculateStandings(g.teams, matches)
    for (let r = 0; r < opts.advancePerGroup; r++) {
      const row: Standing | undefined = standings[r]
      seeded.push({
        team: row?.team ?? `${g.name} ${r + 1}위 대기`,
        group: g.name,
        rank: r + 1,
        placeholder: !row,
      })
    }
  }

  // 글로벌 시드 순위: rank 우선, 같은 rank 안에서는 조 이름 순
  seeded.sort((a, b) => (a.rank - b.rank) || a.group.localeCompare(b.group))

  const bracketSize = nextPowerOfTwo(seeded.length)
  while (seeded.length < bracketSize) {
    seeded.push({ team: 'BYE', group: '-', rank: 99, placeholder: true })
  }

  // 표준 시드 인터리브 — 1라운드 같은조 충돌 회피를 위해 후순위 시드 swap
  const pairings = standardSeedPairings(bracketSize)
  const firstRound: Array<[number, number]> = pairings.map(([a, b]) => [a - 1, b - 1])
  avoidSameGroupCollisions(firstRound, seeded)

  const totalRounds = Math.log2(bracketSize)
  const nodes: BracketNode[] = []
  const nodeIdByRoundPos: Record<string, string> = {}

  // 1라운드
  firstRound.forEach(([hi, ai], pos) => {
    const id = uid()
    nodeIdByRoundPos[`1:${pos}`] = id
    nodes.push({
      id,
      label: roundLabel(1, totalRounds),
      round: 1,
      position: pos,
      home: seeded[hi].team,
      away: seeded[ai].team,
      homeWins: 0,
      awayWins: 0,
      winner: null,
      scores: emptyScores(),
      finalized: false,
    })
  })

  // 이후 라운드
  for (let r = 2; r <= totalRounds; r++) {
    const matchesInRound = bracketSize / Math.pow(2, r)
    for (let pos = 0; pos < matchesInRound; pos++) {
      const id = uid()
      nodeIdByRoundPos[`${r}:${pos}`] = id
      const feedHomeKey = `${r - 1}:${pos * 2}`
      const feedAwayKey = `${r - 1}:${pos * 2 + 1}`
      nodes.push({
        id,
        label: roundLabel(r, totalRounds),
        round: r,
        position: pos,
        home: `${roundLabel(r - 1, totalRounds)} #${pos * 2 + 1} 승자`,
        away: `${roundLabel(r - 1, totalRounds)} #${pos * 2 + 2} 승자`,
        homeWins: 0,
        awayWins: 0,
        winner: null,
        scores: emptyScores(),
        finalized: false,
        feedsHomeFrom: nodeIdByRoundPos[feedHomeKey],
        feedsAwayFrom: nodeIdByRoundPos[feedAwayKey],
      })
    }
  }

  // BYE 자동 통과
  for (const n of nodes.filter(n => n.round === 1)) {
    if (n.home === 'BYE' || n.away === 'BYE') {
      n.winner = n.home === 'BYE' ? n.away : n.home
      n.finalized = true
      propagateWinner(nodes, n)
    }
  }

  return nodes
}

function nextPowerOfTwo(n: number): number {
  let p = 1
  while (p < n) p *= 2
  return Math.max(p, 2)
}

/**
 * 토너먼트 표준 시드 매칭.
 * 8명: (1,8)(4,5)(3,6)(2,7) 같은 패턴.
 */
function standardSeedPairings(size: number): Array<[number, number]> {
  let order = [1, 2]
  while (order.length < size) {
    const next: number[] = []
    const total = order.length * 2 + 1
    for (const s of order) {
      next.push(s)
      next.push(total - s)
    }
    order = next
  }
  const pairings: Array<[number, number]> = []
  for (let i = 0; i < order.length; i += 2) {
    pairings.push([order[i], order[i + 1]])
  }
  return pairings
}

function avoidSameGroupCollisions(
  pairings: Array<[number, number]>,
  seeded: { group: string; placeholder: boolean }[],
) {
  for (let i = 0; i < pairings.length; i++) {
    const [a, b] = pairings[i]
    if (seeded[a].placeholder || seeded[b].placeholder) continue
    if (seeded[a].group !== seeded[b].group) continue
    // 같은 조 충돌 → 뒤쪽 슬롯의 away와 swap
    for (let j = i + 1; j < pairings.length; j++) {
      const [c, d] = pairings[j]
      if (seeded[c].group !== seeded[a].group && seeded[d].group !== seeded[a].group) {
        pairings[i] = [a, d]
        pairings[j] = [c, b]
        break
      }
    }
  }
}

function roundLabel(round: number, totalRounds: number): string {
  const fromEnd = totalRounds - round
  switch (fromEnd) {
    case 0: return '결승'
    case 1: return '4강'
    case 2: return '8강'
    case 3: return '16강'
    case 4: return '32강'
    default: return `${round}라운드`
  }
}

export function propagateWinner(nodes: BracketNode[], updated: BracketNode) {
  if (!updated.winner) return
  for (const n of nodes) {
    if (n.feedsHomeFrom === updated.id) n.home = updated.winner
    if (n.feedsAwayFrom === updated.id) n.away = updated.winner
  }
}

export function evaluateBracketNode(node: BracketNode): { homeWins: number; awayWins: number; winner: string | null } {
  let homeWins = 0
  let awayWins = 0
  for (const ev of Object.values(node.scores)) {
    if (ev.home > ev.away) homeWins += 1
    else if (ev.away > ev.home) awayWins += 1
  }
  let winner: string | null = null
  if (homeWins >= 2) winner = node.home
  else if (awayWins >= 2) winner = node.away
  return { homeWins, awayWins, winner }
}

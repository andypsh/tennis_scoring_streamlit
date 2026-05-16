import type { Player } from '@/types/domain'

export interface Pair {
  players: [Player, Player]
  ratingSum: number
}

export interface DoublesMatchup {
  pairA: Pair
  pairB: Pair
  ratingGap: number
}

const rating = (p: Player) => p.ntrp ?? p.career_years ?? 3

/**
 * 짝수 명의 선수를 받아 라운드별 균형 페어 + 매치업을 만든다.
 *
 * 전략:
 *  1) NTRP(또는 구력)로 정렬
 *  2) 가장 강한 1명 + 가장 약한 1명을 한 페어로 묶어 라운드 내 페어 합을 평준화
 *  3) 만들어진 페어들을 합이 가까운 두 페어씩 매치업
 */
export function makeBalancedRound(players: Player[]): {
  pairs: Pair[]
  matchups: DoublesMatchup[]
} {
  if (players.length < 4 || players.length % 2 !== 0) {
    return { pairs: [], matchups: [] }
  }
  const sorted = [...players].sort((a, b) => rating(b) - rating(a))
  const pairs: Pair[] = []
  let i = 0
  let j = sorted.length - 1
  while (i < j) {
    const strong = sorted[i++]
    const weak = sorted[j--]
    pairs.push({
      players: [strong, weak],
      ratingSum: rating(strong) + rating(weak),
    })
  }
  const byStrength = [...pairs].sort((a, b) => b.ratingSum - a.ratingSum)
  const matchups: DoublesMatchup[] = []
  for (let k = 0; k < byStrength.length - 1; k += 2) {
    const a = byStrength[k]
    const b = byStrength[k + 1]
    if (!b) break
    matchups.push({
      pairA: a,
      pairB: b,
      ratingGap: Math.abs(a.ratingSum - b.ratingSum),
    })
  }
  return { pairs, matchups }
}

/**
 * 한 풀에서 여러 라운드를 돌릴 때, 이전 라운드 페어 조합은 가급적 피한다.
 * 시작점을 셔플해서 ratingGap의 합이 최소인 후보를 선택.
 */
export function makeMultipleRounds(players: Player[], rounds: number): {
  pairs: Pair[]
  matchups: DoublesMatchup[]
}[] {
  const result: ReturnType<typeof makeBalancedRound>[] = []
  const seenPairKeys = new Set<string>()

  for (let r = 0; r < rounds; r++) {
    let best: ReturnType<typeof makeBalancedRound> | null = null
    let bestScore = Infinity
    for (let trial = 0; trial < 24; trial++) {
      const shuffled = [...players]
      for (let i = shuffled.length - 1; i > 0; i--) {
        const k = Math.floor(Math.random() * (i + 1))
        ;[shuffled[i], shuffled[k]] = [shuffled[k], shuffled[i]]
      }
      const round = makeBalancedRound(shuffled)
      const reused = round.pairs.filter(p => seenPairKeys.has(pairKey(p))).length
      const gapTotal = round.matchups.reduce((s, m) => s + m.ratingGap, 0)
      const score = reused * 100 + gapTotal
      if (score < bestScore) {
        bestScore = score
        best = round
      }
    }
    if (!best) break
    best.pairs.forEach(p => seenPairKeys.add(pairKey(p)))
    result.push(best)
  }
  return result
}

function pairKey(p: Pair): string {
  return [p.players[0].id, p.players[1].id].sort().join('-')
}

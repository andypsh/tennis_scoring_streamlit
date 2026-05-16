<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useTournamentStore } from '@/stores/tournament'
import { EVENT_KEYS, EVENT_PLAYER_COUNT, type EventKey } from '@/types/domain'

const store = useTournamentStore()

const advancePerGroup = ref<number>(store.advancePerGroup)
function rebuild() {
  store.generateBracket({ advancePerGroup: advancePerGroup.value })
}

const rounds = computed(() => {
  const map = new Map<number, typeof store.bracket>()
  for (const n of store.bracket) {
    if (!map.has(n.round)) map.set(n.round, [] as any)
    map.get(n.round)!.push(n)
  }
  return [...map.entries()].sort((a, b) => a[0] - b[0]).map(([r, list]) => ({
    round: r,
    label: list[0]?.label ?? `${r}R`,
    nodes: list.sort((a, b) => a.position - b.position),
  }))
})

const selectedId = ref<string>('')
watch(() => store.bracket, list => {
  if (!list.find(n => n.id === selectedId.value)) selectedId.value = list[0]?.id ?? ''
}, { immediate: true })

const selected = computed(() => store.bracket.find(n => n.id === selectedId.value) ?? null)
const event = ref<EventKey>('남단')

const homePool = computed(() =>
  selected.value
    ? store.poolForEvent(selected.value.home, event.value,
        EVENT_KEYS.filter(k => k !== event.value).flatMap(k => selected.value!.scores[k].homePlayers))
    : [])
const awayPool = computed(() =>
  selected.value
    ? store.poolForEvent(selected.value.away, event.value,
        EVENT_KEYS.filter(k => k !== event.value).flatMap(k => selected.value!.scores[k].awayPlayers))
    : [])

const homePicks = ref<string[]>([])
const awayPicks = ref<string[]>([])
const homeScore = ref(0)
const awayScore = ref(0)
const finalize = ref(false)

watch([selected, event], () => {
  if (!selected.value) return
  const s = selected.value.scores[event.value]
  homePicks.value = [...s.homePlayers]
  awayPicks.value = [...s.awayPlayers]
  homeScore.value = s.home
  awayScore.value = s.away
  finalize.value = selected.value.finalized
}, { immediate: true })

const playerCount = computed(() => EVENT_PLAYER_COUNT[event.value])

function togglePick(side: 'home' | 'away', name: string) {
  const arr = side === 'home' ? homePicks : awayPicks
  if (arr.value.includes(name)) arr.value = arr.value.filter(n => n !== name)
  else if (arr.value.length < playerCount.value) arr.value = [...arr.value, name]
  else if (playerCount.value === 1) arr.value = [name]
}

function save() {
  if (!selected.value) return
  if (homePicks.value.length !== playerCount.value || awayPicks.value.length !== playerCount.value) return
  store.updateBracketScore(selected.value.id, event.value, {
    home: homeScore.value,
    away: awayScore.value,
    homePlayers: homePicks.value,
    awayPlayers: awayPicks.value,
    finalized: finalize.value,
  })
}
</script>

<template>
  <section class="space-y-4">
    <div class="card p-5">
      <h1 class="text-xl font-bold flex items-center gap-2">🎯 본선 대진표</h1>
      <p class="text-sm text-slate-500 mt-1">
        조별 라운드로빈 결과를 기반으로 시드를 매겨 빈 토너먼트 브래킷을 만듭니다.
      </p>
      <div class="mt-4 flex flex-wrap items-end gap-3">
        <label class="block">
          <span class="text-xs font-semibold text-slate-600">조당 진출 인원</span>
          <select v-model.number="advancePerGroup" class="input mt-1 w-32">
            <option :value="1">1팀</option>
            <option :value="2">2팀</option>
            <option :value="3">3팀</option>
            <option :value="4">4팀</option>
          </select>
        </label>
        <button class="btn-primary" :disabled="!store.groups.length" @click="rebuild">
          🚀 대진표 자동 생성
        </button>
        <span v-if="!store.groups.length" class="text-xs text-rose-500">조 편성이 먼저 필요해</span>
      </div>
    </div>

    <div v-if="!store.bracket.length" class="card p-10 text-center text-slate-400">
      아직 본선 대진이 없어. 위에서 <span class="font-semibold">대진표 자동 생성</span>을 눌러줘.
    </div>

    <div v-else class="card p-5 overflow-x-auto">
      <div class="flex gap-6 min-w-max">
        <div v-for="r in rounds" :key="r.round" class="flex flex-col gap-4 min-w-[200px]">
          <h3 class="font-bold text-center text-slate-700 sticky top-0 bg-white py-1">{{ r.label }}</h3>
          <div v-for="n in r.nodes" :key="n.id"
            class="rounded-xl border border-slate-200 bg-white shadow-sm cursor-pointer transition hover:shadow-md"
            :class="selectedId === n.id ? 'ring-2 ring-smash-500' : ''"
            @click="selectedId = n.id">
            <div class="bg-slate-800 text-white text-xs px-2 py-1 rounded-t-xl text-center font-semibold">
              {{ n.label }} #{{ n.position + 1 }}
            </div>
            <div class="px-3 py-2 flex justify-between items-center text-sm border-b border-slate-100"
              :class="n.winner === n.home ? 'font-bold text-emerald-700 bg-emerald-50' : ''">
              <span class="truncate">{{ n.home }}</span>
              <span class="font-mono text-blue-600">{{ n.homeWins }}</span>
            </div>
            <div class="px-3 py-2 flex justify-between items-center text-sm rounded-b-xl"
              :class="n.winner === n.away ? 'font-bold text-emerald-700 bg-emerald-50' : ''">
              <span class="truncate">{{ n.away }}</span>
              <span class="font-mono text-blue-600">{{ n.awayWins }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="selected" class="card p-5 space-y-3">
      <h2 class="font-bold">📝 {{ selected.label }} 점수 입력 — {{ selected.home }} vs {{ selected.away }}</h2>
      <div class="flex gap-2">
        <button v-for="ev in EVENT_KEYS" :key="ev" class="btn"
          :class="event === ev ? 'bg-smash-600 text-white' : 'bg-white border border-slate-200'"
          @click="event = ev">{{ ev }}</button>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div class="rounded-xl border border-slate-200 p-3">
          <div class="font-bold text-center bg-slate-100 rounded-lg py-1.5 mb-3">🏠 {{ selected.home }}</div>
          <div class="flex flex-wrap gap-1.5 min-h-[44px]">
            <button v-for="p in homePool" :key="p" class="px-2 py-1 rounded-full text-xs font-medium border"
              :class="homePicks.includes(p) ? 'bg-emerald-600 text-white border-emerald-600' : 'bg-white border-slate-200'"
              @click="togglePick('home', p)">{{ p }}</button>
          </div>
          <input v-model.number="homeScore" type="number" min="0" max="6" class="input mt-3" />
        </div>
        <div class="rounded-xl border border-slate-200 p-3">
          <div class="font-bold text-center bg-slate-100 rounded-lg py-1.5 mb-3">🚀 {{ selected.away }}</div>
          <div class="flex flex-wrap gap-1.5 min-h-[44px]">
            <button v-for="p in awayPool" :key="p" class="px-2 py-1 rounded-full text-xs font-medium border"
              :class="awayPicks.includes(p) ? 'bg-emerald-600 text-white border-emerald-600' : 'bg-white border-slate-200'"
              @click="togglePick('away', p)">{{ p }}</button>
          </div>
          <input v-model.number="awayScore" type="number" min="0" max="6" class="input mt-3" />
        </div>
      </div>

      <label class="flex items-center gap-2 text-sm">
        <input v-model="finalize" type="checkbox" class="rounded" />
        결과 확정 (다음 라운드로 승자 전파)
      </label>
      <div class="text-right">
        <button class="btn-primary" @click="save">💾 저장</button>
      </div>
    </div>
  </section>
</template>

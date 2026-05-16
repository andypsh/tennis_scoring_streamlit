<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useTournamentStore } from '@/stores/tournament'
import { EVENT_KEYS, EVENT_PLAYER_COUNT, type EventKey } from '@/types/domain'

const store = useTournamentStore()

const groupFilter = ref<string>('전체')
const filteredMatches = computed(() => {
  if (groupFilter.value === '전체') return store.matches.filter(m => m.stage === 'group')
  return store.matches.filter(m => m.stage === 'group' && m.groupName === groupFilter.value)
})

const selectedId = ref<string>('')
watch(filteredMatches, list => {
  if (!list.find(m => m.id === selectedId.value)) selectedId.value = list[0]?.id ?? ''
}, { immediate: true })

const selected = computed(() => store.matches.find(m => m.id === selectedId.value))
const event = ref<EventKey>('남단')

const eventOtherUsedHome = computed(() => {
  if (!selected.value) return [] as string[]
  return EVENT_KEYS.filter(k => k !== event.value).flatMap(k => selected.value!.scores[k].homePlayers)
})
const eventOtherUsedAway = computed(() => {
  if (!selected.value) return [] as string[]
  return EVENT_KEYS.filter(k => k !== event.value).flatMap(k => selected.value!.scores[k].awayPlayers)
})

const homePool = computed(() =>
  selected.value
    ? store.poolForEvent(selected.value.home, event.value, eventOtherUsedHome.value)
    : [])
const awayPool = computed(() =>
  selected.value
    ? store.poolForEvent(selected.value.away, event.value, eventOtherUsedAway.value)
    : [])

const playerCount = computed(() => EVENT_PLAYER_COUNT[event.value])

const homePicks = ref<string[]>([])
const awayPicks = ref<string[]>([])
const homeScore = ref(0)
const awayScore = ref(0)
const finalize = ref(false)
const message = ref<{ type: 'ok' | 'err'; text: string } | null>(null)

watch([selected, event], () => {
  if (!selected.value) return
  const s = selected.value.scores[event.value]
  homePicks.value = [...s.homePlayers]
  awayPicks.value = [...s.awayPlayers]
  homeScore.value = s.home
  awayScore.value = s.away
  finalize.value = selected.value.finalized
}, { immediate: true })

function togglePick(side: 'home' | 'away', name: string) {
  const arr = side === 'home' ? homePicks : awayPicks
  if (arr.value.includes(name)) {
    arr.value = arr.value.filter(n => n !== name)
  } else if (arr.value.length < playerCount.value) {
    arr.value = [...arr.value, name]
  } else if (playerCount.value === 1) {
    arr.value = [name]
  }
}

function save() {
  if (!selected.value) return
  if (homePicks.value.length !== playerCount.value || awayPicks.value.length !== playerCount.value) {
    message.value = { type: 'err', text: `${event.value}는 양 팀 각 ${playerCount.value}명을 선택해야 합니다` }
    return
  }
  store.updateMatchScore(selected.value.id, event.value, {
    home: homeScore.value,
    away: awayScore.value,
    homePlayers: homePicks.value,
    awayPlayers: awayPicks.value,
    finalized: finalize.value,
  })
  message.value = { type: 'ok', text: '저장 완료' }
  setTimeout(() => (message.value = null), 2000)
}
</script>

<template>
  <section class="space-y-4">
    <div v-if="!store.matches.length" class="card p-10 text-center text-slate-400">
      먼저 <RouterLink to="/standings" class="text-smash-600 font-semibold">조별순위</RouterLink>에서 조 편성을 완료해.
    </div>

    <template v-else>
      <div class="card p-4 space-y-3">
        <div class="flex flex-wrap gap-2">
          <button class="btn"
            :class="groupFilter === '전체' ? 'bg-slate-900 text-white' : 'bg-white border border-slate-200'"
            @click="groupFilter = '전체'">전체</button>
          <button v-for="g in store.groups" :key="g.name" class="btn"
            :class="groupFilter === g.name ? 'bg-slate-900 text-white' : 'bg-white border border-slate-200'"
            @click="groupFilter = g.name">{{ g.name }}</button>
        </div>

        <select v-model="selectedId" class="input">
          <option v-for="m in filteredMatches" :key="m.id" :value="m.id">
            [{{ m.groupName }}] {{ m.home }} vs {{ m.away }} {{ m.finalized ? '✅' : '' }}
          </option>
        </select>
      </div>

      <div v-if="selected" class="card p-5 space-y-4">
        <div class="flex gap-2">
          <button v-for="ev in EVENT_KEYS" :key="ev" class="btn"
            :class="event === ev ? 'bg-smash-600 text-white' : 'bg-white border border-slate-200'"
            @click="event = ev">
            {{ ev }} ({{ EVENT_PLAYER_COUNT[ev] }}명)
          </button>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div class="rounded-xl border border-slate-200 p-3">
            <div class="font-bold text-center bg-slate-100 rounded-lg py-1.5 mb-3">🏠 {{ selected.home }}</div>
            <div class="flex flex-wrap gap-1.5 min-h-[60px]">
              <button v-for="p in homePool" :key="p" class="px-2 py-1 rounded-full text-xs font-medium border"
                :class="homePicks.includes(p)
                  ? 'bg-emerald-600 text-white border-emerald-600'
                  : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'"
                @click="togglePick('home', p)">{{ p }}</button>
              <p v-if="!homePool.length" class="text-xs text-slate-400">출전 가능 선수 없음</p>
            </div>
            <label class="block mt-3">
              <span class="text-xs font-semibold text-slate-600">세트 스코어 (0–6)</span>
              <input v-model.number="homeScore" type="number" min="0" max="6" class="input mt-1" />
            </label>
          </div>

          <div class="rounded-xl border border-slate-200 p-3">
            <div class="font-bold text-center bg-slate-100 rounded-lg py-1.5 mb-3">🚀 {{ selected.away }}</div>
            <div class="flex flex-wrap gap-1.5 min-h-[60px]">
              <button v-for="p in awayPool" :key="p" class="px-2 py-1 rounded-full text-xs font-medium border"
                :class="awayPicks.includes(p)
                  ? 'bg-emerald-600 text-white border-emerald-600'
                  : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'"
                @click="togglePick('away', p)">{{ p }}</button>
              <p v-if="!awayPool.length" class="text-xs text-slate-400">출전 가능 선수 없음</p>
            </div>
            <label class="block mt-3">
              <span class="text-xs font-semibold text-slate-600">세트 스코어 (0–6)</span>
              <input v-model.number="awayScore" type="number" min="0" max="6" class="input mt-1" />
            </label>
          </div>
        </div>

        <label class="flex items-center gap-2 text-sm">
          <input v-model="finalize" type="checkbox" class="rounded" />
          이 매치 결과 확정 (조별 순위에 반영)
        </label>

        <div class="flex items-center justify-between">
          <p v-if="message" class="text-sm" :class="message.type === 'ok' ? 'text-emerald-600' : 'text-rose-600'">
            {{ message.text }}
          </p>
          <span v-else></span>
          <button class="btn-primary" @click="save">💾 저장</button>
        </div>
      </div>
    </template>
  </section>
</template>

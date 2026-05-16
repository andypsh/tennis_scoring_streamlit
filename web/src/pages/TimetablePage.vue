<script setup lang="ts">
import { computed, ref } from 'vue'
import { useTournamentStore } from '@/stores/tournament'

const store = useTournamentStore()

const courts = ref<number>(6)
const startTime = ref('08:00')
const slotMinutes = ref<number>(40)

interface Slot {
  time: string
  cells: Array<{ label: string; sub: string } | null>
}

function addMinutes(hhmm: string, minutes: number): string {
  const [h, m] = hhmm.split(':').map(Number)
  const total = h * 60 + m + minutes
  const nh = Math.floor(total / 60) % 24
  const nm = total % 60
  return `${String(nh).padStart(2, '0')}:${String(nm).padStart(2, '0')}`
}

const schedule = computed<Slot[]>(() => {
  const events: Array<{ label: string; sub: string }> = []

  // 1) 조별 라운드로빈을 종목별로 풀어서 칸 생성
  const groupMatches = store.matches.filter(m => m.stage === 'group')
  for (const m of groupMatches) {
    for (const ev of ['남단', '남복', '여복'] as const) {
      events.push({ label: `${m.home} vs ${m.away}`, sub: `${m.groupName} · ${ev}` })
    }
  }

  // 2) 본선 — 종목별로 풀어서
  const koMatches = store.bracket
  for (const n of koMatches) {
    for (const ev of ['남단', '남복', '여복'] as const) {
      events.push({ label: `${n.home} vs ${n.away}`, sub: `${n.label} · ${ev}` })
    }
  }

  if (!events.length) return []

  const slots: Slot[] = []
  let t = startTime.value
  let i = 0
  while (i < events.length) {
    const cells: Slot['cells'] = []
    for (let c = 0; c < courts.value; c++) {
      cells.push(events[i++] ?? null)
      if (i >= events.length) break
    }
    while (cells.length < courts.value) cells.push(null)
    slots.push({ time: t, cells })
    t = addMinutes(t, slotMinutes.value)
  }
  return slots
})
</script>

<template>
  <section class="space-y-4">
    <div class="card p-5">
      <h1 class="text-xl font-bold flex items-center gap-2">📅 코트별 타임테이블</h1>
      <p class="text-sm text-slate-500 mt-1">
        조별·본선 매치를 종목까지 풀어서 코트별 시간순으로 자동 배치합니다.
      </p>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-4">
        <label class="block">
          <span class="text-xs font-semibold text-slate-600">코트 수</span>
          <input v-model.number="courts" type="number" min="1" max="12" class="input mt-1" />
        </label>
        <label class="block">
          <span class="text-xs font-semibold text-slate-600">시작 시각</span>
          <input v-model="startTime" type="time" class="input mt-1" />
        </label>
        <label class="block">
          <span class="text-xs font-semibold text-slate-600">슬롯 길이(분)</span>
          <input v-model.number="slotMinutes" type="number" min="10" max="120" step="5" class="input mt-1" />
        </label>
      </div>
    </div>

    <div v-if="!schedule.length" class="card p-10 text-center text-slate-400">
      매치가 아직 없어. 조 편성/본선 생성 먼저.
    </div>

    <div v-else class="card overflow-x-auto">
      <table class="w-full text-xs sm:text-sm">
        <thead>
          <tr class="border-b border-slate-200 bg-slate-50">
            <th class="text-left p-3">시간</th>
            <th v-for="c in courts" :key="c" class="p-3">{{ c }}코트</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(slot, idx) in schedule" :key="idx" class="border-b border-slate-100 last:border-0">
            <td class="p-3 font-semibold text-slate-700">{{ slot.time }}</td>
            <td v-for="(cell, ci) in slot.cells" :key="ci" class="p-2">
              <div v-if="cell" class="rounded-lg bg-smash-50 border border-smash-200 p-2">
                <div class="font-semibold text-slate-800">{{ cell.label }}</div>
                <div class="text-[10px] uppercase tracking-wide text-smash-700">{{ cell.sub }}</div>
              </div>
              <div v-else class="text-slate-300 text-center">—</div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

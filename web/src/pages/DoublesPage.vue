<script setup lang="ts">
import { computed, ref } from 'vue'
import { useTournamentStore } from '@/stores/tournament'
import { makeMultipleRounds } from '@/lib/doubles'
import type { Gender, Player } from '@/types/domain'

const store = useTournamentStore()

const gender = ref<Gender>('남')
const team = ref<string>('전체')
const rounds = ref<number>(3)
const generated = ref<ReturnType<typeof makeMultipleRounds>>([])
const selectedIds = ref<Set<string>>(new Set())

const pool = computed<Player[]>(() => {
  return store.players.filter(p =>
    p.gender === gender.value && (team.value === '전체' || p.team === team.value),
  )
})

const teams = computed(() => {
  const set = new Set<string>()
  for (const p of store.players) set.add(p.team)
  return ['전체', ...[...set].sort()]
})

const selectedPlayers = computed<Player[]>(() => pool.value.filter(p => selectedIds.value.has(p.id)))

function toggleAll() {
  if (selectedIds.value.size === pool.value.length) {
    selectedIds.value = new Set()
  } else {
    selectedIds.value = new Set(pool.value.map(p => p.id))
  }
}

function toggle(id: string) {
  const s = new Set(selectedIds.value)
  if (s.has(id)) s.delete(id); else s.add(id)
  selectedIds.value = s
}

function generate() {
  const players = selectedPlayers.value
  if (players.length < 4 || players.length % 2 !== 0) {
    alert('짝수 명(최소 4명) 선택해야 합니다')
    return
  }
  generated.value = makeMultipleRounds(players, rounds.value)
}

function rating(p: Player) {
  return p.ntrp ?? p.career_years ?? '–'
}
</script>

<template>
  <section class="space-y-4">
    <div class="card p-5">
      <h1 class="text-xl font-bold flex items-center gap-2">🤝 복식 파트너 자동 매칭</h1>
      <p class="text-sm text-slate-500 mt-1">
        선수의 NTRP(없으면 구력)를 기준으로 라운드별 균형 페어/매치업을 만듭니다.
      </p>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-4">
        <label class="block">
          <span class="text-xs font-semibold text-slate-600">성별</span>
          <div class="mt-1 flex gap-2">
            <button v-for="g in ['남','여'] as Gender[]" :key="g" class="btn flex-1"
              :class="gender === g ? 'bg-smash-600 text-white' : 'bg-white border border-slate-200'"
              @click="gender = g; selectedIds = new Set()">{{ g }}</button>
          </div>
        </label>
        <label class="block">
          <span class="text-xs font-semibold text-slate-600">팀 필터</span>
          <select v-model="team" class="input mt-1">
            <option v-for="t in teams" :key="t">{{ t }}</option>
          </select>
        </label>
        <label class="block">
          <span class="text-xs font-semibold text-slate-600">라운드 수</span>
          <input v-model.number="rounds" type="number" min="1" max="10" class="input mt-1" />
        </label>
      </div>
    </div>

    <div class="card p-5">
      <div class="flex items-center justify-between mb-3">
        <h2 class="font-bold">참가 선수 선택 <span class="text-sm font-normal text-slate-500">({{ selectedPlayers.length }} / {{ pool.length }})</span></h2>
        <button class="btn-secondary text-xs" @click="toggleAll">전체선택</button>
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
        <button v-for="p in pool" :key="p.id"
          class="rounded-lg border p-2 text-left transition"
          :class="selectedIds.has(p.id)
            ? 'bg-emerald-50 border-emerald-400 text-emerald-700'
            : 'bg-white border-slate-200 hover:bg-slate-50'"
          @click="toggle(p.id)">
          <div class="font-medium text-sm">{{ p.name }}</div>
          <div class="text-xs text-slate-500">{{ p.team }} · {{ rating(p) }}</div>
        </button>
        <p v-if="!pool.length" class="text-slate-400 text-sm col-span-full text-center py-6">
          해당 조건의 선수가 없어. 선수 명단에서 추가해줘.
        </p>
      </div>
      <div class="mt-4 text-right">
        <button class="btn-primary" :disabled="selectedPlayers.length < 4 || selectedPlayers.length % 2 !== 0" @click="generate">
          🎲 라운드 매칭 생성
        </button>
      </div>
    </div>

    <div v-for="(r, idx) in generated" :key="idx" class="card p-5">
      <h3 class="font-bold mb-3">라운드 {{ idx + 1 }}</h3>
      <div class="space-y-2">
        <div v-for="(m, mi) in r.matchups" :key="mi"
          class="rounded-xl border border-slate-200 p-3 flex items-center gap-3">
          <div class="flex-1">
            <div class="font-semibold">{{ m.pairA.players[0].name }} / {{ m.pairA.players[1].name }}</div>
            <div class="text-xs text-slate-500">실력합 {{ m.pairA.ratingSum.toFixed(1) }}</div>
          </div>
          <div class="text-slate-400 text-sm">vs</div>
          <div class="flex-1 text-right">
            <div class="font-semibold">{{ m.pairB.players[0].name }} / {{ m.pairB.players[1].name }}</div>
            <div class="text-xs text-slate-500">실력합 {{ m.pairB.ratingSum.toFixed(1) }}</div>
          </div>
          <span class="pill" :class="m.ratingGap < 0.5 ? 'pill-win' : ''">
            격차 {{ m.ratingGap.toFixed(1) }}
          </span>
        </div>
      </div>
    </div>
  </section>
</template>

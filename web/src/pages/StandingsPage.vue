<script setup lang="ts">
import { computed, ref } from 'vue'
import { useTournamentStore } from '@/stores/tournament'
import { useAuthStore } from '@/stores/auth'
import { calculateStandings } from '@/lib/scoring'
import type { Group } from '@/types/domain'

const store = useTournamentStore()
const auth = useAuthStore()

const editing = ref(false)
const numGroups = ref<number>(Math.max(2, store.groups.length || 2))
const draft = ref<Group[]>(
  store.groups.length
    ? JSON.parse(JSON.stringify(store.groups))
    : [],
)

const allTeams = computed(() => {
  const set = new Set<string>()
  for (const p of store.players) set.add(p.team)
  return [...set].sort()
})

function startEdit() {
  editing.value = true
  numGroups.value = Math.max(2, store.groups.length || 2)
  draft.value = ensureGroups(store.groups, numGroups.value)
}

function ensureGroups(existing: Group[], n: number): Group[] {
  const groups: Group[] = []
  for (let i = 0; i < n; i++) {
    const name = `${String.fromCharCode(65 + i)}조`
    const found = existing.find(g => g.name === name)
    groups.push({ name, teams: found ? [...found.teams] : [] })
  }
  return groups
}

function setNumGroups(n: number) {
  numGroups.value = n
  draft.value = ensureGroups(draft.value, n)
}

function alreadyPicked(groupIdx: number): string[] {
  const picked: string[] = []
  draft.value.forEach((g, i) => {
    if (i !== groupIdx) picked.push(...g.teams)
  })
  return picked
}

function toggle(groupIdx: number, team: string) {
  const g = draft.value[groupIdx]
  if (g.teams.includes(team)) {
    g.teams = g.teams.filter(t => t !== team)
  } else {
    if (alreadyPicked(groupIdx).includes(team)) return
    g.teams = [...g.teams, team]
  }
}

function autoDistribute() {
  const teams = [...allTeams.value]
  for (let i = teams.length - 1; i > 0; i--) {
    const k = Math.floor(Math.random() * (i + 1))
    ;[teams[i], teams[k]] = [teams[k], teams[i]]
  }
  draft.value.forEach(g => (g.teams = []))
  teams.forEach((t, i) => {
    draft.value[i % numGroups.value].teams.push(t)
  })
}

function save() {
  store.setGroups(draft.value)
  editing.value = false
}

const standingsByGroup = computed(() =>
  store.groups.map(g => ({
    name: g.name,
    rows: calculateStandings(g.teams, store.matches.filter(m => m.groupName === g.name)),
  })),
)
</script>

<template>
  <section class="space-y-4">
    <div class="card p-5">
      <div class="flex items-start justify-between gap-3">
        <div>
          <h1 class="text-xl font-bold flex items-center gap-2">🏆 대회 운영 센터</h1>
          <p class="text-sm text-slate-500 mt-1">
            선수 등록 → 조 편성 → 점수 입력 → 본선 대진 자동 생성
          </p>
        </div>
        <button v-if="auth.isAdmin && !editing" class="btn-secondary" @click="startEdit">⚙️ 조 편성</button>
      </div>

      <div v-if="editing" class="mt-4 border-t border-slate-200 pt-4 space-y-4">
        <div class="flex items-center gap-3 flex-wrap">
          <label class="text-sm font-semibold text-slate-600">조 개수</label>
          <div class="flex gap-1">
            <button v-for="n in [2,3,4,5,6]" :key="n"
              class="btn"
              :class="numGroups === n ? 'bg-smash-600 text-white' : 'bg-white border border-slate-200 text-slate-700'"
              @click="setNumGroups(n)">{{ n }}조</button>
          </div>
          <button class="btn-secondary" @click="autoDistribute">🎲 무작위 배분</button>
        </div>

        <div v-if="!allTeams.length" class="rounded-lg bg-amber-50 border border-amber-200 text-amber-800 text-sm p-3">
          먼저 <RouterLink to="/players" class="underline font-semibold">선수 명단</RouterLink>을 등록해야 팀이 인식됩니다.
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div v-for="(g, gi) in draft" :key="g.name" class="rounded-xl border border-slate-200 p-3">
            <h3 class="font-bold mb-2">📍 {{ g.name }} <span class="text-slate-400 text-sm">({{ g.teams.length }})</span></h3>
            <div class="flex flex-wrap gap-1.5">
              <button v-for="t in allTeams" :key="t"
                class="px-2.5 py-1 rounded-full text-xs font-medium border"
                :class="g.teams.includes(t)
                  ? 'bg-smash-600 text-white border-smash-600'
                  : alreadyPicked(gi).includes(t)
                    ? 'bg-slate-100 text-slate-400 border-slate-100 cursor-not-allowed'
                    : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50'"
                :disabled="alreadyPicked(gi).includes(t) && !g.teams.includes(t)"
                @click="toggle(gi, t)">
                {{ t }}
              </button>
            </div>
          </div>
        </div>

        <div class="flex gap-2 justify-end">
          <button class="btn-ghost" @click="editing = false">취소</button>
          <button class="btn-primary" @click="save">🚀 대진 생성 (라운드로빈)</button>
        </div>
      </div>
    </div>

    <div v-if="!standingsByGroup.length" class="card p-10 text-center text-slate-400">
      아직 조 편성이 안 됐어. 우측 상단 <span class="font-semibold">조 편성</span> 버튼을 눌러줘.
    </div>

    <div v-for="g in standingsByGroup" :key="g.name" class="card p-4">
      <h2 class="font-bold mb-3">📍 {{ g.name }} 현황</h2>
      <table class="w-full text-sm">
        <thead>
          <tr class="text-slate-500 border-b border-slate-200">
            <th class="text-left py-2 pl-2">팀</th>
            <th>경기</th><th>승</th><th>무</th><th>패</th>
            <th class="text-emerald-700">승점</th>
            <th>득실</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(r, idx) in g.rows" :key="r.team"
            class="border-b border-slate-100 last:border-0"
            :class="idx === 0 ? 'bg-emerald-50/50' : ''">
            <td class="py-2 pl-2 font-semibold">
              <span class="text-slate-400 text-xs mr-2">{{ idx + 1 }}</span>{{ r.team }}
            </td>
            <td class="text-center">{{ r.played }}</td>
            <td class="text-center">{{ r.wins }}</td>
            <td class="text-center">{{ r.draws }}</td>
            <td class="text-center">{{ r.losses }}</td>
            <td class="text-center font-bold text-emerald-700">{{ r.points }}</td>
            <td class="text-center" :class="r.goalDiff > 0 ? 'text-emerald-600' : r.goalDiff < 0 ? 'text-rose-600' : ''">
              {{ r.goalDiff > 0 ? '+' : '' }}{{ r.goalDiff }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import * as XLSX from 'xlsx'
import { useTournamentStore } from '@/stores/tournament'
import type { Player } from '@/types/domain'

const store = useTournamentStore()
const filter = ref('')
const fileInput = ref<HTMLInputElement | null>(null)

const filteredPlayers = computed<Player[]>(() => {
  const q = filter.value.trim()
  if (!q) return store.players
  return store.players.filter(p =>
    p.name.includes(q) || p.team.includes(q),
  )
})

const byTeam = computed(() => {
  const map = new Map<string, Player[]>()
  for (const p of filteredPlayers.value) {
    if (!map.has(p.team)) map.set(p.team, [])
    map.get(p.team)!.push(p)
  }
  return [...map.entries()].sort((a, b) => a[0].localeCompare(b[0]))
})

function pickFile() { fileInput.value?.click() }

async function onFile(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  const buf = await file.arrayBuffer()
  const wb = XLSX.read(buf)
  const ws = wb.Sheets[wb.SheetNames[0]]
  const rows = XLSX.utils.sheet_to_json<any>(ws)
  store.importPlayers(rows)
}

function addManual() {
  const name = prompt('이름?')
  if (!name) return
  const team = prompt('소속?') ?? ''
  const gender = (prompt('성별 (남/여)?', '남') ?? '남').startsWith('여') ? '여' : '남'
  const ntrpStr = prompt('NTRP (옵션, 예: 3.5)') ?? ''
  const ntrp = Number.parseFloat(ntrpStr)
  store.importPlayers([
    ...store.players.map(p => ({ 이름: p.name, 소속: p.team, 성별: p.gender, ntrp: p.ntrp ?? undefined, 구력: p.career_years ?? undefined })),
    { 이름: name, 소속: team, 성별: gender, ntrp: Number.isFinite(ntrp) ? ntrp : undefined },
  ])
}
</script>

<template>
  <section class="space-y-4">
    <div class="card p-5">
      <h1 class="text-xl font-bold flex items-center gap-2">👤 선수 명단</h1>
      <p class="text-sm text-slate-500 mt-1">
        엑셀(.xlsx)에 <code class="px-1.5 py-0.5 rounded bg-slate-100 text-xs">이름</code>,
        <code class="px-1.5 py-0.5 rounded bg-slate-100 text-xs">소속</code>,
        <code class="px-1.5 py-0.5 rounded bg-slate-100 text-xs">성별</code>,
        <code class="px-1.5 py-0.5 rounded bg-slate-100 text-xs">구력</code>,
        <code class="px-1.5 py-0.5 rounded bg-slate-100 text-xs">ntrp</code> 컬럼을 넣어 업로드하세요.
      </p>
      <div class="mt-4 flex flex-wrap gap-2">
        <input ref="fileInput" type="file" accept=".xlsx,.xls,.csv" class="hidden" @change="onFile" />
        <button class="btn-primary" @click="pickFile">📂 엑셀 업로드</button>
        <button class="btn-secondary" @click="addManual">+ 직접 추가</button>
        <button class="btn-ghost text-rose-600" @click="store.importPlayers([])" v-if="store.players.length">
          전체 삭제
        </button>
      </div>
    </div>

    <div class="card p-5">
      <div class="flex items-center justify-between gap-3 mb-4">
        <input v-model="filter" placeholder="이름/팀 검색" class="input max-w-xs" />
        <span class="pill">{{ store.players.length }}명 등록</span>
      </div>
      <div v-if="!store.players.length" class="text-center text-slate-400 py-10">
        아직 등록된 선수가 없습니다.
      </div>
      <div v-else class="space-y-4">
        <div v-for="[team, list] in byTeam" :key="team">
          <h3 class="font-semibold text-slate-800 mb-2">📍 {{ team }} <span class="text-slate-400 text-sm">({{ list.length }})</span></h3>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
            <div v-for="p in list" :key="p.id" class="rounded-lg border border-slate-200 px-3 py-2 flex items-center justify-between">
              <div>
                <div class="font-medium text-sm">{{ p.name }}</div>
                <div class="text-xs text-slate-500">
                  {{ p.gender }}
                  <span v-if="p.ntrp"> · NTRP {{ p.ntrp }}</span>
                  <span v-if="p.career_years"> · 구력 {{ p.career_years }}년</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

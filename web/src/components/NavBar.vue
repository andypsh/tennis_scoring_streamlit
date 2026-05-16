<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTournamentStore } from '@/stores/tournament'
import { hasSupabase } from '@/lib/supabase'

const route = useRoute()
const auth = useAuthStore()
const tournament = useTournamentStore()

const syncStatus = computed(() => {
  if (!hasSupabase) return { label: '로컬', color: 'bg-slate-100 text-slate-600' }
  if (tournament.syncing) return { label: '동기화…', color: 'bg-amber-100 text-amber-700' }
  if (tournament.online) return { label: '실시간', color: 'bg-emerald-100 text-emerald-700' }
  return { label: '오프라인', color: 'bg-rose-100 text-rose-700' }
})

const tabs = [
  { to: '/standings', label: '조별순위', icon: '🏆' },
  { to: '/score', label: '점수입력', icon: '📝' },
  { to: '/bracket', label: '본선대진', icon: '🎯' },
  { to: '/doubles', label: '복식매칭', icon: '🤝' },
  { to: '/timetable', label: '타임표', icon: '📅' },
  { to: '/players', label: '선수', icon: '👤' },
]

const isLogin = computed(() => route.path === '/login')
</script>

<template>
  <header class="sticky top-0 z-30 bg-white/95 backdrop-blur border-b border-slate-200">
    <div class="mx-auto max-w-5xl px-4 py-3 flex items-center justify-between">
      <RouterLink to="/standings" class="flex items-center gap-2">
        <span class="text-xl">🎾</span>
        <span class="font-bold text-slate-900">CJ Tennis</span>
      </RouterLink>
      <div class="flex items-center gap-2">
        <span class="inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-bold uppercase tracking-wide" :class="syncStatus.color">
          <span class="size-1.5 rounded-full" :class="tournament.online && hasSupabase ? 'bg-emerald-500 animate-pulse' : tournament.syncing ? 'bg-amber-500' : 'bg-slate-400'"></span>
          {{ syncStatus.label }}
        </span>
        <RouterLink v-if="!auth.isAuthed && !isLogin" to="/login" class="btn-secondary text-xs">로그인</RouterLink>
        <button v-else-if="auth.isAuthed" class="btn-ghost text-xs" @click="auth.signOut()">
          {{ auth.email || auth.role }} · 로그아웃
        </button>
      </div>
    </div>
    <nav class="mx-auto max-w-5xl px-2 overflow-x-auto">
      <ul class="flex gap-1 pb-2 min-w-max">
        <li v-for="t in tabs" :key="t.to">
          <RouterLink
            :to="t.to"
            class="flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm font-medium transition"
            :class="route.path.startsWith(t.to) ? 'bg-smash-600 text-white' : 'text-slate-600 hover:bg-slate-100'"
          >
            <span>{{ t.icon }}</span>
            <span>{{ t.label }}</span>
          </RouterLink>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { hasSupabase } from '@/lib/supabase'

const dismissed = ref(localStorage.getItem('cj_setup_notice_dismissed') === '1')

function dismiss() {
  localStorage.setItem('cj_setup_notice_dismissed', '1')
  dismissed.value = true
}

const open = ref(false)
</script>

<template>
  <div v-if="!hasSupabase && !dismissed" class="card border-amber-200 bg-amber-50 p-4 mb-4">
    <div class="flex items-start gap-3">
      <span class="text-2xl">⚙️</span>
      <div class="flex-1">
        <h3 class="font-bold text-amber-900">데모 모드로 동작 중</h3>
        <p class="text-sm text-amber-800 mt-1">
          지금은 이 기기 안에만 데이터가 저장돼. 동료들과 실시간 공유하려면 Supabase(무료) 연결이 필요해.
        </p>
        <button class="btn-secondary mt-3 text-xs" @click="open = !open">
          {{ open ? '접기' : '연결 방법 보기 (5분)' }}
        </button>

        <div v-if="open" class="mt-3 space-y-2 text-sm text-amber-900">
          <ol class="list-decimal pl-5 space-y-1">
            <li>
              <a href="https://supabase.com" target="_blank" class="underline font-semibold">supabase.com</a>
              에서 GitHub로 1초 가입
            </li>
            <li>"New project" → 이름 적고 2분 대기 (무료)</li>
            <li>
              좌측 메뉴 <b>SQL Editor</b> → New query → 다음 파일 내용 통째로 붙여넣고 <b>Run</b>
              <code class="block mt-1 px-2 py-1 rounded bg-amber-100 text-xs">supabase/schema.sql</code>
            </li>
            <li>
              좌측 <b>Settings → API</b>에서 <i>Project URL</i>과 <i>anon public</i> 키 복사
            </li>
            <li>
              프로젝트 루트의 <code class="px-1 rounded bg-amber-100 text-xs">web/.env</code> 파일에 붙여넣고 저장:
              <pre class="mt-1 p-2 rounded bg-slate-900 text-emerald-300 text-xs overflow-x-auto"><code>VITE_SUPABASE_URL=https://xxxxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGc...</code></pre>
            </li>
            <li>
              <code class="px-1 rounded bg-amber-100 text-xs">npm run dev</code> 재시작 → 우상단 칩이 🟢 실시간으로 바뀜
            </li>
          </ol>
        </div>

        <button class="btn-ghost text-xs text-amber-700 mt-2" @click="dismiss">다시 보지 않기</button>
      </div>
    </div>
  </div>
</template>

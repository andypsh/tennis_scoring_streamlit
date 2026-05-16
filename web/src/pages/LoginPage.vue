<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { hasSupabase } from '@/lib/supabase'

const auth = useAuthStore()
const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function submit() {
  loading.value = true
  error.value = ''
  try {
    await auth.signIn(email.value, password.value)
    router.push('/standings')
  } catch (e: any) {
    error.value = e?.message ?? '로그인 실패'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-sm mx-auto mt-12">
    <div class="card p-6">
      <h1 class="text-2xl font-bold mb-1">로그인</h1>
      <p class="text-sm text-slate-500 mb-4">
        {{ hasSupabase ? 'Supabase 계정으로 로그인하세요' : '데모: admin / admin' }}
      </p>
      <form @submit.prevent="submit" class="space-y-3">
        <label class="block">
          <span class="text-xs font-semibold text-slate-600">이메일 / 아이디</span>
          <input v-model="email" class="input mt-1" autocomplete="username" />
        </label>
        <label class="block">
          <span class="text-xs font-semibold text-slate-600">비밀번호</span>
          <input v-model="password" type="password" class="input mt-1" autocomplete="current-password" />
        </label>
        <p v-if="error" class="text-sm text-rose-600">{{ error }}</p>
        <button class="btn-primary w-full" :disabled="loading">
          {{ loading ? '로그인 중…' : '로그인' }}
        </button>
      </form>
    </div>
  </div>
</template>

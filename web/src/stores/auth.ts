import { defineStore } from 'pinia'
import { hasSupabase, supabase } from '@/lib/supabase'

type Role = 'public' | 'user' | 'admin'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    role: 'public' as Role,
    email: '' as string,
    ready: false,
  }),
  getters: {
    isAdmin: state => state.role === 'admin',
    isAuthed: state => state.role !== 'public',
  },
  actions: {
    async init() {
      if (!hasSupabase || !supabase) {
        // 로컬 데모 모드 — 처음 켜면 admin으로 인정
        const stored = localStorage.getItem('cj_role') as Role | null
        this.role = stored ?? 'admin'
        this.ready = true
        return
      }
      const { data } = await supabase.auth.getSession()
      if (data.session) {
        this.email = data.session.user.email ?? ''
        this.role = (data.session.user.app_metadata?.role as Role) ?? 'user'
      }
      supabase.auth.onAuthStateChange((_evt, session) => {
        if (session) {
          this.email = session.user.email ?? ''
          this.role = (session.user.app_metadata?.role as Role) ?? 'user'
        } else {
          this.email = ''
          this.role = 'public'
        }
      })
      this.ready = true
    },
    async signIn(email: string, password: string) {
      if (!hasSupabase || !supabase) {
        // 데모용 admin/admin
        if (email === 'admin' && password === 'admin') {
          this.role = 'admin'
          localStorage.setItem('cj_role', 'admin')
          return
        }
        throw new Error('Supabase 미설정. 데모 로그인은 admin/admin')
      }
      const { error } = await supabase.auth.signInWithPassword({ email, password })
      if (error) throw error
    },
    async signOut() {
      if (hasSupabase && supabase) await supabase.auth.signOut()
      this.role = 'public'
      this.email = ''
      localStorage.removeItem('cj_role')
    },
  },
})

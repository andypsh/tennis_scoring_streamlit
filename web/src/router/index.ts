import { createRouter, createWebHashHistory } from 'vue-router'

export const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', redirect: '/standings' },
    { path: '/login', name: 'login', component: () => import('@/pages/LoginPage.vue') },
    { path: '/players', name: 'players', component: () => import('@/pages/PlayersPage.vue') },
    { path: '/standings', name: 'standings', component: () => import('@/pages/StandingsPage.vue') },
    { path: '/score', name: 'score', component: () => import('@/pages/ScorePage.vue') },
    { path: '/bracket', name: 'bracket', component: () => import('@/pages/BracketPage.vue') },
    { path: '/timetable', name: 'timetable', component: () => import('@/pages/TimetablePage.vue') },
    { path: '/doubles', name: 'doubles', component: () => import('@/pages/DoublesPage.vue') },
  ],
})

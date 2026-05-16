<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTournamentStore } from '@/stores/tournament'
import NavBar from '@/components/NavBar.vue'
import SetupNotice from '@/components/SetupNotice.vue'

const auth = useAuthStore()
const tournament = useTournamentStore()

onMounted(async () => {
  await auth.init()
  await tournament.loadAll()
})
</script>

<template>
  <div class="min-h-full flex flex-col">
    <NavBar />
    <main class="flex-1 mx-auto w-full max-w-5xl px-4 py-4 pb-24">
      <SetupNotice />
      <RouterView />
    </main>
  </div>
</template>

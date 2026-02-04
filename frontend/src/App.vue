<script setup>
import { onMounted } from 'vue'
import { useUserStore } from './stores/userStore'
import AuthForm from './components/AuthForm.vue'
import UserProfile from './components/UserProfile.vue'

const userStore = useUserStore()

onMounted(() => {
  try {
    // Очищаем старые данные для обновления
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      const user = JSON.parse(savedUser)
      // Если нет coverGradient, то это старые данные - очищаем
      if (!user.coverGradient) {
        localStorage.removeItem('user')
        localStorage.removeItem('isAuthenticated')
      }
    }
    userStore.loadUser()
  } catch (e) {
    console.error('Error loading user:', e)
  }
})
</script>

<template>
  <div class="app-shell">
    <div class="app-container">
      <div class="bg-transparent">
        <!-- Если пользователь не авторизован - показываем форму входа/регистрации -->
        <AuthForm v-if="!userStore.isAuthenticated" />

        <!-- Если пользователь авторизован - показываем профиль -->
        <UserProfile v-else />
      </div>
    </div>
  </div>
</template>

<style>
body {
  margin: 0;
  padding: 0;
}

#app {
  width: 100%;
  margin: 0 auto;
}
</style>

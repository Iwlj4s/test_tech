<template>
  <div id="app">
    <!-- Error State -->
    <div v-if="appError" class="app-error">
      <div class="error-content">
        <h3>Ошибка приложения</h3>
        <p>{{ appError }}</p>
        <button @click="retryInitialization" class="btn btn-primary">
          Повторить
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-else-if="isLoading" class="app-loading">
      <div class="loading-spinner"></div>
      <p>Загрузка приложения...</p>
    </div>

    <!-- Router View -->
    <div v-else>
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from './stores/userStore'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()
const isLoading = ref(true)
const appError = ref(null)

onMounted(async () => {
  await initializeApp()
})

const initializeApp = async () => {
  try {
    await userStore.loadUser()
    
    // Если пользователь авторизован, перенаправляем на профиль
    if (userStore.isAuthenticated && router.currentRoute.value.path === '/auth') {
      router.push('/profile')
    }
  } catch (error) {
    console.error('Ошибка инициализации:', error)
    appError.value = 'Не удалось загрузить приложение. Проверьте соединение с сервером.'
  } finally {
    isLoading.value = false
  }
}

const retryInitialization = async () => {
  appError.value = null
  isLoading.value = true
  try {
    await userStore.loadUser()
  } catch (error) {
    appError.value = error.message
  } finally {
    isLoading.value = false
  }
}
</script>

<style>
#app {
  min-height: 100vh;
  background: #0b0b0b;
  color: #e6eef6;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

.app-error {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  padding: 2rem;
  background: rgba(11, 11, 11, 0.95);
  backdrop-filter: blur(8px);
}

.error-content {
  text-align: center;
  max-width: 400px;
  background: rgba(255, 255, 255, 0.05);
  padding: 2.5rem;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.error-content h3 {
  color: #ef4444;
  margin-bottom: 1rem;
  font-size: 1.5rem;
  font-weight: 700;
}

.error-content p {
  margin-bottom: 1.5rem;
  color: #94a3b8;
  line-height: 1.6;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
  font-size: 0.875rem;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.app-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  gap: 1.5rem;
  background: #0b0b0b;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  border-top-color: #667eea;
  animation: spin 1s linear infinite;
}

.app-loading p {
  color: #94a3b8;
  font-size: 1rem;
  font-weight: 500;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Плавные переходы */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
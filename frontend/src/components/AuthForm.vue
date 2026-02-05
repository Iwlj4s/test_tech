<!-- components/AuthForm.vue -->
<template>
  <div class="auth-container">
    <div class="auth-card">
      <!-- Логотип/Заголовок -->
      <div class="auth-header">
        <h1 class="auth-title">Social Profile</h1>
        <p class="auth-subtitle">Welcome to your profile manager</p>
      </div>

      <!-- Табы -->
      <div class="auth-tabs">
        <button
          @click="isLogin = true"
          :class="['auth-tab', { 'active': isLogin }]"
        >
          Вход
        </button>
        <button
          @click="isLogin = false"
          :class="['auth-tab', { 'active': !isLogin }]"
        >
          Регистрация
        </button>
      </div>

      <!-- Форма входа -->
      <form v-if="isLogin" @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label class="form-label">Email</label>
          <input
            v-model="loginForm.email"
            type="email"
            required
            placeholder="your@email.com"
            class="form-input"
            :disabled="userStore.isLoading"
          />
        </div>

        <div class="form-group">
          <label class="form-label">Пароль</label>
          <input
            v-model="loginForm.password"
            type="password"
            required
            placeholder="••••••••"
            class="form-input"
            :disabled="userStore.isLoading"
          />
        </div>

        <button
          type="submit"
          class="btn btn-primary"
          :disabled="userStore.isLoading"
        >
          <span v-if="userStore.isLoading">Загрузка...</span>
          <span v-else>Войти</span>
        </button>
      </form>

      <!-- Форма регистрации -->
      <form v-else @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label class="form-label">Имя</label>
          <input
            v-model="registerForm.name"
            type="text"
            required
            placeholder="John Doe"
            class="form-input"
            :disabled="userStore.isLoading"
          />
        </div>

        <div class="form-group">
          <label class="form-label">Email</label>
          <input
            v-model="registerForm.email"
            type="email"
            required
            placeholder="your@email.com"
            class="form-input"
            :disabled="userStore.isLoading"
          />
        </div>

        <div class="form-group">
          <label class="form-label">Пароль</label>
          <input
            v-model="registerForm.password"
            type="password"
            required
            placeholder="••••••••"
            class="form-input"
            :disabled="userStore.isLoading"
          />
        </div>

        <div class="form-group">
          <label class="form-label">О себе (необязательно)</label>
          <textarea
            v-model="registerForm.bio"
            placeholder="Расскажите о себе..."
            class="form-textarea"
            :disabled="userStore.isLoading"
            rows="3"
          ></textarea>
        </div>

        <button
          type="submit"
          class="btn btn-primary"
          :disabled="userStore.isLoading"
        >
          <span v-if="userStore.isLoading">Создание...</span>
          <span v-else>Создать аккаунт</span>
        </button>
      </form>

      <!-- Сообщение об ошибке -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '../stores/userStore'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()

const isLogin = ref(true)
const errorMessage = ref('')

const loginForm = ref({
  email: '',
  password: ''
})

const registerForm = ref({
  name: '',
  email: '',
  password: '',
  bio: '',
  location: ''
})

const resetForms = () => {
  loginForm.value = { email: '', password: '' }
  registerForm.value = { name: '', email: '', password: '', bio: '', location: '' }
  errorMessage.value = ''
}

const handleLogin = async () => {
  errorMessage.value = ''
  
  if (!loginForm.value.email || !loginForm.value.password) {
    errorMessage.value = 'Заполните все поля'
    return
  }

  try {
    await userStore.login(loginForm.value.email, loginForm.value.password)
    resetForms()
    
    // После успешного входа перенаправляем на профиль
    if (userStore.isAuthenticated) {
      router.push('/profile')
    }
  } catch (error) {
    errorMessage.value = error.message || 'Ошибка входа. Проверьте email и пароль.'
    console.error('Login error:', error)
  }
}

const handleRegister = async () => {
  errorMessage.value = ''
  
  // Проверяем обязательные поля
  if (!registerForm.value.name || !registerForm.value.email || !registerForm.value.password) {
    errorMessage.value = 'Заполните обязательные поля (имя, email, пароль)'
    return
  }

  // Проверяем email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(registerForm.value.email)) {
    errorMessage.value = 'Введите корректный email'
    return
  }

  // Проверяем пароль
  if (registerForm.value.password.length < 4) {
    errorMessage.value = 'Пароль должен содержать минимум 4 символа'
    return
  }

  try {
    await userStore.register(
      registerForm.value.name,
      registerForm.value.email,
      registerForm.value.password,
      registerForm.value.bio || '',
      registerForm.value.location || ''
    )
    
    resetForms()
    
    // После успешной регистрации перенаправляем на профиль
    if (userStore.isAuthenticated) {
      router.push('/profile')
    }
  } catch (error) {
    errorMessage.value = error.message || 'Ошибка регистрации. Возможно, пользователь уже существует.'
    console.error('Register error:', error)
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.auth-card {
  width: 100%;
  max-width: 400px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-title {
  font-size: 2rem;
  font-weight: 800;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
}

.auth-subtitle {
  color: #666;
  font-size: 0.9rem;
}

.auth-tabs {
  display: flex;
  background: #f0f0f0;
  border-radius: 12px;
  padding: 4px;
  margin-bottom: 2rem;
}

.auth-tab {
  flex: 1;
  padding: 0.75rem;
  border: none;
  background: transparent;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  color: #666;
}

.auth-tab.active {
  background: white;
  color: #1a1a1a;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #333;
  margin-bottom: 0.5rem;
}

.form-input {
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s;
  background: white;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-textarea {
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s;
  background: white;
  resize: vertical;
  min-height: 80px;
}

.form-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.btn {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem 1rem;
  background: #fee;
  border: 1px solid #f99;
  border-radius: 8px;
  color: #c00;
  font-size: 0.875rem;
  text-align: center;
}
</style>
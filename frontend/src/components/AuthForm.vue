<template>
  <div class="min-h-screen bg-white dark:bg-black flex items-center justify-center px-4">
    <div class="w-full max-w-md">
      <!-- Logo/Title -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-primary mb-2">Social Profile</h1>
        <p class="text-gray-500">Welcome to your profile manager</p>
      </div>

      <!-- Tabs для переключения между входом и регистрацией -->
      <div class="flex gap-4 mb-8 bg-gray-100 dark:bg-gray-900 p-1 rounded-2xl">
        <button
          @click="isLogin = true"
          :class="[
            'flex-1 py-3 px-4 font-semibold rounded-xl transition',
            isLogin
              ? 'bg-primary text-white shadow-lg'
              : 'bg-transparent text-gray-700 dark:text-gray-300'
          ]"
        >
          Вход
        </button>
        <button
          @click="isLogin = false"
          :class="[
            'flex-1 py-3 px-4 font-semibold rounded-xl transition',
            !isLogin
              ? 'bg-primary text-white shadow-lg'
              : 'bg-transparent text-gray-700 dark:text-gray-300'
          ]"
        >
          Регистрация
        </button>
      </div>

      <!-- Форма входа -->
      <form v-if="isLogin" @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Email
          </label>
          <input
            v-model="loginForm.email"
            type="email"
            required
            placeholder="your@email.com"
            class="w-full px-4 py-3 border-2 border-gray-300 dark:border-gray-700 rounded-xl
                   bg-white dark:bg-gray-900 text-gray-900 dark:text-white
                   focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Пароль
          </label>
          <input
            v-model="loginForm.password"
            type="password"
            required
            placeholder="••••••••"
            class="w-full px-4 py-3 border-2 border-gray-300 dark:border-gray-700 rounded-xl
                   bg-white dark:bg-gray-900 text-gray-900 dark:text-white
                   focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition"
          />
        </div>

        <button
          type="submit"
          class="w-full py-3 px-4 bg-primary text-white font-bold rounded-xl
                 hover:bg-blue-500 transition duration-200 shadow-lg"
        >
          Войти
        </button>
      </form>

      <!-- Форма регистрации -->
      <form v-else @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Имя
          </label>
          <input
            v-model="registerForm.name"
            type="text"
            required
            placeholder="John Doe"
            class="w-full px-4 py-3 border-2 border-gray-300 dark:border-gray-700 rounded-xl
                   bg-white dark:bg-gray-900 text-gray-900 dark:text-white
                   focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Email
          </label>
          <input
            v-model="registerForm.email"
            type="email"
            required
            placeholder="your@email.com"
            class="w-full px-4 py-3 border-2 border-gray-300 dark:border-gray-700 rounded-xl
                   bg-white dark:bg-gray-900 text-gray-900 dark:text-white
                   focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Пароль
          </label>
          <input
            v-model="registerForm.password"
            type="password"
            required
            placeholder="••••••••"
            class="w-full px-4 py-3 border-2 border-gray-300 dark:border-gray-700 rounded-xl
                   bg-white dark:bg-gray-900 text-gray-900 dark:text-white
                   focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition"
          />
        </div>

        <button
          type="submit"
          class="w-full py-3 px-4 bg-primary text-white font-bold rounded-xl
                 hover:bg-blue-500 transition duration-200 shadow-lg"
        >
          Создать аккаунт
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '../stores/userStore'

const userStore = useUserStore()
const isLogin = ref(true)

const loginForm = ref({
  email: '',
  password: ''
})

const registerForm = ref({
  name: '',
  email: '',
  password: ''
})

const handleLogin = () => {
  if (loginForm.value.email && loginForm.value.password) {
    userStore.login(loginForm.value.email, loginForm.value.password)
    // После входа в App.vue произойдет переключение представления
  }
}

const handleRegister = () => {
  if (registerForm.value.name && registerForm.value.email && registerForm.value.password) {
    userStore.register(registerForm.value.name, registerForm.value.email, registerForm.value.password)
  }
}
</script>

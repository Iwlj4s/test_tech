<template>
  <!-- Backdrop с размытием -->
  <div
    @click="handleBackdropClick"
    class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50 px-4"
  >
    <!-- Modal -->
    <div
      @click.stop
      class="bg-white dark:bg-gray-900 rounded-3xl shadow-2xl w-full max-w-md"
    >
      <!-- Modal Header -->
      <div class="border-b border-gray-200 dark:border-gray-800 px-6 py-4 flex items-center justify-between rounded-t-3xl">
        <h3 class="text-xl font-bold text-gray-900 dark:text-white">
          Редактировать профиль
        </h3>
        <button
          @click="$emit('close')"
          class="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition 
                 hover:bg-gray-100 dark:hover:bg-gray-800 p-2 rounded-full"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Modal Body -->
      <div class="px-6 py-6 space-y-4">
        <!-- Name Field -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            Имя
          </label>
          <input
            v-model="formData.name"
            type="text"
            class="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-700 rounded-xl
                   bg-white dark:bg-gray-800 text-gray-900 dark:text-white
                   focus:outline-none focus:border-primary transition"
            placeholder="Ваше имя"
          />
        </div>

        <!-- Email Field -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            Email
          </label>
          <input
            v-model="formData.email"
            type="email"
            class="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-700 rounded-xl
                   bg-white dark:bg-gray-800 text-gray-900 dark:text-white
                   focus:outline-none focus:border-primary transition"
            placeholder="your@email.com"
          />
        </div>

        <!-- Bio Field -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            О себе
          </label>
          <textarea
            v-model="formData.bio"
            rows="3"
            class="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-700 rounded-xl
                   bg-white dark:bg-gray-800 text-gray-900 dark:text-white
                   focus:outline-none focus:border-primary transition resize-none"
            placeholder="Расскажите о себе..."
          />
        </div>

        <!-- Location Field -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            Местоположение
          </label>
          <input
            v-model="formData.location"
            type="text"
            class="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-700 rounded-xl
                   bg-white dark:bg-gray-800 text-gray-900 dark:text-white
                   focus:outline-none focus:border-primary transition"
            placeholder="Город, Страна"
          />
        </div>
      </div>

      <!-- Modal Footer -->
      <div class="border-t border-gray-200 dark:border-gray-800 px-6 py-4 flex gap-3 rounded-b-3xl">
        <button
          @click="$emit('close')"
          class="flex-1 py-3 px-4 text-gray-700 dark:text-gray-300 font-bold
                 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-xl transition"
        >
          Отмена
        </button>
        <button
          @click="handleSave"
          class="flex-1 py-3 px-4 bg-primary text-white font-bold rounded-xl
                 hover:bg-blue-500 transition duration-200"
        >
          Сохранить
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '../stores/userStore'

const emit = defineEmits(['close', 'save'])
const userStore = useUserStore()

const formData = ref({
  name: userStore.user.name,
  email: userStore.user.email,
  bio: userStore.user.bio,
  location: userStore.user.location
})

const handleSave = () => {
  if (formData.value.name && formData.value.email) {
    emit('save', {
      name: formData.value.name,
      email: formData.value.email,
      bio: formData.value.bio,
      location: formData.value.location
    })
  }
}

const handleBackdropClick = () => {
  emit('close')
}
</script>

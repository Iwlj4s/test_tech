<template>
  <div class="min-h-screen bg-white dark:bg-black">
    <!-- Header -->
    <div class="border-b border-gray-200 dark:border-gray-900 sticky top-0 bg-white/80 dark:bg-black/80 backdrop-blur rounded-b-2xl z-40">
      <div class="max-w-2xl mx-auto px-4 py-3 flex items-center justify-center relative">
        <div>
          <h2 class="text-xl font-bold">Профиль</h2>
        </div>
        <button @click="handleLogout" class="logout-btn btn btn-outline absolute right-4 top-3">Выход</button>
      </div>
    </div>

    <!-- Profile Content -->
    <div class="max-w-2xl mx-auto">
      <!-- Cover Image with gradient -->
      <div 
        class="h-56 rounded-b-3xl"
        :style="{ background: userStore.user.coverGradient }"
      ></div>

      <!-- Profile Info Section -->
      <div class="px-4">
        <!-- Avatar & Button Container -->
        <div class="flex items-end justify-between -mt-20 mb-4 relative z-10">
          <img
            :src="userStore.user.avatar"
            :alt="userStore.user.name"
            class="profile-avatar"
          />
          <div class="flex-1">
            <div class="flex items-center justify-between w-full">
              <div>
                <h1 class="text-4xl font-bold mb-1">{{ userStore.user.name }}</h1>
                <p class="text-gray-500 text-lg mb-2">@{{ userStore.user.email.split('@')[0] }}</p>
              </div>
              <div>
                <button @click="openEditModal" class="btn btn-outline">Изменить</button>
              </div>
            </div>
          </div>
        </div>

        <!-- User Info -->
        <div class="mb-4 mt-4 ">
          <!-- Metadata -->
          <div class="flex gap-6 text-gray-500 dark:text-gray-400 mb-4">
            <!-- Location -->
            <div class="flex items-center gap-2" v-if="userStore.user.location">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
              </svg>
              <span>{{ userStore.user.location }}</span>
            </div>

            <!-- Joined Date -->
            <div class="flex items-center gap-2">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v2H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V7a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v2H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
              </svg>
              <span>{{ formatDate(userStore.user.registrationDate) }}</span>
            </div>
          </div>
        </div>

        <!-- Email Info Box -->
        <div class="rounded-2xl p-4 mb-4">
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Email</p>
          <p class="text-gray-900 dark:text-white font-medium">{{ userStore.user.email }}</p>
        </div>

        <!-- Bio Box (if exists) -->
        <div v-if="userStore.user.bio" class="rounded-2xl p-4 mb-6">
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">О себе</p>
          <p class="text-gray-900 dark:text-white">{{ userStore.user.bio }}</p>
        </div>
      </div>

      <!-- Posts Content -->
      <div class="px-4">
        <div class="posts-list">
          <PostCard v-for="post in posts" :key="post.id" :post="post" />
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <EditProfileModal
      v-if="showEditModal"
      @close="closeEditModal"
      @save="saveProfile"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '../stores/userStore'
import EditProfileModal from './EditProfileModal.vue'
import PostCard from './PostCard.vue'

const userStore = useUserStore()
const showEditModal = ref(false)
const activeTab = ref('posts')

const posts = ref([
  {
    id: 1,
    author: userStore.user.name,
    handle: userStore.user.email.split('@')[0],
    authorAvatar: userStore.user.avatar,
    content: 'Привет! Это мой первый пост в этом приложении. Очень рад быть здесь! 🚀',
    time: 'Сейчас',
    replies: 0,
    retweets: 0,
    likes: 5
  },
  {
    id: 2,
    author: userStore.user.name,
    handle: userStore.user.email.split('@')[0],
    authorAvatar: userStore.user.avatar,
    content: 'Разработка красивых веб-приложений на Vue.js - это так интересно! 💻',
    time: '2 часа назад',
    replies: 2,
    retweets: 1,
    likes: 12
  }
])

const openEditModal = () => {
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
}

const saveProfile = (updatedData) => {
  userStore.updateProfile(updatedData)
  // Обновляем посты с новой аватаркой
  posts.value.forEach(post => {
    post.authorAvatar = userStore.user.avatar
  })
  closeEditModal()
}

const formatDate = (date) => {
  const d = new Date(date)
  return d.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const handleLogout = () => {
  userStore.logout()
}
</script>

<template>
  <div class="user-profile-view">
    <!-- Loading State -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>Загрузка профиля...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-overlay">
      <div class="error-message">
        <h3>Ошибка загрузки</h3>
        <p>{{ error }}</p>
        <button @click="retryLoad" class="btn btn-primary">Повторить</button>
      </div>
    </div>

    <!-- Content -->
    <div v-else-if="user" class="profile-content">
      <!-- Header -->
      <header class="profile-header">
        <div class="header-content">
          <button @click="goBack" class="back-btn">
            <svg class="back-icon" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            Назад
          </button>
          <h1 class="header-title">Профиль пользователя</h1>
        </div>
      </header>

      <!-- Main Content -->
      <main class="profile-main">
        <!-- Cover -->
        <div 
          class="profile-cover"
          :style="{ background: coverGradient }"
        ></div>

        <!-- Profile Info -->
        <div class="profile-info">
          <div class="avatar-section">
            <div 
              class="profile-avatar"
              :style="{ background: avatarGradient }"
            >
              {{ avatarInitials }}
            </div>
            
             <!-- Админские кнопки (только для админов и не для себя) -->
            <div v-if="showAdminActions" class="admin-actions">
              <button 
                v-if="!user.is_admin"
                @click="promoteToAdmin"
                class="admin-action-btn promote-btn"
                :disabled="userStore.isLoading"
              >
                <svg class="admin-action-icon" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                <span v-if="userStore.isLoading">Назначение...</span>
                <span v-else>Назначить админом</span>
              </button>
              
              <button 
                v-else
                @click="demoteFromAdmin"
                class="admin-action-btn demote-btn"
                :disabled="userStore.isLoading"
              >
                <svg class="admin-action-icon" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
                <span v-if="userStore.isLoading">Снятие...</span>
                <span v-else>Снять с должности</span>
              </button>

              <button 
                @click="deleteUser"
                class="admin-action-btn delete-btn"
                :disabled="userStore.isLoading"
              >
                <svg class="admin-action-icon" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
                <span v-if="userStore.isLoading">Удаление...</span>
                <span v-else>Удалить</span>
              </button>
            </div>
          </div>

          <div class="user-details">
            <h1 class="user-name">{{ user.name }}</h1>
            <p class="user-email">{{ user.email }}</p>
            
            <!-- User Metadata -->
            <div class="user-meta">
              <!-- Location -->
              <div v-if="user.location && user.location !== 'Не указано' && user.location !== ''" class="meta-item">
                <svg class="meta-icon" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                </svg>
                <span>{{ user.location }}</span>
              </div>
              
              <!-- Registration Date -->
              <div class="meta-item">
                <svg class="meta-icon" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
                </svg>
                <span>Зарегистрирован {{ formattedDate }}</span>
              </div>
            </div>

            <!-- Bio -->
            <div v-if="user.bio && user.bio !== 'User didn\'t add his bio' && user.bio !== ''" class="info-card">
              <label class="info-label">О себе</label>
              <p class="info-value">{{ user.bio }}</p>
            </div>

            <!-- Admin Badge -->
            <div v-if="user.is_admin" class="admin-badge">
              <svg class="admin-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              <span>Администратор</span>
            </div>
          </div>
        </div>

        <!-- Posts Section -->
        <div class="posts-section">
          <div class="section-header">
            <h2 class="section-title">Посты пользователя</h2>
          </div>

          <!-- Posts Loading -->
          <div v-if="loadingPosts" class="posts-loading">
            <div class="loading-spinner small"></div>
            <p>Загрузка постов...</p>
          </div>

          <!-- Posts List -->
          <div v-else-if="posts.length > 0" class="posts-list">
            <div v-for="post in posts" :key="post.id" class="post-item">
              <div class="post-content">
                <p>{{ post.content }}</p>
                <div class="post-date">{{ formatPostDate(post.created_at) }}</div>
              </div>
            </div>
          </div>

          <!-- No Posts -->
          <div v-else class="no-posts">
            <p>У пользователя пока нет постов</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../stores/userStore'
import { useAdminStore } from '../stores/adminStore'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const adminStore = useAdminStore()

const user = ref(null)
const posts = ref([])
const isLoading = ref(false)
const loadingPosts = ref(false)
const error = ref(null)

const userId = computed(() => parseInt(route.params.id))

// Показывать ли админские действия
const showAdminActions = computed(() => {
  return (
    userStore.user?.is_admin && // Текущий пользователь - админ
    user.value && // Профиль загружен
    user.value.id !== userStore.user?.id && // Не свой профиль
    !isLoading.value // Не в процессе загрузки
  )
})

// Вычисляемые свойства должны быть внутри setup()
const avatarInitials = computed(() => {
  if (!user.value?.name) return '?'
  return user.value.name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
})

const avatarGradient = computed(() => {
  const colors = [
    ['#FF6B6B', '#FF8E72'],
    ['#4ECDC4', '#44A08D'],
    ['#FF9A56', '#FFB347'],
    ['#667EEA', '#764ba2'],
    ['#F093FB', '#F5576C'],
    ['#4FACFE', '#00F2FE'],
    ['#43E97B', '#38F9D7'],
    ['#FA709A', '#FEE140'],
    ['#30CFD0', '#330867'],
    ['#A8EDEA', '#FED6E3'],
  ]
  
  const seed = user.value?.id?.toString() || user.value?.name || ''
  let hash = 0
  for (let i = 0; i < seed.length; i++) {
    hash = seed.charCodeAt(i) + ((hash << 5) - hash)
  }
  const index = Math.abs(hash) % colors.length
  return `linear-gradient(135deg, ${colors[index][0]} 0%, ${colors[index][1]} 100%)`
})

const coverGradient = computed(() => {
  const colors = [
    ['#667eea', '#764ba2'],
    ['#f093fb', '#f5576c'],
    ['#4facfe', '#00f2fe'],
    ['#43e97b', '#38f9d7'],
    ['#fa709a', '#fee140'],
  ]
  
  const seed = user.value?.email || user.value?.name || ''
  let hash = 0
  for (let i = 0; i < seed.length; i++) {
    hash = seed.charCodeAt(i) + ((hash << 5) - hash)
  }
  const index = Math.abs(hash) % colors.length
  return `linear-gradient(135deg, ${colors[index][0]} 0%, ${colors[index][1]} 100%)`
})

const formattedDate = computed(() => {
  if (!user.value?.created_at) return ''
  const date = new Date(user.value.created_at)
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

// Форматирование даты поста
const formatPostDate = (dateString) => {
  if (!dateString) return ''
  
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return ''
  }
}

// Назначить админом
const promoteToAdmin = async () => {
  if (!confirm(`Назначить пользователя "${user.value.name}" администратором?`)) {
    return
  }
  
  try {
    const result = await adminStore.promoteToAdmin(userId.value)
    if (result.status_code === 200) {
      alert('Пользователь назначен администратором!')
      // Обновляем данные пользователя
      user.value = { ...user.value, ...result.data }
    }
  } catch (error) {
    alert('Ошибка: ' + error.message)
  }
}

// Снять права админа
const demoteFromAdmin = async () => {
  if (!confirm(`Снять права администратора с пользователя "${user.value.name}"?`)) {
    return
  }
  
  try {
    const result = await adminStore.demoteFromAdmin(userId.value)
    if (result.status_code === 200) {
      alert('Пользователь снят с должности администратора!')
      // Обновляем данные пользователя
      user.value = { ...user.value, ...result.data }
    }
  } catch (error) {
    alert('Ошибка: ' + error.message)
  }
}

const deleteUser = async () => {  
  if (!confirm(`Удалить пользователя "${user.value.name}"?`)) return
  
  try {
    const result = await adminStore.deleteUser(userId.value)
    alert(result.message)
    router.push('/admin') // Перенаправляем в админку
  } catch (error) {
    alert('Ошибка: ' + error.message)
  }
}

// Загрузка пользователя
const loadUser = async () => {
  if (!userId.value) return
  
  isLoading.value = true
  error.value = null
  loadingPosts.value = true
  
  try {
    const userData = await userStore.getUserById(userId.value)
    if (userData) {
      user.value = userData
      // Посты уже приходят внутри userData.posts
      posts.value = userData.posts || []
    } else {
      error.value = 'Пользователь не найден'
    }
  } catch (err) {
    error.value = err.message
  } finally {
    isLoading.value = false
    loadingPosts.value = false
  }
}

// Назад
const goBack = () => {
  router.back()
}

// Повторная загрузка
const retryLoad = async () => {
  await loadUser()
}

// Загрузка при монтировании
onMounted(async () => {
  await loadUser()
})
</script>

<style scoped>

.admin-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.admin-action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.875rem;
}

.admin-action-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.admin-action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.promote-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.demote-btn {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.admin-action-icon {
  width: 1rem;
  height: 1rem;
}

/* Адаптивность для админских кнопок */
@media (max-width: 640px) {
  .avatar-section {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .admin-actions {
    width: 100%;
    margin-top: 1rem;
  }
  
  .admin-action-btn {
    flex: 1;
    justify-content: center;
  }
}


/* Стили остаются теми же, только добавлю недостающие */
.user-profile-view {
  min-height: 100vh;
  background: #0b0b0b;
  color: #e6eef6;
  position: relative;
}

/* Loading States */
.loading-overlay,
.error-overlay {
  position: fixed;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(11, 11, 11, 0.9);
  backdrop-filter: blur(8px);
  z-index: 1000;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  border-top-color: #667eea;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

.loading-spinner.small {
  width: 30px;
  height: 30px;
  border-width: 3px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  text-align: center;
  max-width: 400px;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.error-message h3 {
  color: #ef4444;
  margin-bottom: 0.5rem;
}

/* Header */
.profile-header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(11, 11, 11, 0.8);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1rem;
}

.header-content {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: inherit;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.back-icon {
  width: 1rem;
  height: 1rem;
}

.header-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
}

/* Main Content */
.profile-main {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}

.profile-cover {
  height: 200px;
  border-radius: 16px;
  margin-bottom: -50px;
  position: relative;
  z-index: 1;
}

.profile-info {
  position: relative;
  z-index: 2;
  padding: 0 1rem;
}

.avatar-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 1.5rem;
}

.profile-avatar {
  width: 100px;
  height: 100px;
  border-radius: 16px;
  border: 4px solid #0b0b0b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 700;
  color: white;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.user-name {
  font-size: 2rem;
  font-weight: 800;
  margin: 0;
}

.user-email {
  color: #94a3b8;
  font-size: 1rem;
  margin: 0 0 1rem;
}

.user-meta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin: 0.5rem 0;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #94a3b8;
  font-size: 0.875rem;
}

.meta-icon {
  width: 1rem;
  height: 1rem;
  opacity: 0.7;
}

.info-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  margin: 0.5rem 0;
}

.info-label {
  display: block;
  font-size: 0.75rem;
  color: #94a3b8;
  margin-bottom: 0.25rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-value {
  font-size: 1rem;
  margin: 0;
  line-height: 1.5;
}

.admin-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  margin-top: 0.5rem;
}

.admin-icon {
  width: 1rem;
  height: 1rem;
}

/* Posts Section */
.posts-section {
  padding: 0 1rem;
  margin-top: 2rem;
}

.section-header {
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 700;
}

.posts-loading,
.no-posts {
  text-align: center;
  padding: 3rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.no-posts {
  color: #94a3b8;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.post-item {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.post-content p {
  margin: 0 0 0.5rem;
  line-height: 1.5;
}

.post-date {
  font-size: 0.875rem;
  color: #94a3b8;
  margin-top: 0.5rem;
}

/* Buttons */
.btn {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}
</style>
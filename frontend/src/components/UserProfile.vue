<template>
  <div class="user-profile">
    <!-- Loading State -->
    <div v-if="userStore.isLoading && !userStore.user" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>Загрузка профиля...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="userStore.error" class="error-overlay">
      <div class="error-message">
        <h3>Ошибка загрузки</h3>
        <p>{{ userStore.error }}</p>
        <button @click="retryLoad" class="btn btn-primary">Повторить</button>
      </div>
    </div>

    <!-- Content -->
    <div v-else>
      <!-- Header -->
      <header class="profile-header">
        <div class="header-content">
          <h1 class="header-title">Профиль</h1>
          <div class="header-actions">
            <button @click="goToFeed" class="nav-btn">
              Лента постов
            </button>
            <button 
              v-if="userStore.user?.is_admin"
              @click="goToAdmin"
              class="nav-btn admin-btn"
            >
              Админка
            </button>
            <button @click="handleLogout" class="logout-btn" :disabled="userStore.isLoading">
              <span v-if="userStore.isLoading">Выход...</span>
              <span v-else>Выход</span>
            </button>
          </div>
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

            <button @click="openEditModal" class="edit-profile-btn" :disabled="userStore.isLoading">
              Редактировать профиль
            </button>
          </div>

          <div class="user-details">
            <h1 class="user-name">{{ userStore.userName }}</h1>
            <p class="user-email">{{ userStore.userEmail }}</p>
            
            <!-- User Metadata -->
            <div class="user-meta">
              <!-- Location -->
              <div v-if="userStore.userLocation && userStore.userLocation !== 'Не указано'" class="meta-item">
                <svg class="meta-icon" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                </svg>
                <span>{{ userStore.userLocation }}</span>
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
            <div v-if="userStore.userBio && userStore.userBio !== 'User didn\'t add his bio'" class="info-card">
              <label class="info-label">О себе</label>
              <p class="info-value">{{ userStore.userBio }}</p>
            </div>

            <!-- Email -->
            <div class="info-card">
              <label class="info-label">Email</label>
              <p class="info-value">{{ userStore.userEmail }}</p>
            </div>

            <!-- Admin Badge -->
            <div v-if="userStore.user?.is_admin" class="admin-badge">
              <svg class="admin-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              <span>Администратор</span>
            </div>
          </div>
        </div>

        <!-- Create Post Section -->
        <div class="create-post-section">
          <CreatePost @created="handlePostCreated" />
        </div>

        <!-- Posts Section -->
        <div class="posts-section">
          <div class="section-header">
            <h2 class="section-title">Мои посты</h2>
            <button @click="refreshPosts" class="refresh-btn" :disabled="loadingPosts">
              <svg class="refresh-icon" :class="{ 'spinning': loadingPosts }" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>

          <!-- Posts Loading -->
          <div v-if="loadingPosts" class="posts-loading">
            <div class="loading-spinner small"></div>
            <p>Загрузка постов...</p>
          </div>

          <!-- Posts Error -->
          <div v-else-if="postsError" class="posts-error">
            <p>Ошибка загрузки постов: {{ postsError }}</p>
            <button @click="loadPosts" class="btn btn-outline">Повторить</button>
          </div>

          <!-- Posts List -->
          <div v-else-if="posts.length > 0" class="posts-list">
            <div v-for="post in posts" :key="post.id" class="post-item">
              <div class="post-content">
                <p>{{ post.content }}</p>
                <div class="post-meta">
                  <div class="post-date">{{ formatFullDate(post.created_at) }}</div>
                  <div class="post-actions">
                    <button @click="editPost(post)" class="post-action-btn" title="Редактировать">
                      <svg class="action-icon" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                      </svg>
                    </button>
                    <button @click="deletePost(post.id)" class="post-action-btn" title="Удалить">
                      <svg class="action-icon" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
              <!-- Форма редактирования поста -->
            <div v-if="editingPostId === post.id" class="edit-post-form">
              <textarea 
                v-model="editContent" 
                class="edit-textarea" 
                rows="3"
                placeholder="Введите новый текст..."
              ></textarea>
              <div class="edit-actions">
                <button @click="saveEdit" class="btn btn-primary" :disabled="!editContent.trim()">
                  Сохранить
                </button>
                <button @click="cancelEdit" class="btn btn-outline">
                  Отмена
                </button>
              </div>
            </div>
          </div>
        </div>

          <!-- No Posts -->
          <div v-else class="no-posts">
            <p>Пока нет постов</p>
          </div>
        </div>
      </main>

      <!-- Edit Modal -->
      <EditProfileModal
        v-if="showEditModal"
        @close="closeEditModal"
        @save="handleSaveProfile"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useUserStore } from '../stores/userStore'
import { usePostStore } from '../stores/postStore'
import EditProfileModal from './EditProfileModal.vue'
import CreatePost from './CreatePost.vue'
import { useRouter } from 'vue-router'
const router = useRouter()

const goToFeed = () => {
  router.push('/feed')
}

const userStore = useUserStore()
const postStore = usePostStore()

const showEditModal = ref(false)
const posts = ref([])
const loadingPosts = ref(false)
const postsError = ref(null)

const editingPostId = ref(null)
const editContent = ref('')

// Функции для редактирования постов
const editPost = (post) => {
  editingPostId.value = post.id
  editContent.value = post.content
}

const saveEdit = async () => {
  if (!editContent.value.trim()) return
  
  try {
    await postStore.updatePost(editingPostId.value, editContent.value)
    editingPostId.value = null
    editContent.value = ''
    await loadPosts() // Обновляем список постов
  } catch (error) {
    console.error('Ошибка редактирования поста:', error)
    alert('Ошибка редактирования поста: ' + error.message)
  }
}

const cancelEdit = () => {
  editingPostId.value = null
  editContent.value = ''
}

const deletePost = async (postId) => {
  if (!confirm('Вы уверены, что хотите удалить этот пост?')) return
  
  try {
    await postStore.deletePost(postId)
    await loadPosts() // Обновляем список постов
  } catch (error) {
    console.error('Ошибка удаления поста:', error)
    alert('Ошибка удаления поста: ' + error.message)
  }
}

// Добавляем функцию для полного форматирования даты
const formatFullDate = (dateString) => {
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

// Вычисляемые свойства для аватарки и градиента
const avatarInitials = computed(() => {
  if (!userStore.user?.name) return '?'
  return userStore.user.name
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
  
  const seed = userStore.user?.id || userStore.user?.name || ''
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
  
  const seed = userStore.user?.email || userStore.user?.name || ''
  let hash = 0
  for (let i = 0; i < seed.length; i++) {
    hash = seed.charCodeAt(i) + ((hash << 5) - hash)
  }
  const index = Math.abs(hash) % colors.length
  return `linear-gradient(135deg, ${colors[index][0]} 0%, ${colors[index][1]} 100%)`
})

const formattedDate = computed(() => {
  if (!userStore.user?.created_at) return ''
  const date = new Date(userStore.user.created_at)
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

const goToAdmin = () => {
  router.push('/admin')
}

// Загрузка постов ТОЛЬКО текущего пользователя
const loadPosts = async () => {
  if (!userStore.user) return
  
  loadingPosts.value = true
  postsError.value = null
  
  try {
    // Используем метод для получения текущего пользователя (с его постами)
    const userData = await userStore.getUserById(userStore.user.id)
    if (userData && userData.posts) {
      posts.value = userData.posts
    } else {
      posts.value = []
    }
  } catch (error) {
    // Если нет постов - нормальная ситуация
    if (error.message.includes('404') || error.message.includes('No posts')) {
      posts.value = []
    } else {
      postsError.value = error.message
      console.error('Ошибка загрузки постов пользователя:', error)
    }
  } finally {
    loadingPosts.value = false
  }
}

// Обновление постов
const refreshPosts = async () => {
  await loadPosts()
}

// Форматирование даты поста
const formatDate = (dateString) => {
  if (!dateString) return ''
  
  try {
    const date = new Date(dateString)
    const now = new Date()
    const diffMs = now - date
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMs / 3600000)
    const diffDays = Math.floor(diffMs / 86400000)
    
    if (diffMins < 1) return 'Только что'
    if (diffMins < 60) return `${diffMins} мин назад`
    if (diffHours < 24) return `${diffHours} ч назад`
    if (diffDays < 7) return `${diffDays} д назад`
    
    return date.toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'short'
    })
  } catch {
    return ''
  }
}

// Загрузка при монтировании
onMounted(async () => {
  if (userStore.user) {
    await loadPosts()
  }
})

// Следим за изменением пользователя
watch(() => userStore.user, (newUser) => {
  if (newUser) {
    loadPosts()
  } else {
    posts.value = []
  }
}, { immediate: true })

const openEditModal = () => {
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
}

const handleSaveProfile = async (updatedData) => {
  try {
    await userStore.updateProfile(updatedData)
    closeEditModal()
  } catch (error) {
    console.error('Ошибка сохранения профиля:', error)
  }
}

const handleLogout = async () => {
  try {
    await userStore.logout()
    // Редирект на страницу авторизации
    router.push('/auth')
  } catch (error) {
    console.error('Ошибка выхода:', error)
    // Все равно редиректим
    router.push('/auth')
  }
}

const retryLoad = async () => {
  await userStore.loadUser()
}

// Обработчик создания нового поста
const handlePostCreated = async () => {
  await loadPosts()
}
</script>

<style scoped>

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.post-actions {
  display: flex;
  gap: 0.5rem;
}

.post-action-btn {
  padding: 0.25rem;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.3s;
}

.post-action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #e6eef6;
}

.action-icon {
  width: 1rem;
  height: 1rem;
}

/* Форма редактирования поста */
.edit-post-form {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.edit-textarea {
  width: 100%;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #e6eef6;
  font-size: 1rem;
  resize: vertical;
  margin-bottom: 1rem;
  font-family: inherit;
}

.edit-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.edit-actions {
  display: flex;
  gap: 1rem;
}

.user-profile {
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
  justify-content: space-between;
  align-items: center;
}

.header-title {
  font-size: 1.5rem;
  font-weight: 700;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}


.logout-btn {
  padding: 0.5rem 1rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 8px;
  color: #ef4444;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s;
}

.logout-btn:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.2);
}

.logout-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

.edit-profile-btn {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: inherit;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s;
}

.edit-profile-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.edit-profile-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

/* Create Post Section */
.create-post-section {
  margin: 2rem 0;
  padding: 0 1rem;
}

/* Posts Section */
.posts-section {
  padding: 0 1rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 700;
}

.refresh-btn {
  padding: 0.5rem;
  background: transparent;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s;
}

.refresh-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
  color: #e6eef6;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.refresh-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

.posts-loading,
.posts-error,
.no-posts {
  text-align: center;
  padding: 3rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.posts-error {
  color: #ef4444;
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

.btn-outline {
  background: transparent;
  color: #e6eef6;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-outline:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}


.profile-navigation {
  display: none;
}

.nav-btn {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: inherit;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s;
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

</style>
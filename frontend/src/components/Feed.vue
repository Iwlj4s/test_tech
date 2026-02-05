<template>
  <div class="feed-page">
    <!-- Заголовок -->
    <header class="feed-header">
      <h1 class="feed-title">Лента постов</h1>
      <div class="feed-actions">
        <button @click="goToProfile" class="nav-btn">
          Мой профиль
        </button>
        <button @click="refreshPosts" class="refresh-btn" :disabled="postStore.isLoading">
          <svg class="refresh-icon" :class="{ 'spinning': postStore.isLoading }" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </header>

    <!-- Состояние загрузки -->
    <div v-if="postStore.isLoading && posts.length === 0" class="loading-state">
      <div class="loading-spinner"></div>
      <p>Загрузка постов...</p>
    </div>

    <!-- Состояние ошибки -->
    <div v-else-if="postStore.error" class="error-state">
      <p class="error-message">Ошибка: {{ postStore.error }}</p>
      <button @click="loadPosts" class="btn btn-primary">Повторить</button>
    </div>

    <!-- Список постов -->
    <div v-else class="posts-container">
      <div v-if="posts.length === 0" class="empty-state">
        <p>Пока нет постов</p>
      </div>

      <div v-for="post in posts" :key="post.id" class="post-card">
        <div class="post-header">
          <div class="author-info" @click="goToUserProfile(post.user_id)">
            <div 
              class="author-avatar"
              :style="{ background: getAvatarGradient(post.user_name, post.user_id) }"
            >
              {{ getInitials(post.user_name || 'Пользователь') }}
            </div>
            <div class="author-details">
              <div class="author-name">{{ post.user_name || 'Пользователь' }}</div>
              <div class="post-date">{{ formatFullDate(post.created_at) }}</div>
            </div>
          </div>
          
          <!-- Действия с постом (только для своих постов) -->
          <div v-if="userStore.user?.id === post.user_id" class="post-actions">
            <button @click="editPost(post)" class="action-btn" title="Редактировать">
              <svg class="action-icon" viewBox="0 0 20 20" fill="currentColor">
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
              </svg>
            </button>
            <button @click="deletePost(post.id)" class="action-btn" title="Удалить">
              <svg class="action-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>

        <div class="post-content">
          <p>{{ post.content }}</p>
        </div>

        <!-- Редактирование поста -->
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePostStore } from '../stores/postStore'
import { useUserStore } from '../stores/userStore'

const router = useRouter()
const postStore = usePostStore()
const userStore = useUserStore()

const posts = ref([])
const editingPostId = ref(null)
const editContent = ref('')

// Загрузка постов
const loadPosts = async () => {
  try {
    const allPosts = await postStore.fetchAllPosts()
    posts.value = allPosts
  } catch (error) {
    console.error('Ошибка загрузки постов:', error)
  }
}

// Обновление постов
const refreshPosts = async () => {
  await loadPosts()
}

// Переход в профиль
const goToProfile = () => {
  router.push('/profile')
}

// Переход в профиль пользователя (будущая функциональность)
const goToUserProfile = (userId) => {
  if (userId === userStore.user?.id) {
    router.push('/profile')
  } else {
    router.push(`/user/${userId}`)
  }
}

// Получение инициалов для аватара
const getInitials = (name) => {
  if (!name) return '?'
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

// Получение градиента для аватара
const getAvatarGradient = (name, userId) => {
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
  
  const seed = userId?.toString() || name || ''
  let hash = 0
  for (let i = 0; i < seed.length; i++) {
    hash = seed.charCodeAt(i) + ((hash << 5) - hash)
  }
  const index = Math.abs(hash) % colors.length
  return `linear-gradient(135deg, ${colors[index][0]} 0%, ${colors[index][1]} 100%)`
}

// Форматирование полной даты
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

// Редактирование поста
const editPost = (post) => {
  editingPostId.value = post.id
  editContent.value = post.content
}

// Сохранение изменений
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

// Отмена редактирования
const cancelEdit = () => {
  editingPostId.value = null
  editContent.value = ''
}

// Удаление поста
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

// Загрузка при монтировании
onMounted(async () => {
  await loadPosts()
})
</script>

<style scoped>
.feed-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
  min-height: 100vh;
  background: #0b0b0b;
  color: #e6eef6;
}

.feed-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.feed-title {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0;
}

.feed-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
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

/* Состояния */
.loading-state,
.error-state,
.empty-state {
  text-align: center;
  padding: 3rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  border-top-color: #667eea;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  color: #ef4444;
  margin-bottom: 1rem;
}

/* Карточка поста */
.posts-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.post-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s;
}

.post-card:hover {
  border-color: rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.08);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  transition: opacity 0.3s;
}

.author-info:hover {
  opacity: 0.8;
}

.author-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.125rem;
  color: white;
}

.author-details {
  flex: 1;
}

.author-name {
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.post-date {
  font-size: 0.875rem;
  color: #94a3b8;
}

.post-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.25rem;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #e6eef6;
}

.action-icon {
  width: 1rem;
  height: 1rem;
}

.post-content {
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.post-content p {
  margin: 0;
}

/* Форма редактирования поста */
.edit-post-form {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
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
</style>
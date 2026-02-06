<!-- src/components/AdminPanel.vue -->
<template>
  <div class="admin-panel">
    <!-- Заголовок -->
    <header class="admin-header">
      <h1 class="admin-title">Панель администратора</h1>
      <div class="admin-actions">
        <button @click="goToProfile" class="btn btn-outline">
          Мой профиль
        </button>
        <button @click="goToFeed" class="btn btn-outline">
          Лента
        </button>
        <button @click="switchView('users')" class="btn" :class="{ 'btn-primary': currentView === 'users' }">
          Пользователи
        </button>
        <button @click="switchView('deleted')" class="btn" :class="{ 'btn-primary': currentView === 'deleted' }">
          Удаленные
        </button>
      </div>
    </header>

    <!-- Поиск -->
    <div class="search-section">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Поиск пользователей по имени, email или местоположению..."
        class="search-input"
        @input="performSearch"
      />
      <button @click="refreshUsers" class="btn btn-primary" :disabled="adminStore.isLoading">
        Обновить
      </button>
    </div>

    <!-- Состояние загрузки -->
    <div v-if="adminStore.isLoading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>Загрузка данных...</p>
    </div>

    <!-- Состояние ошибки -->
    <div v-else-if="adminStore.error" class="error-state">
      <p class="error-message">Ошибка: {{ adminStore.error }}</p>
      <button @click="loadUsers" class="btn btn-primary">Повторить</button>
    </div>

    <!-- Просмотр пользователей -->
    <div v-else-if="currentView === 'users'" class="users-view">
      <h2 class="section-title">Все пользователи ({{ filteredUsers.length }})</h2>
      
      <div v-if="filteredUsers.length === 0" class="empty-state">
        <p>Пользователи не найдены</p>
      </div>

      <div v-else class="users-grid">
        <div v-for="user in filteredUsers" :key="user.id" class="user-card">
          <div class="user-header">
            <div 
              class="user-avatar"
              :style="{ background: getAvatarGradient(user.name, user.id) }"
            >
              {{ getInitials(user.name) }}
            </div>
            <div class="user-info">
              <h3 class="user-name">{{ user.name }}</h3>
              <p class="user-email">{{ user.email }}</p>
              <div class="user-meta">
                <span v-if="user.location" class="meta-item">
                  {{ user.location }}
                </span>
                <span class="meta-item">
                  Зарегистрирован: {{ formatDate(user.created_at) }}
                </span>
              </div>
            </div>
          </div>

          <div class="user-actions">
            <button @click="viewUserProfile(user.id)" class="action-btn">
              Просмотр профиля
            </button>
            
            <div v-if="user.id !== userStore.user?.id" class="admin-actions">
              <button 
                v-if="!user.is_admin"
                @click="promoteUser(user.id)"
                class="action-btn promote-btn"
                :disabled="adminStore.isLoading"
              >
                Назначить админом
              </button>
              
              <button 
                v-else
                @click="demoteUser(user.id)"
                class="action-btn demote-btn"
                :disabled="adminStore.isLoading"
              >
                Снять с должности
              </button>

              <button 
                @click="deleteUser(user.id)"
                class="action-btn delete-btn"
                :disabled="adminStore.isLoading"
              >
                Удалить
              </button>
            </div>
          </div>

          <!-- Бейдж админа -->
          <div v-if="user.is_admin" class="admin-badge">
            Администратор
          </div>
        </div>
      </div>
    </div>

    <!-- Просмотр удаленных пользователей -->
    <div v-else class="deleted-view">
      <h2 class="section-title">Удаленные пользователи ({{ deletedUsers.length }})</h2>
      
      <div v-if="deletedUsers.length === 0" class="empty-state">
        <p>Нет удаленных пользователей</p>
      </div>

      <div v-else class="users-grid">
        <div v-for="user in deletedUsers" :key="user.id" class="user-card deleted">
          <div class="user-header">
            <div 
              class="user-avatar"
              :style="{ background: getAvatarGradient(user.name, user.id) }"
            >
              {{ getInitials(user.name) }}
            </div>
            <div class="user-info">
              <h3 class="user-name">{{ user.name }}</h3>
              <p class="user-email">{{ user.email }}</p>
              <div class="user-meta">
                <span v-if="user.location" class="meta-item">
                  {{ user.location }}
                </span>
                <span class="meta-item deleted-badge">
                  <h3 class="meta-item deleted-badge">Причина блокировки:</h3> 
                  <p class="user-email">{{ user.deletion_reason  || 'Удалил аккаунт самостоятельно'}}</p>
                  Удален
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/userStore'
import { useAdminStore } from '../stores/adminStore'

const router = useRouter()
const userStore = useUserStore()
const adminStore = useAdminStore()

const currentView = ref('users')
const searchQuery = ref('')
const filteredUsers = ref([])

// Получение удаленных пользователей
const deletedUsers = computed(() => adminStore.deletedUsers)

// Переключение вью
const switchView = async (view) => {
  currentView.value = view
  searchQuery.value = ''
  
  if (view === 'users') {
    await loadUsers()
  } else if (view === 'deleted') {
    await loadDeletedUsers()
  }
}

// Загрузка пользователей
const loadUsers = async () => {
  try {
    await adminStore.getAllUsers()
    performSearch()
  } catch (error) {
    console.error('Ошибка загрузки пользователей:', error)
  }
}

// Загрузка удаленных пользователей
const loadDeletedUsers = async () => {
  try {
    await adminStore.fetchDeletedUsers()
  } catch (error) {
    console.error('Ошибка загрузки удаленных пользователей:', error)
  }
}

// Обновление пользователей
const refreshUsers = async () => {
  await loadUsers()
}

// Поиск пользователей
const performSearch = () => {
  if (!searchQuery.value.trim()) {
    filteredUsers.value = adminStore.allUsers
  } else {
    filteredUsers.value = adminStore.searchUsers(searchQuery.value)
  }
}

// Переход в профиль
const goToProfile = () => {
  router.push('/profile')
}

// Переход в ленту
const goToFeed = () => {
  router.push('/feed')
}

// Просмотр профиля пользователя
const viewUserProfile = (userId) => {
  router.push(`/user/${userId}`)
}

// Назначение администратором
const promoteUser = async (userId) => {
  if (!confirm('Назначить пользователя администратором?')) return
  
  try {
    const result = await adminStore.promoteToAdmin(userId)
    if (result.status_code === 200) {
      alert('Пользователь назначен администратором!')
      await loadUsers() // Обновляем список
    }
  } catch (error) {
    alert('Ошибка: ' + error.message)
  }
}

// Снятие прав администратора
const demoteUser = async (userId) => {
  if (!confirm('Снять права администратора?')) return
  
  try {
    const result = await adminStore.demoteFromAdmin(userId)
    if (result.status_code === 200) {
      alert('Пользователь снят с должности администратора!')
      await loadUsers() // Обновляем список
    }
  } catch (error) {
    alert('Ошибка: ' + error.message)
  }
}

// Удаление пользователя (с запросом причины)
const deleteUser = async (userId) => {
  const user = adminStore.allUsers.find(u => u.id === userId)
  if (!user) return
  
  // Запрашиваем причину удаления
  const reason = prompt(`Укажите причину удаления пользователя "${user.name}":`, '')
  
  if (reason === null) return // Пользователь отменил
  if (!reason.trim()) {
    alert('Причина удаления обязательна!')
    return
  }
  
  if (!confirm(`Вы уверены, что хотите удалить пользователя "${user.name}"?`)) return
  
  try {
    const result = await adminStore.deleteUser(userId, reason)
    alert(result.message)
    
    // Обновляем соответствующие списки
    if (currentView.value === 'users') {
      await loadUsers()
    }
    await loadDeletedUsers()
  } catch (error) {
    alert('Ошибка: ' + error.message)
  }
}


// Утилиты для аватаров
const getInitials = (name) => {
  if (!name) return '?'
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const getAvatarGradient = (name, userId) => {
  const colors = [
    ['#FF6B6B', '#FF8E72'],
    ['#4ECDC4', '#44A08D'],
    ['#FF9A56', '#FFB347'],
    ['#667EEA', '#764ba2'],
    ['#F093FB', '#F5576C'],
  ]
  
  const seed = userId?.toString() || name || ''
  let hash = 0
  for (let i = 0; i < seed.length; i++) {
    hash = seed.charCodeAt(i) + ((hash << 5) - hash)
  }
  const index = Math.abs(hash) % colors.length
  return `linear-gradient(135deg, ${colors[index][0]} 0%, ${colors[index][1]} 100%)`
}

// Форматирование даты
const formatDate = (dateString) => {
  if (!dateString) return ''
  
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    })
  } catch {
    return ''
  }
}

// Проверка прав при монтировании
onMounted(async () => {
  if (!userStore.user?.is_admin) {
    alert('У вас нет прав администратора')
    router.push('/profile')
    return
  }
  
  await loadUsers()
})
</script>

<style scoped>
.admin-panel {
  min-height: 100vh;
  background: #0b0b0b;
  color: #e6eef6;
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.admin-header {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.admin-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.admin-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.search-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #e6eef6;
  font-size: 1rem;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
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
  margin: 2rem 0;
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

/* Секции */
.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
}

/* Сетка пользователей */
.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

/* Карточка пользователя */
.user-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s;
  position: relative;
}

.user-card:hover {
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.user-card.deleted {
  opacity: 0.7;
  border-color: rgba(239, 68, 68, 0.3);
}

.user-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.user-avatar {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 0.25rem;
}

.user-email {
  color: #94a3b8;
  font-size: 0.875rem;
  margin: 0 0 0.75rem;
  word-break: break-all;
}

.user-meta {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.meta-item {
  font-size: 0.75rem;
  color: #94a3b8;
}

.deleted-badge {
  color: #ef4444;
  font-weight: 600;
  font-size: 15px;
}

/* Действия с пользователем */
.user-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.action-btn {
  width: 100%;
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
  color: #e6eef6;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.875rem;
  font-weight: 500;
}

.action-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.admin-actions {
  display: flex;
  gap: 0.5rem;
}

.admin-actions .action-btn {
  flex: 1;
}

.promote-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-color: transparent;
  color: white;
}

.demote-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border-color: transparent;
  color: white;
}

.delete-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  border-color: transparent;
  color: white;
}

.restore-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  border-color: transparent;
  color: white;
}

/* Бейдж админа */
.admin-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.25rem 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
}

/* Кнопки */
.btn {
  padding: 0.5rem 1rem;
  border-radius: 8px;
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

/* Адаптивность */
@media (max-width: 768px) {
  .users-grid {
    grid-template-columns: 1fr;
  }
  
  .admin-actions {
    flex-direction: column;
  }
  
  .search-section {
    flex-direction: column;
  }
  
  .user-actions .admin-actions {
    flex-direction: row;
  }
}
</style>
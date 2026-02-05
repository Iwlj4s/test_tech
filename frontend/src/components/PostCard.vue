<template>
  <div class="post-card">
    <!-- Post Header -->
    <div class="post-header">
      <div class="author-info" @click="goToUserProfile">
        <div class="author-avatar">
          {{ getInitials(post.user_name || 'Пользователь') }}
        </div>
        <div class="author-details">
          <div class="author-name">{{ post.user_name || 'Пользователь' }}</div>
          <div class="post-time">{{ formatDate(post.created_at) }}</div>
        </div>
      </div>
    </div>

    <!-- Post Content -->
    <div class="post-content">
      <p>{{ post.content }}</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  post: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['user-click'])

// Получение инициалов для аватара
const getInitials = (name) => {
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

// Форматирование даты
const formatDate = (dateString) => {
  if (!dateString) return ''
  
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
}

// Переход в профиль пользователя
const goToUserProfile = () => {
  if (props.post.user_id) {
    emit('user-click', props.post.user_id)
  }
}
</script>

<style scoped>
.post-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s;
  cursor: pointer;
}

.post-card:hover {
  border-color: rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.08);
}

.post-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.author-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
  color: #e6eef6;
  margin-bottom: 0.25rem;
}

.post-time {
  font-size: 0.875rem;
  color: #94a3b8;
}

.post-content {
  font-size: 1rem;
  line-height: 1.6;
  color: #e6eef6;
}

.post-content p {
  margin: 0;
}
</style>
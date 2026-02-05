<template>
  <div class="create-post">
    <textarea
      v-model="postContent"
      placeholder="Что у вас нового?"
      class="post-textarea"
      :maxlength="maxLength"
      rows="3"
      @input="updateCounter"
      :disabled="postStore.isLoading"
    ></textarea>
    
    <div v-if="postStore.error" class="error-message">
      {{ postStore.error }}
      <button @click="postStore.clearError()" class="error-close">×</button>
    </div>
    
    <div class="create-post-footer">
      <div class="character-counter" :class="{ 
        'warning': characterCount > maxLength * 0.8,
        'danger': characterCount > maxLength 
      }">
        {{ characterCount }} / {{ maxLength }}
      </div>
      
      <button
        @click="handleSubmit"
        class="post-submit-btn"
        :disabled="!canSubmit || postStore.isLoading"
        :class="{ 'loading': postStore.isLoading }"
      >
        <span v-if="postStore.isLoading">Публикация...</span>
        <span v-else>Опубликовать</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { usePostStore } from '../stores/postStore' // ИЗМЕНЕНО: usePostStore вместо UserPostStore

const postStore = usePostStore() // Это уже правильный вызов
const emit = defineEmits(['created'])

const postContent = ref('')
const maxLength = 280

const characterCount = computed(() => postContent.value.length)
const canSubmit = computed(() => {
  return postContent.value.trim().length > 0 && 
         postContent.value.length <= maxLength &&
         !postStore.isLoading
})

const updateCounter = () => {
  if (postContent.value.length > maxLength) {
    postContent.value = postContent.value.substring(0, maxLength)
  }
}

const handleSubmit = async () => {
  if (!canSubmit.value) return
  
  try {
    const newPost = await postStore.createPost(postContent.value.trim())
    emit('created', newPost)
    postContent.value = ''
  } catch (error) {
    console.error('Error creating post:', error)
  }
}
</script>


<style scoped>
.create-post {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 1.5rem;
}

.post-textarea {
  width: 100%;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #e6eef6;
  font-size: 1rem;
  resize: none;
  font-family: inherit;
  transition: all 0.3s;
  min-height: 100px;
  outline: none;
}

.post-textarea:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.post-textarea::placeholder {
  color: #94a3b8;
}

.post-textarea:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  margin: 0.75rem 0;
  padding: 0.75rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 8px;
  color: #ef4444;
  font-size: 0.875rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.error-close {
  background: transparent;
  border: none;
  color: #ef4444;
  cursor: pointer;
  font-size: 1.25rem;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background 0.3s;
}

.error-close:hover {
  background: rgba(239, 68, 68, 0.1);
}

.create-post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.character-counter {
  font-size: 0.875rem;
  font-weight: 500;
  transition: color 0.3s;
}

.character-counter:not(.warning):not(.danger) {
  color: #94a3b8;
}

.character-counter.warning {
  color: #f59e0b;
}

.character-counter.danger {
  color: #ef4444;
}

.post-submit-btn {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 10px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.875rem;
  min-width: 120px;
}

.post-submit-btn:hover:not(:disabled):not(.loading) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
}

.post-submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.post-submit-btn.loading {
  opacity: 0.8;
  cursor: wait;
}
</style>
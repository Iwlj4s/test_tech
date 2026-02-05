<!-- components/EditProfileModal.vue -->
<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <!-- Modal Header -->
      <div class="modal-header">
        <h2 class="modal-title">Редактировать профиль</h2>
        <button @click="closeModal" class="modal-close-btn">
          <svg class="close-icon" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <!-- Modal Body -->
      <div class="modal-body">
        <div class="form-group">
          <label class="form-label">Имя</label>
          <input
            v-model="formData.name"
            type="text"
            class="form-input"
            placeholder="Ваше имя"
            :disabled="isSaving"
          />
        </div>

        <div class="form-group">
          <label class="form-label">Email</label>
          <input
            v-model="formData.email"
            type="email"
            class="form-input"
            placeholder="your@email.com"
            :disabled="isSaving"
          />
        </div>

        <div class="form-group">
          <label class="form-label">О себе</label>
          <textarea
            v-model="formData.bio"
            class="form-textarea"
            placeholder="Расскажите о себе..."
            rows="4"
            :disabled="isSaving"
          ></textarea>
        </div>

        <div class="form-group">
          <label class="form-label">Местоположение</label>
          <input
            v-model="formData.location"
            type="text"
            class="form-input"
            placeholder="Город, Страна"
            :disabled="isSaving"
          />
        </div>
      </div>

      <!-- Modal Footer -->
      <div class="modal-footer">
        <button @click="closeModal" class="btn btn-secondary" :disabled="isSaving">
          Отмена
        </button>
        <button @click="saveProfile" class="btn btn-primary" :disabled="isSaving">
          <span v-if="isSaving">Сохранение...</span>
          <span v-else>Сохранить</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '../stores/userStore'

const emit = defineEmits(['close', 'save'])
const userStore = useUserStore()
const isSaving = ref(false)

const formData = ref({
  name: userStore.user?.name || '',
  email: userStore.user?.email || '',
  bio: userStore.user?.bio || '',
  location: userStore.user?.location || ''
})

const hasChanges = computed(() => {
  if (!userStore.user) return false
  
  return (
    formData.value.name !== userStore.user.name ||
    formData.value.email !== userStore.user.email ||
    formData.value.bio !== userStore.user.bio ||
    formData.value.location !== userStore.user.location
  )
})

const closeModal = () => {
  if (!isSaving.value) {
    emit('close')
  }
}

const saveProfile = async () => {
  if (!hasChanges.value || isSaving.value) return
  
  isSaving.value = true
  
  try {
    const updates = {}
    
    if (formData.value.name !== userStore.user?.name) {
      updates.name = formData.value.name
    }
    if (formData.value.email !== userStore.user?.email) {
      updates.email = formData.value.email
    }
    if (formData.value.bio !== userStore.user?.bio) {
      updates.bio = formData.value.bio
    }
    if (formData.value.location !== userStore.user?.location) {
      updates.location = formData.value.location
    }
    
    if (Object.keys(updates).length > 0) {
      emit('save', updates)
    }
    
    closeModal()
  } catch (error) {
    console.error('Save error:', error)
  } finally {
    isSaving.value = false
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  width: 100%;
  max-width: 500px;
  background: #1a1a1a;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
}

.modal-close-btn {
  padding: 0.5rem;
  background: transparent;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s;
}

.modal-close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #e6eef6;
}

.close-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.modal-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #94a3b8;
  margin-bottom: 0.5rem;
}

.form-input,
.form-textarea {
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #e6eef6;
  font-size: 1rem;
  transition: all 0.3s;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input:disabled,
.form-textarea:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.btn {
  flex: 1;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 8px;
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

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: #e6eef6;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-secondary:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.2);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}
</style>
// src/stores/postStore.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

// Утилита для обработки ошибок
const handleApiError = async (response, defaultMessage = 'Произошла ошибка') => {
  if (!response.ok) {
    let errorMessage = defaultMessage
    try {
      const errorData = await response.json()
      errorMessage = errorData.detail || errorData.message || errorData.error || `${response.status}: ${response.statusText}`
    } catch {
      errorMessage = `${response.status}: ${response.statusText}`
    }
    throw new Error(errorMessage)
  }
  return response
}

export const usePostStore = defineStore('post', () => {
  const posts = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  // Получение всех постов (лента)
  const fetchAllPosts = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetch(`${API_BASE_URL}/posts/`, {
        method: 'GET',
        credentials: 'include'
      })

      await handleApiError(response, 'Ошибка загрузки постов')

      const data = await response.json()
      posts.value = data.data || [] // Теперь точно возвращаем массив
      return posts.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Получение поста по ID
  const fetchPostById = async (postId) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetch(`${API_BASE_URL}/posts/post/${postId}`, {
        method: 'GET',
        credentials: 'include'
      })

      await handleApiError(response, 'Ошибка загрузки поста')

      const data = await response.json()
      return data.data || null
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Создание поста
  const createPost = async (content) => {
    isLoading.value = true
    error.value = null
    
    try {
      // Проверяем, что пользователь авторизован
      const { useUserStore } = await import('./userStore.js')
      const userStore = useUserStore()
      
      if (!userStore.isAuthenticated) {
        throw new Error('Требуется авторизация для создания поста')
      }
      
      console.log('Создание поста, контент:', content)
      
      const response = await fetch(`${API_BASE_URL}/posts/create_post`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        credentials: 'include', // Важно для отправки cookie
        body: JSON.stringify({ content })
      })

      console.log('Создание поста, статус ответа:', response.status)
      
      await handleApiError(response, 'Ошибка создания поста')

      const data = await response.json()
      console.log('Создание поста, успешный ответ:', data)
      
      // Добавляем новый пост в начало списка
      if (data.data) {
        posts.value.unshift(data.data)
      }
      
      return data.data || data
    } catch (err) {
      console.error('Ошибка создания поста:', err)
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Обновление поста
  const updatePost = async (postId, content) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetch(`${API_BASE_URL}/posts/update_post/${postId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ content })
      })

      await handleApiError(response, 'Ошибка обновления поста')

      const data = await response.json()
      
      // Обновляем пост в локальном списке
      const index = posts.value.findIndex(p => p.id === postId)
      if (index !== -1 && data.data) {
        posts.value[index] = { ...posts.value[index], ...data.data }
      }
      
      return data.data || data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Удаление поста
  const deletePost = async (postId) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetch(`${API_BASE_URL}/posts/delete_post/${postId}`, {
        method: 'DELETE',
        credentials: 'include'
      })

      await handleApiError(response, 'Ошибка удаления поста')

      const data = await response.json()
      
      // Удаляем пост из локального списка
      posts.value = posts.value.filter(post => post.id !== postId)
      
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Очистка ошибки
  const clearError = () => {
    error.value = null
  }

  // Сброс состояния
  const reset = () => {
    posts.value = []
    isLoading.value = false
    error.value = null
  }

  return {
    // State
    posts,
    isLoading,
    error,
    
    // Actions
    fetchAllPosts,
    fetchPostById,
    createPost,
    updatePost,
    deletePost,
    clearError,
    reset
  }
})
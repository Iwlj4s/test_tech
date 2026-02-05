import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

// Утилита для обработки ошибок
const handleApiError = async (response, defaultMessage = 'Произошла ошибка') => {
  if (!response.ok) {
    let errorMessage = defaultMessage
    try {
      const errorData = await response.json()
      
      if (errorData.detail) {
        if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail
        } 
        else if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map(err => {
            if (err.loc && err.msg) {
              return `${err.loc.join('.')}: ${err.msg}`
            }
            return JSON.stringify(err)
          }).join('; ')
        }
        else if (typeof errorData.detail === 'object') {
          errorMessage = JSON.stringify(errorData.detail)
        }
      } else if (errorData.message) {
        errorMessage = errorData.message
      } else if (errorData.error) {
        errorMessage = errorData.error
      } else if (typeof errorData === 'string') {
        errorMessage = errorData
      }
    } catch {
      errorMessage = `${response.status}: ${response.statusText}`
    }
    throw new Error(errorMessage)
  }
  return response
}

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const isAuthenticated = ref(false)
  const isLoading = ref(false)
  const error = ref(null)

  const userName = computed(() => user.value?.name || '')
  const userEmail = computed(() => user.value?.email || '')
  const userBio = computed(() => user.value?.bio || '')
  const userLocation = computed(() => user.value?.location || '')
  const isAdmin = computed(() => user.value?.is_admin || false)
  const registrationDate = computed(() => {
    if (!user.value?.created_at) return ''
    return new Date(user.value.created_at).toLocaleDateString('ru-RU')
  })

  // Вход
  const login = async (email, password) => {
    isLoading.value = true
    error.value = null
    
    try {
      if (!email || !password) {
        throw new Error('Email и пароль обязательны')
      }
      
      console.log('Вход, отправляю запрос...')
      
      const response = await fetch(`${API_BASE_URL}/users/sign_in`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        credentials: 'include', 
        body: JSON.stringify({ 
          email: email.trim().toLowerCase(), 
          password: password 
        })
      })
      
      console.log('Вход, статус ответа:', response.status)
      
      if (!response.ok) {
        let errorMessage = 'Ошибка входа'
        try {
          const errorData = await response.json()
          console.log('Вход, ошибка от сервера:', errorData)
          
          if (errorData.detail) {
            errorMessage = errorData.detail
          } else if (errorData.message) {
            errorMessage = errorData.message
          } else if (errorData.error) {
            errorMessage = errorData.error
          }
        } catch {
          errorMessage = `${response.status}: ${response.statusText}`
        }
        throw new Error(errorMessage)
      }
      
      const data = await response.json()
      console.log('Вход, успешный ответ:', data)
      
      // Сохраняем данные пользователя
      if (data.data) {
        user.value = data.data
        isAuthenticated.value = true
        console.log('Вход успешен, пользователь:', data.data)
      } else {
        user.value = data
        isAuthenticated.value = true
      }
      
      await loadUser()
      
      return data
    } catch (err) {
      console.error('Ошибка входа:', err)
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Регистрация 
  const register = async (name, email, password, bio = '', location = '') => {
    isLoading.value = true
    error.value = null
    
    try {
      if (!name || !email || !password) {
        throw new Error('Все обязательные поля должны быть заполнены')
      }
      
      const userData = {
        name: name.trim(),
        email: email.trim().toLowerCase(),
        password: password
      }
      
      if (bio && bio.trim()) {
        userData.bio = bio.trim()
      }
      
      if (location && location.trim()) {
        userData.location = location.trim()
      }
      
      console.log('Регистрация, отправляемые данные:', { ...userData, password: '***' })
      
      const response = await fetch(`${API_BASE_URL}/users/sign_up`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        credentials: 'include', 
        body: JSON.stringify(userData)
      })

      console.log('Регистрация, статус ответа:', response.status)
      
      // Проверяем успешность ответа
      if (!response.ok) {
        let errorMessage = 'Ошибка регистрации'
        try {
          const errorData = await response.json()
          console.log('Регистрация, ошибка от сервера:', errorData)
          
          if (errorData.detail) {
            if (typeof errorData.detail === 'string') {
              errorMessage = errorData.detail
            } else if (Array.isArray(errorData.detail)) {
              errorMessage = errorData.detail.map(err => 
                err.loc ? `${err.loc.join('.')}: ${err.msg}` : err.msg
              ).join('; ')
            }
          } else if (errorData.message) {
            errorMessage = errorData.message
          }
        } catch {
          errorMessage = `${response.status}: ${response.statusText}`
        }
        throw new Error(errorMessage)
      }
      
      const data = await response.json()
      console.log('Регистрация, успешный ответ:', data)
      
      console.log('Автоматический вход после регистрации...')
      try {
        await login(email, password)
        console.log('Автоматический вход успешен')
      } catch (loginError) {
        console.warn('Не удалось автоматически войти после регистрации:', loginError.message)
        if (data.data) {
          user.value = data.data
          isAuthenticated.value = true
        }
      }
      
      return data
    } catch (err) {
      console.error('Ошибка регистрации:', err)
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Загрузка текущего пользователя
  const loadUser = async () => {
    if (isLoading.value) return
    
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetch(`${API_BASE_URL}/users/me/`, {
        method: 'GET',
        credentials: 'include'
      })

      // Если 401 или 403 - пользователь не авторизован
      if (response.status === 401 || response.status === 403) {
        user.value = null
        isAuthenticated.value = false
        return null
      }

      await handleApiError(response, 'Ошибка загрузки пользователя')
      
      const data = await response.json()
      user.value = data.data || data
      isAuthenticated.value = true
      
      return user.value
    } catch (err) {
      console.warn('Ошибка загрузки пользователя:', err.message)
      error.value = err.message
      user.value = null
      isAuthenticated.value = false
      return null
    } finally {
      isLoading.value = false
    }
  }

  // Обновление профиля
  const updateProfile = async (updates) => {
    if (!isAuthenticated.value) {
      throw new Error('Требуется авторизация')
    }
    
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetch(`${API_BASE_URL}/users/me/update`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(updates)
      })

      await handleApiError(response, 'Ошибка обновления профиля')

      const data = await response.json()
      
      // Обновляем локальные данные
      if (user.value && data.data) {
        user.value = { ...user.value, ...data.data }
      }
      
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Выход - исправленная версия
  const logout = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      console.log('Выход, отправляю запрос...')
      
      const response = await fetch(`${API_BASE_URL}/users/logout`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Accept': 'application/json',
        }
      })
      
      console.log('Выход, статус ответа:', response.status)
      
      // Даже если ответ не 200, всё равно сбрасываем состояние
      if (response.ok) {
        try {
          const data = await response.json()
          console.log('Выход успешен:', data)
        } catch {
          console.log('Выход: нет тела ответа')
        }
      } else {
        console.log('Выход: сервер вернул ошибку, но продолжаем выход')
      }
      
      // Всегда сбрасываем состояние
      user.value = null
      isAuthenticated.value = false
      error.value = null
      
      console.log('Состояние сброшено')
      
      return { success: true }
    } catch (err) {
      console.warn('Ошибка при выходе:', err.message)
      // Все равно сбрасываем состояние даже при ошибке сети
      user.value = null
      isAuthenticated.value = false
      error.value = null
      return { success: true }
    } finally {
      isLoading.value = false
    }
  }

  // Получение всех пользователей
  const getAllUsers = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetch(`${API_BASE_URL}/users/`, {
        method: 'GET',
        credentials: 'include'
      })

      await handleApiError(response, 'Ошибка загрузки пользователей')

      const data = await response.json()
      return data.data || [] // Теперь точно возвращаем массив
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Получение пользователя по ID
  const getUserById = async (userId) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetch(`${API_BASE_URL}/users/user/${userId}`, {
        method: 'GET',
        credentials: 'include'
      })

      await handleApiError(response, 'Ошибка загрузки пользователя')

      const data = await response.json()
      return data.data || null
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Получение постов текущего пользователя
  const getUserPosts = async () => {
    if (!isAuthenticated.value) {
      throw new Error('Требуется авторизация')
    }
    
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetch(`${API_BASE_URL}/users/me/posts`, {
        method: 'GET',
        credentials: 'include'
      })

      // Если 404 - у пользователя нет постов, возвращаем пустой массив
      if (response.status === 404) {
        return []
      }

      await handleApiError(response, 'Ошибка загрузки постов пользователя')

      const data = await response.json()
      const posts = data.data?.posts || []
      
      // Сортируем посты от новых к старым
      return posts.sort((a, b) => {
        const dateA = new Date(a.created_at)
        const dateB = new Date(b.created_at)
        return dateB - dateA // Новые сверху
      })
    } catch (err) {
      // Если ошибка связана с отсутствием постов (404), возвращаем пустой массив
      if (err.message.includes('404') || err.message.includes('No posts')) {
        return []
      }
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Получение конкретного поста текущего пользователя
  const getUserPost = async (postId) => {
    if (!isAuthenticated.value) {
      throw new Error('Требуется авторизация')
    }
    
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetch(`${API_BASE_URL}/users/me/post/${postId}`, {
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

  // Получение текущего пользователя с постами
  const getCurrentUserWithPosts = async () => {
    if (!isAuthenticated.value) {
      throw new Error('Требуется авторизация')
    }
    
    isLoading.value = true
    error.value = null
    
    try {
      // Используем эндпоинт для текущего пользователя
      const response = await fetch(`${API_BASE_URL}/users/me/`, {
        method: 'GET',
        credentials: 'include'
      })

      await handleApiError(response, 'Ошибка загрузки пользователя')

      const data = await response.json()
      
      if (data.data) {
        // Обновляем данные пользователя
        user.value = data.data
        return data.data
      }
      
      return null
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }


  // Повышение пользователя до админа
  const promoteToAdmin = async (userId) => {
    if (!isAuthenticated.value || !user.value?.is_admin) {
      throw new Error('Требуются права администратора')
    }
    
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetch(`${API_BASE_URL}/admin/users/promote_to_admin/${userId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        credentials: 'include'
      })

      await handleApiError(response, 'Ошибка назначения админом')

      const data = await response.json()
      
      // Если текущий пользователь обновил свой профиль
      if (user.value?.id === userId && data.data) {
        user.value = { ...user.value, ...data.data }
      }
      
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Понижение пользователя из админа
  const demoteFromAdmin = async (userId) => {
    if (!isAuthenticated.value || !user.value?.is_admin) {
      throw new Error('Требуются права администратора')
    }
    
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetch(`${API_BASE_URL}/admin/users/demote_from_admin/${userId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        credentials: 'include'
      })

      await handleApiError(response, 'Ошибка снятия прав админа')

      const data = await response.json()
      
      // Если текущий пользователь обновил свой профиль
      if (user.value?.id === userId && data.data) {
        user.value = { ...user.value, ...data.data }
      }
      
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Обновление данных пользователя после изменения статуса
  const updateUserAdminStatus = async (userId, isAdmin) => {
    if (isAdmin) {
      return await promoteToAdmin(userId)
    } else {
      return await demoteFromAdmin(userId)
    }
  }

  // Сброс ошибки
  const clearError = () => {
    error.value = null
  }

  // Сброс состояния
  const reset = () => {
    user.value = null
    isAuthenticated.value = false
    isLoading.value = false
    error.value = null
  }

  return {
    // State
    user,
    isAuthenticated,
    isLoading,
    error,
    
    // Computed
    userName,
    userEmail,
    userBio,
    userLocation,
    isAdmin,
    registrationDate,
    
    // Actions
    login,
    register,
    loadUser,
    updateProfile,
    logout,
    getAllUsers,
    getUserById,
    getUserPosts,
    getUserPost,
    getCurrentUserWithPosts,
    promoteToAdmin,
    demoteFromAdmin,
    updateUserAdminStatus,
    clearError,
    reset
  }
})
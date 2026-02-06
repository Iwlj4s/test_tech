// src/stores/adminStore.js
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

export const useAdminStore = defineStore('admin', () => {
  const isLoading = ref(false)
  const error = ref(null)
  const deletedUsers = ref([]) // Для хранения удаленных пользователей
  const allUsers = ref([]) // Все пользователи для админки

  // Проверка прав администратора
  const isAdmin = async () => {
    const { useUserStore } = await import('./userStore.js')
    const userStore = useUserStore()
    
    if (!userStore.user?.is_admin) {
      throw new Error('Требуются права администратора')
    }
    return true
  }

  // Получение всех пользователей (админский метод)
  const getAllUsers = async () => {
    await isAdmin()
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetch(`${API_BASE_URL}/users/`, {
        method: 'GET',
        credentials: 'include'
      })

      await handleApiError(response, 'Ошибка загрузки пользователей')

      const data = await response.json()
      allUsers.value = data.data || []
      return allUsers.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Назначение администратором
  const promoteToAdmin = async (userId) => {
    await isAdmin()
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
      
      // Обновляем в локальном списке
      const index = allUsers.value.findIndex(user => user.id === userId)
      if (index !== -1) {
        allUsers.value[index] = { ...allUsers.value[index], ...data.data }
      }
      
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Снятие прав администратора
  const demoteFromAdmin = async (userId) => {
    await isAdmin()
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
      
      // Обновляем в локальном списке
      const index = allUsers.value.findIndex(user => user.id === userId)
      if (index !== -1) {
        allUsers.value[index] = { ...allUsers.value[index], ...data.data }
      }
      
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

    // Удаление пользователя 
    const deleteUser = async (userId, reason) => {
        await isAdmin()
        isLoading.value = true
        error.value = null
        
        try {
            // Создаем объект с правильным полем
            const requestBody = { reason: reason }
            console.log('Отправляю DELETE запрос с телом:', requestBody)
            
            const response = await fetch(`${API_BASE_URL}/admin/users/delete/${userId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(requestBody)
            })
            
            console.log('Ответ сервера - статус:', response.status)
            
            if (!response.ok) {
                let errorData
                try {
                    errorData = await response.json()
                    console.log('Ошибка от сервера:', errorData)
                } catch (e) {
                    console.log('Не удалось распарсить ошибку')
                }
                
                // Если 422, проверяем, что именно не так
                if (response.status === 422 && errorData) {
                    throw new Error(`Ошибка валидации: ${JSON.stringify(errorData.detail)}`)
                }
                
                throw new Error(`HTTP ${response.status}: ${response.statusText}`)
            }

            const data = await response.json()
            console.log('Успешный ответ:', data)
            
            // Удаляем из списка активных пользователей
            allUsers.value = allUsers.value.filter(user => user.id !== userId)
            
            // Обновляем список удаленных пользователей
            await fetchDeletedUsers()
            
            return data
        } catch (err) {
            console.error('Ошибка удаления пользователя:', err)
            error.value = err.message
            throw err
        } finally {
            isLoading.value = false
        }
    }

// Получение удаленных пользователей с бекенда
  const fetchDeletedUsers = async () => {
    await isAdmin()
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetch(`${API_BASE_URL}/admin/users/deleted`, {
        method: 'GET',
        credentials: 'include'
      })

      await handleApiError(response, 'Ошибка загрузки удаленных пользователей')

      const data = await response.json()
      deletedUsers.value = data.data || []
      return deletedUsers.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

    // Поиск пользователей
    const searchUsers = (query) => {
        if (!query) return allUsers.value
        
        return allUsers.value.filter(user => 
            user.name.toLowerCase().includes(query.toLowerCase()) ||
            user.email.toLowerCase().includes(query.toLowerCase()) ||
            (user.location && user.location.toLowerCase().includes(query.toLowerCase()))
        )
    }

    const getDeletedUsers = () => {
        return deletedUsers.value
    }

    // Инициализация - загрузка всех данных
    const initialize = async () => {
        await getAllUsers()
        await fetchDeletedUsers()
    }


  // Очистка ошибки
  const clearError = () => {
    error.value = null
  }

  // Сброс состояния
  const reset = () => {
    isLoading.value = false
    error.value = null
    allUsers.value = []
    deletedUsers.value = []
  }

  return {
    // State
    isLoading,
    error,
    allUsers,
    deletedUsers,
    
    // Actions
    isAdmin,
    getAllUsers,
    promoteToAdmin,
    demoteFromAdmin,
    deleteUser,
    getDeletedUsers,
    fetchDeletedUsers,
    initialize,
    searchUsers,
    clearError,
    reset
  }
})
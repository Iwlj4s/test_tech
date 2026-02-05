// Утилиты для работы с API
import { API_CONFIG } from '../config'

/**
 * Универсальный метод для API запросов
 * @param {string} endpoint - endpoint API
 * @param {object} options - параметры запроса
 * @returns {Promise} - результат запроса
 */
export const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_CONFIG.BASE_URL}${endpoint}`
  
  const defaultOptions = {
    credentials: 'include',
    headers: API_CONFIG.HEADERS,
    ...options
  }

  // Таймаут запроса
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.TIMEOUT)
  
  try {
    const response = await fetch(url, {
      ...defaultOptions,
      signal: controller.signal
    })

    clearTimeout(timeoutId)

    // Обработка ошибок
    if (!response.ok) {
      let errorMessage = `Ошибка ${response.status}`
      try {
        const errorData = await response.json()
        errorMessage = errorData.detail || errorData.message || errorMessage
      } catch {
        // Не удалось распарсить JSON
      }
      throw new Error(errorMessage)
    }

    // Парсим ответ
    const contentType = response.headers.get('content-type')
    if (contentType && contentType.includes('application/json')) {
      return await response.json()
    }
    
    return await response.text()
  } catch (error) {
    clearTimeout(timeoutId)
    if (error.name === 'AbortError') {
      throw new Error('Таймаут запроса. Сервер не отвечает.')
    }
    throw error
  }
}

/**
 * GET запрос
 * @param {string} endpoint - endpoint API
 * @param {object} params - query параметры
 */
export const apiGet = (endpoint, params = {}) => {
  const queryString = new URLSearchParams(params).toString()
  const url = queryString ? `${endpoint}?${queryString}` : endpoint
  return apiRequest(url, { method: 'GET' })
}

/**
 * POST запрос
 * @param {string} endpoint - endpoint API
 * @param {object} data - данные для отправки
 */
export const apiPost = (endpoint, data = {}) => {
  return apiRequest(endpoint, {
    method: 'POST',
    body: JSON.stringify(data)
  })
}

/**
 * PATCH запрос
 * @param {string} endpoint - endpoint API
 * @param {object} data - данные для обновления
 */
export const apiPatch = (endpoint, data = {}) => {
  return apiRequest(endpoint, {
    method: 'PATCH',
    body: JSON.stringify(data)
  })
}

/**
 * DELETE запрос
 * @param {string} endpoint - endpoint API
 */
export const apiDelete = (endpoint) => {
  return apiRequest(endpoint, { method: 'DELETE' })
}
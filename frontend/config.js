// Конфигурация приложения
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1',
  TIMEOUT: 30000,
  HEADERS: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
}

export const APP_CONFIG = {
  NAME: import.meta.env.VITE_APP_NAME || 'Social Profile Manager',
  VERSION: '1.0.0'
}

// Конфигурация окружения
export const ENV_CONFIG = {
  IS_DEVELOPMENT: import.meta.env.DEV,
  IS_PRODUCTION: import.meta.env.PROD,
  MODE: import.meta.env.MODE
}
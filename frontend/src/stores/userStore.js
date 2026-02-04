import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// Функция для генерации красивого градиента на основе произвольного seed (например, name+email)
const generateGradient = (seed) => {
  const s = String(seed || '')
  let hash = 0
  for (let i = 0; i < s.length; i++) {
    hash = s.charCodeAt(i) + ((hash << 5) - hash)
  }

  const colors = [
    ['#FF6B6B', '#FF8E72'],
    ['#4ECDC4', '#44A08D'],
    ['#FF9A56', '#FFB347'],
    ['#667EEA', '#764BA2'],
    ['#F093FB', '#F5576C'],
    ['#4FACFE', '#00F2FE'],
    ['#43E97B', '#38F9D7'],
    ['#FA709A', '#FEE140'],
    ['#30CFD0', '#330867'],
    ['#A8EDEA', '#FED6E3'],
  ]

  const index = Math.abs(hash) % colors.length
  return `linear-gradient(135deg, ${colors[index][0]} 0%, ${colors[index][1]} 100%)`
}

// Функция для генерации SVG-аватарки с градиентом и инициалами
const generateAvatarSVG = (name, seed) => {
  const initials = String(name || '')
    .split(' ')
    .map((n) => n[0] || '')
    .slice(0, 2)
    .join('')
    .toUpperCase()

  // use seed (name+email) to select colors deterministically
  const s = String(seed || name || '')
  let hash = 0
  for (let i = 0; i < s.length; i++) {
    hash = s.charCodeAt(i) + ((hash << 5) - hash)
  }
  const colorSets = [
    ['#FF6B6B', '#FF8E72'],
    ['#4ECDC4', '#44A08D'],
    ['#FF9A56', '#FFB347'],
    ['#667EEA', '#764BA2'],
    ['#F093FB', '#F5576C'],
    ['#4FACFE', '#00F2FE'],
    ['#43E97B', '#38F9D7'],
    ['#FA709A', '#FEE140'],
    ['#30CFD0', '#330867'],
    ['#A8EDEA', '#FED6E3']
  ]
  const idx = Math.abs(hash) % colorSets.length
  const c1 = colorSets[idx][0]
  const c2 = colorSets[idx][1]

  const svg = `<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400' viewBox='0 0 400 400'>
    <defs>
      <linearGradient id='g' x1='0' x2='1' y1='0' y2='1'>
        <stop offset='0' stop-color='${c1}' />
        <stop offset='1' stop-color='${c2}' />
      </linearGradient>
    </defs>
    <rect width='100%' height='100%' rx='48' fill='url(#g)' />
    <text x='50%' y='54%' font-family='Arial, Helvetica, sans-serif' font-size='140' fill='rgba(255,255,255,0.92)' font-weight='700' text-anchor='middle' dominant-baseline='middle'>${initials}</text>
  </svg>`

  return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`
}

export const useUserStore = defineStore('user', () => {
  // Состояние - данные пользователя
  const user = ref(null)
  const isAuthenticated = ref(false)

  // Функция входа (имитация авторизации)
  const login = (email, password) => {
    // make a deterministic display name from email so different logins get different seeds
    const prefix = String(email || '').split('@')[0] || 'guest'
    const name = prefix.charAt(0).toUpperCase() + prefix.slice(1)
    const seed = `${name}|${email}`
    user.value = {
      id: Math.floor(Math.random() * 100000) + 1,
      name: name,
      email: email,
      bio: 'Welcome to my profile!',
      registrationDate: new Date(),
      location: 'Internet',
      avatar: generateAvatarSVG(name, seed),
      coverGradient: generateGradient(seed)
    }
    isAuthenticated.value = true
    // Сохраняем в localStorage
    localStorage.setItem('user', JSON.stringify(user.value))
    localStorage.setItem('isAuthenticated', 'true')
  }

  // Функция регистрации
  const register = (name, email, password) => {
    const seed = `${name}|${email}`
    user.value = {
      id: Math.floor(Math.random() * 10000),
      name: name,
      email: email,
      bio: 'New member of this awesome platform!',
      registrationDate: new Date(),
      location: '',
      avatar: generateAvatarSVG(name, seed),
      coverGradient: generateGradient(seed)
    }
    isAuthenticated.value = true
    localStorage.setItem('user', JSON.stringify(user.value))
    localStorage.setItem('isAuthenticated', 'true')
  }

  // Функция обновления профиля
  const updateProfile = (updates) => {
    if (user.value) {
      // if name or email changed, regenerate avatar and cover using new seed
      const merged = { ...user.value, ...updates }
      const seed = `${merged.name}|${merged.email}`
      merged.avatar = generateAvatarSVG(merged.name, seed)
      merged.coverGradient = generateGradient(seed)
      user.value = merged
      localStorage.setItem('user', JSON.stringify(user.value))
    }
  }

  // Функция выхода
  const logout = () => {
    user.value = null
    isAuthenticated.value = false
    localStorage.removeItem('user')
    localStorage.removeItem('isAuthenticated')
  }

  // Загрузка пользователя из localStorage при инициализации
  const loadUser = () => {
    const savedUser = localStorage.getItem('user')
    const savedAuth = localStorage.getItem('isAuthenticated')
    if (savedUser && savedAuth === 'true') {
      // ensure avatar/cover are present and deterministic (in case hashing changed)
      const parsed = JSON.parse(savedUser)
      const seed = `${parsed.name}|${parsed.email}`
      parsed.avatar = parsed.avatar || generateAvatarSVG(parsed.name, seed)
      parsed.coverGradient = parsed.coverGradient || generateGradient(seed)
      user.value = parsed
      isAuthenticated.value = true
    }
  }

  return {
    user,
    isAuthenticated,
    login,
    register,
    updateProfile,
    logout,
    loadUser
  }
})

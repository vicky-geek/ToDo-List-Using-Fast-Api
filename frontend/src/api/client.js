const API_BASE = '/api'

let accessToken = localStorage.getItem('accessToken') || null
let onUnauthorized = null

export function setAccessToken(token) {
  accessToken = token
  if (token) {
    localStorage.setItem('accessToken', token)
  } else {
    localStorage.removeItem('accessToken')
  }
}

export function getAccessToken() {
  return accessToken
}

export function setOnUnauthorized(callback) {
  onUnauthorized = callback
}

async function refreshAccessToken() {
  const response = await fetch(`${API_BASE}/refresh-token`, {
    method: 'POST',
    credentials: 'include',
  })
  if (!response.ok) return null
  const data = await response.json()
  setAccessToken(data.accessToken)
  return data.accessToken
}

export async function apiRequest(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  }

  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`
  }

  let response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
    credentials: 'include',
  })

  if (response.status === 401 && accessToken && !options._retry) {
    const newToken = await refreshAccessToken()
    if (newToken) {
      return apiRequest(path, { ...options, _retry: true })
    }
    setAccessToken(null)
    onUnauthorized?.()
  }

  return response
}

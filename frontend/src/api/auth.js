import { apiRequest, setAccessToken } from './client'

export async function login(email, password) {
  const response = await apiRequest('/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
  const data = await response.json()
  if (response.ok && data.accessToken) {
    setAccessToken(data.accessToken)
  }
  return { response, data }
}

export async function register(username, email, password, role) {
  const response = await apiRequest('/register', {
    method: 'POST',
    body: JSON.stringify({ username, email, password, role }),
  })
  const data = await response.json()
  return { response, data }
}

export async function logout() {
  await apiRequest('/logout')
  setAccessToken(null)
}

export function jwtDecode(token) {
  const payload = token.split('.')[1]
  const decoded = atob(payload.replace(/-/g, '+').replace(/_/g, '/'))
  return JSON.parse(decoded)
}

import { apiRequest } from './client'

export async function fetchTodos() {
  const response = await apiRequest('/todos')
  const data = await response.json()
  return { response, data }
}

export async function createTodo(item) {
  const response = await apiRequest('/todos', {
    method: 'POST',
    body: JSON.stringify({ item }),
  })
  const data = await response.json()
  return { response, data }
}

export async function updateTodo(id, item) {
  const response = await apiRequest(`/todos/${id}`, {
    method: 'PUT',
    body: JSON.stringify({ item }),
  })
  const data = await response.json()
  return { response, data }
}

export async function deleteTodo(id) {
  const response = await apiRequest(`/todos/${id}`, {
    method: 'DELETE',
  })
  const data = await response.json()
  return { response, data }
}

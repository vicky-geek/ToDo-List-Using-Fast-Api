import { useCallback, useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { fetchTodos, createTodo, updateTodo, deleteTodo } from '../api/todos'
import TodoForm from './TodoForm'
import TodoItem from './TodoItem'

const PRIORITY_LABELS = { 1: 'Low', 2: 'Medium', 3: 'High' }

export default function TodoList() {
  const { isAdmin } = useAuth()
  const [todos, setTodos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [editingId, setEditingId] = useState(null)

  const loadTodos = useCallback(async () => {
    setError('')
    try {
      const { response, data } = await fetchTodos()
      if (response.ok) {
        setTodos(data.data || [])
      } else {
        setError(data.detail || data.error || 'Failed to load todos')
      }
    } catch {
      setError('Unable to connect to server')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadTodos()
  }, [loadTodos])

  const handleCreate = async (item) => {
    const { response, data } = await createTodo(item)
    if (response.ok) {
      await loadTodos()
      return true
    }
    setError(data.error || data.detail || 'Failed to create todo')
    return false
  }

  const handleUpdate = async (id, item) => {
    const { response, data } = await updateTodo(id, item)
    if (response.ok) {
      setEditingId(null)
      await loadTodos()
      return true
    }
    setError(data.error || data.detail || 'Failed to update todo')
    return false
  }

  const handleDelete = async (id) => {
    const { response, data } = await deleteTodo(id)
    if (response.ok) {
      await loadTodos()
    } else {
      setError(data.error || data.detail || 'Failed to delete todo')
    }
  }

  const editingTodo = todos.find((t) => t.id === editingId)

  return (
    <div className="todo-page">
      <div className="todo-header">
        <div>
          <h2>Your Tasks</h2>
          <p className="text-muted">
            {isAdmin ? 'Full access — create, edit, and delete tasks' : 'Create and view tasks'}
          </p>
        </div>
        <span className="todo-count">{todos.length} task{todos.length !== 1 ? 's' : ''}</span>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <TodoForm onSubmit={handleCreate} submitLabel="Add task" />

      {loading ? (
        <div className="loading">Loading tasks...</div>
      ) : todos.length === 0 ? (
        <div className="empty-state">
          <p>No tasks yet. Add your first one above.</p>
        </div>
      ) : (
        <ul className="todo-list">
          {todos.map((todo) => (
            <TodoItem
              key={todo.id}
              todo={todo}
              priorityLabel={PRIORITY_LABELS[todo.priority] || 'Normal'}
              isEditing={editingId === todo.id}
              canEdit={isAdmin}
              canDelete={isAdmin}
              onEdit={() => setEditingId(todo.id)}
              onCancelEdit={() => setEditingId(null)}
              onUpdate={(item) => handleUpdate(todo.id, item)}
              onDelete={() => handleDelete(todo.id)}
              editingTodo={editingTodo}
            />
          ))}
        </ul>
      )}
    </div>
  )
}

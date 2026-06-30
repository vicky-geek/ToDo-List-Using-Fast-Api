import { useEffect, useState } from 'react'

const emptyItem = { task: '', priority: 2, description: '' }

export default function TodoForm({ onSubmit, submitLabel, initialValues, onCancel }) {
  const [item, setItem] = useState(initialValues || emptyItem)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (initialValues) {
      setItem(initialValues)
    }
  }, [initialValues])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    const success = await onSubmit(item)
    setLoading(false)
    if (success && !initialValues) {
      setItem(emptyItem)
    }
  }

  return (
    <form onSubmit={handleSubmit} className={`todo-form ${initialValues ? 'todo-form-inline' : ''}`}>
      <div className="form-row">
        <input
          type="text"
          value={item.task}
          onChange={(e) => setItem({ ...item, task: e.target.value })}
          placeholder="What needs to be done?"
          required
        />
        <select
          value={item.priority}
          onChange={(e) => setItem({ ...item, priority: Number(e.target.value) })}
        >
          <option value={1}>Low</option>
          <option value={2}>Medium</option>
          <option value={3}>High</option>
        </select>
      </div>
      <textarea
        value={item.description || ''}
        onChange={(e) => setItem({ ...item, description: e.target.value })}
        placeholder="Description (optional)"
        rows={initialValues ? 2 : 2}
      />
      <div className="form-actions">
        {onCancel && (
          <button type="button" className="btn btn-ghost" onClick={onCancel}>
            Cancel
          </button>
        )}
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Saving...' : submitLabel}
        </button>
      </div>
    </form>
  )
}

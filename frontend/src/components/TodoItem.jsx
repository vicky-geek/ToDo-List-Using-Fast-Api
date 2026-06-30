import TodoForm from './TodoForm'

export default function TodoItem({
  todo,
  priorityLabel,
  isEditing,
  canEdit,
  canDelete,
  onEdit,
  onCancelEdit,
  onUpdate,
  onDelete,
  editingTodo,
}) {
  if (isEditing && editingTodo) {
    return (
      <li className="todo-item editing">
        <TodoForm
          initialValues={{
            task: editingTodo.task,
            priority: editingTodo.priority,
            description: editingTodo.description || '',
          }}
          onSubmit={onUpdate}
          submitLabel="Save changes"
          onCancel={onCancelEdit}
        />
      </li>
    )
  }

  return (
    <li className={`todo-item priority-${todo.priority}`}>
      <div className="todo-content">
        <div className="todo-top">
          <span className="todo-task">{todo.task}</span>
          <span className={`priority-badge priority-${todo.priority}`}>{priorityLabel}</span>
        </div>
        {todo.description && <p className="todo-desc">{todo.description}</p>}
      </div>
      {(canEdit || canDelete) && (
        <div className="todo-actions">
          {canEdit && (
            <button type="button" className="btn btn-sm btn-ghost" onClick={onEdit}>
              Edit
            </button>
          )}
          {canDelete && (
            <button type="button" className="btn btn-sm btn-danger" onClick={() => onDelete()}>
              Delete
            </button>
          )}
        </div>
      )}
    </li>
  )
}

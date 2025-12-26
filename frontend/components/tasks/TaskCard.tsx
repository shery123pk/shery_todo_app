'use client'

/**
 * TaskCard Component
 * Displays a single task with title, description, and metadata
 * Author: Sharmeen Asif
 */

import { TaskResponse } from '@/lib/api-client'

interface TaskCardProps {
  task: TaskResponse
  onToggle?: (taskId: string) => void
  onEdit?: (taskId: string) => void
  onDelete?: (taskId: string) => void
}

export default function TaskCard({ task, onToggle, onEdit, onDelete }: TaskCardProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })
  }

  return (
    <div className="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <input
          type="checkbox"
          checked={task.completed}
          onChange={() => onToggle?.(task.id)}
          className="mt-1 h-5 w-5 text-primary focus:ring-primary border-gray-300 rounded cursor-pointer"
        />

        {/* Content */}
        <div className="flex-1 min-w-0">
          {/* Title */}
          <h3
            className={`text-lg font-medium ${
              task.completed ? 'line-through text-gray-500' : 'text-gray-900'
            }`}
          >
            {task.title}
          </h3>

          {/* Description */}
          {task.description && (
            <p
              className={`mt-1 text-sm ${
                task.completed ? 'text-gray-400' : 'text-gray-600'
              }`}
            >
              {task.description}
            </p>
          )}

          {/* Metadata */}
          <div className="mt-2 flex flex-wrap items-center gap-2 text-xs text-gray-500">
            {/* Priority */}
            {task.priority && (
              <span
                className={`px-2 py-1 rounded ${
                  task.priority === 'high'
                    ? 'bg-red-100 text-red-700'
                    : task.priority === 'medium'
                    ? 'bg-yellow-100 text-yellow-700'
                    : 'bg-green-100 text-green-700'
                }`}
              >
                {task.priority}
              </span>
            )}

            {/* Category */}
            {task.category && (
              <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded">
                {task.category}
              </span>
            )}

            {/* Tags */}
            {task.tags.map((tag) => (
              <span key={tag} className="px-2 py-1 bg-gray-100 text-gray-700 rounded">
                #{tag}
              </span>
            ))}

            {/* Created date */}
            <span className="text-gray-400">
              Created {formatDate(task.created_at)}
            </span>
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-2">
          {onEdit && (
            <button
              onClick={() => onEdit(task.id)}
              className="text-sm text-blue-600 hover:text-blue-800"
              title="Edit task"
            >
              Edit
            </button>
          )}
          {onDelete && (
            <button
              onClick={() => onDelete(task.id)}
              className="text-sm text-red-600 hover:text-red-800"
              title="Delete task"
            >
              Delete
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

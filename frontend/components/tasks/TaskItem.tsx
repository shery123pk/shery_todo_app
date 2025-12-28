'use client'

/**
 * Task Item Component
 * Individual task card with actions
 * Author: Sharmeen Asif
 */

import { useState } from 'react'
import type { Task } from '@/types/task'
import { Check, Trash2, Edit2, Tag, Calendar, FolderOpen } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'

interface TaskItemProps {
  task: Task
  onToggleComplete: (taskId: string, completed: boolean) => void
  onDelete: (taskId: string) => void
  onEdit: (task: Task) => void
}

export default function TaskItem({ task, onToggleComplete, onDelete, onEdit }: TaskItemProps) {
  const [isHovered, setIsHovered] = useState(false)

  const getPriorityColor = (priority?: string | null) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-700 border-red-200'
      case 'medium':
        return 'bg-yellow-100 text-yellow-700 border-yellow-200'
      case 'low':
        return 'bg-green-100 text-green-700 border-green-200'
      default:
        return 'bg-gray-100 text-gray-700 border-gray-200'
    }
  }

  return (
    <div
      className={`bg-white/80 backdrop-blur-xl rounded-2xl shadow-lg border border-white/20 p-5 transition-all duration-200 ${
        task.completed ? 'opacity-75' : ''
      } hover:shadow-xl`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="flex items-start gap-4">
        {/* Checkbox */}
        <button
          onClick={() => onToggleComplete(task.id, !task.completed)}
          className={`flex-shrink-0 w-6 h-6 rounded-lg border-2 transition-all duration-200 flex items-center justify-center ${
            task.completed
              ? 'bg-green-500 border-green-500'
              : 'border-gray-300 hover:border-indigo-500 hover:bg-indigo-50'
          }`}
        >
          {task.completed && <Check className="w-4 h-4 text-white" />}
        </button>

        {/* Content */}
        <div className="flex-1 min-w-0">
          {/* Title */}
          <h3
            className={`text-lg font-semibold mb-2 ${
              task.completed ? 'line-through text-gray-500' : 'text-gray-900'
            }`}
          >
            {task.title}
          </h3>

          {/* Description */}
          {task.description && (
            <p className="text-gray-600 text-sm mb-3 line-clamp-2">{task.description}</p>
          )}

          {/* Metadata */}
          <div className="flex flex-wrap items-center gap-3 text-xs text-gray-500">
            {/* Priority */}
            {task.priority && (
              <span
                className={`px-2 py-1 rounded-lg border font-medium ${getPriorityColor(
                  task.priority
                )}`}
              >
                {task.priority.toUpperCase()}
              </span>
            )}

            {/* Category */}
            {task.category && (
              <span className="flex items-center gap-1">
                <FolderOpen className="w-3 h-3" />
                {task.category}
              </span>
            )}

            {/* Tags */}
            {task.tags && task.tags.length > 0 && (
              <div className="flex items-center gap-1">
                <Tag className="w-3 h-3" />
                {task.tags.slice(0, 3).map((tag, index) => (
                  <span
                    key={index}
                    className="px-2 py-0.5 bg-indigo-50 text-indigo-700 rounded-md"
                  >
                    {tag}
                  </span>
                ))}
                {task.tags.length > 3 && (
                  <span className="text-gray-400">+{task.tags.length - 3}</span>
                )}
              </div>
            )}

            {/* Created time */}
            <span className="flex items-center gap-1 ml-auto">
              <Calendar className="w-3 h-3" />
              {formatDistanceToNow(new Date(task.created_at), { addSuffix: true })}
            </span>
          </div>
        </div>

        {/* Actions */}
        <div
          className={`flex items-center gap-2 transition-opacity duration-200 ${
            isHovered ? 'opacity-100' : 'opacity-0'
          }`}
        >
          {/* Edit button */}
          <button
            onClick={() => onEdit(task)}
            className="p-2 text-gray-600 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
            title="Edit task"
          >
            <Edit2 className="w-4 h-4" />
          </button>

          {/* Delete button */}
          <button
            onClick={() => onDelete(task.id)}
            className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            title="Delete task"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  )
}

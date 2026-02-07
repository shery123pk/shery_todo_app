'use client'

/**
 * Task Card Component for Kanban Board
 * Beautiful draggable task card
 * Author: Sharmeen Asif
 */

import { useSortable } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import { Clock, Tag, AlertCircle, CheckCircle2 } from 'lucide-react'
import type { Task } from '@/types/task'

interface TaskCardProps {
  task: Task
  onClick?: () => void
}

export default function TaskCard({ task, onClick }: TaskCardProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: task.id })

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  }

  const getPriorityColor = (priority?: string | null) => {
    switch (priority) {
      case 'high':
        return 'border-l-4 border-l-red-500 bg-red-50/50'
      case 'medium':
        return 'border-l-4 border-l-yellow-500 bg-yellow-50/50'
      case 'low':
        return 'border-l-4 border-l-green-500 bg-green-50/50'
      default:
        return 'border-l-4 border-l-gray-300 bg-white'
    }
  }

  const getPriorityIcon = (priority?: string | null) => {
    switch (priority) {
      case 'high':
        return <AlertCircle className="w-4 h-4 text-red-500" />
      case 'medium':
        return <Clock className="w-4 h-4 text-yellow-500" />
      case 'low':
        return <CheckCircle2 className="w-4 h-4 text-green-500" />
      default:
        return null
    }
  }

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className={`group cursor-grab active:cursor-grabbing ${
        isDragging ? 'opacity-50 rotate-3 scale-105' : ''
      }`}
    >
      <div
        onClick={onClick}
        className={`${getPriorityColor(task.priority)} rounded-xl p-4 shadow-md hover:shadow-xl transition-all duration-200 border border-gray-200 bg-white/90 backdrop-blur-sm`}
      >
        {/* Task Title */}
        <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">
          {task.title}
        </h3>

        {/* Task Description */}
        {task.description && (
          <p className="text-sm text-gray-600 mb-3 line-clamp-2">
            {task.description}
          </p>
        )}

        {/* Tags */}
        {task.tags && task.tags.length > 0 && (
          <div className="flex flex-wrap gap-1 mb-3">
            {task.tags.slice(0, 3).map((tag, index) => (
              <span
                key={index}
                className="inline-flex items-center gap-1 px-2 py-1 bg-indigo-100 text-indigo-700 text-xs font-medium rounded-md"
              >
                <Tag className="w-3 h-3" />
                {tag}
              </span>
            ))}
            {task.tags.length > 3 && (
              <span className="text-xs text-gray-500 px-2 py-1">
                +{task.tags.length - 3} more
              </span>
            )}
          </div>
        )}

        {/* Footer */}
        <div className="flex items-center justify-between text-xs text-gray-500">
          {/* Priority Badge */}
          {task.priority && (
            <div className="flex items-center gap-1 capitalize">
              {getPriorityIcon(task.priority)}
              <span>{task.priority}</span>
            </div>
          )}

          {/* Category */}
          {task.category && (
            <span className="px-2 py-1 bg-gray-100 rounded-md text-gray-700">
              {task.category}
            </span>
          )}
        </div>
      </div>
    </div>
  )
}

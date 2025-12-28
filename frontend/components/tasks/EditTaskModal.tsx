'use client'

/**
 * Edit Task Modal Component
 * Modal for editing existing tasks with pre-filled data
 * Author: Sharmeen Asif
 */

import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { updateTask } from '@/lib/task-client'
import type { Task, TaskUpdate, PriorityLevel } from '@/types/task'
import { X, Save, Loader2, Tag, FolderOpen } from 'lucide-react'

const taskSchema = z.object({
  title: z.string()
    .min(1, 'Title is required')
    .max(200, 'Title must be less than 200 characters'),
  description: z.string().optional(),
  priority: z.enum(['low', 'medium', 'high']).optional(),
  category: z.string().max(50).optional(),
  tags: z.string().optional(), // Will be split into array
})

type TaskFormData = z.infer<typeof taskSchema>

interface EditTaskModalProps {
  task: Task | null
  isOpen: boolean
  onClose: () => void
  onTaskUpdated: () => void
}

export default function EditTaskModal({ task, isOpen, onClose, onTaskUpdated }: EditTaskModalProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch,
    setValue,
  } = useForm<TaskFormData>({
    resolver: zodResolver(taskSchema),
  })

  const selectedPriority = watch('priority')

  // Pre-fill form when task changes
  useEffect(() => {
    if (task && isOpen) {
      reset({
        title: task.title,
        description: task.description || '',
        priority: (task.priority as PriorityLevel) || undefined,
        category: task.category || '',
        tags: task.tags.join(', '),
      })
    }
  }, [task, isOpen, reset])

  const onSubmit = async (data: TaskFormData) => {
    if (!task) return

    setIsSubmitting(true)
    setError(null)

    try {
      // Convert tags string to array
      const tags = data.tags
        ? data.tags.split(',').map(tag => tag.trim()).filter(Boolean)
        : []

      const updateData: TaskUpdate = {
        title: data.title,
        description: data.description || undefined,
        priority: data.priority || undefined,
        category: data.category || undefined,
        tags,
      }

      await updateTask(task.id, updateData)

      // Reset form and close modal
      reset()
      onClose()
      onTaskUpdated()
    } catch (err: any) {
      setError(err.message || 'Failed to update task')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleClose = () => {
    if (!isSubmitting) {
      reset()
      setError(null)
      onClose()
    }
  }

  if (!isOpen || !task) return null

  const getPriorityColor = (priority?: string) => {
    switch (priority) {
      case 'high':
        return 'border-red-500 bg-red-50 text-red-700'
      case 'medium':
        return 'border-yellow-500 bg-yellow-50 text-yellow-700'
      case 'low':
        return 'border-green-500 bg-green-50 text-green-700'
      default:
        return 'border-gray-300 bg-gray-50 text-gray-700'
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-in fade-in">
      <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 max-w-2xl w-full max-h-[90vh] overflow-y-auto animate-in slide-in-from-bottom-4">
        {/* Header */}
        <div className="sticky top-0 bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-4 rounded-t-3xl flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center">
              <Save className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white">Edit Task</h2>
              <p className="text-blue-100 text-sm">Update task details</p>
            </div>
          </div>
          <button
            onClick={handleClose}
            disabled={isSubmitting}
            className="p-2 hover:bg-white/20 rounded-lg transition-colors disabled:opacity-50"
          >
            <X className="w-6 h-6 text-white" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="p-6 space-y-6">
          {/* Error Alert */}
          {error && (
            <div className="bg-red-50 border-2 border-red-200 rounded-xl p-4 text-sm text-red-700">
              {error}
            </div>
          )}

          {/* Title */}
          <div className="space-y-2">
            <label htmlFor="title" className="block text-sm font-semibold text-gray-700">
              Task Title <span className="text-red-500">*</span>
            </label>
            <input
              {...register('title')}
              id="title"
              type="text"
              placeholder="Enter task title..."
              autoFocus
              className={`w-full px-4 py-3 border-2 rounded-xl bg-white/50 backdrop-blur-sm transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                errors.title ? 'border-red-300' : 'border-gray-200 hover:border-gray-300'
              }`}
            />
            {errors.title && (
              <p className="text-sm text-red-600">{errors.title.message}</p>
            )}
          </div>

          {/* Description */}
          <div className="space-y-2">
            <label htmlFor="description" className="block text-sm font-semibold text-gray-700">
              Description
            </label>
            <textarea
              {...register('description')}
              id="description"
              rows={4}
              placeholder="Add more details about this task..."
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl bg-white/50 backdrop-blur-sm transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent hover:border-gray-300 resize-none"
            />
          </div>

          {/* Priority */}
          <div className="space-y-2">
            <label className="block text-sm font-semibold text-gray-700">
              Priority
            </label>
            <div className="grid grid-cols-3 gap-3">
              {(['low', 'medium', 'high'] as PriorityLevel[]).map((priority) => (
                <label
                  key={priority}
                  className={`relative flex items-center justify-center px-4 py-3 border-2 rounded-xl cursor-pointer transition-all duration-200 ${
                    selectedPriority === priority
                      ? getPriorityColor(priority)
                      : 'border-gray-200 bg-white hover:border-gray-300'
                  }`}
                >
                  <input
                    {...register('priority')}
                    type="radio"
                    value={priority}
                    className="sr-only"
                  />
                  <span className="font-medium capitalize">{priority}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Category */}
          <div className="space-y-2">
            <label htmlFor="category" className="block text-sm font-semibold text-gray-700">
              <FolderOpen className="w-4 h-4 inline mr-1" />
              Category
            </label>
            <input
              {...register('category')}
              id="category"
              type="text"
              placeholder="e.g., Work, Personal, Shopping"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl bg-white/50 backdrop-blur-sm transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent hover:border-gray-300"
            />
          </div>

          {/* Tags */}
          <div className="space-y-2">
            <label htmlFor="tags" className="block text-sm font-semibold text-gray-700">
              <Tag className="w-4 h-4 inline mr-1" />
              Tags
            </label>
            <input
              {...register('tags')}
              id="tags"
              type="text"
              placeholder="Separate tags with commas (e.g., urgent, important)"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl bg-white/50 backdrop-blur-sm transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent hover:border-gray-300"
            />
            <p className="text-xs text-gray-500">Use commas to separate multiple tags</p>
          </div>

          {/* Actions */}
          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={handleClose}
              disabled={isSubmitting}
              className="flex-1 px-6 py-3 bg-white border-2 border-gray-200 text-gray-700 font-semibold rounded-xl hover:bg-gray-50 hover:border-gray-300 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex-1 px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-2"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Saving...
                </>
              ) : (
                <>
                  <Save className="w-5 h-5" />
                  Save Changes
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

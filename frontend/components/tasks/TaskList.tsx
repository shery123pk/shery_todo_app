'use client'

/**
 * Task List Component
 * Displays and manages user tasks
 * Author: Sharmeen Asif
 */

import { useState, useEffect } from 'react'
import { getTasks, updateTask, deleteTask } from '@/lib/task-client'
import type { Task, TaskListResponse } from '@/types/task'
import TaskItem from './TaskItem'
import EditTaskModal from './EditTaskModal'
import { Loader2, AlertCircle, CheckSquare } from 'lucide-react'

interface TaskListProps {
  onTasksChange?: (stats: { total: number; completed: number; incomplete: number }) => void
}

export default function TaskList({ onTasksChange }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([])
  const [stats, setStats] = useState({ total: 0, completed: 0, incomplete: 0 })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all')
  const [editingTask, setEditingTask] = useState<Task | null>(null)

  // Fetch tasks
  const fetchTasks = async () => {
    setLoading(true)
    setError(null)

    try {
      const params = filter === 'all' ? {} : { completed: filter === 'completed' }
      const data: TaskListResponse = await getTasks(params)

      setTasks(data.tasks)
      setStats({
        total: data.total,
        completed: data.completed,
        incomplete: data.incomplete,
      })

      // Notify parent of stats change
      if (onTasksChange) {
        onTasksChange({
          total: data.total,
          completed: data.completed,
          incomplete: data.incomplete,
        })
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load tasks')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTasks()
  }, [filter])

  // Toggle task completion
  const handleToggleComplete = async (taskId: string, completed: boolean) => {
    try {
      await updateTask(taskId, { completed })
      await fetchTasks() // Reload all tasks to update stats
    } catch (err: any) {
      setError(err.message || 'Failed to update task')
    }
  }

  // Delete task
  const handleDeleteTask = async (taskId: string) => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return
    }

    try {
      await deleteTask(taskId)
      await fetchTasks() // Reload tasks
    } catch (err: any) {
      setError(err.message || 'Failed to delete task')
    }
  }

  // Open edit modal
  const handleEditTask = (task: Task) => {
    setEditingTask(task)
  }

  // Close edit modal and refresh
  const handleEditClose = () => {
    setEditingTask(null)
  }

  const handleEditComplete = async () => {
    setEditingTask(null)
    await fetchTasks()
  }

  // Loading state
  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-indigo-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading tasks...</p>
        </div>
      </div>
    )
  }

  // Error state
  if (error) {
    return (
      <div className="bg-red-50 border-2 border-red-200 rounded-2xl p-6 flex items-start gap-3">
        <AlertCircle className="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <h4 className="font-semibold text-red-900">Error loading tasks</h4>
          <p className="text-red-700 text-sm mt-1">{error}</p>
          <button
            onClick={fetchTasks}
            className="mt-3 px-4 py-2 bg-red-600 text-white text-sm font-medium rounded-lg hover:bg-red-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Filter Tabs */}
      <div className="flex items-center gap-2 border-b border-gray-200 pb-4">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 font-medium text-sm rounded-lg transition-all ${
            filter === 'all'
              ? 'bg-indigo-600 text-white shadow-lg'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          All ({stats.total})
        </button>
        <button
          onClick={() => setFilter('active')}
          className={`px-4 py-2 font-medium text-sm rounded-lg transition-all ${
            filter === 'active'
              ? 'bg-indigo-600 text-white shadow-lg'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          Active ({stats.incomplete})
        </button>
        <button
          onClick={() => setFilter('completed')}
          className={`px-4 py-2 font-medium text-sm rounded-lg transition-all ${
            filter === 'completed'
              ? 'bg-indigo-600 text-white shadow-lg'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          Completed ({stats.completed})
        </button>
      </div>

      {/* Task List */}
      {tasks.length === 0 ? (
        <div className="text-center py-12">
          <div className="w-20 h-20 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <CheckSquare className="w-10 h-10 text-indigo-600" />
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-2">
            {filter === 'completed' ? 'No completed tasks' : 'No tasks yet'}
          </h3>
          <p className="text-gray-600">
            {filter === 'completed'
              ? 'Complete some tasks to see them here.'
              : 'Create your first task to get started!'}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {tasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onToggleComplete={handleToggleComplete}
              onDelete={handleDeleteTask}
              onEdit={handleEditTask}
            />
          ))}
        </div>
      )}

      {/* Edit Task Modal */}
      <EditTaskModal
        task={editingTask}
        isOpen={!!editingTask}
        onClose={handleEditClose}
        onTaskUpdated={handleEditComplete}
      />
    </div>
  )
}

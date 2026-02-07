'use client'

/**
 * Task List Component with Search & Performance Optimizations
 * Displays and manages user tasks with search, filter, and sort
 * Author: Sharmeen Asif
 */

import { useState, useEffect, useCallback, useMemo } from 'react'
import { getTasks, updateTask, deleteTask } from '@/lib/task-client'
import type { Task, TaskListResponse } from '@/types/task'
import TaskItem from './TaskItem'
import EditTaskModal from './EditTaskModal'
import { Loader2, AlertCircle, Search, X, SlidersHorizontal } from 'lucide-react'

interface TaskListProps {
  onTasksChange?: (stats: { total: number; completed: number; incomplete: number }) => void
  refreshKey?: number
}

export default function TaskList({ onTasksChange, refreshKey }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([])
  const [stats, setStats] = useState({ total: 0, completed: 0, incomplete: 0 })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all')
  const [editingTask, setEditingTask] = useState<Task | null>(null)

  // Search & Sort states
  const [searchQuery, setSearchQuery] = useState('')
  const [sortBy, setSortBy] = useState<'created_at' | 'due_date' | 'priority' | 'title'>('created_at')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc')
  const [priorityFilter, setPriorityFilter] = useState<string>('')
  const [showFilters, setShowFilters] = useState(false)

  // Fetch tasks with search and filters
  const fetchTasks = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const params: any = {}

      // Filter by completion status
      if (filter !== 'all') {
        params.completed = filter === 'completed'
      }

      // Search query
      if (searchQuery.trim()) {
        params.search = searchQuery.trim()
      }

      // Priority filter
      if (priorityFilter) {
        params.priority = priorityFilter
      }

      // Sort
      params.sort_by = sortBy
      params.order = sortOrder

      // Limit initial load
      params.limit = 100

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
      console.error('Task fetch error:', err)
      setError(err.message || 'Failed to load tasks')
    } finally {
      setLoading(false)
    }
  }, [filter, searchQuery, priorityFilter, sortBy, sortOrder, onTasksChange])

  // Refresh on mount and when refreshKey changes
  useEffect(() => {
    fetchTasks()
  }, [fetchTasks, refreshKey])

  // Debounced search - wait 500ms after user stops typing
  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchQuery !== undefined) {
        fetchTasks()
      }
    }, 500)

    return () => clearTimeout(timer)
  }, [searchQuery])

  // Toggle task completion with optimistic update
  const handleToggleComplete = async (taskId: string, completed: boolean) => {
    // Optimistic update
    setTasks(prev => prev.map(t =>
      t.id === taskId ? { ...t, completed } : t
    ))

    try {
      await updateTask(taskId, { completed })
      await fetchTasks() // Refresh to get accurate stats
    } catch (err: any) {
      setError(err.message || 'Failed to update task')
      await fetchTasks() // Revert on error
    }
  }

  // Delete task
  const handleDeleteTask = async (taskId: string) => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return
    }

    // Optimistic delete
    setTasks(prev => prev.filter(t => t.id !== taskId))

    try {
      await deleteTask(taskId)
      await fetchTasks()
    } catch (err: any) {
      setError(err.message || 'Failed to delete task')
      await fetchTasks()
    }
  }

  // Open edit modal
  const handleEditTask = (task: Task) => {
    setEditingTask(task)
  }

  // Close edit modal
  const handleEditClose = () => {
    setEditingTask(null)
  }

  const handleEditComplete = async () => {
    setEditingTask(null)
    await fetchTasks()
  }

  // Clear search
  const clearSearch = () => {
    setSearchQuery('')
  }

  // Clear all filters
  const clearAllFilters = () => {
    setSearchQuery('')
    setPriorityFilter('')
    setSortBy('created_at')
    setSortOrder('desc')
  }

  // Loading state
  if (loading && tasks.length === 0) {
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
  if (error && tasks.length === 0) {
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
      {/* Search Bar */}
      <div className="bg-white/60 backdrop-blur-lg rounded-2xl p-4 shadow-lg border border-white/20">
        <div className="flex items-center gap-3">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search tasks..."
              className="w-full pl-10 pr-10 py-3 bg-white/80 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all"
            />
            {searchQuery && (
              <button
                onClick={clearSearch}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`p-3 rounded-xl transition-all ${
              showFilters
                ? 'bg-indigo-600 text-white'
                : 'bg-white/80 text-gray-700 hover:bg-gray-100'
            }`}
          >
            <SlidersHorizontal className="w-5 h-5" />
          </button>
        </div>

        {/* Advanced Filters */}
        {showFilters && (
          <div className="mt-4 pt-4 border-t border-gray-200 grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Priority Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
              <select
                value={priorityFilter}
                onChange={(e) => setPriorityFilter(e.target.value)}
                className="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="">All Priorities</option>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>

            {/* Sort By */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Sort By</label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="created_at">Created Date</option>
                <option value="due_date">Due Date</option>
                <option value="priority">Priority</option>
                <option value="title">Title</option>
              </select>
            </div>

            {/* Sort Order */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Order</label>
              <select
                value={sortOrder}
                onChange={(e) => setSortOrder(e.target.value as 'asc' | 'desc')}
                className="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="desc">Newest First</option>
                <option value="asc">Oldest First</option>
              </select>
            </div>

            {/* Clear Filters Button */}
            <div className="md:col-span-3">
              <button
                onClick={clearAllFilters}
                className="text-sm text-indigo-600 hover:text-indigo-700 font-medium"
              >
                Clear All Filters
              </button>
            </div>
          </div>
        )}
      </div>

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

        {loading && tasks.length > 0 && (
          <Loader2 className="w-5 h-5 text-indigo-600 animate-spin ml-auto" />
        )}
      </div>

      {/* Task List */}
      {tasks.length === 0 ? (
        <div className="text-center py-12">
          <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Search className="w-12 h-12 text-gray-400" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {searchQuery ? 'No tasks found' : 'No tasks yet'}
          </h3>
          <p className="text-gray-600 max-w-md mx-auto">
            {searchQuery
              ? 'Try adjusting your search or filters'
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
              onEdit={handleEditTask}
              onDelete={handleDeleteTask}
            />
          ))}
        </div>
      )}

      {/* Edit Task Modal */}
      {editingTask && (
        <EditTaskModal
          task={editingTask}
          isOpen={true}
          onClose={handleEditClose}
          onTaskUpdated={handleEditComplete}
        />
      )}
    </div>
  )
}

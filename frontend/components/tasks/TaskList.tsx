'use client'

/**
 * TaskList Component
 * Fetches and displays user's tasks with filtering
 * Author: Sharmeen Asif
 */

import { useState, useEffect } from 'react'
import { getTasks, TaskListResponse, updateTask, deleteTask } from '@/lib/api-client'
import TaskCard from './TaskCard'
import CreateTaskForm from './CreateTaskForm'

export default function TaskList() {
  const [data, setData] = useState<TaskListResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all')

  const fetchTasks = async () => {
    setLoading(true)
    setError(null)

    try {
      let completed: boolean | undefined = undefined
      if (filter === 'active') completed = false
      if (filter === 'completed') completed = true

      const response = await getTasks(completed)
      setData(response)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch tasks')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTasks()
  }, [filter])

  const handleToggle = async (taskId: string) => {
    if (!data) return

    const task = data.tasks.find((t) => t.id === taskId)
    if (!task) return

    try {
      await updateTask(taskId, { completed: !task.completed })
      // Refresh tasks
      fetchTasks()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task')
    }
  }

  const handleDelete = async (taskId: string) => {
    if (!confirm('Are you sure you want to delete this task?')) return

    try {
      await deleteTask(taskId)
      // Refresh tasks
      fetchTasks()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task')
    }
  }

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-primary border-r-transparent"></div>
        <p className="mt-2 text-gray-600">Loading tasks...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
        {error}
      </div>
    )
  }

  if (!data) return null

  return (
    <div>
      {/* Create Task Form */}
      <CreateTaskForm onTaskCreated={fetchTasks} />

      {/* Filter Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setFilter('all')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              filter === 'all'
                ? 'border-primary text-primary'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            All ({data.total})
          </button>
          <button
            onClick={() => setFilter('active')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              filter === 'active'
                ? 'border-primary text-primary'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Active ({data.incomplete})
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              filter === 'completed'
                ? 'border-primary text-primary'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Completed ({data.completed})
          </button>
        </nav>
      </div>

      {/* Task List */}
      {data.tasks.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">
            {filter === 'all' && 'No tasks yet. Create your first task to get started!'}
            {filter === 'active' && 'No active tasks. Great job!'}
            {filter === 'completed' && 'No completed tasks yet.'}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {data.tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              onToggle={handleToggle}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
    </div>
  )
}

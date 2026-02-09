/**
 * Task API Client
 * Functions for interacting with task endpoints
 * Author: Sharmeen Asif
 */

import type { Task, TaskCreate, TaskUpdate, TaskListResponse } from '@/types/task'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

/**
 * Get all tasks for authenticated user
 */
export async function getTasks(params?: {
  completed?: boolean
  limit?: number
  offset?: number
}): Promise<TaskListResponse> {
  const query = new URLSearchParams()
  if (params?.completed !== undefined) {
    query.append('completed', String(params.completed))
  }
  if (params?.limit) {
    query.append('limit', String(params.limit))
  }
  if (params?.offset) {
    query.append('offset', String(params.offset))
  }

  const response = await fetch(`${API_URL}/api/tasks?${query}`, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
  })

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('Not authenticated')
    }
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || 'Failed to fetch tasks')
  }

  return response.json()
}

/**
 * Get a single task by ID
 */
export async function getTask(taskId: string): Promise<Task> {
  const response = await fetch(`${API_URL}/api/tasks/${taskId}`, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
  })

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Task not found')
    }
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || 'Failed to fetch task')
  }

  return response.json()
}

/**
 * Create a new task
 */
export async function createTask(data: TaskCreate): Promise<Task> {
  const response = await fetch(`${API_URL}/api/tasks`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('Not authenticated')
    }
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || 'Failed to create task')
  }

  return response.json()
}

/**
 * Update an existing task
 */
export async function updateTask(taskId: string, data: TaskUpdate): Promise<Task> {
  const response = await fetch(`${API_URL}/api/tasks/${taskId}`, {
    method: 'PATCH',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Task not found')
    }
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || 'Failed to update task')
  }

  return response.json()
}

/**
 * Delete a task
 */
export async function deleteTask(taskId: string): Promise<void> {
  const response = await fetch(`${API_URL}/api/tasks/${taskId}`, {
    method: 'DELETE',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
  })

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Task not found')
    }
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || 'Failed to delete task')
  }
}

/**
 * Toggle task completion status
 */
export async function toggleTaskComplete(taskId: string, completed: boolean): Promise<Task> {
  return updateTask(taskId, { completed })
}

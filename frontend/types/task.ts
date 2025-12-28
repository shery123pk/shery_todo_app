/**
 * Task Type Definitions
 * TypeScript types for task-related data structures
 * Author: Sharmeen Asif
 */

export interface Task {
  id: string
  user_id: string
  title: string
  description?: string | null
  completed: boolean
  priority?: string | null
  tags: string[]
  category?: string | null
  created_at: string
  updated_at: string
}

export interface TaskCreate {
  title: string
  description?: string
  priority?: string
  tags?: string[]
  category?: string
}

export interface TaskUpdate {
  title?: string
  description?: string
  completed?: boolean
  priority?: string
  tags?: string[]
  category?: string
}

export interface TaskListResponse {
  tasks: Task[]
  total: number
  completed: number
  incomplete: number
}

export type PriorityLevel = 'low' | 'medium' | 'high'
export type TaskStatus = 'all' | 'active' | 'completed'

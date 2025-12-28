'use client'

/**
 * Kanban Board Component
 * Drag and drop task board with columns
 * Author: Sharmeen Asif
 */

import { useState, useEffect } from 'react'
import {
  DndContext,
  DragEndEvent,
  DragOverlay,
  DragStartEvent,
  DragOverEvent,
  PointerSensor,
  useSensor,
  useSensors,
  closestCorners,
  useDroppable,
} from '@dnd-kit/core'
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable'
import { getTasks, updateTask } from '@/lib/task-client'
import type { Task } from '@/types/task'
import TaskCard from './TaskCard'
import { Plus, Loader2, AlertCircle } from 'lucide-react'

type ColumnId = 'todo' | 'in_progress' | 'done'

interface Column {
  id: ColumnId
  title: string
  color: string
  bgColor: string
}

const columns: Column[] = [
  { id: 'todo', title: 'To Do', color: 'from-gray-500 to-gray-600', bgColor: 'bg-gray-50' },
  { id: 'in_progress', title: 'In Progress', color: 'from-blue-500 to-indigo-600', bgColor: 'bg-blue-50' },
  { id: 'done', title: 'Done', color: 'from-green-500 to-emerald-600', bgColor: 'bg-green-50' },
]

interface KanbanBoardProps {
  onCreateTask?: () => void
}

// Droppable Column Component
function DroppableColumn({
  column,
  children,
  isOver
}: {
  column: Column;
  children: React.ReactNode;
  isOver: boolean
}) {
  const { setNodeRef } = useDroppable({
    id: column.id,
  })

  return (
    <div ref={setNodeRef} className="flex flex-col">
      {children}
    </div>
  )
}

export default function KanbanBoard({ onCreateTask }: KanbanBoardProps) {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [activeTask, setActiveTask] = useState<Task | null>(null)
  const [overId, setOverId] = useState<string | null>(null)

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  )

  // Fetch tasks
  const fetchTasks = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await getTasks({})
      setTasks(data.tasks)
    } catch (err: any) {
      setError(err.message || 'Failed to load tasks')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTasks()
  }, [])

  // Get task status from completion state
  const getTaskColumn = (task: Task): ColumnId => {
    if (task.completed) return 'done'
    // For now, incomplete tasks go to "to do"
    // Later we can add a "status" field to tasks
    return 'todo'
  }

  // Get tasks for a column
  const getColumnTasks = (columnId: ColumnId): Task[] => {
    return tasks.filter(task => {
      const taskColumn = getTaskColumn(task)
      return taskColumn === columnId
    })
  }

  // Handle drag start
  const handleDragStart = (event: DragStartEvent) => {
    const task = tasks.find(t => t.id === event.active.id)
    setActiveTask(task || null)
  }

  // Handle drag over
  const handleDragOver = (event: DragOverEvent) => {
    const { over } = event
    setOverId(over ? over.id as string : null)
  }

  // Handle drag end
  const handleDragEnd = async (event: DragEndEvent) => {
    const { active, over } = event
    setActiveTask(null)
    setOverId(null)

    if (!over) return

    const taskId = active.id as string
    let targetColumn: ColumnId | null = null

    // Check if dropped over a column
    if (columns.find(col => col.id === over.id)) {
      targetColumn = over.id as ColumnId
    } else {
      // Dropped over a task - find which column the task belongs to
      const targetTask = tasks.find(t => t.id === over.id)
      if (targetTask) {
        targetColumn = getTaskColumn(targetTask)
      }
    }

    if (!targetColumn) return

    // Find the task being dragged
    const task = tasks.find(t => t.id === taskId)
    if (!task) return

    // Determine if task should be completed based on column
    const shouldBeCompleted = targetColumn === 'done'

    // Only update if status changed
    if (task.completed !== shouldBeCompleted) {
      try {
        // Optimistically update UI
        setTasks(prev =>
          prev.map(t =>
            t.id === taskId ? { ...t, completed: shouldBeCompleted } : t
          )
        )

        // Update on server
        await updateTask(taskId, { completed: shouldBeCompleted })

        // Refresh to ensure sync
        await fetchTasks()
      } catch (err: any) {
        // Revert on error
        setError('Failed to update task')
        await fetchTasks()
      }
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin text-indigo-600 mx-auto mb-2" />
          <p className="text-gray-600">Loading board...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border-2 border-red-200 rounded-xl p-6 flex items-start gap-3">
        <AlertCircle className="w-6 h-6 text-red-600 flex-shrink-0" />
        <div>
          <h3 className="font-semibold text-red-900">Error loading board</h3>
          <p className="text-red-700 text-sm mt-1">{error}</p>
          <button
            onClick={fetchTasks}
            className="mt-3 text-sm text-red-600 hover:text-red-700 font-medium"
          >
            Try again
          </button>
        </div>
      </div>
    )
  }

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCorners}
      onDragStart={handleDragStart}
      onDragOver={handleDragOver}
      onDragEnd={handleDragEnd}
    >
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {columns.map(column => {
          const columnTasks = getColumnTasks(column.id)
          const isColumnOver = overId === column.id

          return (
            <DroppableColumn key={column.id} column={column} isOver={isColumnOver}>
              {/* Column Header */}
              <div className={`${column.bgColor} rounded-t-2xl p-4 border-b-4 ${
                isColumnOver ? 'border-indigo-500' : 'border-gray-200'
              } transition-colors duration-200`}>
                <div className="flex items-center justify-between mb-2">
                  <h3 className={`text-lg font-bold bg-gradient-to-r ${column.color} bg-clip-text text-transparent`}>
                    {column.title}
                  </h3>
                  <span className="text-sm font-semibold text-gray-600 bg-white px-3 py-1 rounded-full">
                    {columnTasks.length}
                  </span>
                </div>
              </div>

              {/* Column Content */}
              <SortableContext
                id={column.id}
                items={columnTasks.map(t => t.id)}
                strategy={verticalListSortingStrategy}
              >
                <div className={`bg-white/50 backdrop-blur-sm rounded-b-2xl p-4 min-h-[400px] space-y-3 border-2 border-t-0 ${
                  isColumnOver ? 'border-indigo-500 bg-indigo-50/30' : 'border-gray-200'
                } transition-all duration-200`}>
                  {columnTasks.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-32 text-gray-400">
                      <p className="text-sm">No tasks yet</p>
                      {column.id === 'todo' && onCreateTask && (
                        <button
                          onClick={onCreateTask}
                          className="mt-2 text-xs text-indigo-600 hover:text-indigo-700 font-medium flex items-center gap-1"
                        >
                          <Plus className="w-4 h-4" />
                          Add task
                        </button>
                      )}
                    </div>
                  ) : (
                    columnTasks.map(task => (
                      <TaskCard key={task.id} task={task} />
                    ))
                  )}
                </div>
              </SortableContext>
            </DroppableColumn>
          )
        })}
      </div>

      {/* Drag Overlay */}
      <DragOverlay>
        {activeTask && (
          <div className="rotate-3 scale-105">
            <TaskCard task={activeTask} />
          </div>
        )}
      </DragOverlay>
    </DndContext>
  )
}

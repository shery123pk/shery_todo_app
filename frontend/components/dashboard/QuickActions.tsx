'use client'

/**
 * Quick Actions Component
 * Quick shortcuts for common actions
 * Author: Sharmeen Asif
 */

import { Plus, Calendar, Users, BarChart3 } from 'lucide-react'

interface QuickActionsProps {
  onCreateTask: () => void
}

export default function QuickActions({ onCreateTask }: QuickActionsProps) {
  const actions = [
    {
      title: 'New Task',
      description: 'Create a task',
      icon: Plus,
      color: 'from-indigo-600 to-purple-600',
      onClick: onCreateTask,
      enabled: true,
    },
    {
      title: 'Schedule',
      description: 'View calendar',
      icon: Calendar,
      color: 'from-blue-600 to-cyan-600',
      onClick: () => {},
      enabled: false,
    },
    {
      title: 'Team',
      description: 'Invite members',
      icon: Users,
      color: 'from-green-600 to-emerald-600',
      onClick: () => {},
      enabled: false,
    },
    {
      title: 'Reports',
      description: 'View analytics',
      icon: BarChart3,
      color: 'from-orange-600 to-amber-600',
      onClick: () => {},
      enabled: false,
    },
  ]

  return (
    <div className="bg-white/80 backdrop-blur-xl rounded-2xl shadow-lg border border-white/20 p-6 mb-6">
      <h2 className="text-lg font-bold text-gray-900 mb-4">Quick Actions</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {actions.map((action) => {
          const Icon = action.icon
          return (
            <button
              key={action.title}
              onClick={action.onClick}
              disabled={!action.enabled}
              className={`relative group p-4 rounded-xl border-2 border-gray-200 hover:border-gray-300 transition-all duration-200 ${
                action.enabled
                  ? 'hover:shadow-lg hover:-translate-y-1 cursor-pointer'
                  : 'opacity-50 cursor-not-allowed'
              }`}
            >
              <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${action.color} flex items-center justify-center mb-3 shadow-md`}>
                <Icon className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-sm font-semibold text-gray-900 mb-1">{action.title}</h3>
              <p className="text-xs text-gray-500">{action.description}</p>
              {!action.enabled && (
                <span className="absolute top-2 right-2 text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full">
                  Soon
                </span>
              )}
            </button>
          )
        })}
      </div>
    </div>
  )
}

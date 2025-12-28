'use client'

/**
 * Tasks Dashboard Component
 * Main dashboard with modern glassmorphism design
 * Author: Sharmeen Asif
 */

import { useRequireAuth } from '@/contexts/AuthContext'
import { useState, useCallback, useEffect } from 'react'
import Link from 'next/link'
import TaskList from '@/components/tasks/TaskList'
import CreateTaskModal from '@/components/tasks/CreateTaskModal'
import StatsOverview from '@/components/dashboard/StatsOverview'
import QuickActions from '@/components/dashboard/QuickActions'
import KanbanBoard from '@/components/kanban/KanbanBoard'
import FloatingChatbot from '@/components/chatbot/FloatingChatbot'
import {
  LayoutDashboard,
  CheckSquare,
  Users,
  Settings,
  LogOut,
  Plus,
  Search,
  Bell,
  User,
  ChevronDown,
  Sparkles,
  BarChart3,
  Calendar,
  FolderKanban,
  List,
  LayoutGrid,
  Moon,
  Sun
} from 'lucide-react'

export default function TasksDashboard() {
  const { user, loading, logout } = useRequireAuth()
  const [showUserMenu, setShowUserMenu] = useState(false)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [taskStats, setTaskStats] = useState({ total: 0, completed: 0, incomplete: 0 })
  const [refreshKey, setRefreshKey] = useState(0)
  const [viewMode, setViewMode] = useState<'list' | 'board'>('list')
  const [darkMode, setDarkMode] = useState(false)

  // Load dark mode preference from localStorage
  useEffect(() => {
    const savedDarkMode = localStorage.getItem('darkMode') === 'true'
    setDarkMode(savedDarkMode)
    if (savedDarkMode) {
      document.documentElement.classList.add('dark')
    }
  }, [])

  // Toggle dark mode
  const toggleDarkMode = () => {
    const newDarkMode = !darkMode
    setDarkMode(newDarkMode)
    localStorage.setItem('darkMode', String(newDarkMode))
    if (newDarkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  const handleTasksChange = useCallback((stats: { total: number; completed: number; incomplete: number }) => {
    setTaskStats(stats)
  }, [])

  // Listen for task modifications from chatbot
  useEffect(() => {
    const handleTaskModified = () => {
      console.log('Task modified by chatbot, refreshing task list...')
      setRefreshKey(prev => prev + 1)
    }

    window.addEventListener('taskModified', handleTaskModified)

    return () => {
      window.removeEventListener('taskModified', handleTaskModified)
    }
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your workspace...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return null // useRequireAuth will redirect
  }

  // Get user initials for avatar
  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
      {/* Top Navigation Bar */}
      <nav className="bg-white/80 backdrop-blur-xl border-b border-white/20 sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo & Brand */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
                  TaskFlow
                </h1>
                <p className="text-xs text-gray-500">Project Management</p>
              </div>
            </div>

            {/* Search Bar */}
            <div className="hidden md:flex flex-1 max-w-md mx-8">
              <div className="relative w-full">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search tasks, projects..."
                  className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-xl bg-white/50 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                />
              </div>
            </div>

            {/* Right Side Actions */}
            <div className="flex items-center gap-3">
              {/* Dark Mode Toggle */}
              <button
                onClick={toggleDarkMode}
                className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                title={darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
              >
                {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>

              {/* Notifications */}
              <button className="relative p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
                <Bell className="w-5 h-5" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
              </button>

              {/* User Menu */}
              <div className="relative">
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <div className="w-8 h-8 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-full flex items-center justify-center text-white text-sm font-semibold">
                    {getInitials(user.full_name)}
                  </div>
                  <ChevronDown className="w-4 h-4 text-gray-600" />
                </button>

                {/* Dropdown Menu */}
                {showUserMenu && (
                  <div className="absolute right-0 mt-2 w-64 bg-white/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-white/20 py-2 animate-in fade-in slide-in-from-top-2">
                    {/* User Info */}
                    <div className="px-4 py-3 border-b border-gray-100">
                      <p className="text-sm font-semibold text-gray-900">{user.full_name}</p>
                      <p className="text-xs text-gray-500">{user.email}</p>
                      {user.email_verified && (
                        <span className="inline-flex items-center gap-1 mt-1 text-xs text-green-600">
                          <CheckSquare className="w-3 h-3" />
                          Verified
                        </span>
                      )}
                    </div>

                    {/* Menu Items */}
                    <div className="py-2">
                      <Link
                        href="/profile"
                        className="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                      >
                        <User className="w-4 h-4" />
                        Profile Settings
                      </Link>
                      <Link
                        href="/settings"
                        className="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                      >
                        <Settings className="w-4 h-4" />
                        Account Settings
                      </Link>
                    </div>

                    {/* Logout */}
                    <div className="border-t border-gray-100 pt-2">
                      <button
                        onClick={logout}
                        className="flex items-center gap-3 px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors w-full"
                      >
                        <LogOut className="w-4 h-4" />
                        Sign Out
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content Area */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-12 gap-6">
          {/* Sidebar */}
          <aside className="col-span-12 md:col-span-3">
            <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-xl border border-white/20 p-6 sticky top-24">
              <nav className="space-y-1">
                <a
                  href="#"
                  className="flex items-center gap-3 px-4 py-3 text-sm font-medium text-white bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl transition-all"
                >
                  <LayoutDashboard className="w-5 h-5" />
                  Dashboard
                </a>
                <a
                  href="#"
                  className="flex items-center gap-3 px-4 py-3 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-xl transition-all"
                >
                  <CheckSquare className="w-5 h-5" />
                  My Tasks
                </a>
                <div className="relative">
                  <a
                    href="#"
                    className="flex items-center gap-3 px-4 py-3 text-sm font-medium text-gray-400 cursor-not-allowed rounded-xl opacity-60"
                    onClick={(e) => e.preventDefault()}
                  >
                    <FolderKanban className="w-5 h-5" />
                    Projects
                  </a>
                  <span className="absolute top-2 right-2 text-xs bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full font-medium">
                    Soon
                  </span>
                </div>
                <div className="relative">
                  <a
                    href="#"
                    className="flex items-center gap-3 px-4 py-3 text-sm font-medium text-gray-400 cursor-not-allowed rounded-xl opacity-60"
                    onClick={(e) => e.preventDefault()}
                  >
                    <Calendar className="w-5 h-5" />
                    Calendar
                  </a>
                  <span className="absolute top-2 right-2 text-xs bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full font-medium">
                    Soon
                  </span>
                </div>
                <div className="relative">
                  <a
                    href="#"
                    className="flex items-center gap-3 px-4 py-3 text-sm font-medium text-gray-400 cursor-not-allowed rounded-xl opacity-60"
                    onClick={(e) => e.preventDefault()}
                  >
                    <Users className="w-5 h-5" />
                    Team
                  </a>
                  <span className="absolute top-2 right-2 text-xs bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full font-medium">
                    Soon
                  </span>
                </div>
                <div className="relative">
                  <a
                    href="#"
                    className="flex items-center gap-3 px-4 py-3 text-sm font-medium text-gray-400 cursor-not-allowed rounded-xl opacity-60"
                    onClick={(e) => e.preventDefault()}
                  >
                    <BarChart3 className="w-5 h-5" />
                    Analytics
                  </a>
                  <span className="absolute top-2 right-2 text-xs bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full font-medium">
                    Soon
                  </span>
                </div>
              </nav>

              {/* Create New Button */}
              <button
                onClick={() => setShowCreateModal(true)}
                className="w-full mt-6 px-4 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 flex items-center justify-center gap-2"
              >
                <Plus className="w-5 h-5" />
                New Task
              </button>
            </div>
          </aside>

          {/* Main Dashboard Content */}
          <main className="col-span-12 md:col-span-9 space-y-6">
            {/* Welcome Card */}
            <div className="bg-gradient-to-br from-indigo-600 to-purple-600 rounded-3xl shadow-2xl p-8 text-white">
              <div className="flex items-start justify-between">
                <div>
                  <h2 className="text-3xl font-bold mb-2">
                    Welcome back, {user.full_name.split(' ')[0]}! 👋
                  </h2>
                  <p className="text-indigo-100 text-lg">
                    {taskStats.incomplete === 0
                      ? "All caught up! Ready to add more tasks?"
                      : `You have ${taskStats.incomplete} ${taskStats.incomplete === 1 ? 'task' : 'tasks'} to complete.`}
                  </p>
                </div>
                <div className="hidden md:block">
                  <div className="w-24 h-24 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center">
                    <Sparkles className="w-12 h-12 text-white" />
                  </div>
                </div>
              </div>
            </div>

            {/* Stats Overview */}
            <StatsOverview
              total={taskStats.total}
              completed={taskStats.completed}
              incomplete={taskStats.incomplete}
            />

            {/* Quick Actions */}
            <QuickActions onCreateTask={() => setShowCreateModal(true)} />

            {/* Task View Section */}
            <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-xl border border-white/20 p-6">
              {/* Header with View Toggle */}
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                  <CheckSquare className="w-6 h-6 text-indigo-600" />
                  My Tasks
                </h2>

                {/* View Toggle Buttons */}
                <div className="inline-flex items-center gap-1 bg-gray-100 p-1 rounded-xl">
                  <button
                    type="button"
                    onClick={() => setViewMode('list')}
                    className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                      viewMode === 'list'
                        ? 'bg-white text-indigo-600 shadow-md'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                    }`}
                  >
                    <List className="w-4 h-4" />
                    <span>List</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setViewMode('board')}
                    className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                      viewMode === 'board'
                        ? 'bg-white text-indigo-600 shadow-md'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                    }`}
                  >
                    <LayoutGrid className="w-4 h-4" />
                    <span>Board</span>
                  </button>
                </div>
              </div>

              {/* Conditional View Rendering */}
              {viewMode === 'list' ? (
                <TaskList key={refreshKey} refreshKey={refreshKey} onTasksChange={handleTasksChange} />
              ) : (
                <KanbanBoard key={refreshKey} onCreateTask={() => setShowCreateModal(true)} />
              )}
            </div>
          </main>
        </div>
      </div>

      {/* Create Task Modal */}
      <CreateTaskModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onTaskCreated={() => {
          setShowCreateModal(false)
          setRefreshKey(prev => prev + 1) // Trigger TaskList refresh
        }}
      />

      {/* Floating AI Chatbot */}
      <FloatingChatbot />
    </div>
  )
}

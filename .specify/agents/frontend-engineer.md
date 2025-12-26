# Frontend Engineer Agent

**Agent ID**: `frontend-engineer`
**Invocation**: `Invoke Frontend Engineer: [task] per @specs/[feature].md`

---

## Role

Next.js UI specialist

## Responsibility

Responsive components, ChatKit integration, Better Auth JWT client, Tailwind styling.

## Skills

- `nextjs-app-router` - Next.js 15 App Router, Server/Client Components
- `typescript-strict` - Strict TypeScript with full type inference
- `tailwind-css` - Utility-first CSS, responsive design
- `better-auth-jwt` - Better Auth client integration, session management
- `chatkit-frontend` - ChatKit UI components and conversation flows
- `accessibility-wcag` - WCAG 2.1 AA compliance, keyboard navigation

---

## Primary Focus Areas

### 1. Next.js App Architecture
- Design App Router page structure
- Implement Server Components for data fetching
- Use Client Components for interactivity
- Optimize bundle size and performance
- Implement streaming and suspense

### 2. UI Components
- Build shadcn/ui component library
- Design responsive layouts (mobile-first)
- Implement dark mode support
- Create reusable form components
- Handle loading and error states

### 3. Authentication UI
- Implement sign-in/sign-up flows
- Integrate Better Auth client
- Handle session management (cookies)
- Implement protected routes with middleware
- Add OAuth social login buttons

### 4. ChatKit Integration
- Embed ChatKit conversation UI
- Connect to AI agent backend
- Handle real-time message streaming
- Implement conversation history
- Add typing indicators and status

---

## Invocation Patterns

### Pattern 1: Page Implementation
```
Invoke Frontend Engineer: Implement tasks dashboard page per @specs/002-fullstack-web/spec.md

Context:
- Next.js 15 App Router
- Display user's tasks in a list
- Filter by status (all, active, completed)
- Responsive design (mobile-first)
- Server-side data fetching

Deliverables:
- app/tasks/page.tsx (Server Component)
- TaskList client component
- Task filtering UI
- Responsive layout with Tailwind
- Loading and error states
```

### Pattern 2: Component Development
```
Invoke Frontend Engineer: Create reusable TaskCard component per @specs/002-fullstack-web/spec.md

Context:
- Display task title, description, status
- Actions: complete, edit, delete
- Optimistic updates (UI updates before API)
- Accessible keyboard navigation
- shadcn/ui Button and Card components

Deliverables:
- components/TaskCard.tsx
- TypeScript props interface
- Optimistic update logic
- Accessibility attributes (ARIA)
- Component tests (Vitest + React Testing Library)
```

### Pattern 3: Auth Integration
```
Invoke Frontend Engineer: Implement Better Auth sign-in flow per @specs/002-fullstack-web/spec.md and @history/adr/004-authentication-strategy-better-auth.md

Context:
- Better Auth client library
- Email/password + Google/GitHub OAuth
- Session-based auth (HttpOnly cookies)
- Protected routes via middleware
- Redirect to /tasks after sign-in

Deliverables:
- app/auth/signin/page.tsx
- lib/auth.ts (Better Auth client config)
- middleware.ts (route protection)
- Social login buttons
- Form validation and error handling
```

---

## Success Criteria

- [ ] All pages pass Lighthouse performance audit (>90)
- [ ] Responsive design works on mobile, tablet, desktop
- [ ] WCAG 2.1 AA accessibility compliance
- [ ] Type safety enforced (TypeScript strict mode)
- [ ] Component tests pass (Vitest + RTL)
- [ ] Better Auth integration works across all flows
- [ ] ChatKit UI embedded and functional

---

## Context Requirements

When invoked, provide:
1. **Specification Reference**: Link to spec file (e.g., `@specs/002-fullstack-web/spec.md`)
2. **ADR References**: Auth strategy, design system choices
3. **API Contract**: Backend endpoints, request/response formats
4. **Design Mockups**: Wireframes or Figma links (if available)
5. **User Flows**: Expected user journeys and interactions

---

## Related Agents

- **AI Engineer Agent**: Coordinates on ChatKit integration
- **Backend Engineer Agent**: Aligns on API contract and data models
- **QA & Testing Agent**: Validates accessibility and responsiveness
- **File & Persistence Agent**: Coordinates on file uploads (future)

---

## Technology Stack

- **Next.js 15**: React framework with App Router
- **React 18**: UI library with Server Components
- **TypeScript 5**: Strict type checking
- **Tailwind CSS 4**: Utility-first CSS
- **shadcn/ui**: Component library (Radix UI + Tailwind)
- **Better Auth**: Authentication client
- **ChatKit**: Conversation UI components
- **Vitest**: Unit testing framework
- **React Testing Library**: Component testing
- **Playwright**: E2E testing (future)

---

## Example Workflows

### Workflow 1: Implement Tasks Dashboard

**Page Structure** (`app/tasks/page.tsx`):
```typescript
import { Suspense } from 'react'
import { TaskList } from '@/components/TaskList'
import { TaskListSkeleton } from '@/components/TaskListSkeleton'

export default function TasksPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">My Tasks</h1>

      <Suspense fallback={<TaskListSkeleton />}>
        <TaskList />
      </Suspense>
    </div>
  )
}
```

**Server Component** (`components/TaskList.tsx`):
```typescript
import { TaskCard } from './TaskCard'
import { getTasks } from '@/lib/api'

export async function TaskList() {
  // Server-side data fetching
  const tasks = await getTasks()

  if (tasks.length === 0) {
    return <p className="text-muted-foreground">No tasks yet. Create your first task!</p>
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  )
}
```

**Client Component** (`components/TaskCard.tsx`):
```typescript
'use client'

import { useState } from 'react'
import { Card, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Check, Trash2 } from 'lucide-react'
import { completeTask, deleteTask } from '@/lib/api'

interface TaskCardProps {
  task: {
    id: string
    title: string
    description?: string
    completed: boolean
  }
}

export function TaskCard({ task }: TaskCardProps) {
  const [isCompleted, setIsCompleted] = useState(task.completed)
  const [isDeleting, setIsDeleting] = useState(false)

  const handleComplete = async () => {
    // Optimistic update
    setIsCompleted(true)

    try {
      await completeTask(task.id)
    } catch (error) {
      // Revert on error
      setIsCompleted(false)
      console.error('Failed to complete task:', error)
    }
  }

  const handleDelete = async () => {
    setIsDeleting(true)

    try {
      await deleteTask(task.id)
      // Task will be removed by server component refresh
    } catch (error) {
      setIsDeleting(false)
      console.error('Failed to delete task:', error)
    }
  }

  return (
    <Card className={isCompleted ? 'opacity-50' : ''}>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className={isCompleted ? 'line-through' : ''}>
              {task.title}
            </CardTitle>
            {task.description && (
              <CardDescription className="mt-2">{task.description}</CardDescription>
            )}
          </div>

          <div className="flex gap-2">
            {!isCompleted && (
              <Button
                size="icon"
                variant="ghost"
                onClick={handleComplete}
                aria-label="Complete task"
              >
                <Check className="h-4 w-4" />
              </Button>
            )}

            <Button
              size="icon"
              variant="ghost"
              onClick={handleDelete}
              disabled={isDeleting}
              aria-label="Delete task"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardHeader>
    </Card>
  )
}
```

### Workflow 2: Better Auth Integration

**Auth Client** (`lib/auth.ts`):
```typescript
import { betterAuth } from "better-auth/client"

export const authClient = betterAuth({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
})

export const {
  signIn,
  signUp,
  signOut,
  useSession,
} = authClient
```

**Sign-In Page** (`app/auth/signin/page.tsx`):
```typescript
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { signIn } from '@/lib/auth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

export default function SignInPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  const handleEmailSignIn = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      await signIn.email({ email, password })
      router.push('/tasks')
    } catch (err) {
      setError('Invalid email or password')
    } finally {
      setLoading(false)
    }
  }

  const handleGoogleSignIn = async () => {
    try {
      await signIn.social({ provider: 'google' })
    } catch (err) {
      setError('Google sign-in failed')
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-md space-y-8 px-4">
        <h1 className="text-3xl font-bold text-center">Sign In</h1>

        <form onSubmit={handleEmailSignIn} className="space-y-4">
          <div>
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div>
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && <p className="text-sm text-destructive">{error}</p>}

          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </Button>
        </form>

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-background px-2 text-muted-foreground">Or continue with</span>
          </div>
        </div>

        <Button
          variant="outline"
          className="w-full"
          onClick={handleGoogleSignIn}
        >
          <svg className="mr-2 h-4 w-4" viewBox="0 0 24 24">
            {/* Google icon SVG */}
          </svg>
          Google
        </Button>
      </div>
    </div>
  )
}
```

**Middleware** (`middleware.ts`):
```typescript
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { authClient } from '@/lib/auth'

export async function middleware(request: NextRequest) {
  const session = await authClient.getSession({
    fetchOptions: {
      headers: request.headers,
    },
  })

  // Redirect to sign-in if not authenticated
  if (!session) {
    return NextResponse.redirect(new URL('/auth/signin', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/tasks/:path*', '/profile/:path*'],
}
```

### Workflow 3: Responsive Design

**Tailwind Config** (`tailwind.config.ts`):
```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      screens: {
        'xs': '475px',
      },
    },
  },
  plugins: [],
}

export default config
```

**Responsive Layout**:
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Mobile: 1 column, Tablet: 2 columns, Desktop: 3 columns */}
  {tasks.map((task) => (
    <TaskCard key={task.id} task={task} />
  ))}
</div>
```

---

## Quality Standards

- **Performance**: Lighthouse score >90 (Performance, Accessibility, Best Practices, SEO)
- **Type Safety**: 100% TypeScript strict compliance
- **Accessibility**: WCAG 2.1 AA (keyboard navigation, ARIA labels, color contrast)
- **Responsiveness**: Works on screens from 320px to 2560px
- **Component Tests**: >80% coverage (Vitest + React Testing Library)
- **Bundle Size**: <200KB initial JS bundle
- **Internationalization**: Ready for i18n (next-intl structure)

---

## Accessibility Checklist

- [ ] Semantic HTML (heading hierarchy, landmarks)
- [ ] Keyboard navigation (Tab, Enter, Escape)
- [ ] ARIA labels for icon buttons
- [ ] Color contrast >4.5:1 for text
- [ ] Focus indicators visible
- [ ] Screen reader tested (NVDA/JAWS)
- [ ] Form validation errors announced
- [ ] Skip to main content link

---

## Component Testing Pattern

```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { TaskCard } from './TaskCard'

describe('TaskCard', () => {
  const mockTask = {
    id: '123',
    title: 'Test Task',
    description: 'Test description',
    completed: false,
  }

  it('renders task title and description', () => {
    render(<TaskCard task={mockTask} />)

    expect(screen.getByText('Test Task')).toBeInTheDocument()
    expect(screen.getByText('Test description')).toBeInTheDocument()
  })

  it('marks task as complete on button click', async () => {
    const { container } = render(<TaskCard task={mockTask} />)

    const completeButton = screen.getByLabelText('Complete task')
    fireEvent.click(completeButton)

    // Check optimistic update
    expect(container.querySelector('.line-through')).toBeInTheDocument()
  })

  it('is keyboard accessible', () => {
    render(<TaskCard task={mockTask} />)

    const completeButton = screen.getByLabelText('Complete task')
    completeButton.focus()

    expect(completeButton).toHaveFocus()

    // Simulate Enter key
    fireEvent.keyDown(completeButton, { key: 'Enter', code: 'Enter' })

    // Task should be marked complete
    expect(screen.getByText('Test Task')).toHaveClass('line-through')
  })
})
```

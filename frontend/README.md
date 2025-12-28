# Project Management System - Frontend

Professional multi-tenant project management system frontend built with Next.js 15 and React 18.

## Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript 5.3+
- **UI Library**: React 18
- **Styling**: Tailwind CSS v3
- **State Management**:
  - Zustand (client state)
  - TanStack Query v5 (server state)
- **Forms**: React Hook Form + Zod validation
- **Drag & Drop**: @dnd-kit/core
- **Icons**: Lucide React
- **Testing**: Vitest + Playwright

## Prerequisites

- Node.js 18+
- npm 10+

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

```bash
cp .env.local.example .env.local
```

Edit `.env.local`:
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)

### 3. Run Development Server

```bash
npm run dev
```

Server runs at http://localhost:3000

## Project Structure

```
frontend/
├── app/                        # Next.js App Router pages
│   ├── (auth)/                 # Auth pages (signin, signup)
│   ├── (dashboard)/            # Protected dashboard routes
│   │   ├── dashboard/          # Main dashboard
│   │   ├── projects/           # Project management
│   │   └── tasks/              # Task views
│   ├── layout.tsx              # Root layout
│   └── page.tsx                # Landing page
├── components/                 # React components
│   ├── ui/                     # shadcn/ui base components
│   ├── auth/                   # Auth-related components
│   ├── boards/                 # Kanban board components
│   ├── tasks/                  # Task components
│   └── ...
├── lib/                        # Utilities
│   ├── api.ts                  # API client
│   ├── auth.ts                 # Auth context
│   └── queryClient.ts          # TanStack Query config
├── types/                      # TypeScript definitions
│   └── models.ts               # API models
├── tests/                      # Vitest unit tests
└── e2e/                        # Playwright E2E tests
```

## Available Scripts

```bash
# Development
npm run dev                     # Start dev server

# Build
npm run build                   # Build for production
npm run start                   # Start production server

# Testing
npm run test                    # Run unit tests (Vitest)
npm run test:watch              # Run tests in watch mode
npm run test:coverage           # Generate coverage report
npm run test:e2e                # Run E2E tests (Playwright)
npm run test:e2e:ui             # Run E2E tests with UI

# Code Quality
npm run lint                    # Run ESLint
npm run lint:fix                # Fix ESLint issues
npm run type-check              # TypeScript type checking
npm run format                  # Format code with Prettier
```

## Testing

### Unit Tests (Vitest)

```bash
# Run all tests
npm run test

# Run tests in watch mode
npm run test:watch

# Generate coverage report
npm run test:coverage
```

### E2E Tests (Playwright)

```bash
# Run E2E tests
npm run test:e2e

# Run E2E tests with UI
npm run test:e2e:ui
```

## Development Workflow

1. **Create component**: Add to `components/` directory
2. **Add types**: Define in `types/models.ts`
3. **Write tests**: Add test file in `tests/`
4. **Add to page**: Use in `app/` routes

## Code Style

- **TypeScript strict mode** enabled
- **ESLint** for linting
- **Prettier** for formatting
- **Tailwind CSS** for styling

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import repository in Vercel
3. Set environment variables:
   - `NEXT_PUBLIC_API_URL`: Backend API URL
4. Deploy

### Manual Deployment

```bash
npm run build
npm run start
```

## Development

This is feature `001-project-management-system`. See:
- Specification: `../specs/001-project-management-system/spec.md`
- Architecture Plan: `../specs/001-project-management-system/plan.md`
- Tasks: `../specs/001-project-management-system/tasks.md`

## Key Features

- **Multi-tenant architecture**: Organization-based isolation
- **Kanban boards**: Drag-and-drop task management
- **Role-based access control**: Owner, Admin, Member, Viewer
- **Real-time collaboration**: Comments and activity feeds
- **File attachments**: Upload and manage task attachments
- **Responsive design**: Mobile, tablet, and desktop optimized
- **Dark/light mode**: Theme toggle with system preference
- **Keyboard shortcuts**: Power-user productivity

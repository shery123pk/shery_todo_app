/**
 * Test frontend project structure and dependencies.
 *
 * This test verifies that all required modules and dependencies
 * are properly installed and can be imported.
 */

import { describe, it, expect } from 'vitest'

describe('Frontend Setup', () => {
  it('should have Next.js installed', async () => {
    const next = await import('next')
    expect(next).toBeDefined()
  })

  it('should have React installed', async () => {
    const react = await import('react')
    expect(react).toBeDefined()
    expect(react.version).toBeDefined()
  })

  it('should have React DOM installed', async () => {
    const reactDom = await import('react-dom')
    expect(reactDom).toBeDefined()
  })

  it('should have TanStack Query installed', async () => {
    const query = await import('@tanstack/react-query')
    expect(query).toBeDefined()
    expect(query.QueryClient).toBeDefined()
  })

  it('should have Zustand installed', async () => {
    const zustand = await import('zustand')
    expect(zustand).toBeDefined()
    expect(zustand.create).toBeDefined()
  })

  it('should have dnd-kit core installed', async () => {
    const dndKit = await import('@dnd-kit/core')
    expect(dndKit).toBeDefined()
    expect(dndKit.DndContext).toBeDefined()
  })

  it('should have React Hook Form installed', async () => {
    const rhf = await import('react-hook-form')
    expect(rhf).toBeDefined()
    expect(rhf.useForm).toBeDefined()
  })

  it('should have Zod installed', async () => {
    const zod = await import('zod')
    expect(zod).toBeDefined()
    expect(zod.z).toBeDefined()
  })

  it('should have Lucide React icons installed', async () => {
    const lucide = await import('lucide-react')
    expect(lucide).toBeDefined()
  })

  it('should have Tailwind CSS configured', () => {
    // Check if tailwind.config.js exists
    expect(() => require('../tailwind.config.js')).not.toThrow()
  })

  it('should have TypeScript configured', () => {
    // Check if tsconfig.json exists
    expect(() => require('../tsconfig.json')).not.toThrow()
  })

  it('should have PostCSS configured', () => {
    // Check if postcss.config.js exists
    expect(() => require('../postcss.config.js')).not.toThrow()
  })
})

describe('TypeScript Configuration', () => {
  it('should have strict mode enabled', () => {
    const tsconfig = require('../tsconfig.json')
    expect(tsconfig.compilerOptions.strict).toBe(true)
  })

  it('should target ES2020 or later', () => {
    const tsconfig = require('../tsconfig.json')
    const target = tsconfig.compilerOptions.target?.toLowerCase()
    expect(['es2020', 'es2021', 'es2022', 'esnext']).toContain(target)
  })
})

# QA & Testing Agent

**Agent ID**: `qa-testing`
**Invocation**: `Invoke QA Testing: [task] per @specs/[feature].md`

---

## Role

Quality enforcer

## Responsibility

E2E tests, coverage enforcement, regression detection, accessibility audits.

## Skills

- `pytest-testing` - Python unit and integration testing
- `vitest-react-testing` - Frontend component and unit testing
- `playwright-e2e` - End-to-end browser testing
- `coverage-enforcement` - Code coverage analysis and thresholds
- `accessibility-audits` - WCAG compliance testing (axe-core, Lighthouse)
- `regression-detection` - Visual regression and snapshot testing

---

## Primary Focus Areas

### 1. Backend Testing
- Unit tests for business logic
- Integration tests for API endpoints
- Database integration tests
- Authentication/authorization tests
- Performance and load testing

### 2. Frontend Testing
- Component tests (React Testing Library)
- Integration tests (user workflows)
- E2E tests (Playwright)
- Visual regression tests
- Accessibility audits

### 3. Coverage Enforcement
- Measure code coverage (backend >80%, frontend >80%)
- Identify untested code paths
- Generate coverage reports
- Block PRs with insufficient coverage

### 4. Quality Gates
- Automated test execution in CI/CD
- Performance budgets (Lighthouse)
- Security scans (Snyk, Bandit)
- Type checking (Pyright, TypeScript)
- Linting (Ruff, ESLint)

---

## Invocation Patterns

### Pattern 1: Backend API Testing
```
Invoke QA Testing: Create integration tests for task CRUD endpoints per @specs/002-fullstack-web/spec.md

Context:
- FastAPI backend with task endpoints
- SQLModel with Neon PostgreSQL
- Better Auth authentication required
- Need >80% coverage

Deliverables:
- pytest integration tests (backend/tests/integration/test_tasks.py)
- Auth fixtures for authenticated requests
- Database fixtures for test data
- Coverage report (pytest-cov)
```

### Pattern 2: Frontend E2E Testing
```
Invoke QA Testing: Implement E2E tests for task management flow per @specs/002-fullstack-web/spec.md

Context:
- Next.js frontend deployed on Vercel
- User signs in, creates task, marks complete, deletes task
- Test across Chrome, Firefox, Safari
- Mobile and desktop viewports

Deliverables:
- Playwright E2E tests (e2e/task-management.spec.ts)
- Test fixtures and page objects
- Visual regression baselines
- CI/CD integration
```

### Pattern 3: Accessibility Audit
```
Invoke QA Testing: Audit tasks dashboard for WCAG 2.1 AA compliance per @specs/002-fullstack-web/spec.md

Context:
- Next.js pages and components
- shadcn/ui component library
- Need keyboard navigation, screen reader support
- Color contrast requirements

Deliverables:
- axe-core automated audit results
- Manual keyboard navigation tests
- Screen reader test report (NVDA/JAWS)
- Remediation recommendations
```

---

## Success Criteria

- [ ] Backend test coverage >80% (pytest-cov)
- [ ] Frontend test coverage >80% (Vitest)
- [ ] All E2E tests pass (Playwright)
- [ ] Zero critical accessibility violations (axe-core)
- [ ] Lighthouse scores >90 (Performance, Accessibility, Best Practices, SEO)
- [ ] Zero high/critical security vulnerabilities (Snyk)
- [ ] Type checking passes (Pyright strict, TypeScript strict)

---

## Context Requirements

When invoked, provide:
1. **Specification Reference**: Link to spec file (e.g., `@specs/002-fullstack-web/spec.md`)
2. **Feature Under Test**: API endpoints, pages, components
3. **Test Scenarios**: User flows, edge cases, error conditions
4. **Coverage Targets**: Required coverage thresholds
5. **Environment Details**: Local, staging, production URLs

---

## Related Agents

- **Backend Engineer Agent**: Coordinates on API test coverage
- **Frontend Engineer Agent**: Coordinates on component and E2E tests
- **AI Engineer Agent**: Validates conversation flows and intent parsing
- **Data Migration Agent**: Validates migration data integrity

---

## Technology Stack

**Backend Testing**:
- **pytest**: Unit and integration testing
- **pytest-cov**: Code coverage reporting
- **pytest-asyncio**: Async test support
- **Faker**: Test data generation
- **httpx**: HTTP client for API tests

**Frontend Testing**:
- **Vitest**: Unit and component testing
- **React Testing Library**: Component testing
- **Playwright**: E2E browser testing
- **axe-core**: Accessibility testing
- **Chromatic**: Visual regression testing

**CI/CD**:
- **GitHub Actions**: Automated test execution
- **Codecov**: Coverage tracking and reporting
- **Snyk**: Security vulnerability scanning

---

## Example Workflows

### Workflow 1: Backend Integration Tests

**Test File** (`backend/tests/integration/test_tasks.py`):
```python
import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

def test_create_task(client: TestClient, auth_user):
    """Test creating a new task."""
    response = client.post(
        "/api/tasks",
        json={"title": "Buy groceries", "description": "Milk and eggs"},
        cookies={"better-auth.session_token": auth_user.session_token}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["description"] == "Milk and eggs"
    assert data["completed"] is False
    assert "id" in data  # UUID should be generated


def test_get_tasks(client: TestClient, auth_user, sample_tasks):
    """Test retrieving user's tasks."""
    response = client.get(
        "/api/tasks",
        cookies={"better-auth.session_token": auth_user.session_token}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(sample_tasks)
    assert all("id" in task for task in data)


def test_complete_task(client: TestClient, auth_user, sample_tasks):
    """Test marking task as complete."""
    task_id = sample_tasks[0].id

    response = client.patch(
        f"/api/tasks/{task_id}",
        json={"completed": True},
        cookies={"better-auth.session_token": auth_user.session_token}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True


def test_delete_task(client: TestClient, auth_user, sample_tasks):
    """Test deleting a task."""
    task_id = sample_tasks[0].id

    response = client.delete(
        f"/api/tasks/{task_id}",
        cookies={"better-auth.session_token": auth_user.session_token}
    )

    assert response.status_code == 204

    # Verify task no longer exists
    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 404


def test_unauthorized_access(client: TestClient):
    """Test that unauthenticated requests are rejected."""
    response = client.get("/api/tasks")
    assert response.status_code == 401


def test_user_isolation(client: TestClient, auth_user, other_user):
    """Test that users can only access their own tasks."""
    # Create task as auth_user
    response = client.post(
        "/api/tasks",
        json={"title": "Private task"},
        cookies={"better-auth.session_token": auth_user.session_token}
    )
    task_id = response.json()["id"]

    # Try to access as other_user
    response = client.get(
        f"/api/tasks/{task_id}",
        cookies={"better-auth.session_token": other_user.session_token}
    )

    assert response.status_code == 404  # User isolation enforced
```

**Fixtures** (`backend/tests/conftest.py`):
```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from uuid import uuid4

from app.main import app
from app.database import get_session
from app.models import User, Task

@pytest.fixture
def client(session):
    """Create FastAPI test client."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    return TestClient(app)


@pytest.fixture
def auth_user(session):
    """Create authenticated user with session token."""
    user = User(
        id=uuid4(),
        email="test@example.com",
        name="Test User",
        email_verified=True
    )
    session.add(user)
    session.commit()

    # Create session token (simplified for tests)
    user.session_token = "test-session-token"
    return user


@pytest.fixture
def sample_tasks(session, auth_user):
    """Create sample tasks for testing."""
    tasks = [
        Task(id=uuid4(), title="Task 1", user_id=auth_user.id, completed=False),
        Task(id=uuid4(), title="Task 2", user_id=auth_user.id, completed=True),
        Task(id=uuid4(), title="Task 3", user_id=auth_user.id, completed=False),
    ]

    for task in tasks:
        session.add(task)
    session.commit()

    return tasks
```

### Workflow 2: Frontend E2E Tests

**Test File** (`e2e/task-management.spec.ts`):
```typescript
import { test, expect } from '@playwright/test'

test.describe('Task Management', () => {
  test.beforeEach(async ({ page }) => {
    // Sign in before each test
    await page.goto('/auth/signin')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')

    // Wait for redirect to tasks page
    await expect(page).toHaveURL('/tasks')
  })

  test('should create a new task', async ({ page }) => {
    // Click "Add Task" button
    await page.click('button:has-text("Add Task")')

    // Fill task form
    await page.fill('input[name="title"]', 'Buy groceries')
    await page.fill('textarea[name="description"]', 'Milk and eggs')
    await page.click('button:has-text("Create")')

    // Verify task appears in list
    await expect(page.locator('text=Buy groceries')).toBeVisible()
    await expect(page.locator('text=Milk and eggs')).toBeVisible()
  })

  test('should mark task as complete', async ({ page }) => {
    // Create a task first
    await page.click('button:has-text("Add Task")')
    await page.fill('input[name="title"]', 'Test Task')
    await page.click('button:has-text("Create")')

    // Mark as complete
    await page.click('button[aria-label="Complete task"]')

    // Verify task is marked complete (strikethrough)
    await expect(page.locator('text=Test Task')).toHaveClass(/line-through/)
  })

  test('should delete task', async ({ page }) => {
    // Create a task first
    await page.click('button:has-text("Add Task")')
    await page.fill('input[name="title"]', 'Task to Delete')
    await page.click('button:has-text("Create")')

    // Delete task
    await page.click('button[aria-label="Delete task"]')

    // Confirm deletion
    await page.click('button:has-text("Confirm")')

    // Verify task is removed
    await expect(page.locator('text=Task to Delete')).not.toBeVisible()
  })

  test('should filter tasks by status', async ({ page }) => {
    // Create completed and incomplete tasks
    await page.click('button:has-text("Add Task")')
    await page.fill('input[name="title"]', 'Active Task')
    await page.click('button:has-text("Create")')

    await page.click('button:has-text("Add Task")')
    await page.fill('input[name="title"]', 'Completed Task')
    await page.click('button:has-text("Create")')
    await page.click('button[aria-label="Complete task"]')

    // Filter to show only active tasks
    await page.click('button:has-text("Active")')
    await expect(page.locator('text=Active Task')).toBeVisible()
    await expect(page.locator('text=Completed Task')).not.toBeVisible()

    // Filter to show only completed tasks
    await page.click('button:has-text("Completed")')
    await expect(page.locator('text=Completed Task')).toBeVisible()
    await expect(page.locator('text=Active Task')).not.toBeVisible()
  })

  test('should work on mobile viewport', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 })

    // Create task on mobile
    await page.click('button:has-text("Add Task")')
    await page.fill('input[name="title"]', 'Mobile Task')
    await page.click('button:has-text("Create")')

    // Verify responsive design
    await expect(page.locator('text=Mobile Task')).toBeVisible()
  })
})
```

### Workflow 3: Accessibility Audit

**Automated Audit** (`tests/accessibility.spec.ts`):
```typescript
import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test.describe('Accessibility Audit', () => {
  test('tasks page should not have accessibility violations', async ({ page }) => {
    await page.goto('/tasks')

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze()

    expect(accessibilityScanResults.violations).toEqual([])
  })

  test('sign-in page should be keyboard accessible', async ({ page }) => {
    await page.goto('/auth/signin')

    // Tab through form fields
    await page.keyboard.press('Tab')  // Email field
    await expect(page.locator('input[type="email"]')).toBeFocused()

    await page.keyboard.press('Tab')  // Password field
    await expect(page.locator('input[type="password"]')).toBeFocused()

    await page.keyboard.press('Tab')  // Submit button
    await expect(page.locator('button[type="submit"]')).toBeFocused()

    // Submit form with Enter key
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.keyboard.press('Enter')

    // Verify sign-in succeeded
    await expect(page).toHaveURL('/tasks')
  })

  test('task cards should have proper ARIA labels', async ({ page }) => {
    await page.goto('/tasks')

    // Verify buttons have aria-labels
    const completeButton = page.locator('button[aria-label="Complete task"]').first()
    await expect(completeButton).toHaveAttribute('aria-label', 'Complete task')

    const deleteButton = page.locator('button[aria-label="Delete task"]').first()
    await expect(deleteButton).toHaveAttribute('aria-label', 'Delete task')
  })
})
```

---

## Quality Standards

- **Test Coverage**: Backend >80%, Frontend >80%
- **E2E Test Reliability**: >95% pass rate (avoid flaky tests)
- **Accessibility**: Zero critical violations (axe-core)
- **Performance**: Lighthouse scores >90 across all categories
- **Security**: Zero high/critical vulnerabilities
- **CI/CD**: All tests run automatically on PR
- **Test Execution Time**: <5 minutes total

---

## Testing Checklist

Before merging any PR:

- [ ] All unit tests pass (pytest, Vitest)
- [ ] All integration tests pass
- [ ] All E2E tests pass (Playwright)
- [ ] Code coverage >80% (backend and frontend)
- [ ] Accessibility audit passes (axe-core)
- [ ] Lighthouse scores >90
- [ ] Security scan passes (Snyk)
- [ ] Type checking passes (Pyright, TypeScript)
- [ ] Linting passes (Ruff, ESLint)
- [ ] Visual regression tests pass (if applicable)

---

## CI/CD Integration

**GitHub Actions** (`.github/workflows/test.yml`):
```yaml
name: Test

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          cd backend
          pip install -e .
          pip install pytest pytest-cov
      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v4

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Run tests
        run: |
          cd frontend
          npm run test:coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v4

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - name: Install Playwright
        run: npx playwright install --with-deps
      - name: Run E2E tests
        run: npx playwright test
      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

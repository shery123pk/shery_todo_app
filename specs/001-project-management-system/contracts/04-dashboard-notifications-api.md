# API Contract: Dashboard, Notifications, Search

**Feature**: 001-project-management-system
**Resource Groups**: /api/dashboard, /api/notifications, /api/search
**Date**: 2025-12-27

---

## Dashboard

### GET /api/organizations/{orgSlug}/dashboard

**Purpose**: Organization dashboard statistics

**Authentication**: Required (org member)

**Response** (200 OK):
```json
{
  "organization": {
    "id": "org-uuid",
    "slug": "acme-corp",
    "name": "Acme Corporation",
    "member_count": 15,
    "project_count": 5
  },
  "stats": {
    "total_tasks": 250,
    "completed_this_week": 42,
    "overdue_tasks": 8,
    "active_tasks": 158
  },
  "recent_activity": [
    {
      "id": "activity-uuid",
      "type": "task_created",
      "user": {
        "full_name": "Alice Johnson",
        "avatar_url": "https://example.com/avatar.jpg"
      },
      "project": {
        "key": "WEB",
        "name": "Website Redesign"
      },
      "task": {
        "display_id": "WEB-42",
        "title": "Implement dark mode"
      },
      "created_at": "2025-12-27T10:00:00Z"
    }
  ],
  "projects": [
    {
      "id": "project-uuid",
      "key": "WEB",
      "name": "Website Redesign",
      "task_count": 42,
      "completed_count": 15
    }
  ]
}
```

---

### GET /api/projects/{projectKey}/dashboard

**Purpose**: Project dashboard statistics

**Authentication**: Required (project member)

**Response** (200 OK):
```json
{
  "project": {
    "id": "project-uuid",
    "key": "WEB",
    "name": "Website Redesign",
    "member_count": 5
  },
  "stats": {
    "total_tasks": 42,
    "by_status": {
      "Todo": 15,
      "In Progress": 12,
      "Review": 5,
      "Done": 10
    },
    "completed_this_week": 8,
    "completed_this_month": 25,
    "overdue_tasks": 3,
    "tasks_assigned_to_me": 7
  },
  "recent_activity": [
    {
      "id": "activity-uuid",
      "user": {...},
      "task": {
        "display_id": "WEB-42",
        "title": "Implement dark mode"
      },
      "action": "moved",
      "from_column": "In Progress",
      "to_column": "Review",
      "created_at": "2025-12-27T10:00:00Z"
    }
  ],
  "upcoming_deadlines": [
    {
      "task_id": "task-uuid",
      "display_id": "WEB-38",
      "title": "Deploy homepage",
      "assignee": {...},
      "due_date": "2025-12-28",
      "days_until_due": 1
    }
  ]
}
```

---

### GET /api/users/me/tasks

**Purpose**: My Tasks view (tasks assigned to current user across all projects)

**Authentication**: Required

**Query Parameters**:
- `status`: string (filter by column name)
- `priority`: string (filter by priority)
- `project_key`: string (filter by project)
- `due_before`: date (tasks due before date)
- `group_by`: "project" | "priority" | "due_date" (default: "project")
- `sort_by`: "due_date" | "priority" | "created_at" | "updated_at" (default: "due_date")
- `limit`: int (default: 100)
- `offset`: int (default: 0)

**Response** (200 OK):
```json
{
  "tasks_by_project": {
    "WEB - Website Redesign": [
      {
        "id": "task-uuid",
        "display_id": "WEB-42",
        "title": "Implement dark mode",
        "priority": "high",
        "due_date": "2025-12-30",
        "column": {
          "name": "In Progress"
        },
        "project": {
          "key": "WEB",
          "name": "Website Redesign"
        }
      }
    ],
    "MOBILE - Mobile App": [...]
  },
  "total": 15,
  "overdue_count": 2
}
```

---

## Notifications

### GET /api/notifications

**Purpose**: List user's notifications

**Authentication**: Required

**Query Parameters**:
- `read`: boolean (filter by read status)
- `type`: string (filter by notification type)
- `limit`: int (default: 50, max: 100)
- `offset`: int (default: 0)

**Response** (200 OK):
```json
{
  "notifications": [
    {
      "id": "notif-uuid",
      "type": "task_assigned",
      "title": "Task assigned to you",
      "message": "Alice assigned you to WEB-42: Implement dark mode",
      "reference": {
        "type": "task",
        "id": "task-uuid",
        "display_id": "WEB-42",
        "project_key": "WEB"
      },
      "read": false,
      "created_at": "2025-12-27T10:00:00Z"
    },
    {
      "id": "notif-uuid-2",
      "type": "mentioned",
      "title": "You were mentioned",
      "message": "@you Can you review this design? - Alice on WEB-38",
      "reference": {
        "type": "comment",
        "id": "comment-uuid",
        "task_id": "task-uuid",
        "task_display_id": "WEB-38"
      },
      "read": true,
      "created_at": "2025-12-27T09:00:00Z"
    }
  ],
  "unread_count": 5,
  "total": 42
}
```

---

### PUT /api/notifications/{notificationId}/read

**Purpose**: Mark notification as read

**Authentication**: Required

**Response** (200 OK):
```json
{
  "id": "notif-uuid",
  "read": true
}
```

---

### PUT /api/notifications/read-all

**Purpose**: Mark all notifications as read

**Authentication**: Required

**Response** (200 OK):
```json
{
  "message": "All notifications marked as read",
  "count": 15
}
```

---

## Search

### GET /api/organizations/{orgSlug}/search

**Purpose**: Global search across organization's projects and tasks

**Authentication**: Required (org member)

**Query Parameters**:
- `q`: string (search query, required)
- `project_key`: string (filter by project)
- `assignee_id`: UUID (filter by assignee)
- `priority`: string (filter by priority)
- `labels`: string (comma-separated labels)
- `due_before`: date (tasks due before date)
- `created_after`: date (tasks created after date)
- `limit`: int (default: 50, max: 200)
- `offset`: int (default: 0)

**Response** (200 OK):
```json
{
  "results": {
    "tasks": [
      {
        "id": "task-uuid",
        "display_id": "WEB-42",
        "title": "Implement dark mode",
        "description_snippet": "...users can toggle between light and **dark** themes...",
        "project": {
          "key": "WEB",
          "name": "Website Redesign"
        },
        "priority": "high",
        "assignee": {...},
        "relevance_score": 0.95
      }
    ],
    "projects": [
      {
        "id": "project-uuid",
        "key": "WEB",
        "name": "Website Redesign",
        "description_snippet": "Redesign company website with modern UI...",
        "task_count": 42,
        "relevance_score": 0.82
      }
    ]
  },
  "total_results": 15,
  "search_time_ms": 45
}
```

---

### GET /api/projects/{projectKey}/search

**Purpose**: Search within a specific project

**Authentication**: Required (project member)

**Query Parameters**: Same as organization search

**Response** (200 OK): Same format, but only returns tasks from this project

---

## Rate Limiting

All endpoints enforce rate limiting:

**General Limits**:
- 100 requests per minute per IP (unauthenticated)
- 500 requests per minute per authenticated user

**Sensitive Endpoints** (stricter limits):
- `/api/auth/signin`: 5 attempts per 15 minutes per IP
- `/api/auth/signup`: 3 attempts per hour per IP
- `/api/auth/forgot-password`: 3 attempts per hour per email
- `/api/organizations/{slug}/members/invite`: 10 invites per hour per org

**Headers**:
```
X-RateLimit-Limit: 500
X-RateLimit-Remaining: 495
X-RateLimit-Reset: 1640612400
```

**Error Response** (429 Too Many Requests):
```json
{
  "detail": "Rate limit exceeded. Try again in 45 seconds.",
  "retry_after": 45
}
```

---

## Error Responses (Global)

All endpoints use consistent error response format:

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "Title must be between 1 and 200 characters",
      "type": "value_error.str.max_length"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "An unexpected error occurred. Please try again later."
}
```

---

## Pagination

List endpoints support pagination with these query parameters:
- `limit`: int (default varies, typically 50-100)
- `offset`: int (default: 0)

Response includes pagination metadata:
```json
{
  "items": [...],
  "total": 250,
  "limit": 50,
  "offset": 0,
  "has_more": true
}
```

---

## Filtering & Sorting

List endpoints support common filters:
- `search`: Full-text search
- `sort_by`: Field to sort by
- `order`: "asc" | "desc" (default: "desc" for dates, "asc" for names)

Example: `/api/projects/WEB/tasks?search=homepage&sort_by=due_date&order=asc`

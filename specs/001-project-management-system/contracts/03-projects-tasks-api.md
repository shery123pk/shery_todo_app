# API Contract: Projects, Boards, Tasks

**Feature**: 001-project-management-system
**Resource Groups**: /api/projects, /api/boards, /api/tasks
**Date**: 2025-12-27

---

## Projects

### POST /api/organizations/{orgSlug}/projects

**Purpose**: Create project in organization

**Authentication**: Required (org admin)

**Request**:
```json
{
  "key": "WEB",
  "name": "Website Redesign",
  "description": "Redesign company website",
  "icon": "🌐",
  "visibility": "private"
}
```

**Response** (201 Created):
```json
{
  "id": "project-uuid",
  "organization_id": "org-uuid",
  "key": "WEB",
  "name": "Website Redesign",
  "description": "Redesign company website",
  "icon": "🌐",
  "visibility": "private",
  "created_by": "user-uuid",
  "board": {
    "id": "board-uuid",
    "name": "Main Board",
    "columns": [
      {"id": "col-1", "name": "Todo", "position": 0.0},
      {"id": "col-2", "name": "In Progress", "position": 1000.0},
      {"id": "col-3", "name": "Done", "position": 2000.0}
    ]
  },
  "created_at": "2025-12-27T10:00:00Z"
}
```

---

### GET /api/organizations/{orgSlug}/projects

**Purpose**: List organization projects

**Authentication**: Required (org member)

**Query Parameters**:
- `archived`: boolean (default: false)

**Response** (200 OK):
```json
{
  "projects": [
    {
      "id": "project-uuid",
      "key": "WEB",
      "name": "Website Redesign",
      "icon": "🌐",
      "member_count": 5,
      "task_count": 42,
      "created_at": "2025-12-27T10:00:00Z"
    }
  ]
}
```

---

### GET /api/projects/{projectKey}

**Purpose**: Get project details

**Authentication**: Required (project member)

**Response** (200 OK):
```json
{
  "id": "project-uuid",
  "organization_id": "org-uuid",
  "key": "WEB",
  "name": "Website Redesign",
  "description": "Redesign company website",
  "icon": "🌐",
  "visibility": "private",
  "members": [
    {
      "user_id": "user-uuid",
      "full_name": "Alice Johnson",
      "role": "admin"
    }
  ],
  "stats": {
    "total_tasks": 42,
    "completed_tasks": 15,
    "overdue_tasks": 3
  }
}
```

---

### PUT /api/projects/{projectKey}

**Purpose**: Update project (admin only)

**Authentication**: Required (project admin)

**Request**: Partial update (all fields optional)
```json
{
  "name": "Website Redesign 2.0",
  "description": "Updated description"
}
```

**Response** (200 OK): Updated project

---

### POST /api/projects/{projectKey}/archive

**Purpose**: Archive project (admin only)

**Authentication**: Required (project admin)

**Response** (200 OK):
```json
{
  "message": "Project archived",
  "archived": true
}
```

---

### DELETE /api/projects/{projectKey}

**Purpose**: Delete project permanently (admin only)

**Authentication**: Required (project admin)

**Response** (204 No Content)

**Note**: CASCADE deletes all boards, tasks, comments, attachments

---

### GET /api/projects/{projectKey}/members

**Purpose**: List project members

**Authentication**: Required (project member)

**Response** (200 OK):
```json
{
  "members": [
    {
      "user_id": "user-uuid",
      "email": "alice@example.com",
      "full_name": "Alice Johnson",
      "avatar_url": "https://example.com/avatar.jpg",
      "role": "admin",
      "added_at": "2025-12-27T10:00:00Z"
    }
  ]
}
```

---

### POST /api/projects/{projectKey}/members

**Purpose**: Add member to project

**Authentication**: Required (project admin)

**Request**:
```json
{
  "user_id": "user-uuid",
  "role": "member"
}
```

**Response** (201 Created): Created membership

**Note**: User must be organization member

---

## Boards

### GET /api/projects/{projectKey}/boards

**Purpose**: List project boards

**Authentication**: Required (project member)

**Response** (200 OK):
```json
{
  "boards": [
    {
      "id": "board-uuid",
      "name": "Main Board",
      "task_count": 42
    }
  ]
}
```

**Note**: MVP supports one board per project (auto-created)

---

### GET /api/boards/{boardId}

**Purpose**: Get board with columns and tasks

**Authentication**: Required (project member)

**Query Parameters**:
- `include_tasks`: boolean (default: true)

**Response** (200 OK):
```json
{
  "id": "board-uuid",
  "project_id": "project-uuid",
  "name": "Main Board",
  "columns": [
    {
      "id": "col-uuid-1",
      "name": "Todo",
      "color": "#6366F1",
      "position": 0.0,
      "wip_limit": null,
      "tasks": [
        {
          "id": "task-uuid-1",
          "task_number": 1,
          "title": "Redesign homepage",
          "task_type": "story",
          "priority": "high",
          "assignee": {
            "id": "user-uuid",
            "full_name": "Alice Johnson",
            "avatar_url": "https://example.com/avatar.jpg"
          },
          "due_date": "2025-12-30",
          "position": 1000.0
        }
      ]
    },
    {
      "id": "col-uuid-2",
      "name": "In Progress",
      "color": "#F59E0B",
      "position": 1000.0,
      "tasks": []
    },
    {
      "id": "col-uuid-3",
      "name": "Done",
      "color": "#10B981",
      "position": 2000.0,
      "tasks": []
    }
  ]
}
```

---

### POST /api/boards/{boardId}/columns

**Purpose**: Create new column (admin only)

**Authentication**: Required (project admin)

**Request**:
```json
{
  "name": "Code Review",
  "color": "#8B5CF6",
  "position": 1500.0,
  "wip_limit": 5
}
```

**Response** (201 Created): Created column

---

### PUT /api/columns/{columnId}

**Purpose**: Update column (admin only)

**Authentication**: Required (project admin)

**Request**: Partial update
```json
{
  "name": "Review",
  "wip_limit": 3
}
```

**Response** (200 OK): Updated column

---

### DELETE /api/columns/{columnId}

**Purpose**: Delete column (admin only)

**Authentication**: Required (project admin)

**Query Parameters**:
- `move_tasks_to`: column_id (required if column has tasks)

**Response** (204 No Content)

**Note**: Moves all tasks to specified column before deletion

---

## Tasks

### POST /api/projects/{projectKey}/tasks

**Purpose**: Create task in project

**Authentication**: Required (project member)

**Request**:
```json
{
  "title": "Redesign homepage",
  "description": "# Homepage Redesign\n\nModern, responsive design",
  "task_type": "story",
  "priority": "high",
  "assignee_id": "user-uuid",
  "due_date": "2025-12-30",
  "story_points": 5,
  "labels": ["design", "urgent"],
  "column_id": "col-uuid-1"
}
```

**Response** (201 Created):
```json
{
  "id": "task-uuid",
  "project_id": "project-uuid",
  "board_id": "board-uuid",
  "column_id": "col-uuid-1",
  "task_number": 1,
  "display_id": "WEB-1",
  "title": "Redesign homepage",
  "description": "# Homepage Redesign\n\nModern, responsive design",
  "task_type": "story",
  "priority": "high",
  "assignee": {
    "id": "user-uuid",
    "full_name": "Alice Johnson",
    "avatar_url": "https://example.com/avatar.jpg"
  },
  "reporter": {
    "id": "reporter-uuid",
    "full_name": "Bob Smith"
  },
  "due_date": "2025-12-30",
  "story_points": 5,
  "labels": ["design", "urgent"],
  "position": 1000.0,
  "created_at": "2025-12-27T10:00:00Z"
}
```

---

### GET /api/projects/{projectKey}/tasks

**Purpose**: List project tasks with filters

**Authentication**: Required (project member)

**Query Parameters**:
- `assignee_id`: UUID (filter by assignee)
- `priority`: string (filter by priority)
- `status`: string (filter by column name)
- `labels`: string (comma-separated labels)
- `due_before`: date (tasks due before date)
- `search`: string (search title/description)
- `archived`: boolean (default: false)
- `limit`: int (default: 100, max: 500)
- `offset`: int (default: 0)

**Response** (200 OK):
```json
{
  "tasks": [
    {
      "id": "task-uuid",
      "display_id": "WEB-1",
      "title": "Redesign homepage",
      "task_type": "story",
      "priority": "high",
      "assignee": {...},
      "due_date": "2025-12-30",
      "column": {
        "id": "col-uuid",
        "name": "Todo"
      }
    }
  ],
  "total": 42,
  "limit": 100,
  "offset": 0
}
```

---

### GET /api/tasks/{taskId}

**Purpose**: Get task details

**Authentication**: Required (project member)

**Response** (200 OK):
```json
{
  "id": "task-uuid",
  "display_id": "WEB-1",
  "project": {
    "id": "project-uuid",
    "key": "WEB",
    "name": "Website Redesign"
  },
  "title": "Redesign homepage",
  "description": "# Homepage Redesign\n\nModern, responsive design",
  "task_type": "story",
  "priority": "high",
  "assignee": {...},
  "reporter": {...},
  "due_date": "2025-12-30",
  "story_points": 5,
  "labels": ["design", "urgent"],
  "column": {
    "id": "col-uuid",
    "name": "Todo"
  },
  "comment_count": 5,
  "attachment_count": 2,
  "created_at": "2025-12-27T10:00:00Z",
  "updated_at": "2025-12-27T11:00:00Z"
}
```

---

### PUT /api/tasks/{taskId}

**Purpose**: Update task

**Authentication**: Required (project member)

**Request**: Partial update (all fields optional)
```json
{
  "title": "Redesign homepage and footer",
  "priority": "critical",
  "assignee_id": "new-user-uuid",
  "due_date": "2025-12-28"
}
```

**Response** (200 OK): Updated task

**Note**: Creates ActivityLog entry for each changed field

---

### PUT /api/tasks/{taskId}/move

**Purpose**: Move task to different column/position

**Authentication**: Required (project member)

**Request**:
```json
{
  "column_id": "col-uuid-2",
  "position": 1500.0
}
```

**Response** (200 OK): Updated task

**Note**: Creates ActivityLog entry with "moved" action

---

### POST /api/tasks/{taskId}/duplicate

**Purpose**: Duplicate task (copy all fields except comments)

**Authentication**: Required (project member)

**Response** (201 Created): New task with incremented task_number

---

### POST /api/tasks/{taskId}/archive

**Purpose**: Archive task (soft delete)

**Authentication**: Required (project member)

**Response** (200 OK):
```json
{
  "message": "Task archived",
  "archived": true
}
```

---

### DELETE /api/tasks/{taskId}

**Purpose**: Delete task permanently (admin only)

**Authentication**: Required (project admin)

**Response** (204 No Content)

**Note**: CASCADE deletes all comments, attachments, activity logs

---

### GET /api/tasks/{taskId}/comments

**Purpose**: List task comments

**Authentication**: Required (project member)

**Query Parameters**:
- `sort`: "asc" | "desc" (default: "asc")

**Response** (200 OK):
```json
{
  "comments": [
    {
      "id": "comment-uuid",
      "user": {
        "id": "user-uuid",
        "full_name": "Alice Johnson",
        "avatar_url": "https://example.com/avatar.jpg"
      },
      "content": "@bob Can you review this design?",
      "edited": false,
      "created_at": "2025-12-27T10:00:00Z"
    }
  ]
}
```

---

### POST /api/tasks/{taskId}/comments

**Purpose**: Add comment to task

**Authentication**: Required (project member)

**Request**:
```json
{
  "content": "@bob Can you review this design?"
}
```

**Response** (201 Created): Created comment

**Note**: Triggers notification for @mentioned users

---

### PUT /api/comments/{commentId}

**Purpose**: Edit comment (author only, within 5 minutes)

**Authentication**: Required (comment author)

**Request**:
```json
{
  "content": "@bob Please review this design when you can"
}
```

**Response** (200 OK): Updated comment with `edited: true`

**Error**: 403 Forbidden if > 5 minutes since creation

---

### DELETE /api/comments/{commentId}

**Purpose**: Delete comment (author or project admin)

**Authentication**: Required (author or admin)

**Response** (204 No Content)

---

### GET /api/tasks/{taskId}/activity

**Purpose**: Get task activity log

**Authentication**: Required (project member)

**Response** (200 OK):
```json
{
  "activities": [
    {
      "id": "activity-uuid",
      "user": {
        "id": "user-uuid",
        "full_name": "Alice Johnson"
      },
      "action": "updated",
      "field_name": "priority",
      "old_value": "medium",
      "new_value": "high",
      "created_at": "2025-12-27T11:00:00Z"
    },
    {
      "id": "activity-uuid-2",
      "user": {...},
      "action": "created",
      "created_at": "2025-12-27T10:00:00Z"
    }
  ]
}
```

---

## File Attachments

### POST /api/tasks/{taskId}/attachments

**Purpose**: Upload file to task

**Authentication**: Required (project member)

**Request**: multipart/form-data
- `file`: binary file (max 10MB)

**Response** (201 Created):
```json
{
  "id": "attachment-uuid",
  "task_id": "task-uuid",
  "filename": "mockup.png",
  "file_size": 2048576,
  "mime_type": "image/png",
  "created_at": "2025-12-27T10:00:00Z"
}
```

**Errors**:
- 413 Payload Too Large: File > 10MB
- 400 Bad Request: Invalid file type
- 400 Bad Request: Task has 20 attachments already

---

### GET /api/tasks/{taskId}/attachments

**Purpose**: List task attachments

**Authentication**: Required (project member)

**Response** (200 OK):
```json
{
  "attachments": [
    {
      "id": "attachment-uuid",
      "filename": "mockup.png",
      "file_size": 2048576,
      "mime_type": "image/png",
      "user": {
        "id": "user-uuid",
        "full_name": "Alice Johnson"
      },
      "created_at": "2025-12-27T10:00:00Z"
    }
  ]
}
```

---

### GET /api/attachments/{attachmentId}/download

**Purpose**: Download attachment

**Authentication**: Required (project member)

**Response** (200 OK): Binary file with headers:
- `Content-Type`: {mime_type}
- `Content-Disposition`: attachment; filename="{filename}"

---

### DELETE /api/attachments/{attachmentId}

**Purpose**: Delete attachment (uploader or admin)

**Authentication**: Required (uploader or admin)

**Response** (204 No Content)

**Note**: Deletes file from storage

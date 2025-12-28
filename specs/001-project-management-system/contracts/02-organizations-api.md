# API Contract: Organizations & Members

**Feature**: 001-project-management-system
**Resource Groups**: /api/organizations, /api/invitations
**Date**: 2025-12-27

---

## Organizations

### POST /api/organizations

**Purpose**: Create a new organization (workspace)

**Authentication**: Required

**Request**:
```json
{
  "slug": "acme-corp",
  "name": "Acme Corporation",
  "description": "Our company workspace"
}
```

**Response** (201 Created):
```json
{
  "id": "org-uuid",
  "slug": "acme-corp",
  "name": "Acme Corporation",
  "description": "Our company workspace",
  "owner_id": "user-uuid",
  "created_at": "2025-12-27T10:00:00Z"
}
```

---

### GET /api/organizations

**Purpose**: List user's organizations

**Authentication**: Required

**Response** (200 OK):
```json
{
  "organizations": [
    {
      "id": "org-uuid",
      "slug": "acme-corp",
      "name": "Acme Corporation",
      "role": "owner",
      "member_count": 15,
      "project_count": 5
    }
  ]
}
```

---

### GET /api/organizations/{slug}

**Purpose**: Get organization details

**Authentication**: Required (must be member)

**Response** (200 OK):
```json
{
  "id": "org-uuid",
  "slug": "acme-corp",
  "name": "Acme Corporation",
  "description": "Our company workspace",
  "logo_url": "https://example.com/logo.png",
  "owner_id": "user-uuid",
  "member_count": 15,
  "project_count": 5,
  "created_at": "2025-12-27T10:00:00Z"
}
```

---

### PUT /api/organizations/{slug}

**Purpose**: Update organization (admin/owner only)

**Authentication**: Required (admin/owner)

**Request**:
```json
{
  "name": "Acme Corp",
  "description": "Updated description",
  "logo_url": "https://example.com/new-logo.png"
}
```

**Response** (200 OK): Updated organization

---

### DELETE /api/organizations/{slug}

**Purpose**: Delete organization (owner only)

**Authentication**: Required (owner)

**Response** (204 No Content)

**Note**: CASCADE deletes all projects, boards, tasks, comments, attachments

---

### GET /api/organizations/{slug}/members

**Purpose**: List organization members

**Authentication**: Required (member)

**Response** (200 OK):
```json
{
  "members": [
    {
      "user_id": "user-uuid",
      "email": "alice@example.com",
      "full_name": "Alice Johnson",
      "role": "owner",
      "joined_at": "2025-12-27T10:00:00Z"
    }
  ]
}
```

---

### POST /api/organizations/{slug}/members/invite

**Purpose**: Invite member by email

**Authentication**: Required (admin/owner)

**Request**:
```json
{
  "email": "bob@example.com",
  "role": "member"
}
```

**Response** (201 Created):
```json
{
  "id": "invitation-uuid",
  "email": "bob@example.com",
  "role": "member",
  "token": "invite-token-uuid",
  "expires_at": "2026-01-03T10:00:00Z"
}
```

---

### DELETE /api/organizations/{slug}/members/{user_id}

**Purpose**: Remove member (admin/owner)

**Authentication**: Required (admin/owner)

**Response** (204 No Content)

**Note**: Cannot remove owner

---

### PUT /api/organizations/{slug}/members/{user_id}/role

**Purpose**: Change member role (owner only)

**Authentication**: Required (owner)

**Request**:
```json
{
  "role": "admin"
}
```

**Response** (200 OK): Updated member

---

## Invitations

### GET /api/invitations/{token}

**Purpose**: View invitation details

**Authentication**: None (token-based)

**Response** (200 OK):
```json
{
  "id": "invitation-uuid",
  "organization": {
    "slug": "acme-corp",
    "name": "Acme Corporation"
  },
  "email": "bob@example.com",
  "role": "member",
  "invited_by": "Alice Johnson",
  "expires_at": "2026-01-03T10:00:00Z"
}
```

---

### POST /api/invitations/{token}/accept

**Purpose**: Accept invitation

**Authentication**: Required OR creates account if doesn't exist

**Response** (200 OK):
```json
{
  "message": "Invitation accepted",
  "organization": {
    "slug": "acme-corp",
    "name": "Acme Corporation"
  }
}
```

---

### POST /api/invitations/{token}/decline

**Purpose**: Decline invitation

**Authentication**: None

**Response** (200 OK):
```json
{
  "message": "Invitation declined"
}
```

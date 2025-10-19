# API Documentation

## Authentication

All endpoints except `/auth/register` and `/auth/login` require authentication via JWT Bearer token.

### Register a New User

```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "full_name": "John Doe",
  "role": "client"  // Options: "admin", "agent", "client"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "John Doe",
  "role": "client",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Login

```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=username&password=password123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

## Users

### Get Current User

```http
GET /users/me
Authorization: Bearer <token>
```

### List All Users (Admin Only)

```http
GET /users/?skip=0&limit=100
Authorization: Bearer <token>
```

### Get User by ID (Admin Only)

```http
GET /users/{user_id}
Authorization: Bearer <token>
```

### Update User (Admin Only)

```http
PUT /users/{user_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "email": "newemail@example.com",
  "role": "agent",
  "is_active": true
}
```

### Delete User (Admin Only)

```http
DELETE /users/{user_id}
Authorization: Bearer <token>
```

## Tickets

### Create Ticket

```http
POST /tickets/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Issue with login",
  "description": "Cannot login to the system",
  "priority": "high",  // Options: "low", "medium", "high", "critical"
  "contract_id": 1  // Optional
}
```

### List Tickets

```http
GET /tickets/?status=open&priority=high
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 100)
- `status`: Filter by status
- `priority`: Filter by priority

### Get Ticket by ID

```http
GET /tickets/{ticket_id}
Authorization: Bearer <token>
```

### Update Ticket

```http
PUT /tickets/{ticket_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "in_progress",  // Options: "open", "in_progress", "pending", "resolved", "closed"
  "assignee_id": 2,
  "actual_hours": 3.5
}
```

### Delete Ticket (Agent/Admin Only)

```http
DELETE /tickets/{ticket_id}
Authorization: Bearer <token>
```

### Add Comment to Ticket

```http
POST /tickets/{ticket_id}/comments
Authorization: Bearer <token>
Content-Type: application/json

{
  "content": "Working on this issue",
  "is_internal": 0  // 0 = public, 1 = internal (agent/admin only)
}
```

### Get Ticket Comments

```http
GET /tickets/{ticket_id}/comments
Authorization: Bearer <token>
```

## Contracts

### Create Contract (Agent/Admin Only)

```http
POST /contracts/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Premium Support",
  "description": "24/7 premium support contract",
  "client_id": 3,
  "base_rate": 100.00,
  "hourly_rate": 50.00,
  "included_hours": 10.0,
  "overage_rate": 75.00,
  "response_time_hours": 2,
  "resolution_time_hours": 24,
  "start_date": "2024-01-01T00:00:00",
  "end_date": "2024-12-31T23:59:59"
}
```

### List Contracts

```http
GET /contracts/
Authorization: Bearer <token>
```

### Get Contract by ID

```http
GET /contracts/{contract_id}
Authorization: Bearer <token>
```

### Update Contract (Agent/Admin Only)

```http
PUT /contracts/{contract_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "hourly_rate": 60.00,
  "is_active": 1
}
```

### Delete Contract (Agent/Admin Only)

```http
DELETE /contracts/{contract_id}
Authorization: Bearer <token>
```

## Reports

### Generate PDF Report (Agent/Admin Only)

```http
GET /reports/tickets/pdf?status=open&priority=high
Authorization: Bearer <token>
```

**Response:** PDF file download

### Generate CSV Report (Agent/Admin Only)

```http
GET /reports/tickets/csv?status=open&priority=high
Authorization: Bearer <token>
```

**Response:** CSV file download

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Error message describing what went wrong"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Rate Limiting

Currently, there is no rate limiting implemented. For production use, consider adding rate limiting middleware.

## Pagination

List endpoints support pagination using `skip` and `limit` query parameters:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100, max: 100)

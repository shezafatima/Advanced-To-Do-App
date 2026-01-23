# Data Model for Phase 2 - Advanced Todo Features and Professional UI

## Entities

### AdvancedTask
Extends the existing Task entity with additional fields:
- **id**: UUID (primary key)
- **title**: String (required, max 500 chars)
- **description**: String (optional, max 1000 chars)
- **completed**: Boolean (default: false)
- **priority**: Enum(low, medium, high) (default: medium)
- **due_date**: DateTime (nullable)
- **recurrence_rule**: String (nullable, RFC 5545 RRULE format)
- **tags**: Array of Tag references
- **user_id**: UUID (foreign key to User)
- **created_at**: DateTime (auto-generated)
- **updated_at**: DateTime (auto-generated)

**Validation rules**:
- Priority must be one of the defined enum values
- Due date must be a valid future date if provided
- Recurrence rule must follow RFC 5545 format if provided

### Tag
Category entity for organizing tasks:
- **id**: UUID (primary key)
- **name**: String (required, unique, max 50 chars)
- **color**: String (required, hex color code)
- **created_at**: DateTime (auto-generated)

**Validation rules**:
- Name must be unique across all tags
- Color must be a valid hex color code
- Name must follow acceptable character rules

### UserProfile
User profile entity with personalization settings:
- **id**: UUID (primary key)
- **user_id**: UUID (foreign key to User, unique)
- **display_name**: String (required, max 100 chars)
- **preferred_language**: String (default: "en", options: "en", "ur")
- **theme_preference**: String (nullable, future extensibility)
- **notification_preferences**: JSON (default: {"toast_notifications": true})
- **avatar**: Bytes (nullable, max 2MB, validated format)
- **created_at**: DateTime (auto-generated)
- **updated_at**: DateTime (auto-generated)

**Validation rules**:
- User_id must reference an existing User
- Preferred language must be one of supported options
- Avatar must be in allowed format (JPEG, PNG, GIF) and under size limit
- Display name must not be empty

### TaskShare
Entity representing task collaboration relationships:
- **id**: UUID (primary key)
- **task_id**: UUID (foreign key to AdvancedTask)
- **user_id**: UUID (foreign key to User)
- **role**: Enum(owner, editor, viewer) (default: viewer)
- **shared_at**: DateTime (auto-generated)
- **permissions**: JSON (computed from role)

**Validation rules**:
- Task_id must reference an existing AdvancedTask owned by the sharing user
- User_id must reference an existing User (but not the task owner)
- Role must be one of the defined enum values
- Only one relationship per task-user pair

### Notification
In-app notification entity for tracking user alerts:
- **id**: UUID (primary key)
- **user_id**: UUID (foreign key to User)
- **type**: Enum(success, error, warning, info) (required)
- **title**: String (required, max 100 chars)
- **message**: String (required, max 500 chars)
- **read**: Boolean (default: false)
- **created_at**: DateTime (auto-generated)

**Validation rules**:
- Type must be one of the defined enum values
- Title and message must not be empty
- Created timestamp cannot be in the future

## Relationships

### AdvancedTask ↔ User
- One-to-many (User creates many AdvancedTasks)
- Cascade delete on User removal (deletes user's tasks)

### AdvancedTask ↔ Tag
- Many-to-many through an implicit junction
- Tags can be shared across multiple tasks

### AdvancedTask ↔ TaskShare
- One-to-many (AdvancedTask can be shared with multiple users)
- Cascade delete on AdvancedTask removal (removes shares)

### User ↔ TaskShare
- One-to-many (User can be collaborator on multiple tasks)
- Cascade delete on User removal (removes user's collaborations)

### User ↔ UserProfile
- One-to-one (User has one profile)
- Cascade delete on User removal (removes profile)

## State Transitions

### Task Completion State
- `incomplete` → `completed` (via user action)
- `completed` → `incomplete` (via user action)

### Task Share Role
- `viewer` → `editor` (via owner action)
- `editor` → `owner` (via current owner action)
- `editor` → `viewer` (via owner action)
- `owner` → `editor` (via owner action, creates new owner)

### Notification Read Status
- `unread` → `read` (via user action)
- No reverse transition (notifications remain read once read)
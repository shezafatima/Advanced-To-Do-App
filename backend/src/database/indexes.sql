-- Database Indexing Strategy for Todo Application

-- Indexes for Users table
-- Primary key index is automatically created for id field
-- Index on email field for fast lookups during authentication
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Index on created_at for time-based queries
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

-- Index on is_active for filtering active/inactive users
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);

-- Index on updated_at for tracking recent changes
CREATE INDEX IF NOT EXISTS idx_users_updated_at ON users(updated_at);


-- Indexes for Todos table
-- Primary key index is automatically created for id field
-- Index on user_id for efficient retrieval of todos per user
CREATE INDEX IF NOT EXISTS idx_todos_user_id ON todos(user_id);

-- Index on completed for filtering completed/incomplete todos
CREATE INDEX IF NOT EXISTS idx_todos_completed ON todos(completed);

-- Index on created_at for chronological ordering and time-based queries
CREATE INDEX IF NOT EXISTS idx_todos_created_at ON todos(created_at);

-- Index on updated_at for tracking recent changes
CREATE INDEX IF NOT EXISTS idx_todos_updated_at ON todos(updated_at);

-- Composite index for common query pattern: user_id and completed status
CREATE INDEX IF NOT EXISTS idx_todos_user_id_completed ON todos(user_id, completed);

-- Index on title for text searches (if needed)
-- Only create this if you anticipate searching within titles
-- CREATE INDEX IF NOT EXISTS idx_todos_title ON todos USING gin(to_tsvector('english', title));

-- Index on description for text searches (if needed)
-- Only create this if you anticipate searching within descriptions
-- CREATE INDEX IF NOT EXISTS idx_todos_description ON todos USING gin(to_tsvector('english', description));


-- Additional indexes that might be useful based on query patterns
-- Index for retrieving todos by user and completion status
CREATE INDEX IF NOT EXISTS idx_todos_user_completed_created ON todos(user_id, completed, created_at DESC);

-- Index for retrieving recently created todos across all users
CREATE INDEX IF NOT EXISTS idx_todos_created_user ON todos(created_at DESC, user_id);

-- Partial indexes for better performance on common filters
-- Only index completed todos if there's a specific use case for querying them
CREATE INDEX IF NOT EXISTS idx_todos_completed_only ON todos(created_at) WHERE completed = true;
CREATE INDEX IF NOT EXISTS idx_todos_pending_only ON todos(created_at) WHERE completed = false;


-- Recommendations for index maintenance
-- Regularly analyze the database to update statistics
-- ANALYZE;

-- To check index usage, run:
-- SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
-- FROM pg_stat_user_indexes
-- ORDER BY idx_scan ASC;

-- To check for unused indexes:
-- SELECT schemaname, tablename, indexname, idx_scan
-- FROM pg_stat_user_indexes
-- WHERE idx_scan < 100  -- Threshold can be adjusted
-- ORDER BY idx_scan ASC;
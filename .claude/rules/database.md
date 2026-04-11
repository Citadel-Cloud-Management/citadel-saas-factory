# Database Rules
- All schema changes via migrations (Alembic)
- Indexes on foreign keys and frequently queried columns
- Row-level security for multi-tenant data isolation
- No raw SQL in application code — use ORM/query builder
- Parameterized queries only
- Soft deletes where business requires audit trail

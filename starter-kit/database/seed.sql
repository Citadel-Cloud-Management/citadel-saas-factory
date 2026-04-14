INSERT INTO users (email, full_name)
VALUES ('admin@example.com', 'Admin User')
ON CONFLICT (email) DO NOTHING;

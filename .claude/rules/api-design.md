# API Design Rules
- RESTful conventions: nouns for resources, HTTP verbs for actions
- Consistent response envelope: { data, error, meta }
- API versioning via URL prefix: /api/v1/
- Pagination on all list endpoints (cursor or offset)
- OpenAPI spec for all endpoints
- Rate limiting headers in responses

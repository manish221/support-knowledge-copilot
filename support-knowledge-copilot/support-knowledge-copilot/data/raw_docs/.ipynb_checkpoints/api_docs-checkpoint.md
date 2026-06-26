---
source_name: API Documentation
document_type: api_doc
last_updated: 2026-05-21
access_level: public
product: SupportPortal API
version: v2.1
---
# SupportPortal API Documentation

## Authentication
All API requests require a Bearer token in the Authorization header. Tokens expire after 60 minutes. Refresh tokens should be stored securely and rotated every 90 days.

## Rate limits
The default API rate limit is 600 requests per minute per tenant. When the limit is exceeded, the API returns HTTP 429 with error code ERR-429.

## Pagination
List endpoints support cursor-based pagination using the `next_cursor` field. Clients should continue requesting pages until `next_cursor` is null.

## Webhooks
Webhook endpoints must respond within 5 seconds. Failed webhook deliveries are retried up to 6 times with exponential backoff.

---
source_name: Troubleshooting Guide
document_type: troubleshooting
last_updated: 2026-04-28
access_level: public
product: SupportPortal
version: v2.1
---
# Troubleshooting Guide

## ERR-429 Too Many Requests
ERR-429 means the client exceeded the API rate limit. Wait at least 60 seconds before retrying. For automated integrations, use exponential backoff and avoid retry storms.

## ERR-401 Unauthorized
ERR-401 means the request did not include a valid access token. Confirm that the token has not expired and that the Authorization header uses the Bearer scheme.

## Sync failed after password rotation
If a sync job fails after password rotation, update the service credential in the integration settings and run a manual test connection.

## Upload stuck in processing
If an upload remains in processing for more than 15 minutes, check whether the file exceeds 500 MB or uses an unsupported format.

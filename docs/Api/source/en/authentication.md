# Authentication

Authentication is the process of verifying the identity of a user or application attempting to access the API.

## Methods

### API Key
An API key is a unique identifier used to authenticate requests.

### OAuth 2.0
OAuth 2.0 is a token-based authentication protocol.

## Implementation
- Include the API key in the request header.
- Use OAuth 2.0 tokens for enhanced security.

## Example
```http
GET /user/profile HTTP/1.1
Host: api.example.com
Authorization: Bearer your-token-here

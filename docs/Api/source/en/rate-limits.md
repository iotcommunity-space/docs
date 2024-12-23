
---

### **`rate-limits.md`**
```markdown
# API Rate Limits

## Overview
Rate limits are enforced to ensure fair use of resources and to prevent abuse of the API.

---

## Standard Rate Limits
### Request Limits
- **GET Requests**: 1000 requests per hour.  
- **POST Requests**: 500 requests per hour.  

### Burst Limits
- Allows up to 50 requests in 10 seconds for high-traffic scenarios.

---

## Exceeding Rate Limits
If the rate limit is exceeded, the API responds with an HTTP 429 status code:

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json

{
  "error": "Rate limit exceeded. Try again later."
}

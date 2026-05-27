---
name: immunize-fetch-missing-credentials
description: Use when writing cross-origin fetch() calls that require cookies or session auth to ensure `credentials: 'include'` is set.
---

# fetch-missing-credentials

When you call a cross-origin endpoint that requires cookies, session tokens,
or any credentialed auth, include `credentials: 'include'` in the fetch
options. Browsers default to `credentials: 'same-origin'`, which drops
cookies on cross-origin requests — the backend rejects the call with
401/403 and the response fails CORS preflight.

## Example

Wrong — bare fetch to another origin; cookies won't be sent:

```jsx
async function fetchUser() {
  const response = await fetch('https://api.example.com/me');
  return response.json();
}
```

Right — credentials flag forces cookies to travel:

```jsx
async function fetchUser() {
  const response = await fetch('https://api.example.com/me', {
    credentials: 'include',
  });
  return response.json();
}
```

## Server side must match

For `credentials: 'include'` to work, the server must respond with
`Access-Control-Allow-Credentials: true` AND an explicit
`Access-Control-Allow-Origin: <origin>` (never `*`). If either is
missing, the browser blocks the response even though the network call
succeeded.

## When not to use it

Same-origin requests, public endpoints, and requests that rely on a
Bearer token in the `Authorization` header don't need this flag. Adding
it unnecessarily is a minor security footgun — the browser sends cookies
the endpoint doesn't care about.

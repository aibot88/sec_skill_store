---
name: bog-payment-gateway
description: Bank of Georgia (BOG) Payment Gateway API integration for accepting online payments. Use this skill when implementing BOG payment processing, creating payment orders, handling refunds, checking payment status, or integrating with BOG's OAuth authentication. Triggers include mentions of BOG, Bank of Georgia, Georgian payments, ipay.ge, or requests for payment gateway integration in Georgia.
---

# BOG Payment Gateway Integration

This skill provides guidance for integrating with the Bank of Georgia (BOG) Online Payment API.

## Quick Reference

| Item | Value |
|------|-------|
| Auth URL | `https://oauth2.bog.ge/auth/realms/bog/protocol/openid-connect/token` |
| API Base | `https://api.bog.ge/payments/v1` |
| Auth Method | OAuth 2.0 Client Credentials |
| Data Format | JSON |

**IMPORTANT**:
- All callback URLs MUST use HTTPS
- All API requests MUST include `Accept-Language: ka` or `Accept-Language: en` header

## Integration Flow

1. **Authenticate** - Get access token using client credentials
2. **Create Order** - Submit order with basket items and callbacks
3. **Redirect** - Send customer to payment page (URL from response)
4. **Handle Callback** - Receive payment result at callback URL
5. **Verify** - Check payment status via API

## Authentication

```typescript
const getAccessToken = async (clientId: string, clientSecret: string) => {
  const credentials = Buffer.from(`${clientId}:${clientSecret}`).toString('base64');

  const response = await fetch(
    'https://oauth2.bog.ge/auth/realms/bog/protocol/openid-connect/token',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': `Basic ${credentials}`
      },
      body: 'grant_type=client_credentials'
    }
  );

  const { access_token, expires_in } = await response.json();
  return { access_token, expires_in };
};
```

## Core Endpoints

### Create Order
```
POST https://api.bog.ge/payments/v1/ecommerce/orders
Authorization: Bearer {access_token}
Content-Type: application/json
```

Request body:
```json
{
  "callback_url": "https://example.com/callback",
  "external_order_id": "ORDER-123",
  "purchase_units": {
    "currency": "GEL",
    "total_amount": 100.00,
    "basket": [
      {
        "product_id": "PROD-1",
        "quantity": 1,
        "unit_price": 100.00
      }
    ]
  },
  "redirect_urls": {
    "success": "https://example.com/success",
    "fail": "https://example.com/fail"
  }
}
```

Response includes `_links.redirect.href` for payment page URL.

### Get Payment Details
```
GET https://api.bog.ge/payments/v1/receipt/{order_id}
Authorization: Bearer {access_token}
```

### Refund Payment
```
POST https://api.bog.ge/payments/v1/payment/refund/{order_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{"amount": 50.00}  // Optional - omit for full refund
```

## Response Codes

| Code | Meaning |
|------|---------|
| 100 | Successful payment |
| 200 | Successful preauthorization |
| 101 | Card usage limited |
| 102 | Saved card not found |
| 103 | Invalid card |
| 104 | Transaction limit exceeded |
| 105 | Card expired |
| 106 | Amount limit exceeded |
| 107 | Insufficient funds |
| 108 | Authentication declined |
| 109 | Technical issue |
| 110 | Transaction expired |
| 111 | Authentication timeout |
| 112 | General error |

## Detailed References

- **Full API Reference**: See [references/api.md](references/api.md) for complete endpoint documentation
- **TypeScript Types**: See [references/types.ts](references/types.ts) for type definitions
- **Error Handling**: See [references/api.md](references/api.md) for error code details

## Implementation Checklist

1. Store `client_id` and `client_secret` securely (env vars)
2. Implement token caching with expiry handling
3. Use HTTPS for all callback URLs
4. Implement idempotency keys for order creation
5. Handle all response codes appropriately
6. Log transaction IDs for debugging

# Tapjoy Integration Guide

## Your Postback URL

Give this URL to Tapjoy:

```
https://www.creditgamerarea.com/api/postback/tapjoy?click_id={click_id}&user_id={user_id}&payout={payout}&currency={currency}&offer_id={offer_id}&device_id={device_id}&signature={signature}
```

## Supported Macros

Tapjoy will replace these macros with actual values:

| Macro | Description | Example |
|-------|-------------|---------|
| `{click_id}` | Unique click identifier | clk_abc123xyz |
| `{user_id}` | Tapjoy user ID | tj_user_456 |
| `{payout}` | Payout amount | 0.50 |
| `{currency}` | Currency code | USD |
| `{offer_id}` | Offer/campaign ID | offer_789 |
| `{device_id}` | Device identifier | idfa/gaid |
| `{signature}` | Security signature | (optional) |

## Setup Steps

### 1. In Tapjoy Dashboard:
1. Go to your campaign settings
2. Find "Postback URL" or "Conversion Tracking"
3. Paste the URL above
4. Save

### 2. Test the Integration:

```bash
curl "https://www.creditgamerarea.com/api/postback/tapjoy?click_id=test123&payout=0.50&currency=USD"
```

Expected response:
```json
{
  "success": true,
  "message": "Conversion tracked",
  "click_id": "test123",
  "payout": 0.50
}
```

### 3. View Conversions:

Check `/tracking/data/tapjoy_conversions.json` for logged conversions.

## How It Works

1. **User clicks** your Tapjoy ad
2. **Tapjoy redirects** to your landing page with `click_id`
3. **User completes** your quiz
4. **Tapjoy sends** postback to your URL with payout info
5. **You track** the conversion and revenue

## Security (Optional)

If Tapjoy provides a secret key for signature verification:

1. Add to environment variables: `TAPJOY_SECRET=your_secret`
2. Uncomment signature verification in `tapjoy.js`
3. Invalid signatures will be rejected

## Troubleshooting

### Postback not received?
- Check Vercel logs in dashboard
- Verify URL is correct (no typos)
- Ensure HTTPS is used

### Wrong payout amount?
- Check Tapjoy campaign payout settings
- Verify `{payout}` macro is in URL

### Duplicate conversions?
- System logs all postbacks
- You can deduplicate by `click_id` in your reporting

## Example Flow

```
1. User sees Tapjoy offer: "Complete Credit Quiz - Earn $0.50"
2. User clicks → Tapjoy redirects to:
   https://creditgamerarea.com/credit-basics-quiz.html?click_id=tj_abc123

3. User completes quiz → quiz-complete.html loads

4. Tapjoy sends postback to:
   https://creditgamerarea.com/api/postback/tapjoy?click_id=tj_abc123&payout=0.50&currency=USD&user_id=user_456&offer_id=credit_quiz_01

5. Your server logs conversion with $0.50 payout
```

## Cost

- **Free** - Included in Vercel serverless functions

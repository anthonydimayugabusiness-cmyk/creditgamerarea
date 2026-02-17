# S2S Tracking API for Credit Gamer Area

Server-to-server tracking system for Facebook, Google Ads, and Tapjoy.

## Architecture

```
Traffic Source → Landing Page → Quiz Flow → Conversion → Postback
     ↓              ↓            ↓            ↓            ↓
  Click ID      Store CID    Pass CID    Log Conv.   Send to Source
```

## API Endpoints

### 1. Track Click
`GET /api/track/click`

Parameters:
- `source` (required): facebook, google, tapjoy
- `campaign_id` (optional): your campaign ID
- `creative_id` (optional): ad creative ID
- `sub1`, `sub2`, `sub3` (optional): custom parameters

Response:
```json
{
  "click_id": "clk_abc123xyz",
  "source": "facebook",
  "timestamp": "2026-02-17T08:45:00Z"
}
```

### 2. Track Conversion
`POST /api/track/conversion`

Parameters:
- `click_id` (required): from track/click
- `quiz_name` (required): which quiz
- `score` (optional): quiz score
- `value` (optional): revenue value

Response:
```json
{
  "success": true,
  "postback_sent": ["facebook", "google"]
}
```

### 3. Postback URLs (for traffic sources)

**Facebook:**
```
https://creditgamerarea.com/api/postback/facebook?click_id={click_id}&value={value}
```

**Google:**
```
https://creditgamerarea.com/api/postback/google?click_id={click_id}&conversion={name}
```

**Tapjoy:**
```
https://creditgamerarea.com/api/postback/tapjoy?click_id={click_id}&payout={value}
```

## Setup Instructions

### 1. Environment Variables
Create `.env` file:
```
FACEBOOK_PIXEL_ID=your_pixel_id
FACEBOOK_ACCESS_TOKEN=your_token
GOOGLE_CONVERSION_ID=your_conversion_id
GOOGLE_CONVERSION_LABEL=your_label
TAPJOY_API_KEY=your_key
DATABASE_URL=sqlite:./tracking.db
```

### 2. Database Schema
SQLite database with tables:
- clicks
- conversions
- postbacks

### 3. Frontend Integration
Add tracking script to landing pages (see tracking.js)

## Testing

```bash
# Test click tracking
curl "https://creditgamerarea.com/api/track/click?source=facebook&campaign_id=test123"

# Test conversion
curl -X POST "https://creditgamerarea.com/api/track/conversion" \
  -H "Content-Type: application/json" \
  -d '{"click_id":"clk_abc123","quiz_name":"credit-basics","score":8}'
```

## Cost
- Vercel Serverless Functions: Free tier (100GB bandwidth)
- SQLite: Free (file-based)
- Total: $0/month

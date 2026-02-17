# S2S Tracking Setup Guide

## Step 1: Add Tracking Script to Landing Pages

Add this to the `<head>` of all quiz landing pages (credit-basics-quiz.html, etc.):

```html
<script src="/tracking/tracking.js"></script>
```

## Step 2: Update Quiz Landing Page Links for Ads

When creating ads, use tracking URLs:

**Facebook:**
```
https://www.creditgamerarea.com/credit-basics-quiz.html?utm_source=facebook&utm_campaign=fb_credit_01
```

**Google:**
```
https://www.creditgamerarea.com/investing-quiz.html?utm_source=google&utm_campaign=gg_invest_01
```

**Tapjoy:**
```
https://www.creditgamerarea.com/make-money-online-quiz.html?utm_source=tapjoy&utm_campaign=tj_mmo_01
```

## Step 3: Add Conversion Tracking

Add this to `quiz-complete.html` before `</body>`:

```html
<script src="/tracking/tracking.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
  const quizName = sessionStorage.getItem('last_quiz') || 'unknown';
  const score = parseInt(sessionStorage.getItem('last_score') || '0');
  
  if (window.CGTracking) {
    window.CGTracking.trackConversion(quizName, score, 0);
  }
});
</script>
```

## Step 4: Deploy API Endpoints

The API endpoints are in `/tracking/api/`:
- `/api/track/click` - Logs clicks
- `/api/track/conversion` - Logs conversions

## Step 5: View Tracking Data

Data is stored in:
- `/tracking/data/clicks.json` - All clicks
- `/tracking/data/conversions.json` - All conversions

## Testing

1. Visit: `https://www.creditgamerarea.com/credit-basics-quiz.html?utm_source=facebook&utm_campaign=test`
2. Check browser console for "Tracking: Click logged"
3. Complete quiz
4. Check console for "Tracking: Conversion logged"

## Facebook CAPI Setup (Advanced)

1. Get Pixel ID and Access Token from Facebook Events Manager
2. Add to environment variables
3. Enable server-side tracking in `/api/track/conversion.js`

## Google Ads Setup (Advanced)

1. Get Conversion ID and Label from Google Ads
2. Add to environment variables
3. Enable conversion tracking in `/api/track/conversion.js`

## Cost

- **Vercel Serverless**: Free tier (100GB/month)
- **Storage**: File-based (free)
- **Total**: $0/month

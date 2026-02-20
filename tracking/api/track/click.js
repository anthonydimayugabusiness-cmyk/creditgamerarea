// S2S Tracking API - Serverless Functions for Vercel
// File: api/track/click.js

const { v4: uuidv4 } = require('uuid');

// Simple in-memory rate limiter (use Redis in production)
const rateLimiter = new Map();
const RATE_LIMIT_WINDOW = 3600000; // 1 hour
const RATE_LIMIT_MAX = 100; // 100 requests per hour per IP

function checkRateLimit(ip) {
  const now = Date.now();
  const key = ip;
  
  if (!rateLimiter.has(key)) {
    rateLimiter.set(key, { count: 1, resetTime: now + RATE_LIMIT_WINDOW });
    return { allowed: true, remaining: RATE_LIMIT_MAX - 1 };
  }
  
  const record = rateLimiter.get(key);
  
  // Reset if window expired
  if (now > record.resetTime) {
    rateLimiter.set(key, { count: 1, resetTime: now + RATE_LIMIT_WINDOW });
    return { allowed: true, remaining: RATE_LIMIT_MAX - 1 };
  }
  
  // Check limit
  if (record.count >= RATE_LIMIT_MAX) {
    return { allowed: false, remaining: 0, retryAfter: Math.ceil((record.resetTime - now) / 1000) };
  }
  
  record.count++;
  return { allowed: true, remaining: RATE_LIMIT_MAX - record.count };
}

// Sanitize string input
function sanitizeString(input, maxLength = 100) {
  if (typeof input !== 'string') return '';
  return input
    .replace(/[<>\"']/g, '') // Remove potential XSS chars
    .substring(0, maxLength)
    .trim();
}

// Validate UUID format
function isValidClickId(clickId) {
  return /^clk_[a-f0-9]{16}$/.test(clickId);
}

module.exports = async (req, res) => {
  // Enable CORS - restrict to known domains
  const allowedOrigins = ['https://www.creditgamerarea.com', 'https://creditgamerarea.com'];
  const origin = req.headers.origin;
  if (allowedOrigins.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
  }
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    // Rate limiting
    const clientIp = req.headers['x-forwarded-for']?.split(',')[0]?.trim() || 
                     req.connection.remoteAddress || 
                     'unknown';
    
    const rateLimit = checkRateLimit(clientIp);
    if (!rateLimit.allowed) {
      res.setHeader('Retry-After', rateLimit.retryAfter);
      return res.status(429).json({ 
        error: 'Rate limit exceeded',
        retryAfter: rateLimit.retryAfter 
      });
    }

    const { 
      source, 
      campaign_id = '', 
      creative_id = '',
      sub1 = '',
      sub2 = '',
      sub3 = ''
    } = req.query;

    // Validate source
    const validSources = ['facebook', 'google', 'tapjoy', 'tiktok', 'reddit', 'native', 'organic'];
    if (!source || !validSources.includes(source.toLowerCase())) {
      return res.status(400).json({ 
        error: 'Invalid or missing source. Valid: facebook, google, tapjoy, tiktok, reddit, native, organic' 
      });
    }

    // Sanitize inputs
    const sanitizedCampaignId = sanitizeString(campaign_id, 50);
    const sanitizedCreativeId = sanitizeString(creative_id, 50);
    const sanitizedSub1 = sanitizeString(sub1, 100);
    const sanitizedSub2 = sanitizeString(sub2, 100);
    const sanitizedSub3 = sanitizeString(sub3, 100);

    // Generate click ID
    const clickId = `clk_${uuidv4().replace(/-/g, '').substring(0, 16)}`;
    
    // Get user info (but don't store raw IP without consent)
    const ip = req.headers['x-forwarded-for'] || req.connection.remoteAddress;
    // Hash the IP for privacy
    const ipHash = require('crypto')
      .createHash('sha256')
      .update(ip + process.env.IP_HASH_SALT || 'default-salt')
      .digest('hex')
      .substring(0, 16);
    
    const userAgent = sanitizeString(req.headers['user-agent'] || '', 200);
    
    // Store in database (using simple JSON file for now)
    const clickData = {
      click_id: clickId,
      source: source.toLowerCase(),
      campaign_id: sanitizedCampaignId,
      creative_id: sanitizedCreativeId,
      sub1: sanitizedSub1,
      sub2: sanitizedSub2,
      sub3: sanitizedSub3,
      ip_hash: ipHash, // Store hash, not raw IP
      user_agent: userAgent,
      timestamp: new Date().toISOString(),
      converted: false,
      revenue: 0
    };

    // Store in Vercel KV or file-based storage
    // For now, return the click ID for frontend storage
    
    // Set tracking cookie with Secure flag
    const isSecure = req.headers['x-forwarded-proto'] === 'https';
    const secureFlag = isSecure ? '; Secure' : '';
    res.setHeader('Set-Cookie', `cg_click_id=${clickId}; Path=/; Max-Age=2592000; SameSite=Lax${secureFlag}; HttpOnly`);

    // Add rate limit headers
    res.setHeader('X-RateLimit-Limit', RATE_LIMIT_MAX);
    res.setHeader('X-RateLimit-Remaining', rateLimit.remaining);

    return res.status(200).json({
      success: true,
      click_id: clickId,
      source: source.toLowerCase(),
      timestamp: clickData.timestamp
    });

  } catch (error) {
    console.error('Tracking error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
};

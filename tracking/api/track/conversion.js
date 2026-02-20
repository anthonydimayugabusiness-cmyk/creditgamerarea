// S2S Tracking API - Conversion Tracking
// File: api/track/conversion.js

const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

// Simple in-memory rate limiter
const rateLimiter = new Map();
const RATE_LIMIT_WINDOW = 3600000; // 1 hour
const RATE_LIMIT_MAX = 50; // 50 conversions per hour per IP

function checkRateLimit(ip) {
  const now = Date.now();
  const key = 'conv_' + ip;
  
  if (!rateLimiter.has(key)) {
    rateLimiter.set(key, { count: 1, resetTime: now + RATE_LIMIT_WINDOW });
    return { allowed: true };
  }
  
  const record = rateLimiter.get(key);
  
  if (now > record.resetTime) {
    rateLimiter.set(key, { count: 1, resetTime: now + RATE_LIMIT_WINDOW });
    return { allowed: true };
  }
  
  if (record.count >= RATE_LIMIT_MAX) {
    return { allowed: false, retryAfter: Math.ceil((record.resetTime - now) / 1000) };
  }
  
  record.count++;
  return { allowed: true };
}

// Sanitize string input
function sanitizeString(input, maxLength = 100) {
  if (typeof input !== 'string') return '';
  return input
    .replace(/[<>\"']/g, '')
    .substring(0, maxLength)
    .trim();
}

// Validate click_id format
function isValidClickId(clickId) {
  return typeof clickId === 'string' && /^clk_[a-f0-9]{16}$/.test(clickId);
}

// Hash IP for privacy
function hashIp(ip, salt = 'default-salt') {
  return crypto
    .createHash('sha256')
    .update(ip + salt)
    .digest('hex')
    .substring(0, 16);
}

// Simple file-based storage (upgrade to Redis/Postgres later)
const DB_PATH = path.join(process.cwd(), 'tracking', 'data', 'clicks.json');

async function readDB() {
  try {
    const data = await fs.readFile(DB_PATH, 'utf8');
    return JSON.parse(data);
  } catch {
    return {};
  }
}

async function writeDB(data) {
  await fs.mkdir(path.dirname(DB_PATH), { recursive: true });
  await fs.writeFile(DB_PATH, JSON.stringify(data, null, 2));
}

module.exports = async (req, res) => {
  // Restrict CORS to known domains
  const allowedOrigins = ['https://www.creditgamerarea.com', 'https://creditgamerarea.com'];
  const origin = req.headers.origin;
  if (allowedOrigins.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
  }
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
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
      click_id, 
      quiz_name, 
      score = 0, 
      value = 0,
      quiz_completed = true
    } = req.body;

    // Validate click_id format
    if (!click_id || !isValidClickId(click_id)) {
      return res.status(400).json({ error: 'Invalid or missing click_id' });
    }

    // Validate and sanitize inputs
    const sanitizedQuizName = sanitizeString(quiz_name, 50);
    const numericScore = Math.min(Math.max(parseInt(score) || 0, 0), 100);
    const numericValue = Math.max(parseFloat(value) || 0, 0);
    const isCompleted = quiz_completed === true || quiz_completed === 'true';

    if (!sanitizedQuizName) {
      return res.status(400).json({ error: 'Invalid quiz_name' });
    }

    // Read existing clicks
    const db = await readDB();
    
    if (!db[click_id]) {
      // Click not found - still log conversion but flag it
      console.log(`Conversion for unknown click_id: ${click_id}`);
    }

    // Hash IP for privacy
    const ipHash = hashIp(clientIp, process.env.IP_HASH_SALT);

    // Store conversion
    const conversionData = {
      click_id,
      quiz_name: sanitizedQuizName,
      score: numericScore,
      value: numericValue,
      quiz_completed: isCompleted,
      timestamp: new Date().toISOString(),
      ip_hash: ipHash // Store hash, not raw IP
    };

    // Update click record
    if (db[click_id]) {
      db[click_id].converted = true;
      db[click_id].conversion = conversionData;
      db[click_id].revenue = numericValue;
    }

    // Save to conversions log
    const conversionsPath = path.join(process.cwd(), 'tracking', 'data', 'conversions.json');
    let conversions = [];
    try {
      const convData = await fs.readFile(conversionsPath, 'utf8');
      conversions = JSON.parse(convData);
    } catch {}
    
    conversions.push(conversionData);
    await fs.mkdir(path.dirname(conversionsPath), { recursive: true });
    await fs.writeFile(conversionsPath, JSON.stringify(conversions, null, 2));

    // Send postbacks asynchronously (don't await)
    sendPostbacks(click_id, db[click_id], conversionData).catch(console.error);

    await writeDB(db);

    return res.status(200).json({
      success: true,
      click_id,
      timestamp: conversionData.timestamp
    });

  } catch (error) {
    console.error('Conversion tracking error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
};

async function sendPostbacks(clickId, clickData, conversionData) {
  const results = [];
  
  if (!clickData) return results;

  const source = clickData.source;
  
  try {
    switch(source) {
      case 'facebook':
        // Facebook Conversions API
        results.push({ platform: 'facebook', status: 'queued' });
        break;
        
      case 'google':
        // Google Ads conversion
        results.push({ platform: 'google', status: 'queued' });
        break;
        
      case 'tapjoy':
        // Tapjoy postback
        results.push({ platform: 'tapjoy', status: 'queued' });
        break;
        
      default:
        results.push({ platform: source, status: 'no_postback_configured' });
    }
  } catch (error) {
    console.error(`Postback error for ${source}:`, error);
    results.push({ platform: source, status: 'error', error: error.message });
  }
  
  return results;
}

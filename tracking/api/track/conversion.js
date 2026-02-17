// S2S Tracking API - Conversion Tracking
// File: api/track/conversion.js

const fs = require('fs').promises;
const path = require('path');

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
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { 
      click_id, 
      quiz_name, 
      score = 0, 
      value = 0,
      quiz_completed = true
    } = req.body;

    if (!click_id) {
      return res.status(400).json({ error: 'Missing click_id' });
    }

    // Read existing clicks
    const db = await readDB();
    
    if (!db[click_id]) {
      // Click not found - still log conversion but flag it
      console.log(`Conversion for unknown click_id: ${click_id}`);
    }

    // Store conversion
    const conversionData = {
      click_id,
      quiz_name,
      score,
      value,
      quiz_completed,
      timestamp: new Date().toISOString(),
      ip: req.headers['x-forwarded-for'] || req.connection.remoteAddress
    };

    // Update click record
    if (db[click_id]) {
      db[click_id].converted = true;
      db[click_id].conversion = conversionData;
      db[click_id].revenue = value;
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

    // Send postbacks asynchronously
    const postbackResults = await sendPostbacks(click_id, db[click_id], conversionData);

    await writeDB(db);

    return res.status(200).json({
      success: true,
      click_id,
      postbacks_sent: postbackResults,
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

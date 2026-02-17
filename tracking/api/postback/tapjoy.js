// Tapjoy Postback Receiver
// File: api/postback/tapjoy.js

const fs = require('fs').promises;
const path = require('path');

const CONVERSIONS_PATH = path.join(process.cwd(), 'tracking', 'data', 'tapjoy_conversions.json');

module.exports = async (req, res) => {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    // Tapjoy sends data as query parameters
    const { 
      click_id,
      user_id,
      payout,
      currency,
      offer_id,
      device_id,
      signature
    } = req.query;

    // Log raw postback for debugging
    console.log('Tapjoy Postback Received:', {
      timestamp: new Date().toISOString(),
      query: req.query,
      ip: req.headers['x-forwarded-for'] || req.connection.remoteAddress
    });

    // Validate required fields
    if (!click_id) {
      return res.status(400).json({ 
        error: 'Missing click_id',
        received: req.query 
      });
    }

    // Verify signature (if you have a secret key)
    // const expectedSignature = verifyTapjoySignature(req.query, process.env.TAPJOY_SECRET);
    // if (signature && signature !== expectedSignature) {
    //   return res.status(401).json({ error: 'Invalid signature' });
    // }

    // Store conversion
    const conversionData = {
      platform: 'tapjoy',
      click_id,
      user_id: user_id || '',
      payout: parseFloat(payout) || 0,
      currency: currency || 'USD',
      offer_id: offer_id || '',
      device_id: device_id || '',
      signature: signature || '',
      timestamp: new Date().toISOString(),
      ip: req.headers['x-forwarded-for'] || req.connection.remoteAddress,
      user_agent: req.headers['user-agent'] || ''
    };

    // Save to file
    let conversions = [];
    try {
      const data = await fs.readFile(CONVERSIONS_PATH, 'utf8');
      conversions = JSON.parse(data);
    } catch {}
    
    conversions.push(conversionData);
    await fs.mkdir(path.dirname(CONVERSIONS_PATH), { recursive: true });
    await fs.writeFile(CONVERSIONS_PATH, JSON.stringify(conversions, null, 2));

    // Also update main conversions log
    const mainConversionsPath = path.join(process.cwd(), 'tracking', 'data', 'conversions.json');
    let mainConversions = [];
    try {
      const data = await fs.readFile(mainConversionsPath, 'utf8');
      mainConversions = JSON.parse(data);
    } catch {}
    
    mainConversions.push({
      click_id,
      source: 'tapjoy',
      value: parseFloat(payout) || 0,
      timestamp: conversionData.timestamp,
      platform_data: conversionData
    });
    
    await fs.writeFile(mainConversionsPath, JSON.stringify(mainConversions, null, 2));

    // Return success to Tapjoy
    return res.status(200).json({
      success: true,
      message: 'Conversion tracked',
      click_id,
      payout: conversionData.payout
    });

  } catch (error) {
    console.error('Tapjoy postback error:', error);
    return res.status(500).json({ 
      error: 'Internal server error',
      message: error.message 
    });
  }
};

// Helper to verify Tapjoy signature (if needed)
function verifyTapjoySignature(params, secret) {
  // Tapjoy signature verification logic
  // This depends on their specific signing method
  // Usually involves HMAC with your secret key
  return true; // Placeholder
}

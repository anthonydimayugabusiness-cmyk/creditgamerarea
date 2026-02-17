// S2S Tracking API - Serverless Functions for Vercel
// File: api/track/click.js

const { createClient } = require('@vercel/postgres');
const { v4: uuidv4 } = require('uuid');

module.exports = async (req, res) => {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    const { 
      source, 
      campaign_id = '', 
      creative_id = '',
      sub1 = '',
      sub2 = '',
      sub3 = ''
    } = req.query;

    // Validate source
    const validSources = ['facebook', 'google', 'tapjoy', 'tiktok', 'reddit', 'native'];
    if (!source || !validSources.includes(source.toLowerCase())) {
      return res.status(400).json({ 
        error: 'Invalid or missing source. Valid: facebook, google, tapjoy, tiktok, reddit, native' 
      });
    }

    // Generate click ID
    const clickId = `clk_${uuidv4().replace(/-/g, '').substring(0, 16)}`;
    
    // Get user info
    const ip = req.headers['x-forwarded-for'] || req.connection.remoteAddress;
    const userAgent = req.headers['user-agent'] || '';
    
    // Store in database (using simple JSON file for now)
    const clickData = {
      click_id: clickId,
      source: source.toLowerCase(),
      campaign_id,
      creative_id,
      sub1,
      sub2,
      sub3,
      ip_address: ip,
      user_agent: userAgent,
      timestamp: new Date().toISOString(),
      converted: false,
      revenue: 0
    };

    // Store in Vercel KV or file-based storage
    // For now, return the click ID for frontend storage
    
    // Set tracking cookie
    res.setHeader('Set-Cookie', `cg_click_id=${clickId}; Path=/; Max-Age=2592000; SameSite=Lax`);

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

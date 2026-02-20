/**
 * Cloudflare Bot Management Integration
 * Add this to your site for bot detection and rate limiting
 */

// Cloudflare Turnstile (CAPTCHA alternative, privacy-friendly)
// Sign up at: https://dash.cloudflare.com/sign-up
// Get site key from: Workers & Pages > Turnstile

const CLOUDFLARE_TURNSTILE_SITE_KEY = 'YOUR_TURNSTILE_SITE_KEY'; // Replace after signup

// Bot detection script
(function() {
  'use strict';
  
  // Track suspicious behavior
  const suspiciousSignals = {
    rapidClicks: 0,
    mouseMovement: [],
    lastClickTime: 0,
    jsEnabled: true
  };
  
  // Check if JavaScript is enabled (bots often don't run JS)
  window.addEventListener('load', function() {
    document.body.setAttribute('data-js-enabled', 'true');
  });
  
  // Monitor rapid clicking (bot behavior)
  document.addEventListener('click', function(e) {
    const now = Date.now();
    const timeSinceLastClick = now - suspiciousSignals.lastClickTime;
    
    if (timeSinceLastClick < 100) { // Less than 100ms between clicks
      suspiciousSignals.rapidClicks++;
      
      if (suspiciousSignals.rapidClicks > 5) {
        // Suspicious activity detected - could trigger verification
        if (typeof gtag !== 'undefined') {
          gtag('event', 'suspicious_activity', {
            'type': 'rapid_clicking',
            'clicks': suspiciousSignals.rapidClicks
          });
        }
      }
    }
    
    suspiciousSignals.lastClickTime = now;
  });
  
  // Track mouse movement (bots often have linear or no movement)
  let mousePositions = [];
  document.addEventListener('mousemove', function(e) {
    mousePositions.push({
      x: e.clientX,
      y: e.clientY,
      time: Date.now()
    });
    
    // Keep only last 100 positions
    if (mousePositions.length > 100) {
      mousePositions.shift();
    }
  });
  
  // Check for bot-like mouse patterns
  function analyzeMousePattern() {
    if (mousePositions.length < 10) return 'insufficient_data';
    
    // Check for perfectly linear movement (bot signature)
    let linearMovements = 0;
    for (let i = 2; i < mousePositions.length; i++) {
      const slope1 = (mousePositions[i-1].y - mousePositions[i-2].y) / 
                     (mousePositions[i-1].x - mousePositions[i-2].x || 1);
      const slope2 = (mousePositions[i].y - mousePositions[i-1].y) / 
                     (mousePositions[i].x - mousePositions[i-1].x || 1);
      
      if (Math.abs(slope1 - slope2) < 0.1) {
        linearMovements++;
      }
    }
    
    const linearPercentage = (linearMovements / (mousePositions.length - 2)) * 100;
    
    if (linearPercentage > 80) {
      return 'suspicious_linear';
    }
    
    return 'natural';
  }
  
  // Rate limiting for quiz attempts
  const quizAttempts = {};
  
  window.checkQuizRateLimit = function(quizName) {
    const now = Date.now();
    const key = quizName + '_' + (localStorage.getItem('visitor_id') || 'anonymous');
    
    if (!quizAttempts[key]) {
      quizAttempts[key] = [];
    }
    
    // Remove attempts older than 1 hour
    quizAttempts[key] = quizAttempts[key].filter(time => now - time < 3600000);
    
    // Check if more than 10 attempts in 1 hour
    if (quizAttempts[key].length > 10) {
      if (typeof gtag !== 'undefined') {
        gtag('event', 'rate_limit_exceeded', {
          'quiz_name': quizName,
          'attempts': quizAttempts[key].length
        });
      }
      return false;
    }
    
    quizAttempts[key].push(now);
    return true;
  };
  
  // Generate visitor ID for tracking
  if (!localStorage.getItem('visitor_id')) {
    localStorage.setItem('visitor_id', 'v_' + Math.random().toString(36).substr(2, 9));
  }
  
  // Expose for use in quizzes
  window.BOT_PROTECTION = {
    analyzeMousePattern,
    getRapidClickCount: () => suspiciousSignals.rapidClicks,
    isSuspicious: () => suspiciousSignals.rapidClicks > 5 || analyzeMousePattern() === 'suspicious_linear'
  };
})();

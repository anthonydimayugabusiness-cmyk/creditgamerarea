/**
 * reCAPTCHA v3 Integration for AdSense Protection
 * Sign up at: https://www.google.com/recaptcha/admin
 * Get site key and secret key
 */

// Configuration - Replace with your actual keys after signup
const RECAPTCHA_V3_SITE_KEY = 'YOUR_RECAPTCHA_V3_SITE_KEY';
const RECAPTCHA_V3_SECRET_KEY = 'YOUR_RECAPTCHA_V3_SECRET_KEY'; // Server-side only

// reCAPTCHA v3 Implementation
(function() {
  'use strict';
  
  // Load reCAPTCHA v3 script
  function loadRecaptcha() {
    if (document.getElementById('recaptcha-script')) return;
    
    const script = document.createElement('script');
    script.id = 'recaptcha-script';
    script.src = `https://www.google.com/recaptcha/api.js?render=${RECAPTCHA_V3_SITE_KEY}`;
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);
  }
  
  // Execute reCAPTCHA on specific actions
  window.executeRecaptcha = function(action) {
    return new Promise((resolve, reject) => {
      if (typeof grecaptcha === 'undefined') {
        reject('reCAPTCHA not loaded');
        return;
      }
      
      grecaptcha.ready(function() {
        grecaptcha.execute(RECAPTCHA_V3_SITE_KEY, {action: action})
          .then(function(token) {
            // Send token to your server for verification
            // For now, log it (in production, verify server-side)
            console.log('reCAPTCHA token for', action, ':', token.substring(0, 20) + '...');
            
            // Store score locally (actual verification needs server)
            localStorage.setItem('recaptcha_token_' + action, token);
            localStorage.setItem('recaptcha_time_' + action, Date.now());
            
            resolve(token);
          })
          .catch(reject);
      });
    });
  };
  
  // Protect quiz submissions
  window.protectQuizSubmission = async function(quizName) {
    try {
      const token = await window.executeRecaptcha('quiz_submit');
      
      // Check if user is likely human (score > 0.3)
      // Note: Actual score verification requires server-side check
      // This is client-side only for demonstration
      
      if (typeof gtag !== 'undefined') {
        gtag('event', 'recaptcha_executed', {
          'action': 'quiz_submit',
          'quiz_name': quizName
        });
      }
      
      return true;
    } catch (error) {
      console.error('reCAPTCHA error:', error);
      return false;
    }
  };
  
  // Protect ad clicks (indirectly by monitoring)
  window.monitorAdInteraction = function() {
    // Execute reCAPTCHA when user interacts with ad areas
    const adAreas = document.querySelectorAll('.ad-container, [data-ad-slot]');
    
    adAreas.forEach(ad => {
      ad.addEventListener('mouseenter', function() {
        window.executeRecaptcha('ad_interaction').catch(() => {});
      }, {once: true});
    });
  };
  
  // Initialize on load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      loadRecaptcha();
      setTimeout(window.monitorAdInteraction, 2000);
    });
  } else {
    loadRecaptcha();
    setTimeout(window.monitorAdInteraction, 2000);
  }
  
  // Execute on important actions
  window.addEventListener('load', function() {
    // Score page load
    setTimeout(() => {
      window.executeRecaptcha('page_load').catch(() => {});
    }, 3000);
  });
})();

// Instructions for server-side verification:
// POST to: https://www.google.com/recaptcha/api/siteverify
// Parameters: secret, response (token), remoteip
// Response: { "success": true, "score": 0.9, "action": "quiz_submit" }
// Score interpretation: 1.0 = human, 0.0 = bot, threshold typically 0.5

// Frontend Tracking Script for Credit Gamer Area
// Add this to all landing pages and quiz pages

(function() {
  'use strict';
  
  const Tracking = {
    clickId: null,
    source: null,
    
    // Initialize tracking
    init: function() {
      // Check URL parameters for tracking info
      const urlParams = new URLSearchParams(window.location.search);
      this.source = urlParams.get('utm_source') || urlParams.get('source');
      const campaignId = urlParams.get('utm_campaign') || urlParams.get('campaign_id');
      
      // If we have a source, track the click
      if (this.source) {
        this.trackClick(this.source, campaignId);
      } else {
        // Try to get from cookie
        this.clickId = this.getCookie('cg_click_id');
        this.source = this.getCookie('cg_source');
      }
      
      // Store in session for quiz flow
      if (this.clickId) {
        sessionStorage.setItem('cg_click_id', this.clickId);
        sessionStorage.setItem('cg_source', this.source);
      }
    },
    
    // Track a new click
    trackClick: function(source, campaignId) {
      const params = new URLSearchParams({
        source: source,
        campaign_id: campaignId || '',
        sub1: this.getCookie('cg_sub1') || '',
        sub2: this.getCookie('cg_sub2') || ''
      });
      
      fetch(`/api/track/click?${params.toString()}`)
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            this.clickId = data.click_id;
            this.source = source;
            
            // Store for later
            this.setCookie('cg_click_id', this.clickId, 30);
            this.setCookie('cg_source', this.source, 30);
            sessionStorage.setItem('cg_click_id', this.clickId);
            sessionStorage.setItem('cg_source', this.source);
          }
        })
        .catch(err => {
          // Silently fail - tracking shouldn't break functionality
        });
    },
    
    // Track conversion (quiz completion)
    trackConversion: function(quizName, score, value) {
      const clickId = this.clickId || sessionStorage.getItem('cg_click_id');
      
      if (!clickId) {
        console.log('Tracking: No click ID found, skipping conversion');
        return Promise.resolve({ success: false, reason: 'no_click_id' });
      }
      
      const conversionData = {
        click_id: clickId,
        quiz_name: quizName,
        score: score || 0,
        value: value || 0,
        quiz_completed: true
      };
      
      return fetch('/api/track/conversion', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(conversionData)
      })
      .then(res => res.json())
      .then(data => {
        return data;
      })
      .catch(err => {
        return { success: false, error: err.message };
      });
    },
    
    // Helper: Get cookie
    getCookie: function(name) {
      const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
      return match ? match[2] : null;
    },
    
    // Helper: Set cookie
    setCookie: function(name, value, days) {
      const expires = new Date(Date.now() + days * 864e5).toUTCString();
      const secure = window.location.protocol === 'https:' ? '; Secure' : '';
      document.cookie = name + '=' + encodeURIComponent(value) + '; expires=' + expires + '; path=/; SameSite=Lax' + secure;
    },
    
    // Get tracking URL for ads (append to landing page URLs)
    getTrackingUrl: function(baseUrl, source, campaignId) {
      const separator = baseUrl.includes('?') ? '&' : '?';
      return `${baseUrl}${separator}utm_source=${source}&utm_campaign=${campaignId || ''}`;
    }
  };
  
  // Auto-init on page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => Tracking.init());
  } else {
    Tracking.init();
  }
  
  // Expose globally
  window.CGTracking = Tracking;
})();

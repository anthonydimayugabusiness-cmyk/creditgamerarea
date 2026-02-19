/**
 * Cookie Consent Banner for Credit Gamer Area
 * Add this script to the bottom of your HTML pages before </body>
 */

(function() {
  'use strict';

  // Configuration
  const config = {
    title: "We value your privacy",
    message: "We use cookies to enhance your browsing experience, serve personalized content, and analyze our traffic. By clicking 'Accept All', you consent to our use of cookies.",
    acceptButton: "Accept All",
    declineButton: "Decline",
    privacyPolicyLink: "/privacy.html",
    theme: 'dark', // 'dark' or 'light'
    position: 'bottom', // 'bottom', 'top', or 'center'
  };

  // Check if user has already made a choice
  const consent = localStorage.getItem('cookie-consent');
  if (consent) return;

  // Create banner HTML
  function createBanner() {
    const banner = document.createElement('div');
    banner.id = 'cookie-consent-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Cookie consent');
    
    const isDark = config.theme === 'dark';
    const themeClass = isDark ? 'cookie-banner-dark' : 'cookie-banner-light';
    const positionClass = `cookie-banner-${config.position}`;
    
    banner.className = `cookie-consent-banner ${themeClass} ${positionClass}`;
    
    banner.innerHTML = `
      <div class="cookie-banner-content">
        <div class="cookie-banner-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
          </svg>
        </div>
        <div class="cookie-banner-text">
          <h3>${config.title}</h3>
          <p>${config.message}</p>
          <div class="cookie-banner-buttons">
            <button class="cookie-btn-accept">${config.acceptButton}</button>
            <button class="cookie-btn-decline">${config.declineButton}</button>
          </div>
          <div class="cookie-banner-links">
            <a href="${config.privacyPolicyLink}">Privacy Policy</a>
          </div>
        </div>
        <button class="cookie-banner-close" aria-label="Close">&times;</button>
      </div>
    `;
    
    return banner;
  }

  // Add styles
  function addStyles() {
    if (document.getElementById('cookie-consent-styles')) return;
    
    const styles = document.createElement('style');
    styles.id = 'cookie-consent-styles';
    styles.textContent = `
      .cookie-consent-banner {
        position: fixed;
        z-index: 9999;
        padding: 24px;
        border-radius: 12px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(8px);
        max-width: 420px;
        animation: cookie-slide-in 0.3s ease-out;
      }
      
      @keyframes cookie-slide-in {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
      }
      
      @keyframes cookie-slide-out {
        from { opacity: 1; transform: translateY(0); }
        to { opacity: 0; transform: translateY(20px); }
      }
      
      .cookie-consent-banner.cookie-banner-dark {
        background: rgba(15, 23, 42, 0.98);
        border: 1px solid #334155;
        color: #fff;
      }
      
      .cookie-consent-banner.cookie-banner-light {
        background: rgba(255, 255, 255, 0.98);
        border: 1px solid #e2e8f0;
        color: #0f172a;
      }
      
      .cookie-consent-banner.cookie-banner-bottom {
        bottom: 16px;
        right: 16px;
        left: 16px;
      }
      
      @media (min-width: 640px) {
        .cookie-consent-banner.cookie-banner-bottom {
          left: auto;
        }
      }
      
      .cookie-consent-banner.cookie-banner-top {
        top: 16px;
        right: 16px;
        left: 16px;
      }
      
      @media (min-width: 640px) {
        .cookie-consent-banner.cookie-banner-top {
          left: auto;
        }
      }
      
      .cookie-consent-banner.cookie-banner-center {
        top: 50%;
        left: 16px;
        right: 16px;
        transform: translateY(-50%);
      }
      
      @media (min-width: 640px) {
        .cookie-consent-banner.cookie-banner-center {
          left: 50%;
          right: auto;
          transform: translate(-50%, -50%);
          max-width: 480px;
        }
      }
      
      .cookie-banner-content {
        display: flex;
        gap: 16px;
      }
      
      .cookie-banner-icon {
        flex-shrink: 0;
        width: 40px;
        height: 40px;
        background: #3b82f6;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
      }
      
      .cookie-banner-text {
        flex: 1;
      }
      
      .cookie-banner-text h3 {
        margin: 0 0 8px 0;
        font-size: 16px;
        font-weight: 600;
      }
      
      .cookie-banner-text p {
        margin: 0 0 16px 0;
        font-size: 14px;
        line-height: 1.5;
        opacity: 0.8;
      }
      
      .cookie-banner-buttons {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
      }
      
      .cookie-btn-accept {
        padding: 8px 16px;
        background: #3b82f6;
        color: white;
        border: none;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: background 0.2s;
      }
      
      .cookie-btn-accept:hover {
        background: #2563eb;
      }
      
      .cookie-banner-dark .cookie-btn-decline {
        padding: 8px 16px;
        background: #334155;
        color: white;
        border: none;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: background 0.2s;
      }
      
      .cookie-banner-dark .cookie-btn-decline:hover {
        background: #475569;
      }
      
      .cookie-banner-light .cookie-btn-decline {
        padding: 8px 16px;
        background: #e2e8f0;
        color: #0f172a;
        border: none;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: background 0.2s;
      }
      
      .cookie-banner-light .cookie-btn-decline:hover {
        background: #cbd5e1;
      }
      
      .cookie-banner-links {
        margin-top: 12px;
        font-size: 12px;
      }
      
      .cookie-banner-links a {
        color: inherit;
        opacity: 0.6;
        text-decoration: underline;
      }
      
      .cookie-banner-links a:hover {
        opacity: 1;
      }
      
      .cookie-banner-close {
        flex-shrink: 0;
        width: 32px;
        height: 32px;
        background: transparent;
        border: none;
        font-size: 24px;
        line-height: 1;
        cursor: pointer;
        opacity: 0.5;
        transition: opacity 0.2s;
        color: inherit;
      }
      
      .cookie-banner-close:hover {
        opacity: 1;
      }
      
      .cookie-consent-banner.hiding {
        animation: cookie-slide-out 0.3s ease-out forwards;
      }
    `;
    
    document.head.appendChild(styles);
  }

  // Initialize
  function init() {
    addStyles();
    
    const banner = createBanner();
    document.body.appendChild(banner);
    
    // Handle accept
    banner.querySelector('.cookie-btn-accept').addEventListener('click', function() {
      localStorage.setItem('cookie-consent', 'accepted');
      localStorage.setItem('cookie-consent-date', new Date().toISOString());
      
      // Initialize Google Analytics here
      if (typeof gtag !== 'undefined') {
        gtag('consent', 'update', {
          'analytics_storage': 'granted',
          'ad_storage': 'granted'
        });
      }
      
      hideBanner(banner);
    });
    
    // Handle decline
    banner.querySelector('.cookie-btn-decline').addEventListener('click', function() {
      localStorage.setItem('cookie-consent', 'declined');
      localStorage.setItem('cookie-consent-date', new Date().toISOString());
      hideBanner(banner);
    });
    
    // Handle close
    banner.querySelector('.cookie-banner-close').addEventListener('click', function() {
      localStorage.setItem('cookie-consent', 'declined');
      localStorage.setItem('cookie-consent-date', new Date().toISOString());
      hideBanner(banner);
    });
  }
  
  function hideBanner(banner) {
    banner.classList.add('hiding');
    setTimeout(function() {
      banner.remove();
    }, 300);
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

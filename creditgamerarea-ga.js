/**
 * Google Analytics 4 with Cookie Consent Integration
 * Add this to your HTML <head> section
 * Replace GA_MEASUREMENT_ID with your actual ID (G-XXXXXXXXXX)
 */

// Google Analytics 4 Configuration
const GA_MEASUREMENT_ID = 'G-3CWB6BPJRN'; // Credit Gamer Area GA4 ID

// Default consent settings (denied until user accepts)
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}

gtag('js', new Date());
gtag('config', GA_MEASUREMENT_ID, {
  'send_page_view': false // Don't send until consent is granted
});

// Set default consent to denied
gtag('consent', 'default', {
  'analytics_storage': 'denied',
  'ad_storage': 'denied',
  'functionality_storage': 'denied',
  'personalization_storage': 'denied',
  'security_storage': 'granted' // Always granted for security
});

// Check for existing consent
const existingConsent = localStorage.getItem('cookie-consent');
if (existingConsent === 'accepted') {
  gtag('consent', 'update', {
    'analytics_storage': 'granted',
    'ad_storage': 'granted'
  });
  gtag('event', 'page_view');
}

// Load GA4 script
const script = document.createElement('script');
script.async = true;
script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
document.head.appendChild(script);

// Credit Gamer Area - Traffic Quality Protection System
// Protects against bots and low-quality traffic for AdSense safety

(function() {
    'use strict';
    
    // Configuration
    const CONFIG = {
        minEngagementScore: 50,      // Score needed to show AdSense ads
        engagementDelay: 10000,      // 10 seconds before checking
        botCheckInterval: 1000,      // Check every second
        maxSuspiciousSignals: 3,     // Block after 3 suspicious signals
        debug: false                 // Set to true for console logging
    };
    
    // Traffic source detection
    function getTrafficSource() {
        const urlParams = new URLSearchParams(window.location.search);
        const utmSource = urlParams.get('utm_source');
        const utmMedium = urlParams.get('utm_medium');
        
        if (utmSource) {
            return {
                source: utmSource,
                medium: utmMedium || 'unknown',
                quality: getSourceQuality(utmSource)
            };
        }
        
        // Check referrer
        const referrer = document.referrer;
        if (referrer.includes('google.com')) return { source: 'google', medium: 'organic', quality: 'high' };
        if (referrer.includes('bing.com')) return { source: 'bing', medium: 'organic', quality: 'high' };
        if (referrer.includes('reddit.com')) return { source: 'reddit', medium: 'social', quality: 'medium' };
        if (referrer.includes('facebook.com')) return { source: 'facebook', medium: 'social', quality: 'medium' };
        if (referrer.includes('twitter.com') || referrer.includes('x.com')) return { source: 'twitter', medium: 'social', quality: 'medium' };
        
        return { source: 'direct', medium: 'none', quality: 'unknown' };
    }
    
    function getSourceQuality(source) {
        const qualityMap = {
            'google': 'high',
            'bing': 'high',
            'reddit': 'medium',
            'facebook': 'medium',
            'twitter': 'medium',
            'linkedin': 'medium',
            'paid': 'low',
            'incent': 'low',
            'pop': 'low'
        };
        return qualityMap[source] || 'unknown';
    }
    
    // Engagement tracking
    let engagementScore = 0;
    let suspiciousSignals = 0;
    let mouseMovements = 0;
    let lastMousePosition = { x: 0, y: 0 };
    let linearMovements = 0;
    
    // Bot detection signals
    const botSignals = {
        noMouseMovement: false,
        linearMousePattern: false,
        noScrolling: false,
        instantClick: false,
        javascriptDisabled: false,
        headlessBrowser: false
    };
    
    // Track mouse movements
    document.addEventListener('mousemove', function(e) {
        mouseMovements++;
        
        // Check for linear patterns (bot behavior)
        if (mouseMovements > 5) {
            const deltaX = Math.abs(e.clientX - lastMousePosition.x);
            const deltaY = Math.abs(e.clientY - lastMousePosition.y);
            
            // Bots often move in perfectly straight lines
            if (deltaX === 0 || deltaY === 0) {
                linearMovements++;
                if (linearMovements > 10) {
                    botSignals.linearMousePattern = true;
                    suspiciousSignals++;
                }
            }
        }
        
        lastMousePosition = { x: e.clientX, y: e.clientY };
        
        // Good signal: natural mouse movement
        if (mouseMovements > 20) {
            engagementScore += 5;
        }
    });
    
    // Track scrolling
    let maxScrollDepth = 0;
    document.addEventListener('scroll', function() {
        const scrollPercent = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
        maxScrollDepth = Math.max(maxScrollDepth, scrollPercent);
        
        // Engagement bonuses for scrolling
        if (scrollPercent > 25) engagementScore += 5;
        if (scrollPercent > 50) engagementScore += 10;
        if (scrollPercent > 75) engagementScore += 15;
    });
    
    // Track clicks
    document.addEventListener('click', function(e) {
        // Internal link clicks = high engagement
        if (e.target.tagName === 'A') {
            const href = e.target.getAttribute('href') || '';
            if (href.includes('creditgamerarea.com') || href.startsWith('/') || href.startsWith('./')) {
                engagementScore += 15;
            }
        }
        
        // Check for instant clicks (bot behavior)
        if (Date.now() - pageLoadTime < 2000) {
            botSignals.instantClick = true;
            suspiciousSignals++;
        }
    });
    
    // Time on page bonuses
    const pageLoadTime = Date.now();
    setTimeout(() => { engagementScore += 5; }, 5000);   // 5 seconds
    setTimeout(() => { engagementScore += 10; }, 15000); // 15 seconds
    setTimeout(() => { engagementScore += 15; }, 30000); // 30 seconds
    setTimeout(() => { engagementScore += 20; }, 60000); // 1 minute
    
    // Check for no mouse movement (bot)
    setTimeout(() => {
        if (mouseMovements < 5) {
            botSignals.noMouseMovement = true;
            suspiciousSignals += 2;
        }
    }, 5000);
    
    // Check for no scrolling (bot)
    setTimeout(() => {
        if (maxScrollDepth < 10) {
            botSignals.noScrolling = true;
            suspiciousSignals++;
        }
    }, 10000);
    
    // Headless browser detection
    function detectHeadless() {
        const signals = [
            navigator.webdriver,
            navigator.plugins.length === 0,
            navigator.languages.length === 0,
            window.outerWidth === 0 || window.outerHeight === 0,
            !window.chrome && navigator.userAgent.includes('Chrome'),
            /HeadlessChrome/.test(navigator.userAgent)
        ];
        
        const headlessScore = signals.filter(Boolean).length;
        if (headlessScore >= 3) {
            botSignals.headlessBrowser = true;
            suspiciousSignals += 3;
        }
    }
    detectHeadless();
    
    // Honeypot field check
    function checkHoneypot() {
        const honeypot = document.querySelector('input[name="website"], input[name="company"]');
        if (honeypot && honeypot.value) {
            suspiciousSignals += 5; // Bot filled hidden field
        }
    }
    
    // Ad serving decision
    function shouldShowAds() {
        const traffic = getTrafficSource();
        
        // High quality traffic: show ads immediately
        if (traffic.quality === 'high') {
            return { show: true, reason: 'High quality organic traffic' };
        }
        
        // Medium quality: check engagement
        if (traffic.quality === 'medium') {
            if (engagementScore >= CONFIG.minEngagementScore) {
                return { show: true, reason: 'Medium quality with sufficient engagement' };
            }
            return { show: false, reason: 'Medium quality, engagement too low' };
        }
        
        // Low quality (paid/incent): strict engagement check
        if (traffic.quality === 'low' || traffic.quality === 'unknown') {
            if (suspiciousSignals >= CONFIG.maxSuspiciousSignals) {
                return { show: false, reason: 'Low quality traffic with bot signals' };
            }
            if (engagementScore >= CONFIG.minEngagementScore * 1.5) {
                return { show: true, reason: 'Low quality but high engagement' };
            }
            return { show: false, reason: 'Low quality traffic, engagement gate not met' };
        }
        
        return { show: false, reason: 'Unknown traffic quality' };
    }
    
    // Hide ads initially
    function hideAdsInitially() {
        const adContainers = document.querySelectorAll('.adsbygoogle, .ad-container, [data-ad-slot]');
        adContainers.forEach(ad => {
            ad.style.display = 'none';
            ad.setAttribute('data-ad-hidden', 'true');
        });
    }
    
    // Reveal ads
    function revealAds() {
        const adContainers = document.querySelectorAll('[data-ad-hidden="true"]');
        adContainers.forEach(ad => {
            ad.style.display = '';
            ad.removeAttribute('data-ad-hidden');
        });
        
        // Trigger AdSense refresh if needed
        if (typeof adsbygoogle !== 'undefined') {
            adsbygoogle.push({});
        }
    }
    
    // Analytics tracking
    function trackQualityMetrics() {
        const traffic = getTrafficSource();
        const adDecision = shouldShowAds();
        
        // Send to Google Analytics (if available)
        if (typeof gtag !== 'undefined') {
            gtag('event', 'traffic_quality_check', {
                'traffic_source': traffic.source,
                'traffic_quality': traffic.quality,
                'engagement_score': engagementScore,
                'suspicious_signals': suspiciousSignals,
                'ads_shown': adDecision.show,
                'mouse_movements': mouseMovements,
                'scroll_depth': maxScrollDepth
            });
        }
        
        if (CONFIG.debug) {
            console.log('Traffic Quality Report:', {
                source: traffic,
                engagement: engagementScore,
                suspicious: suspiciousSignals,
                botSignals: botSignals,
                showAds: adDecision
            });
        }
    }
    
    // Main execution
    function init() {
        const traffic = getTrafficSource();
        
        // Always hide ads initially for low/unknown quality traffic
        if (traffic.quality !== 'high') {
            hideAdsInitially();
        }
        
        // Check and reveal ads after delay
        setTimeout(() => {
            checkHoneypot();
            const decision = shouldShowAds();
            
            if (decision.show) {
                revealAds();
            } else {
                // For low quality traffic, show affiliate ads instead
                showAffiliateFallback();
            }
            
            trackQualityMetrics();
        }, CONFIG.engagementDelay);
    }
    
    // Affiliate fallback for low-quality traffic
    function showAffiliateFallback() {
        const adContainers = document.querySelectorAll('[data-ad-hidden="true"]');
        adContainers.forEach(ad => {
            ad.innerHTML = '<div class="affiliate-fallback">' +
                '<p>Recommended for you:</p>' +
                '<a href="/recommended.html" target="_blank">Best Credit Cards for Gamers</a>' +
                '</div>';
            ad.style.display = '';
            ad.removeAttribute('data-ad-hidden');
        });
    }
    
    // Run on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Expose for debugging
    window.TrafficQuality = {
        getScore: () => engagementScore,
        getSignals: () => suspiciousSignals,
        getSource: getTrafficSource,
        shouldShowAds: shouldShowAds
    };
    
})();
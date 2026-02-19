/**
 * Quiz Completion Tracking with Source Attribution
 * Add this to all quiz pages
 */

// Quiz Tracking Configuration
const QUIZ_TRACKING = {
  // Track quiz start with source
  trackQuizStart: function(quizName, source = 'direct') {
    // Get UTM parameters or referrer
    const urlParams = new URLSearchParams(window.location.search);
    const utmSource = urlParams.get('utm_source');
    const utmMedium = urlParams.get('utm_medium');
    const utmCampaign = urlParams.get('utm_campaign');
    
    // Determine actual source
    const actualSource = utmSource || this.getReferrerSource() || source;
    const medium = utmMedium || 'organic';
    
    // Store in session for completion attribution
    sessionStorage.setItem('quiz_start_source', actualSource);
    sessionStorage.setItem('quiz_start_medium', medium);
    sessionStorage.setItem('quiz_name', quizName);
    sessionStorage.setItem('quiz_start_time', Date.now());
    
    if (typeof gtag !== 'undefined') {
      gtag('event', 'quiz_start', {
        'quiz_name': quizName,
        'source': actualSource,
        'medium': medium,
        'campaign': utmCampaign || '(not set)',
        'landing_page': window.location.pathname,
        'user_type': localStorage.getItem('cookie-consent') === 'accepted' ? 'consented' : 'anonymous'
      });
    }
    
    console.log('Quiz started:', quizName, 'Source:', actualSource);
  },
  
  // Track quiz completion with full attribution
  trackQuizComplete: function(quizName, score, totalQuestions, timeSpentSeconds) {
    const source = sessionStorage.getItem('quiz_start_source') || 'direct';
    const medium = sessionStorage.getItem('quiz_start_medium') || 'organic';
    const startTime = parseInt(sessionStorage.getItem('quiz_start_time') || Date.now());
    const actualTimeSpent = timeSpentSeconds || Math.round((Date.now() - startTime) / 1000);
    const scorePercentage = Math.round((score / totalQuestions) * 100);
    
    // Determine score tier
    let scoreTier = 'needs_work';
    if (scorePercentage >= 80) scoreTier = 'elite';
    else if (scorePercentage >= 60) scoreTier = 'average';
    else if (scorePercentage >= 40) scoreTier = 'below_average';
    
    if (typeof gtag !== 'undefined') {
      gtag('event', 'quiz_complete', {
        'quiz_name': quizName,
        'source': source,
        'medium': medium,
        'score': score,
        'total_questions': totalQuestions,
        'score_percentage': scorePercentage,
        'score_tier': scoreTier,
        'time_spent_seconds': actualTimeSpent,
        'user_type': localStorage.getItem('cookie-consent') === 'accepted' ? 'consented' : 'anonymous',
        'value': scorePercentage // For GA4 value metric
      });
      
      // Also track as conversion if score is good
      if (scorePercentage >= 60) {
        gtag('event', 'quiz_pass', {
          'quiz_name': quizName,
          'source': source,
          'score_tier': scoreTier
        });
      }
    }
    
    // Clear session data
    sessionStorage.removeItem('quiz_start_source');
    sessionStorage.removeItem('quiz_start_medium');
    sessionStorage.removeItem('quiz_start_time');
    
    console.log('Quiz completed:', quizName, 'Score:', scorePercentage + '%', 'Source:', source);
    
    return {
      quizName,
      source,
      medium,
      score,
      scorePercentage,
      scoreTier,
      timeSpent: actualTimeSpent
    };
  },
  
  // Track quiz abandonment
  trackQuizAbandon: function(quizName, questionNumber) {
    const source = sessionStorage.getItem('quiz_start_source') || 'direct';
    
    if (typeof gtag !== 'undefined') {
      gtag('event', 'quiz_abandon', {
        'quiz_name': quizName,
        'source': source,
        'question_reached': questionNumber,
        'user_type': localStorage.getItem('cookie-consent') === 'accepted' ? 'consented' : 'anonymous'
      });
    }
  },
  
  // Get referrer source
  getReferrerSource: function() {
    const referrer = document.referrer;
    if (!referrer) return null;
    
    if (referrer.includes('google')) return 'google';
    if (referrer.includes('facebook')) return 'facebook';
    if (referrer.includes('twitter') || referrer.includes('x.com')) return 'twitter';
    if (referrer.includes('reddit')) return 'reddit';
    if (referrer.includes('tiktok')) return 'tiktok';
    if (referrer.includes('youtube')) return 'youtube';
    if (referrer.includes('creditgamerarea.com')) return 'internal';
    
    return 'referral';
  },
  
  // Track share events
  trackShare: function(quizName, platform) {
    if (typeof gtag !== 'undefined') {
      gtag('event', 'quiz_share', {
        'quiz_name': quizName,
        'platform': platform,
        'user_type': localStorage.getItem('cookie-consent') === 'accepted' ? 'consented' : 'anonymous'
      });
    }
  },
  
  // Generate shareable URL with tracking
  getShareableUrl: function(quizName, scoreTier) {
    const baseUrl = window.location.origin + window.location.pathname;
    const params = new URLSearchParams({
      'utm_source': 'share',
      'utm_medium': 'social',
      'utm_campaign': 'quiz_results',
      'ref': scoreTier
    });
    return baseUrl + '?' + params.toString();
  }
};

// Auto-initialize on quiz pages
if (document.querySelector('.quiz-container') || document.querySelector('[data-quiz-name]')) {
  const quizName = document.querySelector('[data-quiz-name]')?.dataset.quizName || 
                   document.title.replace(' - Credit Gamer Area', '');
  
  // Track start when page loads
  QUIZ_TRACKING.trackQuizStart(quizName, 'quiz_page');
  
  // Track abandonment on page unload
  window.addEventListener('beforeunload', function() {
    const currentQuestion = document.querySelector('.question-active')?.dataset.questionNumber;
    if (currentQuestion) {
      QUIZ_TRACKING.trackQuizAbandon(quizName, parseInt(currentQuestion));
    }
  });
}

// Make available globally
window.QUIZ_TRACKING = QUIZ_TRACKING;

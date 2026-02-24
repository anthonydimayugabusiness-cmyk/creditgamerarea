<!-- Enhanced Analytics Tracking -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID', {
    'send_page_view': true,
    'anonymize_ip': true,
    'allow_google_signals': false,
    'transport_type': 'beacon',
    'custom_map': {
      'custom_parameter_1': 'content_type',
      'custom_parameter_2': 'quiz_category'
    }
  });

  // Enhanced Event Tracking
  document.addEventListener('DOMContentLoaded', function() {
    // Track quiz starts
    document.querySelectorAll('[data-quiz-start]').forEach(function(el) {
      el.addEventListener('click', function() {
        gtag('event', 'quiz_start', {
          'event_category': 'engagement',
          'event_label': el.dataset.quizName || 'unknown',
          'content_type': 'quiz'
        });
      });
    });

    // Track quiz completions
    document.querySelectorAll('[data-quiz-complete]').forEach(function(el) {
      el.addEventListener('click', function() {
        gtag('event', 'quiz_complete', {
          'event_category': 'conversion',
          'event_label': el.dataset.quizName || 'unknown',
          'value': el.dataset.score || 0
        });
      });
    });

    // Track scroll depth
    let scrollMarks = [25, 50, 75, 90];
    let scrolledMarks = [];
    
    window.addEventListener('scroll', function() {
      let scrollPercent = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
      
      scrollMarks.forEach(function(mark) {
        if (scrollPercent >= mark && !scrolledMarks.includes(mark)) {
          scrolledMarks.push(mark);
          gtag('event', 'scroll_depth', {
            'event_category': 'engagement',
            'event_label': mark + '%',
            'value': mark
          });
        }
      });
    });

    // Track outbound links
    document.querySelectorAll('a[href^="http"]').forEach(function(link) {
      if (!link.href.includes(window.location.hostname)) {
        link.addEventListener('click', function() {
          gtag('event', 'outbound_click', {
            'event_category': 'engagement',
            'event_label': link.href,
            'transport_type': 'beacon'
          });
        });
      }
    });

    // Track time on page (send at 30s, 60s, 180s)
    [30, 60, 180].forEach(function(seconds) {
      setTimeout(function() {
        gtag('event', 'time_on_page', {
          'event_category': 'engagement',
          'event_label': seconds + 's',
          'value': seconds
        });
      }, seconds * 1000);
    });
  });
</script>
// Quiz Token System - Prevents skipping and unauthorized access
// Each question generates a token that must be presented to access the next question

const QuizToken = {
    // Generate a simple hash from string
    hash: function(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash).toString(36);
    },
    
    // Generate token for next question
    generate: function(quizName, questionNum, score) {
        const timestamp = Math.floor(Date.now() / 1000 / 60); // Changes every minute
        const secret = 'cga2026'; // Simple secret - should be more complex in production
        const data = `${quizName}|${questionNum}|${score}|${timestamp}|${secret}`;
        return this.hash(data);
    },
    
    // Validate token
    validate: function(token, quizName, questionNum, score) {
        const timestamp = Math.floor(Date.now() / 1000 / 60);
        const secret = 'cga2026';
        
        // Check current and previous minute (allows 1-2 min window)
        for (let t = timestamp; t >= timestamp - 1; t--) {
            const data = `${quizName}|${questionNum}|${score}|${t}|${secret}`;
            if (this.hash(data) === token) {
                return true;
            }
        }
        return false;
    },
    
    // Get URL parameters
    getParams: function() {
        const params = new URLSearchParams(window.location.search);
        return {
            token: params.get('t'),
            score: parseInt(params.get('s') || '0')
        };
    },
    
    // Build URL with token
    buildUrl: function(baseUrl, quizName, questionNum, score) {
        const token = this.generate(quizName, questionNum, score);
        return `${baseUrl}?t=${token}&s=${score}`;
    }
};

// Export for use in quiz pages
if (typeof module !== 'undefined' && module.exports) {
    module.exports = QuizToken;
}

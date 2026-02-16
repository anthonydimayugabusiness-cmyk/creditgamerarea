// Credit Gamer Area - Main JavaScript

// Quiz Data
const quizData = {
    'credit-basics': {
        title: 'Credit Basics Quiz',
        description: 'Test your knowledge of credit scores, reports, and building credit',
        questions: [
            {
                question: 'What is the most commonly used credit scoring model?',
                options: ['VantageScore', 'FICO Score', 'Experian Score', 'TransUnion Score'],
                correct: 1,
                explanation: 'FICO Score is used by 90% of top lenders. It ranges from 300-850.'
            },
            {
                question: 'What percentage of your credit score is based on payment history?',
                options: ['15%', '35%', '50%', '65%'],
                correct: 1,
                explanation: 'Payment history makes up 35% of your FICO score - the single biggest factor.'
            },
            {
                question: 'How long do negative items (like late payments) stay on your credit report?',
                options: ['3 years', '5 years', '7 years', '10 years'],
                correct: 2,
                explanation: 'Most negative items stay for 7 years. Bankruptcies can stay for 10.'
            },
            {
                question: 'What is the recommended credit utilization ratio?',
                options: ['Under 10%', 'Under 30%', 'Under 50%', 'Under 70%'],
                correct: 1,
                explanation: 'Keep utilization under 30% (ideally under 10%) for best scores.'
            },
            {
                question: 'How often can you get a free credit report from each bureau?',
                options: ['Monthly', 'Every 6 months', 'Annually', 'Every 3 years'],
                correct: 2,
                explanation: 'AnnualCreditReport.com gives you one free report per bureau per year.'
            },
            {
                question: 'What is a "hard inquiry" on your credit report?',
                options: ['Checking your own score', 'A lender checking your credit', 'A soft credit check', 'An error on your report'],
                correct: 1,
                explanation: 'Hard inquiries happen when you apply for credit and can lower your score slightly.'
            },
            {
                question: 'How long does it take to build credit from scratch?',
                options: ['1 month', '3-6 months', '1 year', '2 years'],
                correct: 1,
                explanation: 'It takes 3-6 months of credit activity to generate a FICO score.'
            },
            {
                question: 'What is the best first credit card for beginners?',
                options: ['Premium travel card', 'Secured credit card', 'Business credit card', 'Store credit card'],
                correct: 1,
                explanation: 'Secured cards require a deposit and are designed for building credit.'
            },
            {
                question: 'Does closing a credit card help your credit score?',
                options: ['Yes, always', 'Yes, if it has a balance', 'No, it usually hurts', 'No effect'],
                correct: 2,
                explanation: 'Closing cards reduces available credit and can hurt your utilization ratio.'
            },
            {
                question: 'What is the average credit score in the US?',
                options: ['650', '700', '718', '750'],
                correct: 2,
                explanation: 'The average FICO score is around 718 as of 2024.'
            }
        ]
    }
};

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    
    // Smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
    
    // Newsletter form
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', handleSubscribe);
    }
    
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 100) {
            navbar.style.boxShadow = '0 4px 20px rgba(0,0,0,0.1)';
        } else {
            navbar.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
        }
    });
    
    // Animate elements on scroll
    const observerOptions = { threshold: 0.1 };
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.topic-card, .feature-card, .blog-card').forEach(el => {
        observer.observe(el);
    });
    
});

// Handle newsletter subscription
function handleSubscribe(e) {
    e.preventDefault();
    const email = e.target.querySelector('input[type="email"]').value;
    
    // Show success message
    alert('🎉 Welcome to Credit Gamer Area!\n\nYou\'ll receive weekly quizzes and money tips at: ' + email);
    e.target.reset();
    
    // Track event (for analytics)
    console.log('Newsletter signup:', email);
}

// Start quiz function
function startQuiz() {
    alert('🎮 Starting Credit Basics Quiz!\n\n10 questions • 5 minutes • Instant results\n\n(In production, this would launch the interactive quiz)');
}

// Scroll to learn section
function scrollToLearn() {
    document.getElementById('topics').scrollIntoView({ behavior: 'smooth' });
}

// Quiz functionality (for quiz pages)
let currentQuiz = null;
let currentQuestion = 0;
let score = 0;
let answers = [];

function loadQuiz(quizId) {
    currentQuiz = quizData[quizId];
    currentQuestion = 0;
    score = 0;
    answers = [];
    
    if (!currentQuiz) {
        console.error('Quiz not found:', quizId);
        return;
    }
    
    showQuestion();
}

function showQuestion() {
    const question = currentQuiz.questions[currentQuestion];
    const quizContainer = document.getElementById('quiz-container');
    
    if (!quizContainer) return;
    
    quizContainer.innerHTML = `
        <div class="quiz-progress">
            <div class="progress-bar" style="width: ${((currentQuestion + 1) / currentQuiz.questions.length) * 100}%"></div>
            <span>Question ${currentQuestion + 1} of ${currentQuiz.questions.length}</span>
        </div>
        
        <div class="question-card">
            <h3>${question.question}</h3>
            <div class="options">
                ${question.options.map((opt, idx) => `
                    <button class="option-btn" onclick="selectAnswer(${idx})">${opt}</button>
                `).join('')}
            </div>
        </div>
    `;
}

function selectAnswer(answerIndex) {
    const question = currentQuiz.questions[currentQuestion];
    const isCorrect = answerIndex === question.correct;
    
    answers.push({
        question: question.question,
        selected: answerIndex,
        correct: question.correct,
        isCorrect: isCorrect
    });
    
    if (isCorrect) score++;
    
    // Show explanation
    const quizContainer = document.getElementById('quiz-container');
    quizContainer.innerHTML += `
        <div class="explanation ${isCorrect ? 'correct' : 'incorrect'}">
            <strong>${isCorrect ? '✓ Correct!' : '✗ Incorrect'}</strong>
            <p>${question.explanation}</p>
            <button class="btn-primary" onclick="nextQuestion()">Next Question →</button>
        </div>
    `;
}

function nextQuestion() {
    currentQuestion++;
    
    if (currentQuestion < currentQuiz.questions.length) {
        showQuestion();
    } else {
        showResults();
    }
}

function showResults() {
    const percentage = Math.round((score / currentQuiz.questions.length) * 100);
    let message = '';
    let emoji = '';
    
    if (percentage >= 90) {
        message = 'Finance Master!';
        emoji = '🏆';
    } else if (percentage >= 70) {
        message = 'Well Done!';
        emoji = '⭐';
    } else if (percentage >= 50) {
        message = 'Keep Learning!';
        emoji = '📚';
    } else {
        message = 'Time to Study!';
        emoji = '💪';
    }
    
    const quizContainer = document.getElementById('quiz-container');
    quizContainer.innerHTML = `
        <div class="quiz-results">
            <div class="result-emoji">${emoji}</div>
            <h2>${message}</h2>
            <div class="score-display">${score}/${currentQuiz.questions.length}</div>
            <p class="score-percentage">${percentage}%</p>
            
            <div class="result-actions">
                <button class="btn-primary" onclick="location.reload()">Retake Quiz</button>
                <button class="btn-secondary" onclick="window.location.href='/quiz/credit-cards.html'">Next Quiz →</button>
            </div>
            
            <div class="result-share">
                <p>Share your score:</p>
                <button onclick="shareResult(${percentage})">Share on Twitter</button>
            </div>
        </div>
    `;
}

function shareResult(percentage) {
    const text = `I scored ${percentage}% on the Credit Basics Quiz at Credit Gamer Area! 🎮💳 Can you beat my score?`;
    const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent('https://creditgamerarea.com')}`;
    window.open(url, '_blank');
}

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { quizData, loadQuiz };
}

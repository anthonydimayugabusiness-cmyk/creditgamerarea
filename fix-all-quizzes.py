#!/usr/bin/env python3
"""Fix quiz pages - remove broken reCAPTCHA and standardize header/footer."""

import os
import glob
import re

# Standard header for all quiz pages
STANDARD_HEADER = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="robots" content="noindex, nofollow">
    <link rel="stylesheet" href="/styles.css">
    <link rel="stylesheet" href="/square-quiz-cards.css">
    <style>
        .quiz-page {{ padding: 40px 0; min-height: calc(100vh - 200px); }}
        .quiz-container {{ max-width: 700px; margin: 0 auto; background: white; border-radius: 16px; padding: 40px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }}
        .quiz-header {{ text-align: center; margin-bottom: 32px; }}
        .category-tag {{ display: inline-block; background: {color}; color: white; padding: 6px 16px; border-radius: 20px; font-size: 0.875rem; font-weight: 600; margin-bottom: 16px; }}
        .progress-container {{ margin-bottom: 32px; }}
        .progress-bar-bg {{ background: #e2e8f0; height: 8px; border-radius: 4px; overflow: hidden; }}
        .progress-bar {{ background: linear-gradient(90deg, {color}, {color2}); height: 100%; border-radius: 4px; }}
        .progress-text {{ font-size: 0.875rem; color: #64748b; margin-top: 8px; text-align: center; }}
        .question-container h2 {{ font-size: 1.5rem; margin-bottom: 24px; line-height: 1.5; }}
        .options-list {{ display: flex; flex-direction: column; gap: 12px; }}
        .option {{ background: white; border: 2px solid #e2e8f0; padding: 16px 20px; border-radius: 12px; cursor: pointer; transition: all 0.2s; font-size: 1rem; text-align: left; }}
        .option:hover {{ border-color: {color}; background: #f8fafc; }}
        .explanation {{ margin-top: 24px; padding: 20px; border-radius: 12px; display: none; }}
        .explanation.correct {{ background: #d1fae5; border: 1px solid #10b981; display: block; }}
        .explanation.incorrect {{ background: #fee2e2; border: 1px solid #ef4444; display: block; }}
        .next-btn {{ margin-top: 16px; background: {color}; color: white; border: none; padding: 14px 28px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 1rem; text-decoration: none; display: inline-block; }}
        .ad-container {{ max-width: 700px; margin: 32px auto; text-align: center; }}
        .ad-label {{ font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-bottom: 8px; }}
        .error-message {{ background: #fee2e2; border: 1px solid #ef4444; color: #b91c1c; padding: 20px; border-radius: 12px; text-align: center; display: none; }}
    </style>
    <script src="/quiz-token.js"></script>
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <a href="/" class="logo">💳 Credit Gamer Area</a>
            <ul class="nav-links">
                <li><a href="/quizzes/">Quizzes</a></li>
                <li><a href="/blog/">Blog</a></li>
            </ul>
        </div>
    </nav>

    <div id="error-msg" class="error-message" style="max-width: 700px; margin: 40px auto;">
        <h3>⚠️ Invalid Access</h3>
        <p>Please start the quiz from the beginning.</p>
        <a href="{landing_page}" class="next-btn">Go to Quiz Start</a>
    </div>

    <section class="quiz-page" id="quiz-content">
        <div class="container">
            <div class="quiz-container">
                <div class="quiz-header">
                    <span class="category-tag">{quiz_name} - Question {q_num} of {total}</span>
                </div>
                
                <div class="progress-container">
                    <div class="progress-bar-bg">
                        <div class="progress-bar" style="width: {progress}%;"></div>
                    </div>
                    <div class="progress-text">Question {q_num} of {total}</div>
                </div>
                
                <div class="question-container">
                    <h2>{question}</h2>
                    <div class="options-list">
                        <button class="option" onclick="selectAnswer(0, {correct})">{opt0}</button>
                        <button class="option" onclick="selectAnswer(1, {correct})">{opt1}</button>
                        <button class="option" onclick="selectAnswer(2, {correct})">{opt2}</button>
                        <button class="option" onclick="selectAnswer(3, {correct})">{opt3}</button>
                    </div>
                    
                    <div id="explanation" class="explanation">
                        <h4 id="result-text"></h4>
                        <p>{explanation}</p>
                        <a href="{next_page}" id="next-btn" class="next-btn">{next_text}</a>
                    </div>
                </div>
            </div>
            
            <div class="ad-container">
                <div class="ad-label">Advertisement</div>
                <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins>
                <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer" style="background: #0f0d2e; color: white; padding: 60px 0 30px;">
        <div class="container">
            <div class="footer-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 40px; margin-bottom: 40px;">
                <div class="footer-brand">
                    <h3 style="font-size: 1.25rem; margin-bottom: 16px;">💳 Credit Gamer Area</h3>
                    <p style="color: #94a3b8; font-size: 0.875rem; line-height: 1.6;">Helping gamers and young adults master credit, finance, and money-making skills through fun, interactive quizzes.</p>
                </div>
                
                <div class="footer-links">
                    <h4 style="font-size: 1rem; margin-bottom: 16px;">Learn</h4>
                    <ul style="list-style: none; padding: 0;">
                        <li style="margin-bottom: 8px;"><a href="/credit-basics-quiz.html" style="color: #94a3b8; text-decoration: none;">Credit Basics</a></li>
                        <li style="margin-bottom: 8px;"><a href="/investing-quiz.html" style="color: #94a3b8; text-decoration: none;">Investing</a></li>
                        <li style="margin-bottom: 8px;"><a href="/quizzes/" style="color: #94a3b8; text-decoration: none;">All Quizzes</a></li>
                    </ul>
                </div>
                
                <div class="footer-links">
                    <h4 style="font-size: 1rem; margin-bottom: 16px;">Resources</h4>
                    <ul style="list-style: none; padding: 0;">
                        <li style="margin-bottom: 8px;"><a href="/blog/" style="color: #94a3b8; text-decoration: none;">Blog</a></li>
                        <li style="margin-bottom: 8px;"><a href="/resources.html" style="color: #94a3b8; text-decoration: none;">Calculators</a></li>
                        <li style="margin-bottom: 8px;"><a href="/faq.html" style="color: #94a3b8; text-decoration: none;">FAQ</a></li>
                    </ul>
                </div>
            </div>
            <p style="text-align: center; color: #64748b;">&copy; 2026 Credit Gamer Area. Not financial advice.</p>
        </div>
    </footer>

    <script>
        const QUIZ_NAME = '{quiz_id}';
        const QUESTION_NUM = {q_num};
        const IS_LAST = {is_last};
        
        // Validate token on page load
        document.addEventListener('DOMContentLoaded', function() {
            const params = QuizToken.getParams();
            
            // First question doesn't need token
            if (QUESTION_NUM === 1) {
                sessionStorage.setItem('{score_key}', '0');
                return;
            }
            
            // Validate token for subsequent questions
            if (!params.token || !QuizToken.validate(params.token, QUIZ_NAME, QUESTION_NUM - 1, params.score)) {
                document.getElementById('quiz-content').style.display = 'none';
                document.getElementById('error-msg').style.display = 'block';
            } else {
                // Update score from token
                sessionStorage.setItem('{score_key}', params.score.toString());
            }
        });
        
        let answered = false;
        let currentScore = parseInt(sessionStorage.getItem('{score_key}') || '0');
        
        function selectAnswer(selected, correct) {
            if (answered) return;
            answered = true;
            
            const isCorrect = selected === correct;
            const explanation = document.getElementById('explanation');
            const resultText = document.getElementById('result-text');
            
            document.querySelectorAll('.option').forEach((btn, idx) => {
                btn.style.pointerEvents = 'none';
                if (idx === correct) {
                    btn.style.borderColor = '#10b981';
                    btn.style.background = '#d1fae5';
                } else if (idx === selected && !isCorrect) {
                    btn.style.borderColor = '#ef4444';
                    btn.style.background = '#fee2e2';
                }
            });
            
            explanation.className = 'explanation ' + (isCorrect ? 'correct' : 'incorrect');
            resultText.textContent = isCorrect ? '✓ Correct!' : '✗ Incorrect';
            
            if (isCorrect) {
                currentScore++;
                sessionStorage.setItem('{score_key}', currentScore.toString());
            }
            
            // Update next button with token
            const nextBtn = document.getElementById('next-btn');
            if (IS_LAST) {
                nextBtn.href = QuizToken.buildUrl('/quiz-complete.html', QUIZ_NAME, 'complete', currentScore);
            } else {
                nextBtn.href = QuizToken.buildUrl('{next_page}', QUIZ_NAME, QUESTION_NUM, currentScore);
            }
        }
    </script>
</body>
</html>'''

QUIZ_DATA = {
    "credit-basics": {"name": "Credit Basics", "color": "#6366f1", "color2": "#8b5cf6", "landing": "/credit-basics-quiz.html", "score_key": "cb_score"},
    "credit-cards": {"name": "Credit Cards", "color": "#10b981", "color2": "#34d399", "landing": "/credit-cards-quiz.html", "score_key": "cc_score"},
    "taxes": {"name": "Taxes", "color": "#f59e0b", "color2": "#fbbf24", "landing": "/taxes-quiz.html", "score_key": "tax_score"},
    "student-loans": {"name": "Student Loans", "color": "#3b82f6", "color2": "#60a5fa", "landing": "/student-loans-quiz.html", "score_key": "sl_score"},
    "investing": {"name": "Investing", "color": "#10b981", "color2": "#059669", "landing": "/investing-quiz.html", "score_key": "inv_score"},
    "make-money-online": {"name": "Make Money Online", "color": "#ec4899", "color2": "#f472b6", "landing": "/make-money-online-quiz.html", "score_key": "make_score"},
    "budgeting": {"name": "Budgeting", "color": "#8b5cf6", "color2": "#a78bfa", "landing": "/budgeting-quiz.html", "score_key": "bud_score"},
    "banking": {"name": "Banking", "color": "#3b82f6", "color2": "#2563eb", "landing": "/banking-quiz.html", "score_key": "bank_score"},
    "prediction-markets": {"name": "Prediction Markets", "color": "#f97316", "color2": "#fb923c", "landing": "/prediction-markets-quiz.html", "score_key": "pred_score"},
    "credit-rewards": {"name": "Credit Card Rewards", "color": "#10b981", "color2": "#84cc16", "landing": "/quiz-credit-rewards.html", "score_key": "reward_score"},
    "fed-rates": {"name": "Fed Rates", "color": "#0ea5e9", "color2": "#06b6d4", "landing": "/quiz-fed-rates.html", "score_key": "fed_score"},
    "auto-loans": {"name": "Auto Loans", "color": "#ef4444", "color2": "#f87171", "landing": "/auto-loans-quiz.html", "score_key": "auto_score"},
    "car-shopping": {"name": "Car Shopping", "color": "#f97316", "color2": "#fb923c", "landing": "/car-shopping-quiz.html", "score_key": "cars_score"},
    "auto-insurance": {"name": "Auto Insurance", "color": "#06b6d4", "color2": "#22d3ee", "landing": "/auto-insurance-quiz.html", "score_key": "auto_score"},
    "ai-skills": {"name": "AI Skills", "color": "#8b5cf6", "color2": "#a78bfa", "landing": "/ai-skills-quiz.html", "score_key": "aisk_score"},
    "glp1-effects": {"name": "GLP-1 Effects", "color": "#14b8a6", "color2": "#2dd4bf", "landing": "/glp1-effects-quiz.html", "score_key": "glp1_score"},
}

def extract_question_data(filepath):
    """Extract question data from existing quiz page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    data = {}
    
    # Extract quiz name from title
    title_match = re.search(r'<title>(.*?) - Question', content)
    if title_match:
        data['title'] = title_match.group(1)
    
    # Extract question
    q_match = re.search(r'<h2>(.*?)</h2>', content)
    if q_match:
        data['question'] = q_match.group(1)
    
    # Extract options
    opt_matches = re.findall(r'onclick="selectAnswer\(\d+, \d+\)">(.*?)</button>', content)
    data['options'] = opt_matches
    
    # Extract correct answer
    correct_match = re.search(r'selectAnswer\(\d+, (\d+)\)', content)
    if correct_match:
        data['correct'] = correct_match.group(1)
    
    # Extract explanation
    expl_match = re.search(r'<p>(.*?)</p>\s*<a href=', content, re.DOTALL)
    if expl_match:
        data['explanation'] = expl_match.group(1).strip()
    
    return data

def fix_quiz_page(filepath, quiz_id, q_num, total=10):
    """Fix a single quiz page with standard template."""
    quiz_info = QUIZ_DATA.get(quiz_id, {})
    if not quiz_info:
        print(f"Unknown quiz: {quiz_id}")
        return False
    
    # Extract existing data
    data = extract_question_data(filepath)
    
    # Determine next page
    is_last = q_num == total
    next_q = q_num + 1
    next_page = f"q{next_q}.html" if not is_last else "/quiz-complete.html"
    next_text = "Next Question →" if not is_last else "See Results →"
    progress = q_num * 10
    
    # Build HTML
    html = STANDARD_HEADER.format(
        title=f"{quiz_info['name']} Quiz - Question {q_num} of {total}",
        description=f"{quiz_info['name']} Quiz - Test your knowledge. Question {q_num} of {total}.",
        color=quiz_info['color'],
        color2=quiz_info['color2'],
        landing_page=quiz_info['landing'],
        quiz_name=quiz_info['name'],
        q_num=q_num,
        total=total,
        progress=progress,
        question=data.get('question', 'Question text'),
        opt0=data.get('options', ['Option 1', 'Option 2', 'Option 3', 'Option 4'])[0] if len(data.get('options', [])) > 0 else 'Option 1',
        opt1=data.get('options', ['Option 1', 'Option 2', 'Option 3', 'Option 4'])[1] if len(data.get('options', [])) > 1 else 'Option 2',
        opt2=data.get('options', ['Option 1', 'Option 2', 'Option 3', 'Option 4'])[2] if len(data.get('options', [])) > 2 else 'Option 3',
        opt3=data.get('options', ['Option 1', 'Option 2', 'Option 3', 'Option 4'])[3] if len(data.get('options', [])) > 3 else 'Option 4',
        correct=data.get('correct', '0'),
        explanation=data.get('explanation', 'Explanation text'),
        next_page=next_page,
        next_text=next_text,
        quiz_id=quiz_id,
        is_last=str(is_last).lower(),
        score_key=quiz_info['score_key']
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return True

def main():
    """Fix all quiz pages."""
    base_dir = "/root/.openclaw/workspace/triviacaptain-website/quiz"
    
    fixed = 0
    for quiz_id in QUIZ_DATA.keys():
        quiz_dir = os.path.join(base_dir, quiz_id)
        if not os.path.exists(quiz_dir):
            continue
        
        for q_num in range(1, 11):
            filepath = os.path.join(quiz_dir, f"q{q_num}.html")
            if os.path.exists(filepath):
                if fix_quiz_page(filepath, quiz_id, q_num):
                    fixed += 1
                    print(f"Fixed: {quiz_id}/q{q_num}.html")
    
    print(f"\nFixed {fixed} quiz pages")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Complete rebuild of quiz pages with simple working JavaScript."""

import os
import glob

# Simple working HTML template
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{quiz_name} Quiz - Question {q_num} of 10</title>
    <meta name="description" content="{quiz_name} Quiz - Question {q_num} of 10">
    <meta name="robots" content="noindex, nofollow">
    <link rel="stylesheet" href="/styles.css">
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
        .option.correct {{ border-color: #10b981; background: #d1fae5; }}
        .option.wrong {{ border-color: #ef4444; background: #fee2e2; }}
        .explanation {{ margin-top: 24px; padding: 20px; border-radius: 12px; display: none; }}
        .explanation.correct {{ background: #d1fae5; border: 1px solid #10b981; display: block; }}
        .explanation.incorrect {{ background: #fee2e2; border: 1px solid #ef4444; display: block; }}
        .next-btn {{ margin-top: 16px; background: {color}; color: white; border: none; padding: 14px 28px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 1rem; text-decoration: none; display: inline-block; }}
        .ad-container {{ max-width: 700px; margin: 32px auto; text-align: center; }}
        .ad-label {{ font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-bottom: 8px; }}
    </style>
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

    <section class="quiz-page">
        <div class="container">
            <div class="quiz-container">
                <div class="quiz-header">
                    <span class="category-tag">{quiz_name} - Question {q_num} of 10</span>
                </div>
                
                <div class="progress-container">
                    <div class="progress-bar-bg">
                        <div class="progress-bar" style="width: {progress}%;"></div>
                    </div>
                    <div class="progress-text">Question {q_num} of 10</div>
                </div>
                
                <div class="question-container">
                    <h2>{question}</h2>
                    <div class="options-list" id="options">
                        <button class="option" onclick="checkAnswer(0)">{opt0}</button>
                        <button class="option" onclick="checkAnswer(1)">{opt1}</button>
                        <button class="option" onclick="checkAnswer(2)">{opt2}</button>
                        <button class="option" onclick="checkAnswer(3)">{opt3}</button>
                    </div>
                    
                    <div id="explanation" class="explanation">
                        <h4 id="result-text"></h4>
                        <p>{explanation}</p>
                        <a href="{next_url}" class="next-btn">{next_text}</a>
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

    <footer class="footer" style="background: #0f0d2e; color: white; padding: 60px 0 30px;">
        <div class="container">
            <div class="footer-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 40px; margin-bottom: 40px;">
                <div class="footer-brand">
                    <h3 style="font-size: 1.25rem; margin-bottom: 16px;">💳 Credit Gamer Area</h3>
                    <p style="color: #94a3b8; font-size: 0.875rem;">Helping gamers master credit and finance.</p>
                </div>
                <div class="footer-links">
                    <h4 style="font-size: 1rem; margin-bottom: 16px;">Learn</h4>
                    <ul style="list-style: none; padding: 0;">
                        <li><a href="/credit-basics-quiz.html" style="color: #94a3b8; text-decoration: none;">Credit Basics</a></li>
                        <li><a href="/investing-quiz.html" style="color: #94a3b8; text-decoration: none;">Investing</a></li>
                        <li><a href="/quizzes/" style="color: #94a3b8; text-decoration: none;">All Quizzes</a></li>
                    </ul>
                </div>
            </div>
            <p style="text-align: center; color: #64748b;">&copy; 2026 Credit Gamer Area</p>
        </div>
    </footer>

    <script>
        const correctAnswer = {correct};
        let answered = false;
        
        function checkAnswer(selected) {
            if (answered) return;
            answered = true;
            
            const isCorrect = selected === correctAnswer;
            const explanation = document.getElementById('explanation');
            const resultText = document.getElementById('result-text');
            const options = document.querySelectorAll('.option');
            
            // Style the buttons
            options[correctAnswer].classList.add('correct');
            if (!isCorrect) {
                options[selected].classList.add('wrong');
            }
            
            // Disable all buttons
            options.forEach(btn => btn.style.pointerEvents = 'none');
            
            // Show explanation
            explanation.style.display = 'block';
            resultText.textContent = isCorrect ? '✓ Correct!' : '✗ Incorrect';
        }
    </script>
</body>
</html>'''

QUIZ_DATA = {
    "credit-basics": {"name": "Credit Basics", "color": "#6366f1", "color2": "#8b5cf6"},
    "credit-cards": {"name": "Credit Cards", "color": "#10b981", "color2": "#34d399"},
    "taxes": {"name": "Taxes", "color": "#f59e0b", "color2": "#fbbf24"},
    "student-loans": {"name": "Student Loans", "color": "#3b82f6", "color2": "#60a5fa"},
    "investing": {"name": "Investing", "color": "#10b981", "color2": "#059669"},
    "make-money-online": {"name": "Make Money Online", "color": "#ec4899", "color2": "#f472b6"},
    "budgeting": {"name": "Budgeting", "color": "#8b5cf6", "color2": "#a78bfa"},
    "banking": {"name": "Banking", "color": "#3b82f6", "color2": "#2563eb"},
    "prediction-markets": {"name": "Prediction Markets", "color": "#f97316", "color2": "#fb923c"},
    "credit-rewards": {"name": "Credit Card Rewards", "color": "#10b981", "color2": "#84cc16"},
    "fed-rates": {"name": "Fed Rates", "color": "#0ea5e9", "color2": "#06b6d4"},
    "auto-loans": {"name": "Auto Loans", "color": "#ef4444", "color2": "#f87171"},
    "car-shopping": {"name": "Car Shopping", "color": "#f97316", "color2": "#fb923c"},
    "auto-insurance": {"name": "Auto Insurance", "color": "#06b6d4", "color2": "#22d3ee"},
    "ai-skills": {"name": "AI Skills", "color": "#8b5cf6", "color2": "#a78bfa"},
    "glp1-effects": {"name": "GLP-1 Effects", "color": "#14b8a6", "color2": "#2dd4bf"},
}

def extract_question_data(filepath):
    """Extract question data from existing quiz page."""
    import re
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    data = {}
    
    # Extract question
    q_match = re.search(r'<h2>(.*?)</h2>', content)
    if q_match:
        data['question'] = q_match.group(1)
    
    # Extract options
    opt_matches = re.findall(r'onclick="checkAnswer\(\d+\)"\s*\u003e([^\u003c]+)<', content)
    if not opt_matches:
        opt_matches = re.findall(r'onclick="selectAnswer\(\d+, \d+\)"\s*\u003e([^\u003c]+)<', content)
    data['options'] = [o.strip() for o in opt_matches]
    
    # Extract correct answer
    correct_match = re.search(r'const correctAnswer = (\d+)', content)
    if not correct_match:
        correct_match = re.search(r'selectAnswer\(\d+, (\d+)\)', content)
    if correct_match:
        data['correct'] = correct_match.group(1)
    else:
        data['correct'] = '0'
    
    # Extract explanation
    expl_match = re.search(r'<p>([^\u003c]+)</p>\s*<a href=', content)
    if expl_match:
        data['explanation'] = expl_match.group(1).strip()
    else:
        data['explanation'] = 'Explanation text'
    
    return data

def rebuild_quiz_page(filepath, quiz_id, q_num):
    """Rebuild a quiz page with simple working JavaScript."""
    quiz_info = QUIZ_DATA.get(quiz_id, {"name": quiz_id, "color": "#6366f1", "color2": "#8b5cf6"})
    
    # Extract existing data
    data = extract_question_data(filepath)
    
    # Ensure we have 4 options
    options = data.get('options', ['Option 1', 'Option 2', 'Option 3', 'Option 4'])
    while len(options) < 4:
        options.append(f'Option {len(options) + 1}')
    
    # Determine next URL
    is_last = q_num == 10
    if is_last:
        next_url = '/quiz-complete.html'
        next_text = 'See Results →'
    else:
        next_url = f'q{q_num + 1}.html'
        next_text = 'Next Question →'
    
    # Build HTML
    html = HTML_TEMPLATE.format(
        quiz_name=quiz_info['name'],
        q_num=q_num,
        color=quiz_info['color'],
        color2=quiz_info['color2'],
        progress=q_num * 10,
        question=data.get('question', 'Question text'),
        opt0=options[0],
        opt1=options[1],
        opt2=options[2],
        opt3=options[3],
        correct=data.get('correct', '0'),
        explanation=data.get('explanation', 'Explanation'),
        next_url=next_url,
        next_text=next_text
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return True

def main():
    """Rebuild all quiz pages."""
    base_dir = "/root/.openclaw/workspace/triviacaptain-website/quiz"
    
    fixed = 0
    for quiz_id in QUIZ_DATA.keys():
        quiz_dir = os.path.join(base_dir, quiz_id)
        if not os.path.exists(quiz_dir):
            continue
        
        for q_num in range(1, 11):
            filepath = os.path.join(quiz_dir, f"q{q_num}.html")
            if os.path.exists(filepath):
                if rebuild_quiz_page(filepath, quiz_id, q_num):
                    fixed += 1
    
    print(f"✅ Rebuilt {fixed} quiz pages with simple working JavaScript")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Add proper header and footer to all quiz pages."""

import os
import glob
import re

HEADER = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="robots" content="noindex, nofollow">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💳</text></svg>">
    <link rel="stylesheet" href="/styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
    <style>
        .quiz-page { padding: 40px 0; min-height: calc(100vh - 300px); }
        .quiz-container { max-width: 700px; margin: 0 auto; background: white; border-radius: 16px; padding: 40px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
        .quiz-header { text-align: center; margin-bottom: 32px; }
        .category-tag { display: inline-block; background: {color}; color: white; padding: 6px 16px; border-radius: 20px; font-size: 0.875rem; font-weight: 600; margin-bottom: 16px; }
        .progress-container { margin-bottom: 32px; }
        .progress-bar-bg { background: #e2e8f0; height: 8px; border-radius: 4px; overflow: hidden; }
        .progress-bar { background: linear-gradient(90deg, {color}, {color2}); height: 100%; border-radius: 4px; transition: width 0.3s ease; }
        .progress-text { font-size: 0.875rem; color: #64748b; margin-top: 8px; text-align: center; }
        .question { font-size: 1.5rem; margin: 24px 0; line-height: 1.5; font-weight: 600; }
        .option { display: block; width: 100%; padding: 16px 20px; margin: 8px 0; border: 2px solid #e2e8f0; border-radius: 12px; background: white; cursor: pointer; font-size: 1rem; text-align: left; transition: all 0.2s; }
        .option:hover { border-color: {color}; background: #f8fafc; }
        .option.correct { background: #d1fae5; border-color: #10b981; }
        .option.wrong { background: #fee2e2; border-color: #ef4444; }
        .explanation { display: none; margin-top: 24px; padding: 20px; border-radius: 12px; background: #f8fafc; border: 1px solid #e2e8f0; }
        .explanation.show { display: block; }
        .explanation strong { font-size: 1.125rem; }
        .next-btn { display: inline-block; margin-top: 16px; padding: 14px 28px; background: {color}; color: white; text-decoration: none; border-radius: 8px; font-weight: 600; transition: opacity 0.2s; }
        .next-btn:hover { opacity: 0.9; }
        .ad-container { max-width: 700px; margin: 32px auto; text-align: center; }
        .ad-label { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px; }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <a href="/" class="logo">💳 Credit Gamer Area</a>
            <ul class="nav-links">
                <li><a href="/quizzes/">Quizzes</a></li>
                <li><a href="/blog/">Blog</a></li>
                <li><a href="/resources.html">Resources</a></li>
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
                
                <div class="question">{question}</div>
                
                <button class="option" id="opt0" onclick="answer(0)">{opt0}</button>
                <button class="option" id="opt1" onclick="answer(1)">{opt1}</button>
                <button class="option" id="opt2" onclick="answer(2)">{opt2}</button>
                <button class="option" id="opt3" onclick="answer(3)">{opt3}</button>
                
                <div id="exp" class="explanation">
                    <strong id="res"></strong><br><br>
                    {explanation}<br><br>
                    <a href="{next_url}" class="next-btn">{next_text} →</a>
                </div>
            </div>
            
            <div class="ad-container">
                <div class="ad-label">Advertisement</div>
                <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins>
                <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
            </div>
        </div>
    </section>

    <footer class="footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <h3>💳 Credit Gamer Area</h3>
                    <p>Helping gamers and young adults master credit, finance, and money-making skills through fun, interactive quizzes.</p>
                    <div class="social-links">
                        <a href="#">Twitter</a>
                        <a href="#">Discord</a>
                    </div>
                </div>
                
                <div class="footer-links">
                    <h4>Learn</h4>
                    <ul>
                        <li><a href="/credit-basics-quiz.html">Credit Basics</a></li>
                        <li><a href="/credit-cards-quiz.html">Credit Cards</a></li>
                        <li><a href="/taxes-quiz.html">Taxes</a></li>
                        <li><a href="/investing-quiz.html">Investing</a></li>
                        <li><a href="/student-loans-quiz.html">Student Loans</a></li>
                        <li><a href="/budgeting-quiz.html">Budgeting</a></li>
                        <li><a href="/banking-quiz.html">Banking</a></li>
                        <li><a href="/make-money-online-quiz.html">Make Money Online</a></li>
                    </ul>
                </div>
                
                <div class="footer-links">
                    <h4>Company</h4>
                    <ul>
                        <li><a href="/about.html">About Us</a></li>
                        <li><a href="/blog/">Blog</a></li>
                        <li><a href="/contact.html">Contact</a></li>
                        <li><a href="/privacy.html">Privacy Policy</a></li>
                        <li><a href="/terms.html">Terms of Service</a></li>
                    </ul>
                </div>
                
                <div class="footer-links">
                    <h4>Resources</h4>
                    <ul>
                        <li><a href="/quizzes/">All Quizzes</a></li>
                        <li><a href="/resources.html">Financial Calculators</a></li>
                        <li><a href="/faq.html">FAQ</a></li>
                        <li><a href="/sitemap.html">Sitemap</a></li>
                        <li><a href="/blog/">Credit Guides</a></li>
                        <li><a href="/blog/">Money Tips</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>&copy; 2026 Credit Gamer Area. All rights reserved. | Not financial advice</p>
            </div>
        </div>
    </footer>

    <script>
        var correct = {correct};
        var answered = false;
        function answer(n) {{
            if (answered) return;
            answered = true;
            document.getElementById('opt' + correct).classList.add('correct');
            if (n != correct) document.getElementById('opt' + n).classList.add('wrong');
            document.getElementById('exp').classList.add('show');
            document.getElementById('res').textContent = (n == correct) ? '✓ Correct!' : '✗ Incorrect';
        }}
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

def extract_quiz_data(filepath):
    """Extract data from existing quiz page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    data = {}
    
    # Extract question
    q = re.search(r'<div class="question"[^>]*>(.*?)</div>', content, re.DOTALL)
    if q:
        data['question'] = q.group(1).strip()
    else:
        data['question'] = 'Question'
    
    # Extract options
    opts = re.findall(r'id="opt\d+"[^>]*>([^<]+)</button>', content)
    data['options'] = [o.strip() for o in opts]
    while len(data['options']) < 4:
        data['options'].append(f'Option {len(data["options"])+1}')
    
    # Extract correct answer
    c = re.search(r'var correct = (\d+)', content)
    data['correct'] = c.group(1) if c else '0'
    
    # Extract explanation
    e = re.search(r'<div id="exp"[^>]*>.*?<strong id="res"></strong><br><br>([^<]+)', content, re.DOTALL)
    if e:
        data['explanation'] = e.group(1).strip()
    else:
        data['explanation'] = 'Explanation'
    
    return data

def rebuild_page(filepath, quiz_id, q_num):
    """Rebuild a quiz page with proper header and footer."""
    info = QUIZ_DATA.get(quiz_id, {"name": quiz_id, "color": "#6366f1", "color2": "#8b5cf6"})
    data = extract_quiz_data(filepath)
    
    if q_num == 10:
        next_url = '/quiz-complete.html'
        next_text = 'See Results'
    else:
        next_url = f'q{q_num+1}.html'
        next_text = 'Next Question'
    
    # Use safe substitution to avoid issues with CSS curly braces
    html = HEADER.replace('{title}', f"{info['name']} Quiz - Question {q_num} of 10")
    html = html.replace('{description}', f"Test your knowledge of {info['name']} - Question {q_num} of 10")
    html = html.replace('{color}', info['color'])
    html = html.replace('{color2}', info['color2'])
    html = html.replace('{quiz_name}', info['name'])
    html = html.replace('{q_num}', str(q_num))
    html = html.replace('{progress}', str(q_num * 10))
    html = html.replace('{question}', data['question'])
    html = html.replace('{opt0}', data['options'][0])
    html = html.replace('{opt1}', data['options'][1])
    html = html.replace('{opt2}', data['options'][2])
    html = html.replace('{opt3}', data['options'][3])
    html = html.replace('{correct}', data['correct'])
    html = html.replace('{explanation}', data['explanation'])
    html = html.replace('{next_url}', next_url)
    html = html.replace('{next_text}', next_text)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return True

def main():
    base_dir = "/root/.openclaw/workspace/triviacaptain-website/quiz"
    
    fixed = 0
    for quiz_id in QUIZ_DATA.keys():
        for q_num in range(1, 11):
            filepath = os.path.join(base_dir, quiz_id, f"q{q_num}.html")
            if os.path.exists(filepath):
                if rebuild_page(filepath, quiz_id, q_num):
                    fixed += 1
    
    print(f"✅ Rebuilt {fixed} quiz pages with proper header and footer")

if __name__ == "__main__":
    main()

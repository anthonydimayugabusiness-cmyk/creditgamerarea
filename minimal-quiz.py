#!/usr/bin/env python3
"""Create minimal working quiz pages."""

import os
import glob
import re

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

def extract_data(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    data = {}
    q = re.search(r'<h2>([^\u003c]+)</h2>', content)
    if q:
        data['question'] = q.group(1).strip()
    
    opts = re.findall(r'checkAnswer\(\d+\)"\s*\u003e([^\u003c]+)', content)
    if not opts:
        opts = re.findall(r'selectAnswer\(\d+, \d+\)"\s*\u003e([^\u003c]+)', content)
    data['options'] = [o.strip() for o in opts]
    
    c = re.search(r'correctAnswer\s*=\s*(\d+)', content)
    if not c:
        c = re.search(r'selectAnswer\(\d+,\s*(\d+)\)', content)
    data['correct'] = c.group(1) if c else '0'
    
    e = re.search(r'explanation.*?\u003cp\u003e([^\u003c]+)', content, re.DOTALL)
    data['explanation'] = e.group(1).strip() if e else 'Explanation'
    
    return data

def create_page(filepath, quiz_id, q_num):
    info = QUIZ_DATA.get(quiz_id, {"name": quiz_id, "color": "#6366f1", "color2": "#8b5cf6"})
    data = extract_data(filepath)
    
    opts = data.get('options', ['A', 'B', 'C', 'D'])
    while len(opts) < 4:
        opts.append(f'Option {len(opts)+1}')
    
    correct = int(data.get('correct', 0))
    
    if q_num == 10:
        next_url = '/quiz-complete.html'
        next_text = 'See Results'
    else:
        next_url = f'q{q_num+1}.html'
        next_text = 'Next Question'
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{info['name']} - Question {q_num}</title>
<link rel="stylesheet" href="/styles.css">
<style>
.quiz-container {{ max-width: 700px; margin: 40px auto; background: white; padding: 40px; border-radius: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
.category-tag {{ background: {info['color']}; color: white; padding: 6px 16px; border-radius: 20px; font-size: 0.875rem; font-weight: 600; display: inline-block; margin-bottom: 16px; }}
.question {{ font-size: 1.5rem; margin: 24px 0; }}
.option {{ display: block; width: 100%; padding: 16px; margin: 8px 0; border: 2px solid #e2e8f0; border-radius: 12px; background: white; cursor: pointer; font-size: 1rem; text-align: left; }}
.option:hover {{ border-color: {info['color']}; }}
.option.correct {{ background: #d1fae5; border-color: #10b981; }}
.option.wrong {{ background: #fee2e2; border-color: #ef4444; }}
.explanation {{ display: none; margin-top: 24px; padding: 20px; border-radius: 12px; }}
.explanation.show {{ display: block; }}
.next-btn {{ display: inline-block; margin-top: 16px; padding: 14px 28px; background: {info['color']}; color: white; text-decoration: none; border-radius: 8px; font-weight: 600; }}
</style>
</head>
<body>

<nav class="navbar"><div class="container"><a href="/" class="logo">💳 Credit Gamer Area</a></div></nav>

<div class="quiz-container">
<span class="category-tag">{info['name']} - Question {q_num} of 10</span>
<div class="question">{data.get('question', 'Question')}</div>

<button class="option" id="opt0" onclick="answer(0)">{opts[0]}</button>
<button class="option" id="opt1" onclick="answer(1)">{opts[1]}</button>
<button class="option" id="opt2" onclick="answer(2)">{opts[2]}</button>
<button class="option" id="opt3" onclick="answer(3)">{opts[3]}</button>

<div id="exp" class="explanation">
<strong id="res"></strong><br><br>
{data.get('explanation', 'Explanation')}<br><br>
<a href="{next_url}" class="next-btn">{next_text} →</a>
</div>
</div>

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
</html>"""
    
    with open(filepath, 'w') as f:
        f.write(html.strip())
    return True

def main():
    base = "/root/.openclaw/workspace/triviacaptain-website/quiz"
    for qid in QUIZ_DATA:
        for n in range(1, 11):
            p = f"{base}/{qid}/q{n}.html"
            if os.path.exists(p):
                create_page(p, qid, n)
                print(f"Fixed: {qid}/q{n}")
    print("\n✅ All quizzes rebuilt with minimal working code")

if __name__ == "__main__":
    main()

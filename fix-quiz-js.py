#!/usr/bin/env python3
"""Fix all quiz pages - rewrite JavaScript completely."""

import os
import glob
import re

# Clean JavaScript template
JS_TEMPLATE = """    <script>
        const QUIZ_NAME = '{quiz_id}';
        const QUESTION_NUM = {q_num};
        const IS_LAST = {is_last};
        const SCORE_KEY = '{score_key}';
        
        let answered = false;
        let currentScore = 0;
        
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {
            // Get or initialize score
            const savedScore = sessionStorage.getItem(SCORE_KEY);
            if (savedScore) {
                currentScore = parseInt(savedScore);
            } else if (QUESTION_NUM === 1) {
                sessionStorage.setItem(SCORE_KEY, '0');
            }
            
            // Check token for subsequent questions
            if (QUESTION_NUM > 1) {
                const params = QuizToken.getParams();
                if (!params.token || !QuizToken.validate(params.token, QUIZ_NAME, QUESTION_NUM - 1, params.score)) {
                    document.getElementById('quiz-content').style.display = 'none';
                    document.getElementById('error-msg').style.display = 'block';
                    return;
                }
                currentScore = parseInt(params.score) || 0;
                sessionStorage.setItem(SCORE_KEY, currentScore.toString());
            }
        });
        
        function selectAnswer(selected, correct) {
            if (answered) return;
            answered = true;
            
            const isCorrect = selected === correct;
            const explanation = document.getElementById('explanation');
            const resultText = document.getElementById('result-text');
            const nextBtn = document.getElementById('next-btn');
            
            // Style buttons
            document.querySelectorAll('.option').forEach(function(btn, idx) {
                btn.style.pointerEvents = 'none';
                if (idx === correct) {
                    btn.style.borderColor = '#10b981';
                    btn.style.background = '#d1fae5';
                } else if (idx === selected && !isCorrect) {
                    btn.style.borderColor = '#ef4444';
                    btn.style.background = '#fee2e2';
                }
            });
            
            // Show explanation
            explanation.className = 'explanation ' + (isCorrect ? 'correct' : 'incorrect');
            resultText.textContent = isCorrect ? '✓ Correct!' : '✗ Incorrect';
            
            // Update score
            if (isCorrect) {
                currentScore++;
                sessionStorage.setItem(SCORE_KEY, currentScore.toString());
            }
            
            // Set up next button with token
            var nextUrl;
            if (IS_LAST) {
                nextUrl = QuizToken.buildUrl('/quiz-complete.html', QUIZ_NAME, 'complete', currentScore);
            } else {
                nextUrl = QuizToken.buildUrl('q' + (QUESTION_NUM + 1) + '.html', QUIZ_NAME, QUESTION_NUM, currentScore);
            }
            nextBtn.href = nextUrl;
            nextBtn.onclick = function() {
                window.location.href = nextUrl;
                return false;
            };
        }
    </script>"""

def fix_quiz_page(filepath):
    """Fix a single quiz page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract quiz info from path
    parts = filepath.split('/')
    quiz_id = parts[-2] if len(parts) >= 2 else 'unknown'
    q_num = int(parts[-1].replace('q', '').replace('.html', '')) if len(parts) >= 1 else 1
    
    # Determine score key based on quiz_id
    score_keys = {
        'credit-basics': 'cb_score',
        'credit-cards': 'cc_score',
        'taxes': 'tax_score',
        'student-loans': 'sl_score',
        'investing': 'inv_score',
        'make-money-online': 'make_score',
        'budgeting': 'bud_score',
        'banking': 'bank_score',
        'prediction-markets': 'pred_score',
        'credit-rewards': 'reward_score',
        'fed-rates': 'fed_score',
        'auto-loans': 'auto_score',
        'car-shopping': 'cars_score',
        'auto-insurance': 'auto_score',
        'ai-skills': 'aisk_score',
        'glp1-effects': 'glp1_score',
    }
    score_key = score_keys.get(quiz_id, 'quiz_score')
    
    is_last = 'true' if q_num == 10 else 'false'
    next_q = q_num + 1
    
    # Remove all existing script tags
    content = re.sub(r'<script>.*?</script>', '', content, flags=re.DOTALL)
    
    # Add clean JavaScript before </body>
    js_code = JS_TEMPLATE.format(
        quiz_id=quiz_id,
        q_num=q_num,
        is_last=is_last,
        score_key=score_key,
        next_q=next_q
    )
    
    content = content.replace('</body>', js_code + '\n</body>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """Fix all quiz pages."""
    base_dir = "/root/.openclaw/workspace/triviacaptain-website/quiz"
    quiz_pages = glob.glob(os.path.join(base_dir, "*", "q*.html"))
    
    fixed = 0
    for filepath in quiz_pages:
        if fix_quiz_page(filepath):
            fixed += 1
            print(f"Fixed: {filepath}")
    
    print(f"\n✅ Fixed {fixed} quiz pages")

if __name__ == "__main__":
    main()

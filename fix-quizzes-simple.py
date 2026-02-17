#!/usr/bin/env python3
"""Fix all quiz pages - remove broken reCAPTCHA, fix navigation, standardize header/footer."""

import os
import glob
import re

# Quiz configuration
QUIZ_CONFIG = {
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

STANDARD_NAV = '''    <nav class="navbar">
        <div class="container">
            <a href="/" class="logo">💳 Credit Gamer Area</a>
            <ul class="nav-links">
                <li><a href="/quizzes/">Quizzes</a></li>
                <li><a href="/blog/">Blog</a></li>
            </ul>
        </div>
    </nav>'''

STANDARD_FOOTER = '''    <footer class="footer" style="background: #0f0d2e; color: white; padding: 60px 0 30px; margin-top: 40px;">
        <div class="container">
            <div class="footer-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 40px; margin-bottom: 40px;">
                <div class="footer-brand">
                    <h3 style="font-size: 1.25rem; margin-bottom: 16px;">💳 Credit Gamer Area</h3>
                    <p style="color: #94a3b8; font-size: 0.875rem; line-height: 1.6;">Helping gamers and young adults master credit, finance, and money-making skills through fun, interactive quizzes.</p>
                </div>
                
                <div class="footer-links">
                    <h4 style="font-size: 1rem; margin-bottom: 16px; color: white;">Learn</h4>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="margin-bottom: 8px;"><a href="/credit-basics-quiz.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Credit Basics</a></li>
                        <li style="margin-bottom: 8px;"><a href="/investing-quiz.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Investing</a></li>
                        <li style="margin-bottom: 8px;"><a href="/quizzes/" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">All Quizzes</a></li>
                    </ul>
                </div>
                
                <div class="footer-links">
                    <h4 style="font-size: 1rem; margin-bottom: 16px; color: white;">Resources</h4>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="margin-bottom: 8px;"><a href="/blog/" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Blog</a></li>
                        <li style="margin-bottom: 8px;"><a href="/resources.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Calculators</a></li>
                        <li style="margin-bottom: 8px;"><a href="/faq.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">FAQ</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-bottom" style="border-top: 1px solid #1e293b; padding-top: 20px; text-align: center;">
                <p style="color: #64748b; font-size: 0.875rem;">&copy; 2026 Credit Gamer Area. All rights reserved. | Not financial advice</p>
            </div>
        </div>
    </footer>'''

def remove_recaptcha(content):
    """Remove broken reCAPTCHA code."""
    # Remove reCAPTCHA script
    content = re.sub(r'<!-- reCAPTCHA v3 -->.*?grecaptcha\.ready.*?\}\);\s*\}\);\s*\u003c/script>', '', content, flags=re.DOTALL)
    # Remove reCAPTCHA validation code
    content = re.sub(r'// reCAPTCHA validation.*?callback\(true\);\s*\}', '', content, flags=re.DOTALL)
    content = re.sub(r'// Wrap selectAnswer.*?\}\);\s*\}\);', '', content, flags=re.DOTALL)
    return content

def fix_navigation(content, quiz_id, q_num):
    """Fix quiz navigation to properly build URLs with tokens."""
    # Fix goToNext function to properly use QuizToken
    old_pattern = r'function goToNext\(\) \{[^}]+\}'
    new_func = '''function goToNext() {
            if (answered) {
                const nextBtn = document.getElementById('next-btn');
                const href = nextBtn.getAttribute('href');
                if (href) window.location.href = href;
            }
        }'''
    content = re.sub(old_pattern, new_func, content, flags=re.DOTALL)
    return content

def standardize_header_footer(content):
    """Replace nav and footer with standardized versions."""
    # Replace nav
    content = re.sub(r'<nav class="navbar".*?</nav>', STANDARD_NAV, content, flags=re.DOTALL)
    # Replace footer
    content = re.sub(r'<footer class="footer".*?</footer>', STANDARD_FOOTER, content, flags=re.DOTALL)
    return content

def fix_quiz_page(filepath):
    """Fix a single quiz page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract quiz info from path
    parts = filepath.split('/')
    quiz_id = parts[-2] if len(parts) >= 2 else 'unknown'
    q_num = int(parts[-1].replace('q', '').replace('.html', '')) if len(parts) >= 1 else 1
    
    config = QUIZ_CONFIG.get(quiz_id, {})
    if not config:
        print(f"Warning: Unknown quiz {quiz_id}")
        return False
    
    # Apply fixes
    content = remove_recaptcha(content)
    content = fix_navigation(content, quiz_id, q_num)
    content = standardize_header_footer(content)
    
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
    print("\nChanges made:")
    print("- Removed broken reCAPTCHA code")
    print("- Fixed navigation to properly advance questions")
    print("- Standardized headers and footers")

if __name__ == "__main__":
    main()

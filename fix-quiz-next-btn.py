#!/usr/bin/env python3
"""Fix quiz pages - add href to next button in selectAnswer function."""

import os
import glob
import re

def fix_quiz_page(filepath):
    """Fix a single quiz page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract quiz info
    quiz_match = re.search(r"const QUIZ_NAME = '(.*?)'", content)
    q_num_match = re.search(r'const QUESTION_NUM = (\d+)', content)
    is_last_match = re.search(r'const IS_LAST = (\w+)', content)
    
    if not quiz_match or not q_num_match:
        print(f"Skipping {filepath} - missing quiz info")
        return False
    
    quiz_id = quiz_match.group(1)
    q_num = int(q_num_match.group(1))
    is_last = is_last_match.group(1) if is_last_match else 'false'
    
    # Determine next page
    if is_last == 'true':
        next_page = '/quiz-complete.html'
    else:
        next_page = f"q{q_num + 1}.html"
    
    # Fix the selectAnswer function to set href
    old_pattern = r"(if \(isCorrect\) \{\s*currentScore\+\+;\s*sessionStorage\.setItem\([^)]+\);\s*\})"
    new_code = r"""\1
            
            // Set up next button URL
            const nextBtn = document.getElementById('next-btn');
            nextBtn.setAttribute('href', QuizToken.buildUrl('""" + next_page + """', QUIZ_NAME, QUESTION_NUM, currentScore));"""
    
    content = re.sub(old_pattern, new_code, content)
    
    # Simplify goToNext function
    old_gotonext = r"function goToNext\(\) \{[^}]+\}[^}]*\}"
    new_gotonext = """function goToNext() {
            if (answered) {
                const nextBtn = document.getElementById('next-btn');
                const href = nextBtn.getAttribute('href');
                if (href) {
                    window.location.href = href;
                }
            }
        }"""
    
    content = re.sub(old_gotonext, new_gotonext, content, flags=re.DOTALL)
    
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

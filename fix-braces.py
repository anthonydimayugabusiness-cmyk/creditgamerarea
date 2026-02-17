#!/usr/bin/env python3
"""Fix extra closing brace in all quiz pages."""

import os
import glob

def fix_quiz_page(filepath):
    """Fix a single quiz page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the extra closing brace before </script>
    content = content.replace('        }\n        }\n    \u003c/script>', '        }\n    \u003c/script>')
    content = content.replace('        }\n        }\n\n    \u003c/script>', '        }\n    \u003c/script>')
    
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
    
    print(f"✅ Fixed {fixed} quiz pages")

if __name__ == "__main__":
    main()

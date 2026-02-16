#!/usr/bin/env python3
"""Fix double footer issue on quiz pages."""

import os
import glob
import re

def fix_double_footer(filepath):
    """Remove the simple footer, keep the 4-column footer."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if has double footer
    if content.count('<footer class="footer"') >= 2:
        # Remove the simple footer (the one with just copyright)
        content = re.sub(
            r'<footer class="footer" style="background: #1e1b4b; color: white; padding: 40px 0; text-align: center;">\s*<div class="container">\s*<p>&copy; 2026 Credit Gamer Area\. All rights reserved\.</p>\s*</div>\s*</footer>',
            '',
            content
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    """Fix all quiz pages."""
    base_dir = "/root/.openclaw/workspace/triviacaptain-website"
    
    # Find all quiz question pages
    quiz_pages = glob.glob(os.path.join(base_dir, "quiz", "*", "q*.html"))
    
    updated = 0
    for filepath in quiz_pages:
        if fix_double_footer(filepath):
            updated += 1
            print(f"Fixed: {filepath}")
    
    print(f"\nFixed {updated} quiz pages with double footer")

if __name__ == "__main__":
    main()

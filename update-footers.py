#!/usr/bin/env python3
"""Update all HTML pages with the consistent footer format."""

import os
import re
import glob

# New footer HTML to replace existing footers
NEW_FOOTER = '''    <footer class="footer" style="background: #0f0d2e; color: white; padding: 60px 0 30px;">
        <div class="container">
            <div class="footer-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 40px; margin-bottom: 40px;">
                <div class="footer-brand">
                    <h3 style="font-size: 1.5rem; margin-bottom: 16px;">💳 Credit Gamer Area</h3>
                    <p style="opacity: 0.7; line-height: 1.6; margin-bottom: 16px;">Helping gamers and young adults master credit, finance, and money-making skills through fun, interactive quizzes.</p>
                    <div class="social-links" style="display: flex; gap: 12px; flex-wrap: wrap;">
                        <a href="#" style="color: #6366f1; text-decoration: none;">Twitter</a>
                        <a href="#" style="color: #6366f1; text-decoration: none;">Instagram</a>
                        <a href="#" style="color: #6366f1; text-decoration: none;">TikTok</a>
                        <a href="#" style="color: #6366f1; text-decoration: none;">Discord</a>
                    </div>
                </div>
                
                <div class="footer-links">
                    <h4 style="font-size: 1rem; margin-bottom: 16px; font-weight: 600;">Learn</h4>
                    <ul style="list-style: none;">
                        <li style="margin-bottom: 8px;"><a href="/credit-basics-quiz.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">Credit Basics</a></li>
                        <li style="margin-bottom: 8px;"><a href="/credit-cards-quiz.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">Credit Cards</a></li>
                        <li style="margin-bottom: 8px;"><a href="/taxes-quiz.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">Taxes</a></li>
                        <li style="margin-bottom: 8px;"><a href="/investing-quiz.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">Investing</a></li>
                        <li style="margin-bottom: 8px;"><a href="/student-loans-quiz.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">Student Loans</a></li>
                        <li style="margin-bottom: 8px;"><a href="/budgeting-quiz.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">Budgeting</a></li>
                        <li style="margin-bottom: 8px;"><a href="/banking-quiz.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">Banking</a></li>
                        <li style="margin-bottom: 8px;"><a href="/make-money-online-quiz.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">Make Money Online</a></li>
                    </ul>
                </div>
                
                <div class="footer-links">
                    <h4 style="font-size: 1rem; margin-bottom: 16px; font-weight: 600;">Company</h4>
                    <ul style="list-style: none;">
                        <li style="margin-bottom: 8px;"><a href="/about.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">About Us</a></li>
                        <li style="margin-bottom: 8px;"><a href="/blog-build-credit.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">Blog</a></li>
                        <li style="margin-bottom: 8px;"><a href="/contact.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">Contact</a></li>
                        <li style="margin-bottom: 8px;"><a href="/privacy.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">Privacy Policy</a></li>
                        <li style="margin-bottom: 8px;"><a href="/terms.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">Terms of Service</a></li>
                    </ul>
                </div>
                
                <div class="footer-links">
                    <h4 style="font-size: 1rem; margin-bottom: 16px; font-weight: 600;">Resources</h4>
                    <ul style="list-style: none;">
                        <li style="margin-bottom: 8px;"><a href="/quizzes/" style="color: rgba(255,255,255,0.7); text-decoration: none;">All Quizzes</a></li>
                        <li style="margin-bottom: 8px;"><a href="/resources.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">Financial Calculators</a></li>
                        <li style="margin-bottom: 8px;"><a href="/faq.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">FAQ</a></li>
                        <li style="margin-bottom: 8px;"><a href="/sitemap.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">Sitemap</a></li>
                        <li style="margin-bottom: 8px;"><a href="/blog-build-credit.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">Credit Guides</a></li>
                        <li style="margin-bottom: 8px;"><a href="/blog-make-money.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">Money Tips</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-bottom" style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 30px; text-align: center; opacity: 0.6;">
                <p>&copy; 2026 Credit Gamer Area. All rights reserved. | Not financial advice</p>
            </div>
        </div>
    </footer>'''

def update_footer_in_file(filepath):
    """Replace the footer in a single HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace footer - match various footer patterns
        # Pattern 1: Simple footer with just copyright
        pattern1 = r'<footer[^>]*>.*?&copy;.*?Credit Gamer Area.*?</footer>'
        
        # Pattern 2: Footer with footer-bottom class
        pattern2 = r'<footer[^>]*>.*?<div[^>]*class="footer-bottom".*?</footer>'
        
        # Pattern 3: Any footer tag (more general)
        pattern3 = r'<footer[^>]*>.*?</footer>'
        
        # Try patterns in order of specificity
        if re.search(pattern1, content, re.DOTALL | re.IGNORECASE):
            new_content = re.sub(pattern1, NEW_FOOTER, content, flags=re.DOTALL | re.IGNORECASE)
            return True, "Pattern 1"
        elif re.search(pattern2, content, re.DOTALL | re.IGNORECASE):
            new_content = re.sub(pattern2, NEW_FOOTER, content, flags=re.DOTALL | re.IGNORECASE)
            return True, "Pattern 2"
        elif re.search(pattern3, content, re.DOTALL | re.IGNORECASE):
            new_content = re.sub(pattern3, NEW_FOOTER, content, flags=re.DOTALL | re.IGNORECASE)
            return True, "Pattern 3"
        else:
            # No footer found - add one before </body>
            if '</body>' in content:
                new_content = content.replace('</body>', NEW_FOOTER + '\n</body>')
                return True, "Added new"
            return False, "No footer or body tag found"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "Updated"
        
    except Exception as e:
        return False, str(e)

def main():
    """Update footers in all HTML files."""
    base_dir = "/root/.openclaw/workspace/triviacaptain-website"
    
    # Find all HTML files
    html_files = []
    for pattern in ['*.html', 'blog/*.html', 'quiz/**/*.html']:
        html_files.extend(glob.glob(os.path.join(base_dir, pattern), recursive=True))
    
    # Remove duplicates and sort
    html_files = sorted(set(html_files))
    
    updated = []
    failed = []
    
    for filepath in html_files:
        filename = os.path.basename(filepath)
        success, msg = update_footer_in_file(filepath)
        
        if success:
            updated.append(filename)
            print(f"✅ {filename}: {msg}")
        else:
            failed.append((filename, msg))
            print(f"❌ {filename}: {msg}")
    
    print(f"\n{'='*60}")
    print(f"Updated: {len(updated)} files")
    print(f"Failed: {len(failed)} files")
    
    if failed:
        print("\nFailed files:")
        for fname, msg in failed:
            print(f"  - {fname}: {msg}")

if __name__ == "__main__":
    main()

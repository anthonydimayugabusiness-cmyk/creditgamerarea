#!/usr/bin/env python3
"""Add 4-column footer to all quiz question pages."""

import os
import glob

# The proper 4-column footer to insert before </body>
FOOTER_HTML = '''
    <!-- Footer -->
    <footer class="footer" style="background: #0f0d2e; color: white; padding: 60px 0 30px; margin-top: 40px;">
        <div class="container">
            <div class="footer-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 40px; margin-bottom: 40px;">
                <div class="footer-brand">
                    <h3 style="font-size: 1.25rem; margin-bottom: 16px;">💳 Credit Gamer Area</h3>
                    <p style="color: #94a3b8; font-size: 0.875rem; line-height: 1.6; margin-bottom: 20px;">Helping gamers and young adults master credit, finance, and money-making skills through fun, interactive quizzes.</p>
                </div>
                
                <div class="footer-links">
                    <h4 style="font-size: 1rem; margin-bottom: 16px; color: white;">Learn</h4>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="margin-bottom: 8px;"><a href="/credit-basics-quiz.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Credit Basics</a></li>
                        <li style="margin-bottom: 8px;"><a href="/credit-cards-quiz.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Credit Cards</a></li>
                        <li style="margin-bottom: 8px;"><a href="/taxes-quiz.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Taxes</a></li>
                        <li style="margin-bottom: 8px;"><a href="/investing-quiz.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Investing</a></li>
                        <li style="margin-bottom: 8px;"><a href="/student-loans-quiz.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Student Loans</a></li>
                        <li style="margin-bottom: 8px;"><a href="/budgeting-quiz.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Budgeting</a></li>
                        <li style="margin-bottom: 8px;"><a href="/banking-quiz.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Banking</a></li>
                        <li style="margin-bottom: 8px;"><a href="/make-money-online-quiz.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Make Money Online</a></li>
                    </ul>
                </div>
                
                <div class="footer-links">
                    <h4 style="font-size: 1rem; margin-bottom: 16px; color: white;">Company</h4>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="margin-bottom: 8px;"><a href="/about.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">About Us</a></li>
                        <li style="margin-bottom: 8px;"><a href="/blog-build-credit.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Blog</a></li>
                        <li style="margin-bottom: 8px;"><a href="/contact.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Contact</a></li>
                        <li style="margin-bottom: 8px;"><a href="/privacy.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Privacy Policy</a></li>
                        <li style="margin-bottom: 8px;"><a href="/terms.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Terms of Service</a></li>
                    </ul>
                </div>
                
                <div class="footer-links">
                    <h4 style="font-size: 1rem; margin-bottom: 16px; color: white;">Resources</h4>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="margin-bottom: 8px;"><a href="/quizzes/" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">All Quizzes</a></li>
                        <li style="margin-bottom: 8px;"><a href="/resources.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Financial Calculators</a></li>
                        <li style="margin-bottom: 8px;"><a href="/faq.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">FAQ</a></li>
                        <li style="margin-bottom: 8px;"><a href="/sitemap.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Sitemap</a></li>
                        <li style="margin-bottom: 8px;"><a href="/blog-build-credit.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Credit Guides</a></li>
                        <li style="margin-bottom: 8px;"><a href="/blog-make-money.html" style="color: #94a3b8; text-decoration: none; font-size: 0.875rem;">Money Tips</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-bottom" style="border-top: 1px solid #1e293b; padding-top: 20px; text-align: center;">
                <p style="color: #64748b; font-size: 0.875rem;">&copy; 2026 Credit Gamer Area. All rights reserved. | Not financial advice</p>
            </div>
        </div>
    </footer>
'''

def add_footer_to_quiz_page(filepath):
    """Add/update footer on a quiz page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if has minimal footer (just the tag with no content)
    if '<footer class="footer" style="background: #1e1b4b; color: white; padding: 40px 0; text-align: center;">\n    </footer>' in content:
        # Replace minimal footer with full footer
        content = content.replace(
            '<footer class="footer" style="background: #1e1b4b; color: white; padding: 40px 0; text-align: center;">\n    </footer>',
            FOOTER_HTML
        )
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    # Check if already has full footer
    if 'footer-brand' in content or 'footer-grid' in content:
        return False
    
    # Add footer before </body>
    content = content.replace('</body>', FOOTER_HTML + '\n</body>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def main():
    """Add footer to all quiz pages."""
    base_dir = "/root/.openclaw/workspace/triviacaptain-website"
    
    # Find all quiz question pages
    quiz_pages = glob.glob(os.path.join(base_dir, "quiz", "*", "q*.html"))
    
    updated = 0
    for filepath in quiz_pages:
        if add_footer_to_quiz_page(filepath):
            updated += 1
            print(f"Added footer: {filepath}")
    
    print(f"\nAdded footer to {updated} quiz pages")

if __name__ == "__main__":
    main()

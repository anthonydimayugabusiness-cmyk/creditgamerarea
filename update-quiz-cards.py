#!/usr/bin/env python3
"""Update quiz cards to use square design with category colors."""

import re

# Quiz data with categories
QUIZZES = [
    ("/credit-basics-quiz.html", "credit", "💳", "Credit Basics", "4.9", "🔥 Popular"),
    ("/credit-cards-quiz.html", "credit", "💰", "Credit Cards 101", "4.8", None),
    ("/taxes-quiz.html", "taxes", "📋", "Taxes for Beginners", "4.7", "🆕 New"),
    ("/student-loans-quiz.html", "banking", "🎓", "Student Loans", "4.6", None),
    ("/investing-quiz.html", "investing", "📈", "Investing Basics", "4.8", None),
    ("/make-money-online-quiz.html", "side-hustle", "💻", "Make Money Online", "4.9", "📈 Trending"),
    ("/budgeting-quiz.html", "banking", "🎯", "Budgeting", "4.7", None),
    ("/banking-quiz.html", "banking", "🏦", "Banking Basics", "4.5", None),
    ("/prediction-markets-quiz.html", "prediction", "🎲", "Prediction Markets", "4.6", None),
    ("/quiz-credit-rewards.html", "credit", "🎁", "Credit Card Rewards", "4.9", "🆕 New"),
    ("/quiz-fed-rates.html", "investing", "📊", "Fed Rates & Your Money", "4.7", "🆕 New"),
    ("/auto-loans-quiz.html", "auto", "🚗", "Auto Loans", "4.5", None),
    ("/car-shopping-quiz.html", "auto", "🚙", "Car Shopping", "4.6", None),
    ("/auto-insurance-quiz.html", "insurance", "🛡️", "Auto Insurance", "4.5", None),
    ("/ai-skills-quiz.html", "career", "🤖", "AI Skills", "4.7", None),
    ("/glp1-effects-quiz.html", "health", "💉", "GLP-1 Effects", "4.6", None),
]

def generate_card(url, category, emoji, title, rating, badge):
    badge_html = f'                    <div class="topic-badge">{badge}</div>\n' if badge else ''
    return f'''                <a href="{url}" class="topic-card {category}">
{badge_html}                    <div class="topic-icon">{emoji}</div>
                    <h3>{title}</h3>
                    <div class="topic-meta">
                        <span>10 Questions</span>
                        <span>⭐ {rating}</span>
                    </div>
                </a>'''

def main():
    with open('/root/.openclaw/workspace/triviacaptain-website/index.html', 'r') as f:
        content = f.read()
    
    # Find the topic-grid section
    pattern = r'(<div class="topic-grid">)(.*?)(</div>\s*</div>\s*</section>)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        # Generate new cards
        new_cards = '\n'.join([generate_card(*quiz) for quiz in QUIZZES])
        
        # Replace the content
        new_section = f'{match.group(1)}\n{new_cards}\n            {match.group(3)}'
        content = content[:match.start()] + new_section + content[match.end():]
        
        with open('/root/.openclaw/workspace/triviacaptain-website/index.html', 'w') as f:
            f.write(content)
        
        print(f"Updated {len(QUIZZES)} quiz cards to square design")
    else:
        print("Could not find topic-grid section")

if __name__ == "__main__":
    main()

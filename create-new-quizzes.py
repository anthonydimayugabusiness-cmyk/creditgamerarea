#!/usr/bin/env python3
"""Create landing pages for the 5 new quizzes."""

import os

QUIZ_DATA = {
    "auto-loans": {
        "title": "Auto Loans Quiz",
        "category": "Auto",
        "description": "Car financing, interest rates, and avoiding common mistakes",
        "color": "#ef4444",
        "color2": "#f87171",
        "emoji": "🚗",
        "blog_title": "Auto Loans: Drive Away Without Driving Yourself Into Debt",
        "score_key": "autoloans_score",
        "quiz_path": "/quiz/auto-loans/q1"
    },
    "car-shopping": {
        "title": "Car Shopping Quiz",
        "category": "Auto",
        "description": "New vs used, negotiating, and getting the best deal",
        "color": "#f97316",
        "color2": "#fb923c",
        "emoji": "🚙",
        "blog_title": "Car Shopping Mastery: How to Get the Best Deal",
        "score_key": "carshopping_score",
        "quiz_path": "/quiz/car-shopping/q1"
    },
    "auto-insurance": {
        "title": "Auto Insurance Quiz",
        "category": "Insurance",
        "description": "Coverage types, deductibles, and saving money",
        "color": "#06b6d4",
        "color2": "#22d3ee",
        "emoji": "🛡️",
        "blog_title": "Auto Insurance Decoded: Protect Your Ride Without Overpaying",
        "score_key": "autoinsurance_score",
        "quiz_path": "/quiz/auto-insurance/q1"
    },
    "ai-skills": {
        "title": "AI Skills Quiz",
        "category": "Career",
        "description": "ChatGPT, prompt engineering, and future-proofing your career",
        "color": "#8b5cf6",
        "color2": "#a78bfa",
        "emoji": "🤖",
        "blog_title": "AI Skills: The Career Upgrade You Can't Afford to Ignore",
        "score_key": "aiskills_score",
        "quiz_path": "/quiz/ai-skills/q1"
    },
    "glp1-effects": {
        "title": "GLP-1 Effects Quiz",
        "category": "Health & Finance",
        "description": "Weight loss drugs, costs, and financial impact",
        "color": "#14b8a6",
        "color2": "#2dd4bf",
        "emoji": "💉",
        "blog_title": "GLP-1 Drugs: The Real Cost Beyond the Price Tag",
        "score_key": "glp1effects_score",
        "quiz_path": "/quiz/glp1-effects/q1"
    }
}

BLOG_CONTENT = {
    "auto-loans": """
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Buying a car is one of the biggest purchases you'll make, and how you finance it can cost or save you thousands. The auto loan industry is designed to confuse buyers with jargon, hidden fees, and long-term traps that keep you paying for years after the new car smell fades. Understanding auto loans isn't just about getting a car—it's about protecting your financial future.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                The average new car loan now exceeds $40,000 with monthly payments over $700. With terms stretching to 72 or even 84 months, many buyers find themselves "upside down"—owing more than the car is worth—for years. This negative equity trap makes it impossible to sell or trade without bringing thousands to the table, effectively chaining you to your vehicle.
            </p>
            
            <h2 style="font-size: 1.75rem; margin: 40px 0 20px; color: #1e1b4b;">The True Cost of Financing</h2>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                A $35,000 car with a 72-month loan at 6% APR will cost you over $41,000 by the time you pay it off—and that's assuming you don't roll negative equity from a previous loan. The same car with a 48-month loan at a better rate could save you $3,000+ in interest. The difference between a good and bad auto loan isn't just the monthly payment; it's the total cost over the life of the loan.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Your credit score is the biggest factor in your interest rate. A score of 720+ might get you 4% APR, while a score below 600 could mean 12% or higher. On a $30,000 loan, that's the difference between paying $1,200 in interest versus $4,000+ over five years. Before car shopping, check your credit and take steps to improve it if needed.
            </p>""",
    
    "car-shopping": """
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Walking onto a car lot without preparation is like bringing a knife to a gunfight. Dealers have decades of experience extracting maximum profit from buyers who don't know the game. The good news? With the right knowledge, you can turn the tables and drive away with a great deal that doesn't destroy your budget.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                The first rule of car shopping: never negotiate based on monthly payment. Dealers love monthly payment shoppers because they can hide inflated prices, high interest rates, and unnecessary add-ons in a "manageable" monthly number. Instead, negotiate the out-the-door price—the actual amount you'll pay including taxes, fees, and extras. Only then should you discuss financing.
            </p>
            
            <h2 style="font-size: 1.75rem; margin: 40px 0 20px; color: #1e1b4b;">New vs. Used: The Real Math</h2>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                New cars lose 20-30% of their value in the first year and 60% within five years. That $40,000 new car is worth $28,000 the moment you drive it off the lot. A 2-3 year old certified pre-owned vehicle offers nearly the same features, remaining warranty, and significant savings. The sweet spot is often 2-4 years old with 20,000-40,000 miles.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Timing matters too. End of month, quarter, and model year are when dealers need to hit quotas and clear inventory. December often brings the best deals as dealers try to meet annual targets. Shop on weekdays when lots are empty and salespeople are hungry. And always get pre-approved for financing before you shop—it gives you leverage and a baseline to compare against dealer offers.
            </p>""",
    
    "auto-insurance": """
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Auto insurance is a legal requirement in almost every state, but that doesn't mean you should overpay for it. The average driver spends $1,500+ per year on car insurance, yet most have no idea what they're actually paying for. Understanding coverage types, how rates are calculated, and where to find discounts can save you hundreds annually.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Liability insurance—the minimum required by law—only covers damage you cause to others. It doesn't protect your car at all. If you have a loan or lease, you'll need comprehensive and collision coverage. But if you own an older car outright, carrying only liability might make financial sense. The key is understanding the trade-offs and making informed decisions.
            </p>
            
            <h2 style="font-size: 1.75rem; margin: 40px 0 20px; color: #1e1b4b;">Decoding Your Premium</h2>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Insurance companies use complex algorithms considering your age, driving record, credit score, location, vehicle type, and even your occupation. A speeding ticket can increase rates by 20-30%. A DUI can double or triple them. But good news: accidents and tickets typically stop affecting your rates after 3-5 years, and many insurers offer accident forgiveness programs.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                The deductible—the amount you pay before insurance kicks in—is a powerful lever. Raising your deductible from $500 to $1,000 can lower premiums by 10-20%. Just make sure you have that $1,000 saved in an emergency fund. And shop around every year or two; loyalty rarely pays in insurance, and rates vary dramatically between companies.
            </p>""",
    
    "ai-skills": """
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Artificial intelligence isn't coming for your job—it's coming for the routine parts of your job. The workers who thrive in the AI era won't be those who compete with machines, but those who learn to leverage them. AI literacy is becoming as fundamental as computer literacy was in the 1990s. The question isn't whether AI will change your industry, but whether you'll be ready.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                The data is clear: workers who effectively use AI tools are 10-50% more productive than those who don't. They're writing better emails faster, analyzing data more deeply, creating content more efficiently, and solving problems more creatively. This productivity advantage translates directly to career advancement and higher salaries. AI isn't replacing humans; it's amplifying them.
            </p>
            
            <h2 style="font-size: 1.75rem; margin: 40px 0 20px; color: #1e1b4b;">Where to Start</h2>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                You don't need to learn coding or become a data scientist. Start with ChatGPT, Claude, or Gemini—powerful AI assistants that can help with writing, analysis, research, and problem-solving. Learn prompt engineering: the art of asking AI the right questions to get useful answers. Practice daily. Apply AI to real tasks in your job. The learning curve is surprisingly gentle, but the payoff is enormous.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Beyond writing assistants, explore AI tools for your specific field. Designers should try Midjourney and DALL-E. Programmers should experiment with GitHub Copilot. Analysts should learn AI-powered Excel features. Marketers should explore AI content tools. The key is starting now, while these tools are still emerging and competitive advantage is available to early adopters.
            </p>""",
    
    "glp1-effects": """
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                GLP-1 drugs like Ozempic, Wegovy, and Mounjaro have become cultural phenomena, promising significant weight loss for millions struggling with obesity. But beyond the headlines about shrinking waistlines lies a complex financial reality. At $800-1,400+ per month without insurance, these medications represent one of the most significant healthcare expenses many people will face—and the costs extend far beyond the pharmacy counter.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                The financial impact of GLP-1 drugs is multifaceted. Yes, they're expensive. But many users report spending 10-30% less on food due to dramatically reduced appetite. Some offset medication costs through reduced grocery bills. However, rapid weight loss creates its own expenses: new wardrobes in multiple sizes, potential nutritional supplements, and more frequent doctor visits for monitoring.
            </p>
            
            <h2 style="font-size: 1.75rem; margin: 40px 0 20px; color: #1e1b4b;">The Mental Health Connection</h2>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Perhaps the most profound effect users report isn't physical—it's mental. "Food noise," the constant obsessive thoughts about eating that many people experience, often diminishes dramatically. Users describe feeling freed from the mental burden of constant hunger and cravings. This cognitive relief can translate to improved focus at work, better productivity, and enhanced quality of life that extends far beyond weight loss.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                But there's a catch: these effects typically last only as long as you take the medication. Studies show most people regain significant weight within a year of stopping. This creates a long-term financial commitment that must be factored into your budget indefinitely. Before starting, consider not just whether you can afford it now, but whether you can sustain that expense for years to come.
            </p>"""
}

CLOSING_PARAGRAPHS = {
    "auto-loans": "Take the quiz above to test your auto loan knowledge. Whether you're buying your first car or your fifth, understanding financing can save you thousands. Don't let dealer jargon confuse you—know the terms, know your credit, and know when to walk away.",
    "car-shopping": "Take the quiz above to test your car shopping knowledge. Remember: the best deal isn't the one with the lowest monthly payment—it's the one that costs you the least overall. Do your research, get pre-approved, and negotiate with confidence.",
    "auto-insurance": "Take the quiz above to test your auto insurance knowledge. The right coverage protects you without breaking the bank. Review your policy annually, shop around, and make sure you're getting every discount you deserve.",
    "ai-skills": "Take the quiz above to test your AI knowledge. The AI revolution isn't coming—it's here. The workers who embrace these tools today will be the ones leading tomorrow. Start learning, start experimenting, and start future-proofing your career.",
    "glp1-effects": "Take the quiz above to test your knowledge of GLP-1 drugs and their effects. Whether you're considering these medications or just curious about the phenomenon, understanding the full picture—financial, physical, and mental—helps you make informed decisions."
}

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - {description} (Free)</title>
    <meta name="description" content="Take our free {title}! {description}. 10 questions with instant results and detailed explanations.">
    <meta name="keywords" content="{quiz_name} quiz, learn {quiz_name}, personal finance, money tips, free quiz">
    <meta name="author" content="Credit Gamer Area">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://www.creditgamerarea.com/{quiz_name}-quiz.html">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://www.creditgamerarea.com/{quiz_name}-quiz.html">
    <meta property="og:title" content="{title} - {description}">
    <meta property="og:description" content="Take our free {title}! {description}.">
    <meta property="og:image" content="https://www.creditgamerarea.com/og-{quiz_name}.jpg">
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://www.creditgamerarea.com/{quiz_name}-quiz.html">
    <meta property="twitter:title" content="{title} - {description}">
    <meta property="twitter:description" content="Take our free {title}! {description}.">
    <meta property="twitter:image" content="https://www.creditgamerarea.com/og-{quiz_name}.jpg">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💳</text></svg>">
    <link rel="stylesheet" href="/styles.css">
    <style>
        .quiz-page {{ padding: 40px 0; min-height: calc(100vh - 200px); }}
        .quiz-container {{ max-width: 700px; margin: 0 auto; background: white; border-radius: 16px; padding: 40px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }}
        .quiz-header {{ text-align: center; margin-bottom: 32px; }}
        .quiz-header .category-tag {{ display: inline-block; background: {color}; color: white; padding: 6px 16px; border-radius: 20px; font-size: 0.875rem; font-weight: 600; margin-bottom: 16px; }}
        .quiz-header h1 {{ font-size: 1.875rem; margin-bottom: 8px; }}
        .progress-container {{ margin-bottom: 32px; }}
        .progress-bar-bg {{ background: #e2e8f0; height: 8px; border-radius: 4px; overflow: hidden; }}
        .progress-bar {{ background: linear-gradient(90deg, {color}, {color2}); height: 100%; border-radius: 4px; transition: width 0.3s ease; }}
        .progress-text {{ font-size: 0.875rem; color: #64748b; margin-top: 8px; text-align: center; }}
        .question-container h2 {{ font-size: 1.375rem; margin-bottom: 24px; line-height: 1.5; }}
        .options-list {{ display: flex; flex-direction: column; gap: 12px; }}
        .option {{ background: white; border: 2px solid #e2e8f0; padding: 16px 20px; border-radius: 12px; cursor: pointer; transition: all 0.2s; font-size: 1rem; text-align: left; }}
        .option:hover {{ border-color: {color}; background: #f8fafc; }}
        .option.correct {{ border-color: #10b981; background: #d1fae5; }}
        .option.incorrect {{ border-color: #ef4444; background: #fee2e2; }}
        .option.disabled {{ pointer-events: none; opacity: 0.7; }}
        .explanation {{ margin-top: 24px; padding: 20px; border-radius: 12px; }}
        .explanation.correct {{ background: #d1fae5; border: 1px solid #10b981; }}
        .explanation.incorrect {{ background: #fee2e2; border: 1px solid #ef4444; }}
        .explanation h4 {{ margin-bottom: 8px; font-size: 1.125rem; }}
        .next-btn {{ margin-top: 16px; background: {color}; color: white; border: none; padding: 14px 28px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 1rem; }}
        .results-container {{ text-align: center; padding: 40px 20px; }}
        .results-emoji {{ font-size: 4rem; margin-bottom: 16px; }}
        .results-score {{ font-size: 3.5rem; font-weight: 800; background: linear-gradient(135deg, {color}, {color2}); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 16px 0; }}
        .results-message {{ font-size: 1.5rem; font-weight: 600; margin-bottom: 8px; }}
        .results-subtitle {{ color: #64748b; margin-bottom: 32px; }}
        .results-actions {{ display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }}
        .btn {{ padding: 14px 28px; border-radius: 8px; font-weight: 600; text-decoration: none; display: inline-block; cursor: pointer; border: none; font-size: 1rem; }}
        .btn-primary {{ background: {color}; color: white; }}
        .btn-secondary {{ background: white; color: {color}; border: 2px solid {color}; }}
        .btn-large {{ font-size: 1.25rem; padding: 18px 36px; }}
        .start-screen {{ text-align: center; padding: 40px 20px; }}
        .quiz-meta {{ display: flex; gap: 24px; justify-content: center; margin-bottom: 32px; flex-wrap: wrap; }}
        .quiz-meta span {{ display: flex; align-items: center; gap: 8px; color: #64748b; }}
        .ad-container {{ max-width: 700px; margin: 32px auto; text-align: center; }}
        .ad-label {{ font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-bottom: 8px; }}
        .ad-inline {{ width: 300px; height: 250px; background: #e2e8f0; margin: 24px auto; display: flex; align-items: center; justify-content: center; color: #64748b; border-radius: 8px; }}
        .quiz-cta-section {{ background: linear-gradient(135deg, {color}, {color2}); color: white; padding: 60px 20px; text-align: center; margin: 40px 0; border-radius: 16px; }}
        .quiz-cta-section h2 {{ font-size: 2rem; margin-bottom: 16px; }}
        .quiz-cta-section p {{ font-size: 1.125rem; margin-bottom: 24px; opacity: 0.9; }}
    </style>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <a href="/" class="logo">💳 Credit Gamer Area</a>
            <ul class="nav-links">
                <li><a href="/quizzes/">Quizzes</a></li>
                <li><a href="/blog-build-credit.html">Blog</a></li>
            </ul>
        </div>
    </nav>

    <!-- Top Ad Unit -->
    <div class="ad-container">
        <div class="ad-label">Advertisement</div>
        <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    </div>

    <!-- Blog Content Section -->
    <section class="quiz-blog-content" style="padding: 60px 0; background: #f8fafc;">
        <div class="container" style="max-width: 800px;">
            <span style="display: inline-block; background: {color}; color: white; padding: 6px 16px; border-radius: 20px; font-size: 0.875rem; font-weight: 600; margin-bottom: 16px;">{category}</span>
            <h1 style="font-size: 2.5rem; margin-bottom: 24px; color: #1e1b4b;">{blog_title}</h1>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px; color: #64748b;">
                <strong>Reading time:</strong> 5 minutes | <strong>Quiz:</strong> 10 questions
            </p>

            <!-- Inline Ad 1 -->
            <div class="ad-inline">
                <div>
                    <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-bottom: 8px;">Advertisement</div>
                    <ins class="adsbygoogle" style="display:inline-block;width:300px;height:250px" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX"></ins>
                    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
                </div>
            </div>
            
            {blog_content}

            <!-- Inline Ad 2 -->
            <div class="ad-inline">
                <div>
                    <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-bottom: 8px;">Advertisement</div>
                    <ins class="adsbygoogle" style="display:inline-block;width:300px;height:250px" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX"></ins>
                    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
                </div>
            </div>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                {closing_paragraph}
            </p>

            <!-- Inline Ad 3 -->
            <div class="ad-inline">
                <div>
                    <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-bottom: 8px;">Advertisement</div>
                    <ins class="adsbygoogle" style="display:inline-block;width:300px;height:250px" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX"></ins>
                    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
                </div>
            </div>
        </div>
    </section>

    <!-- Bottom Ad Unit -->
    <div class="ad-container">
        <div class="ad-label">Advertisement</div>
        <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    </div>

    <!-- CTA Section -->
    <section class="quiz-cta-section">
        <div class="container" style="max-width: 600px;">
            <h2>{emoji} Ready to Test Your Knowledge?</h2>
            <p>Take our free 10-question quiz to see how much you've learned about {quiz_name}. Get instant results and detailed explanations for each question.</p>
            
            <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; margin-bottom: 24px;">
                <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px;">📝 10 Questions</span>
                <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px;">⏱️ ~5 Minutes</span>
                <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px;">📊 Instant Results</span>
            </div>
            
            <button class="btn btn-primary btn-large" onclick="startMultiPageQuiz()">Start the Quiz →</button>
        </div>
    </section>

    <footer class="footer" style="background: #0f0d2e; color: white; padding: 40px 0; text-align: center;">
        <div class="container">
            <p>&copy; 2026 Credit Gamer Area. All rights reserved. | <a href="/privacy.html" style="color: #a5b4fc;">Privacy</a> | <a href="/terms.html" style="color: #a5b4fc;">Terms</a></p>
        </div>
    </footer>

    <script>
        function startMultiPageQuiz() {{
            sessionStorage.setItem('{score_key}', '0');
            window.location.href = '{quiz_path}';
        }}
    </script>
</body>
</html>'''

def generate_landing_page(quiz_name, data):
    """Generate a quiz landing page."""
    return HTML_TEMPLATE.format(
        title=data["title"],
        description=data["description"],
        quiz_name=quiz_name,
        category=data["category"],
        color=data["color"],
        color2=data["color2"],
        emoji=data["emoji"],
        blog_title=data["blog_title"],
        blog_content=BLOG_CONTENT[quiz_name],
        closing_paragraph=CLOSING_PARAGRAPHS[quiz_name],
        score_key=data["score_key"],
        quiz_path=data["quiz_path"]
    )

def main():
    """Generate all 5 new quiz landing pages."""
    base_dir = "/root/.openclaw/workspace/triviacaptain-website"
    
    for quiz_name, data in QUIZ_DATA.items():
        filename = f"{quiz_name}-quiz.html"
        filepath = os.path.join(base_dir, filename)
        
        html_content = generate_landing_page(quiz_name, data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Created {filename}")
    
    print("\nAll 5 new quiz landing pages created!")

if __name__ == "__main__":
    main()

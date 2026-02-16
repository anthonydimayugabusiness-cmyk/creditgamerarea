#!/usr/bin/env python3
"""Standardize all quiz landing pages to match credit-basics-quiz format."""

import os
import re

# Quiz data for each quiz
QUIZ_INFO = {
    "banking": {
        "title": "Banking Basics Quiz",
        "category": "Finance",
        "description": "Checking vs savings, APY, fees, and online banks",
        "color": "#3b82f6",
        "color2": "#60a5fa",
        "emoji": "🏦",
        "blog_title": "Banking Basics: Choosing the Right Bank for You",
        "score_key": "banking_score",
        "quiz_path": "/quiz/banking/q1"
    },
    "budgeting": {
        "title": "Budgeting Quiz",
        "category": "Money Management",
        "description": "50/30/20 rule, apps, and saving strategies",
        "color": "#f59e0b",
        "color2": "#fbbf24",
        "emoji": "🎯",
        "blog_title": "Mastering Budgeting: The Foundation of Financial Success",
        "score_key": "budgeting_score",
        "quiz_path": "/quiz/budgeting/q1"
    },
    "investing": {
        "title": "Investing Basics Quiz",
        "category": "Investing",
        "description": "Stocks, ETFs, 401k, and how to start with $100",
        "color": "#10b981",
        "color2": "#34d399",
        "emoji": "📈",
        "blog_title": "Investing 101: Building Wealth for Your Future",
        "score_key": "investing_score",
        "quiz_path": "/quiz/investing/q1"
    },
    "make-money-online": {
        "title": "Make Money Online Quiz",
        "category": "Side Hustle",
        "description": "Side hustles, freelancing, streaming, and passive income",
        "color": "#8b5cf6",
        "color2": "#a78bfa",
        "emoji": "💰",
        "blog_title": "Making Money Online: Real Opportunities in 2026",
        "score_key": "makemoneyonline_score",
        "quiz_path": "/quiz/make-money-online/q1"
    },
    "student-loans": {
        "title": "Student Loans Quiz",
        "category": "Education",
        "description": "Federal vs private, repayment plans, and forgiveness",
        "color": "#ec4899",
        "color2": "#f472b6",
        "emoji": "🎓",
        "blog_title": "Student Loans: Navigate Your Education Debt",
        "score_key": "studentloans_score",
        "quiz_path": "/quiz/student-loans/q1"
    },
    "taxes": {
        "title": "Taxes Quiz",
        "category": "Taxes",
        "description": "W-2s, 1099s, deductions, and how to not overpay",
        "color": "#f59e0b",
        "color2": "#fbbf24",
        "emoji": "📋",
        "blog_title": "Taxes for Beginners: Keep More of Your Money",
        "score_key": "taxes_score",
        "quiz_path": "/quiz/taxes/q1"
    }
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

    <footer class="footer" style="background: #1e1b4b; color: white; padding: 40px 0; text-align: center;">
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

BLOG_CONTENT = {
    "banking": """<p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Banking is the foundation of your financial life. Your checking account is where your paycheck lands, your bills get paid from, and your daily transactions flow through. Your savings account is where your emergency fund grows and your short-term goals take shape. Choosing the right bank—and understanding how to use its services—can save you hundreds of dollars in fees and help your money work harder for you.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                The banking landscape has transformed dramatically in recent years. Traditional brick-and-mortar banks with their extensive branch networks now compete with online-only banks that offer higher interest rates and lower fees by eliminating physical locations. Both have their place—traditional banks excel at services requiring in-person interaction like notarization or cash deposits, while online banks typically offer better rates and fewer fees for digital-native customers.
            </p>
            
            <h2 style="font-size: 1.75rem; margin: 40px 0 20px; color: #1e1b4b;">Understanding Account Types</h2>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Checking accounts are designed for daily transactions—receiving deposits, paying bills, making purchases. They typically offer low or no interest but provide unlimited transactions and easy access to your money. Savings accounts are for storing money you don't need immediate access to, offering interest (APY) in exchange for limited monthly withdrawals. The best strategy is maintaining both: a checking account for daily operations and a savings account for your emergency fund and short-term goals.
            </p>
            
            <h2 style="font-size: 1.75rem; margin: 40px 0 20px; color: #1e1b4b;">Protecting Your Money</h2>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                FDIC insurance is a crucial protection that many young adults don't know about. The Federal Deposit Insurance Corporation insures bank deposits up to $250,000 per depositor, per bank, per account ownership category. This means if your bank fails, you won't lose your money. Always verify your bank is FDIC-insured—most legitimate banks are, but it's worth confirming. Credit unions have similar protection through the NCUA.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                When comparing banks, look beyond the marketing. Monthly maintenance fees can range from $0 to $25 or more—over a year, that's $300 in unnecessary costs. Many banks waive these fees if you maintain a minimum balance or set up direct deposit. ATM fees can add up quickly too; choose a bank with a large ATM network or one that reimburses out-of-network fees. Overdraft fees, typically $35 per transaction, can turn a small mistake into a major expense.
            </p>""",
    
    "budgeting": """<p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Budgeting isn't about restriction—it's about intentionality. When you create a budget, you're not limiting your spending; you're ensuring your money goes toward what actually matters to you. Whether that's traveling, paying off debt, building an emergency fund, or investing for the future, a budget is simply a plan that aligns your spending with your values and goals.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                The 50/30/20 rule is a popular starting point for budgeting beginners. It suggests allocating 50% of your after-tax income to needs (rent, groceries, utilities, minimum debt payments), 30% to wants (dining out, entertainment, hobbies), and 20% to savings and extra debt payments. While this framework works well for many people, it's not one-size-fits-all. High-cost-of-living areas might require adjusting to 60/20/20, while aggressive savers might prefer 50/20/30.
            </p>
            
            <h2 style="font-size: 1.75rem; margin: 40px 0 20px; color: #1e1b4b;">The Power of Automation</h2>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                The most successful budgeters automate their finances. Set up automatic transfers to your savings account on payday, before you have a chance to spend that money. Automate bill payments to avoid late fees and credit score damage. Use apps that round up your purchases and save the change. The less willpower required to stick to your budget, the more likely you are to succeed.
            </p>
            
            <h2 style="font-size: 1.75rem; margin: 40px 0 20px; color: #1e1b4b;">Tracking and Adjusting</h2>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                A budget is a living document, not a set-it-and-forget-it task. Review your spending weekly at first, then monthly as you get comfortable. Look for patterns: Are you consistently overspending on dining out? Maybe you need to increase that category and decrease another. Are you saving more than expected? Consider increasing your automatic transfers. The goal is progress, not perfection.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Budgeting apps like YNAB, Mint, or even a simple spreadsheet can help you track where your money goes. But the tool matters less than the habit. Find a method you can stick with consistently, whether that's an app, a spreadsheet, or the envelope method with physical cash.
            </p>""",
    
    "investing": """<p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Investing is how you turn your savings into wealth. While saving money in a bank account protects it, investing grows it. Thanks to compound interest, even small investments made early can grow into significant sums over time. The key is starting early, staying consistent, and letting time do the heavy lifting.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                The stock market has historically returned about 10% annually before inflation. That means $1,000 invested today could be worth over $6,700 in 20 years, even without adding another dime. Add regular monthly contributions, and the growth becomes even more powerful. This is why starting in your 20s gives you such an advantage over those who wait until their 30s or 40s.
            </p>
            
            <h2 style="font-size: 1.75rem; margin: 40px 0 20px; color: #1e1b4b;">Getting Started with Little Money</h2>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                You don't need thousands of dollars to start investing. Many brokers now offer fractional shares, letting you buy pieces of expensive stocks with as little as $1. Index funds and ETFs allow you to own hundreds or thousands of companies with a single purchase, providing instant diversification. Start with whatever you can afford—even $25 per month—and increase as your income grows.
            </p>
            
            <h2 style="font-size: 1.75rem; margin: 40px 0 20px; color: #1e1b4b;">Understanding Risk and Return</h2>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                All investments carry risk, but not all risks are equal. Generally, higher potential returns come with higher risk. Stocks are riskier than bonds but have historically provided better returns. Cryptocurrency is even riskier but has the potential for massive gains—or total loss. The key is diversification: don't put all your eggs in one basket. Spread your investments across different asset classes, industries, and geographies.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Your risk tolerance should match your timeline. Money you'll need in the next 3-5 years should be in safer investments like high-yield savings or bonds. Money you won't touch for decades can be invested more aggressively in stocks. As you approach your goal, gradually shift to more conservative investments to protect your gains.
            </p>""",
    
    "make-money-online": """<p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                The internet has created unprecedented opportunities to earn money outside of traditional employment. Whether you're looking to supplement your income, build a side business, or eventually replace your 9-to-5, there are legitimate ways to make money online. The key is finding something that matches your skills, interests, and available time.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Freelancing is one of the most accessible entry points. Platforms like Upwork, Fiverr, and Freelancer connect skilled workers with clients who need their services. Writing, graphic design, programming, video editing, virtual assistance—the demand for digital skills is enormous. Start by offering services you're already good at, then expand your skills as you build your portfolio and reputation.
            </p>
            
            <h2 style="font-size: 1.75rem; margin: 40px 0 20px; color: #1e1b4b;">Content Creation and Passive Income</h2>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Content creation on YouTube, TikTok, Instagram, or a blog can generate income through ads, sponsorships, and affiliate marketing. While it takes time to build an audience, successful creators can earn substantial passive income from content they created months or years ago. The key is consistency and providing genuine value to your audience.
            </p>
            
            <h2 style="font-size: 1.75rem; margin: 40px 0 20px; color: #1e1b4b;">Avoiding Scams</h2>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Not all online money-making opportunities are legitimate. Be wary of anything that promises easy money with little effort, requires upfront payment to start, or seems too good to be true. Real online income requires real work, real skills, and real time investment. Research any opportunity thoroughly before committing time or money.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                The most successful online earners typically combine multiple income streams. They might freelance for steady income, run a blog for passive income, and sell digital products for scalable income. Diversification protects you if one stream dries up and accelerates your path to financial independence.
            </p>""",
    
    "student-loans": """<p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Student loans are a reality for millions of Americans pursuing higher education. While they can open doors to better career opportunities, they also represent a significant financial burden that can follow you for decades. Understanding how student loans work—from borrowing to repayment—is essential for minimizing their impact on your financial future.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Federal student loans should be your first choice when borrowing for school. They offer lower interest rates, more flexible repayment options, and better protections than private loans. Subsidized federal loans are particularly valuable because the government pays the interest while you're in school and during deferment periods. Unsubsidized loans accrue interest immediately but still offer better terms than most private alternatives.
            </p>
            
            <h2 style="font-size: 1.75rem; margin: 40px 0 20px; color: #1e1b4b;">Repayment Strategies</h2>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                The standard repayment plan spans 10 years with fixed monthly payments. However, income-driven repayment plans can lower your payments to 10-20% of your discretionary income, with forgiveness after 20-25 years. Public Service Loan Forgiveness offers complete forgiveness after 10 years of payments for those working in qualifying public service jobs. Understanding these options can save you thousands.
            </p>
            
            <h2 style="font-size: 1.75rem; margin: 40px 0 20px; color: #1e1b4b;">Managing Your Debt</h2>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Never ignore your student loans. Defaulting damages your credit score for years, can result in wage garnishment, and makes you ineligible for future federal aid. If you're struggling, contact your loan servicer immediately. Options like deferment, forbearance, or switching repayment plans can provide temporary relief while you get back on your feet.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Refinancing can lower your interest rate and monthly payment, but it converts federal loans to private loans, meaning you'll lose federal protections and forgiveness options. Only refinance if you have a stable income, good credit, and don't plan to use income-driven repayment or forgiveness programs.
            </p>""",
    
    "taxes": """<p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Taxes are an unavoidable part of earning money, but understanding how they work can help you keep more of what you earn. From withholding to deductions to credits, the tax system offers numerous opportunities to reduce your bill—if you know where to look. Whether you're a W-2 employee, a freelancer, or both, tax literacy pays dividends.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Your W-4 form determines how much tax is withheld from your paycheck. Claim too few allowances, and you're giving the government an interest-free loan. Claim too many, and you'll owe money at tax time. Use the IRS withholding estimator to get it right. For freelancers and gig workers, quarterly estimated tax payments are required to avoid penalties—set aside 25-30% of every payment you receive.
            </p>
            
            <h2 style="font-size: 1.75rem; margin: 40px 0 20px; color: #1e1b4b;">Deductions vs. Credits</h2>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Deductions reduce your taxable income. If you're in the 22% tax bracket, a $1,000 deduction saves you $220. Credits reduce your tax bill dollar-for-dollar—a $1,000 credit saves you $1,000. Common deductions include student loan interest, mortgage interest, and charitable donations. Common credits include the Earned Income Tax Credit, Child Tax Credit, and education credits.
            </p>
            
            <h2 style="font-size: 1.75rem; margin: 40px 0 20px; color: #1e1b4b;">Filing Strategies</h2>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                The standard deduction nearly doubled in recent years, meaning fewer people benefit from itemizing. For 2024, it's $13,850 for single filers and $27,700 for married couples filing jointly. Unless your itemized deductions (mortgage interest, state taxes, charitable donations, medical expenses) exceed these amounts, take the standard deduction—it's simpler and usually better.
            </p>
            
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 20px;">
                Free filing options exist for most taxpayers. IRS Free File offers guided tax preparation for those earning under $79,000. Many states offer free e-filing for state returns. Even if you don't qualify for free filing, simple returns can often be filed for under $50 using online software. Only pay for professional help if your situation is genuinely complex.
            </p>"""
}

CLOSING_PARAGRAPHS = {
    "banking": "Take the quiz above to test your banking knowledge. Understanding these fundamentals will help you choose the right bank, avoid unnecessary fees, and make your money work harder for you. Your banking choices might seem small, but over time, they significantly impact your financial health.",
    "budgeting": "Take the quiz above to test your budgeting knowledge. Remember, the best budget is one you'll actually follow. Start simple, track your progress, and adjust as needed. Financial freedom begins with understanding where your money goes.",
    "investing": "Take the quiz above to test your investing knowledge. Remember, time in the market beats timing the market. The best day to start investing was yesterday. The second best day is today.",
    "make-money-online": "Take the quiz above to test your knowledge of online income opportunities. Whether you're looking for side income or a full-time online career, understanding the landscape helps you make informed decisions and avoid scams.",
    "student-loans": "Take the quiz above to test your student loan knowledge. Whether you're still in school, in repayment, or considering borrowing, understanding your options empowers you to make the best decisions for your financial future.",
    "taxes": "Take the quiz above to test your tax knowledge. Understanding taxes isn't just about filing correctly—it's about keeping more of your hard-earned money through smart planning and taking advantage of available deductions and credits."
}

def generate_quiz_page(quiz_name, info):
    """Generate a standardized quiz landing page."""
    return HTML_TEMPLATE.format(
        title=info["title"],
        description=info["description"],
        quiz_name=quiz_name,
        category=info["category"],
        color=info["color"],
        color2=info["color2"],
        emoji=info["emoji"],
        blog_title=info["blog_title"],
        blog_content=BLOG_CONTENT[quiz_name],
        closing_paragraph=CLOSING_PARAGRAPHS[quiz_name],
        score_key=info["score_key"],
        quiz_path=info["quiz_path"]
    )

def main():
    """Generate all quiz landing pages."""
    base_dir = "/root/.openclaw/workspace/triviacaptain-website"
    
    for quiz_name, info in QUIZ_INFO.items():
        filename = f"{quiz_name}-quiz.html"
        filepath = os.path.join(base_dir, filename)
        
        html_content = generate_quiz_page(quiz_name, info)
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        print(f"Created {filename}")
    
    print("\nAll quiz landing pages standardized!")

if __name__ == "__main__":
    main()

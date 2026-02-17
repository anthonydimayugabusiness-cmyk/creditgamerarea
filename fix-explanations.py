#!/usr/bin/env python3
"""Fix quiz explanations - restore proper educational content."""

import os
import glob
import re

# Question explanations for each quiz
EXPLANATIONS = {
    "credit-basics": [
        "FICO Score is used by 90% of top lenders. It ranges from 300-850.",
        "Payment history makes up 35% of your FICO score - the single biggest factor.",
        "Hard inquiries can temporarily lower your score by a few points and stay on your report for 2 years.",
        "Credit utilization (how much you use vs your limit) makes up 30% of your FICO score.",
        "Checking your own credit is a soft inquiry and never affects your score.",
        "The three major credit bureaus are Experian, Equifax, and TransUnion.",
        "Most negative items fall off your credit report after 7 years (10 years for bankruptcies).",
        "Becoming an authorized user on someone else's card can help build your credit history.",
        "Secured cards require a deposit and are designed for people building or rebuilding credit.",
        "Credit reports are free at AnnualCreditReport.com - the only federally authorized source."
    ],
    "credit-cards": [
        "The Schumer Box is a standardized table showing all card terms and fees.",
        "Grace periods let you avoid interest if you pay your full balance by the due date.",
        "Credit card interest compounds daily, making it expensive to carry a balance.",
        "Maxing out cards hurts your credit utilization ratio and can lower your score significantly.",
        "Balance transfers can save money on interest but usually have a 3-5% transfer fee.",
        "Minimum payments are designed to keep you in debt longer and pay more interest.",
        "Late payments over 30 days get reported to credit bureaus and damage your score.",
        "Credit cards offer stronger fraud protection than debit cards under federal law.",
        "Store cards often have higher interest rates and lower credit limits than general cards.",
        "Cash advances start accruing interest immediately with no grace period and often have high fees."
    ],
    "taxes": [
        "The W-4 tells your employer how much tax to withhold from your paycheck.",
        "The standard deduction for single filers in 2024 is $14,600.",
        "W-2 forms report your wages and taxes withheld; 1099s report other income types.",
        "Tax brackets are marginal - you only pay the higher rate on income above each threshold.",
        "Contributions to traditional 401(k)s and IRAs can reduce your taxable income.",
        "The deadline to file taxes or request an extension is typically April 15.",
        "Self-employment tax covers Social Security and Medicare taxes for self-employed individuals.",
        "Tax credits directly reduce your tax bill dollar-for-dollar, better than deductions.",
        "Freelancers should make quarterly estimated tax payments to avoid penalties.",
        "Itemizing only makes sense if your deductions exceed the standard deduction amount."
    ],
    "investing": [
        "A 401(k) is an employer-sponsored retirement plan with potential matching contributions.",
        "Compound interest earns returns on both your principal and accumulated interest over time.",
        "Index funds track market indexes like the S&P 500 with low fees and broad diversification.",
        "Diversification spreads risk across different investments to reduce volatility.",
        "A bear market is a 20%+ decline; a bull market is sustained rising prices.",
        "Dollar-cost averaging means investing regular amounts regardless of market conditions.",
        "Higher potential returns almost always come with higher risk.",
        "An emergency fund should cover 3-6 months of expenses before aggressive investing.",
        "Target-date funds automatically adjust asset allocation as you approach retirement.",
        "Long-term capital gains (held over 1 year) have lower tax rates than short-term gains."
    ],
    "student-loans": [
        "Federal loans generally have lower rates and better protections than private loans.",
        "Subsidized loans don't accrue interest while you're in school; unsubsidized do.",
        "The FAFSA determines eligibility for federal student aid including grants and loans.",
        "The standard repayment plan is 10 years, but income-driven plans can extend to 20-25 years.",
        "Consolidation combines multiple loans but doesn't lower your interest rate.",
        "Deferment pauses payments; forbearance also pauses but interest may still accrue.",
        "Public Service Loan Forgiveness forgives remaining balance after 120 qualifying payments.",
        "Missing payments can lead to default, damaged credit, and wage garnishment.",
        "Refinancing can lower rates but converts federal loans to private, losing protections.",
        "The grace period is typically 6 months after graduation before repayment begins."
    ],
    "budgeting": [
        "The 50/30/20 rule allocates 50% to needs, 30% to wants, and 20% to savings/debt.",
        "An emergency fund should cover 3-6 months of essential expenses.",
        "Tracking spending reveals where your money actually goes versus where you think it goes.",
        "Zero-based budgeting assigns every dollar a job so income minus expenses equals zero.",
        "Sinking funds save for irregular expenses like car repairs or holiday gifts.",
        "Paying yourself first means automatically saving before spending on discretionary items.",
        "The envelope system uses cash in labeled envelopes to control spending categories.",
        "Discretionary spending is non-essential; non-discretionary is required (rent, food).",
        "Lifestyle creep happens when spending increases with income, preventing wealth building.",
        "YNAB, Mint, and PocketGuard are popular budgeting apps with different approaches."
    ],
    "banking": [
        "FDIC insurance protects up to $250,000 per depositor, per bank, per ownership category.",
        "High-yield savings accounts offer better interest rates than traditional savings.",
        "Checking accounts are for daily transactions; savings accounts are for storing money.",
        "Overdraft fees average $35 per transaction and can add up quickly.",
        "Credit unions are member-owned nonprofits that often offer better rates than banks.",
        "Online banks typically offer higher interest rates due to lower overhead costs.",
        "CDs lock your money for a set term in exchange for a guaranteed interest rate.",
        "A wire transfer is an electronic funds transfer between banks, often used for large amounts.",
        "Mobile deposit lets you deposit checks by taking photos through your banking app.",
        "Regulation D limits certain withdrawals from savings accounts to 6 per month."
    ],
    "make-money-online": [
        "Freelancing platforms like Upwork and Fiverr connect you with clients worldwide.",
        "Dropshipping lets you sell products without holding inventory.",
        "Affiliate marketing earns commissions by promoting other companies' products.",
        "Online tutoring pays well if you have expertise in high-demand subjects.",
        "Print-on-demand lets you sell custom designs on products without upfront costs.",
        "YouTube monetization requires 1,000 subscribers and 4,000 watch hours.",
        "Virtual assistants handle administrative tasks remotely for businesses.",
        "Selling digital products (courses, ebooks, templates) has high profit margins.",
        "Most online money-making methods require consistent effort before seeing significant income.",
        "Be wary of get-rich-quick schemes - legitimate online income takes work and skill."
    ],
    "prediction-markets": [
        "Prediction markets aggregate collective wisdom to forecast event probabilities.",
        "Kalshi is a regulated U.S. exchange for trading event contracts.",
        "Polymarket uses cryptocurrency and is not available to U.S. users.",
        "Event contracts pay $1 if the event happens, $0 if it doesn't.",
        "Prediction markets can be more accurate than polls for forecasting elections.",
        "No-deposit bonuses let you trade without risking your own money.",
        "Liquidity refers to how easily you can buy or sell contracts at fair prices.",
        "Regulatory status varies - Kalshi is CFTC-regulated; others operate in gray areas.",
        "Market prices reflect the crowd's estimate of an event's probability.",
        "Prediction markets have been shown to outperform expert forecasts in many cases."
    ],
    "credit-rewards": [
        "Cash back cards return a percentage of purchases as statement credits or deposits.",
        "Points and miles programs vary in value - typically 1-2 cents per point.",
        "Sign-up bonuses can be worth $500+ but require meeting minimum spending requirements.",
        "Rotating category cards offer 5% back on changing categories each quarter.",
        "Flat-rate cards offer consistent rewards on all purchases, good for simplicity.",
        "Travel cards often include perks like lounge access and travel insurance.",
        "Annual fees can be worth it if benefits exceed the cost for your spending.",
        "Credit card rewards are not taxable - they're considered rebates on purchases.",
        "Chase Ultimate Rewards and Amex Membership Rewards are highly flexible programs.",
        "Maximizing rewards requires matching cards to your spending patterns and goals."
    ],
    "fed-rates": [
        "The Federal Reserve sets the federal funds rate, which influences all other interest rates.",
        "Higher rates make borrowing more expensive but savings accounts pay more interest.",
        "Credit card APRs typically rise within 1-2 billing cycles after Fed rate hikes.",
        "Mortgage rates are influenced by Fed policy but also market forces like inflation.",
        "When rates rise, bond prices fall - they have an inverse relationship.",
        "The Fed raises rates to fight inflation and lowers them to stimulate the economy.",
        "Variable rate loans become more expensive as the Fed raises rates.",
        "CD rates usually increase when the Fed raises rates, benefiting savers.",
        "The Fed has a dual mandate: maximum employment and stable prices.",
        "Markets often react immediately to Fed announcements and policy changes."
    ],
    "auto-loans": [
        "Auto loan preapproval lets you shop like a cash buyer and negotiate better deals.",
        "Longer loan terms mean lower monthly payments but much more total interest paid.",
        "Gap insurance covers the difference between what you owe and the car's value if totaled.",
        "Credit unions often offer lower auto loan rates than banks or dealer financing.",
        "The 20/4/10 rule: 20% down, 4-year max term, 10% of income max payment.",
        "Dealer financing sometimes includes markups - compare with outside lenders.",
        "Refinancing can lower your rate if your credit has improved since purchase.",
        "New car loans typically have lower rates than used car loans.",
        "A larger down payment reduces your loan amount and may get you better rates.",
        "Loan origination fees add to the total cost - factor them into your comparison."
    ],
    "car-shopping": [
        "The sticker price (MSRP) is just a starting point - most cars sell for less.",
        "Certified pre-owned cars include warranties and inspections but cost more than regular used.",
        "Depreciation is steepest in the first few years - buying used can save thousands.",
        "Total cost of ownership includes insurance, gas, maintenance, not just the purchase price.",
        "Edmunds, Kelley Blue Book, and TrueCar provide pricing data to help negotiate.",
        "End of month, quarter, and year are often best times to negotiate deals.",
        "A vehicle history report (Carfax/AutoCheck) reveals accidents and maintenance records.",
        "Leasing offers lower monthly payments but you don't own the car at the end.",
        "Test drives should include highway speeds, parking, and your daily commute route.",
        "Getting multiple quotes from different dealers creates competition for your business."
    ],
    "auto-insurance": [
        "Liability coverage is required by law; it covers damage you cause to others.",
        "Full coverage includes liability plus collision and comprehensive for your own vehicle.",
        "A deductible is what you pay out of pocket before insurance kicks in.",
        "Your driving record is the biggest factor in determining your insurance rates.",
        "Bundling auto and home/renters insurance often provides significant discounts.",
        "Young drivers typically pay the highest rates due to inexperience and risk.",
        "Usage-based insurance tracks driving behavior and can lower rates for safe drivers.",
        "Gap insurance is crucial if you owe more than your car is worth.",
        "Credit scores often affect insurance rates - better credit means lower premiums.",
        "Shopping around annually can save hundreds as rates vary significantly between insurers."
    ],
    "ai-skills": [
        "Prompt engineering is the skill of writing effective instructions for AI systems.",
        "ChatGPT, Claude, and Gemini are leading conversational AI tools with different strengths.",
        "AI can automate repetitive tasks like data entry, email drafting, and research.",
        "AI-generated content should always be reviewed for accuracy and bias.",
        "Midjourney, DALL-E, and Stable Diffusion create images from text descriptions.",
        "GitHub Copilot and similar tools assist with coding and can boost productivity.",
        "AI excels at pattern recognition, summarization, and generating creative ideas.",
        "Critical thinking is essential - AI can hallucinate facts and make errors.",
        "AI skills are increasingly valuable across industries from marketing to healthcare.",
        "Staying current with AI developments is important as the technology evolves rapidly."
    ],
    "glp1-effects": [
        "GLP-1 drugs like Ozempic and Wegovy were originally developed for type 2 diabetes.",
        "These medications reduce appetite by mimicking a hormone that signals fullness.",
        "Common side effects include nausea, diarrhea, and constipation, especially when starting.",
        "Weight loss of 15-20% is typical, but results vary by individual.",
        "Insurance coverage varies widely - many plans don't cover them for weight loss.",
        "Muscle loss can occur along with fat loss - strength training is recommended.",
        "These drugs require prescriptions and medical supervision for safe use.",
        "Stopping the medication often leads to weight regain without lifestyle changes.",
        "Cardiovascular benefits have been shown in recent clinical trials.",
        "The long-term effects of these drugs are still being studied and monitored."
    ]
}

def fix_quiz_explanations(filepath, quiz_id, q_num):
    """Fix explanations in a quiz page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get the correct explanation
    explanations = EXPLANATIONS.get(quiz_id, ["Explanation text"] * 10)
    if q_num <= len(explanations):
        explanation = explanations[q_num - 1]
    else:
        explanation = "Explanation text"
    
    # Replace the bad explanation
    content = re.sub(
        r'(<div id="exp" class="explanation">\s*<strong id="res"></strong><br><br>)[^<]+',
        r'\1' + explanation,
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    base_dir = "/root/.openclaw/workspace/triviacaptain-website/quiz"
    
    fixed = 0
    for quiz_id in EXPLANATIONS.keys():
        for q_num in range(1, 11):
            filepath = os.path.join(base_dir, quiz_id, f"q{q_num}.html")
            if os.path.exists(filepath):
                if fix_quiz_explanations(filepath, quiz_id, q_num):
                    fixed += 1
    
    print(f"✅ Fixed explanations in {fixed} quiz pages")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate token-protected quiz question pages."""

import os
import sys

QUIZ_DATA = {
    "credit-basics": {
        "title": "Credit Basics",
        "landing": "/credit-basics-quiz.html",
        "questions": [
            {"q": "What is the most commonly used credit scoring model?", "opts": ["VantageScore", "FICO Score", "Experian Score", "TransUnion Score"], "correct": 1, "expl": "FICO Score is used by 90% of top lenders. It ranges from 300-850."},
            {"q": "What percentage of your credit score is based on payment history?", "opts": ["15%", "35%", "50%", "65%"], "correct": 1, "expl": "Payment history makes up 35% of your FICO score - the single biggest factor."},
            {"q": "How long do negative items stay on your credit report?", "opts": ["3 years", "5 years", "7 years", "10 years"], "correct": 2, "expl": "Most negative items stay for 7 years. Bankruptcies can stay for 10."},
            {"q": "What is the recommended credit utilization ratio?", "opts": ["Under 10%", "Under 30%", "Under 50%", "Under 70%"], "correct": 1, "expl": "Keep utilization under 30% (ideally under 10%) for best scores."},
            {"q": "How often can you get a free credit report from each bureau?", "opts": ["Monthly", "Every 6 months", "Annually", "Every 3 years"], "correct": 2, "expl": "AnnualCreditReport.com gives you one free report per bureau per year."},
            {"q": "What is a 'hard inquiry' on your credit report?", "opts": ["Checking your own score", "A lender checking your credit", "A soft credit check", "An error on your report"], "correct": 1, "expl": "Hard inquiries happen when you apply for credit and can lower your score slightly."},
            {"q": "How long does it take to build credit from scratch?", "opts": ["1 month", "3-6 months", "1 year", "2 years"], "correct": 1, "expl": "It takes 3-6 months of credit activity to generate a FICO score."},
            {"q": "What is the best first credit card for beginners?", "opts": ["Premium travel card", "Secured credit card", "Business credit card", "Store credit card"], "correct": 1, "expl": "Secured cards require a deposit and are designed for building credit."},
            {"q": "Does closing a credit card help your credit score?", "opts": ["Yes, always", "Yes, if it has a balance", "No, it usually hurts", "No effect"], "correct": 2, "expl": "Closing cards reduces available credit and can hurt your utilization ratio."},
            {"q": "What is the average credit score in the US?", "opts": ["650", "700", "718", "750"], "correct": 2, "expl": "The average FICO score is around 718 as of 2024."},
        ]
    },
    "credit-cards": {
        "title": "Credit Cards",
        "landing": "/credit-cards-quiz.html",
        "questions": [
            {"q": "What is the Schumer Box?", "opts": ["A type of credit card", "A fee disclosure table", "A credit limit", "A rewards program"], "correct": 1, "expl": "The Schumer Box is a standardized table that discloses all fees and APRs."},
            {"q": "What is a grace period on a credit card?", "opts": ["Late payment forgiveness", "Interest-free period to pay", "Extended warranty", "Fraud protection"], "correct": 1, "expl": "The grace period is the time between your statement date and payment due date when no interest is charged."},
            {"q": "What does APR stand for?", "opts": ["Annual Payment Rate", "Annual Percentage Rate", "Applied Payment Rate", "Average Payment Rate"], "correct": 1, "expl": "APR is the Annual Percentage Rate - the yearly cost of borrowing including fees."},
            {"q": "Which transaction type typically has the highest APR?", "opts": ["Purchases", "Balance transfers", "Cash advances", "Foreign transactions"], "correct": 2, "expl": "Cash advances usually have the highest APR and often have additional fees with no grace period."},
            {"q": "What is a balance transfer?", "opts": ["Moving debt to another card", "Paying off your card", "Splitting payments", "Adding an authorized user"], "correct": 0, "expl": "A balance transfer moves debt from one card to another, often to get a lower promotional rate."},
            {"q": "What is the typical minimum payment?", "opts": ["1-3% of balance", "10% of balance", "Fixed $25", "Full balance"], "correct": 0, "expl": "Minimum payments are usually 1-3% of your balance plus interest, or a flat fee like $25."},
            {"q": "What happens if you only pay the minimum?", "opts": ["No interest charged", "You pay off faster", "You pay significant interest", "Credit score improves"], "correct": 2, "expl": "Paying only the minimum means you carry a balance and pay interest, potentially for years."},
            {"q": "What is a credit card sign-up bonus?", "opts": ["Annual fee waiver", "Reward for spending threshold", "Lower APR", "Higher credit limit"], "correct": 1, "expl": "Sign-up bonuses reward you with points/cash back after spending a certain amount in the first months."},
            {"q": "What is an authorized user?", "opts": ["Card company employee", "Someone who can use your card", "Fraud protection service", "Credit counselor"], "correct": 1, "expl": "An authorized user gets their own card on your account but you're responsible for their charges."},
            {"q": "What is a foreign transaction fee?", "opts": ["Fee for late payments abroad", "Fee for purchases in foreign currency", "Fee for traveling", "Fee for currency exchange"], "correct": 1, "expl": "Foreign transaction fees (typically 3%) are charged on purchases made in non-USD currency."},
        ]
    },
    "prediction-markets": {
        "title": "Prediction Markets",
        "landing": "/prediction-markets-quiz.html",
        "questions": [
            {"q": "What is a prediction market?", "opts": ["A stock exchange", "A market for betting on event outcomes", "A weather forecast", "A sports book"], "correct": 1, "expl": "Prediction markets let you trade contracts on the probability of future events occurring."},
            {"q": "Which is a regulated US prediction market?", "opts": ["Polymarket", "Kalshi", "Augur", "BetFair"], "correct": 1, "expl": "Kalshi is CFTC-regulated and available to US traders. Polymarket is offshore."},
            {"q": "How are prediction market prices interpreted?", "opts": ["Dollar value", "Percentage probability", "Number of traders", "Time remaining"], "correct": 1, "expl": "A contract trading at 65 cents implies a 65% probability of that outcome occurring."},
            {"q": "What does 'Yes' mean in a prediction market?", "opts": ["You want the event to happen", "You're betting the event WILL happen", "You're betting against the event", "You approve the market"], "correct": 1, "expl": "Buying 'Yes' shares means you profit if the event occurs. Each share pays $1 if correct."},
            {"q": "What is market liquidity?", "opts": ["Total money in the market", "Ease of trading without moving prices", "Number of markets available", "Withdrawal speed"], "correct": 1, "expl": "High liquidity means you can buy/sell quickly at fair prices without affecting the market."},
            {"q": "What is the efficient market hypothesis?", "opts": ["Markets are always right", "Prices reflect all available information", "You can't beat the market", "All of the above"], "correct": 3, "expl": "EMH suggests prices incorporate all known info, making consistent outperformance difficult."},
            {"q": "What is arbitrage in prediction markets?", "opts": ["Guaranteed profit from price differences", "Illegal trading", "Market manipulation", "Insider trading"], "correct": 0, "expl": "Arbitrage exploits price differences - like when Yes+No prices don't sum to $1."},
            {"q": "What happens when a prediction market resolves?", "opts": ["Trading continues", "Winning shares pay out $1, losing shares $0", "All money is returned", "Market resets"], "correct": 1, "expl": "When the event outcome is known, winning contracts pay $1 per share, losers expire worthless."},
            {"q": "What is the 'wisdom of crowds'?", "opts": ["Group decisions are always right", "Aggregated predictions often beat experts", "Crowdfunding markets", "Social trading"], "correct": 1, "expl": "The wisdom of crowds theory says aggregated group predictions often outperform individual experts."},
            {"q": "What fees do prediction markets typically charge?", "opts": ["Monthly subscription", "Trading fees on profits only", "Fees on deposits", "No fees"], "correct": 1, "expl": "Most charge a percentage of profits only - you don't pay fees on losing trades or withdrawals."},
        ]
    },
    "taxes": {
        "title": "Taxes",
        "landing": "/taxes-quiz.html",
        "questions": [
            {"q": "What is the deadline to file federal taxes?", "opts": ["March 15", "April 15", "May 1", "June 15"], "correct": 1, "expl": "Federal taxes are typically due April 15, though it may shift if that date falls on a weekend."},
            {"q": "What is a W-2 form?", "opts": ["Contractor income report", "Employee wage statement", "Investment income", "Tax refund form"], "correct": 1, "expl": "W-2 reports your annual wages and taxes withheld. Employers must send by January 31."},
            {"q": "What is the standard deduction for single filers in 2024?", "opts": ["$12,000", "$13,850", "$15,000", "$25,900"], "correct": 1, "expl": "For 2024, the standard deduction is $13,850 for single filers and $27,700 for married filing jointly."},
            {"q": "What is a 1099 form used for?", "opts": ["Employee wages", "Non-employee income", "Tax refunds", "Property taxes"], "correct": 1, "expl": "1099 forms report income from freelancing, investments, rentals, and other non-wage sources."},
            {"q": "What does 'withholding' mean?", "opts": ["Taxes taken from paychecks", "Tax refund delay", "Audit process", "Tax extension"], "correct": 0, "expl": "Withholding is when your employer takes taxes from your paycheck and sends them to the IRS."},
            {"q": "What is a tax bracket?", "opts": ["Fixed tax rate for everyone", "Range of income taxed at a rate", "Tax filing category", "Refund amount"], "correct": 1, "expl": "Tax brackets are income ranges with specific rates. Only income within each bracket is taxed at that rate."},
            {"q": "What is an IRA?", "opts": ["International Revenue Account", "Individual Retirement Account", "Internal Refund Application", "Investment Return Agreement"], "correct": 1, "expl": "An IRA is an Individual Retirement Account with tax advantages for retirement savings."},
            {"q": "What happens if you file taxes late?", "opts": ["Nothing", "Penalty and interest charges", "Automatic extension", "Audit"], "correct": 1, "expl": "Late filing incurs penalties (5% per month) and interest on taxes owed. File even if you can't pay."},
            {"q": "What is a tax credit vs deduction?", "opts": ["Same thing", "Credit reduces tax owed, deduction reduces taxable income", "Deduction is better", "Credit is only for businesses"], "correct": 1, "expl": "Credits directly reduce your tax bill. Deductions reduce income that's taxed. Credits are usually better."},
            {"q": "Who needs to file taxes?", "opts": ["Everyone", "Only those who owe money", "Those meeting income thresholds", "Only W-2 employees"], "correct": 2, "expl": "Filing requirements depend on income, age, and filing status. Not everyone must file."},
        ]
    },
    "investing": {
        "title": "Investing",
        "landing": "/investing-quiz.html",
        "questions": [
            {"q": "What is compound interest?", "opts": ["Interest on principal only", "Interest earning interest", "Simple interest", "Bank fees"], "correct": 1, "expl": "Compound interest is when you earn interest on both your principal AND previously earned interest."},
            {"q": "What does diversification mean?", "opts": ["Investing in one stock", "Spreading investments across assets", "Timing the market", "Day trading"], "correct": 1, "expl": "Diversification spreads risk by holding different asset types, sectors, and geographies."},
            {"q": "What is an index fund?", "opts": ["Actively managed fund", "Fund tracking a market index", "High-fee investment", "Crypto fund"], "correct": 1, "expl": "Index funds passively track indexes like the S&P 500 with low fees and broad diversification."},
            {"q": "What is the S&P 500?", "opts": ["500 savings accounts", "Index of 500 large US companies", "Government bond", "International index"], "correct": 1, "expl": "The S&P 500 tracks 500 of the largest US publicly traded companies."},
            {"q": "What is a 401(k)?", "opts": ["Bank account", "Employer-sponsored retirement plan", "Stock ticker", "Tax form"], "correct": 1, "expl": "A 401(k) is an employer-sponsored retirement account with tax advantages and potential employer matching."},
            {"q": "What is dollar-cost averaging?", "opts": ["Investing all at once", "Investing fixed amounts regularly", "Timing market lows", "Currency trading"], "correct": 1, "expl": "Dollar-cost averaging invests fixed amounts at regular intervals, reducing timing risk."},
            {"q": "What is a bear market?", "opts": ["Market up 20%+", "Market down 20%+", "Sideways market", "New market high"], "correct": 1, "expl": "A bear market is a 20%+ decline from recent highs. Bull markets are 20%+ gains."},
            {"q": "What is an ETF?", "opts": ["Electronic Transfer Fund", "Exchange-Traded Fund", "Equity Tax Form", "Extended Trading Fund"], "correct": 1, "expl": "ETFs are exchange-traded funds that trade like stocks but hold diversified baskets of assets."},
            {"q": "What is a stock dividend?", "opts": ["Stock price increase", "Company profit sharing payment", "Stock split", "Trading fee"], "correct": 1, "expl": "Dividends are payments companies make to shareholders from profits, usually quarterly."},
            {"q": "What is risk tolerance?", "opts": ["Amount you can invest", "Your comfort with investment losses", "Investment time horizon", "Number of stocks owned"], "correct": 1, "expl": "Risk tolerance is your emotional and financial ability to handle investment losses without panic selling."},
        ]
    },
    "student-loans": {
        "title": "Student Loans",
        "landing": "/student-loans-quiz.html",
        "questions": [
            {"q": "What is the difference between subsidized and unsubsidized loans?", "opts": ["No difference", "Government pays interest on subsidized while in school", "Unsubsidized has lower rates", "Subsidized is private"], "correct": 1, "expl": "With subsidized loans, the government covers interest while you're in school. Unsubsidized accrues interest immediately."},
            {"q": "What is the FAFSA?", "opts": ["A loan servicer", "Financial aid application", "Scholarship program", "Bank account"], "correct": 1, "expl": "FAFSA is the Free Application for Federal Student Aid - required for federal loans and grants."},
            {"q": "What is loan deferment?", "opts": ["Loan forgiveness", "Temporary payment pause", "Lower interest rate", "Refinancing"], "correct": 1, "expl": "Deferment temporarily pauses payments, often without interest accrual on subsidized loans."},
            {"q": "What is the standard repayment term for federal loans?", "opts": ["5 years", "10 years", "20 years", "30 years"], "correct": 1, "expl": "Standard repayment is 10 years, though income-driven plans can extend to 20-25 years."},
            {"q": "What is loan consolidation?", "opts": ["Paying off loans", "Combining multiple loans into one", "Getting a cosigner", "Defaulting"], "correct": 1, "expl": "Consolidation combines multiple federal loans into one with a weighted average interest rate."},
            {"q": "What happens if you default on student loans?", "opts": ["Nothing", "Damaged credit, wage garnishment, lost eligibility", "Automatic forgiveness", "Lower payments"], "correct": 1, "expl": "Default damages credit, can lead to wage garnishment, tax refund seizure, and loss of federal benefits."},
            {"q": "What is Public Service Loan Forgiveness?", "opts": ["All loans forgiven after 10 years", "Forgiveness for qualifying public service work", "Military benefit only", "State program"], "correct": 1, "expl": "PSLF forgives remaining balance after 120 qualifying payments while working in public service."},
            {"q": "Can student loans be discharged in bankruptcy?", "opts": ["Yes, easily", "Rarely, must prove undue hardship", "Always", "Only private loans"], "correct": 1, "expl": "Student loans are extremely difficult to discharge in bankruptcy - you must prove 'undue hardship.'"},
            {"q": "What is an income-driven repayment plan?", "opts": ["Fixed payment plan", "Payments based on income and family size", "Graduated payment plan", "Extended repayment"], "correct": 1, "expl": "IDR plans cap payments at 10-20% of discretionary income with forgiveness after 20-25 years."},
            {"q": "What is a grace period?", "opts": ["Time before first payment is due after graduating", "Late payment forgiveness", "Interest-free period", "Loan application time"], "correct": 0, "expl": "The grace period is typically 6 months after graduating or dropping below half-time enrollment before payments begin."},
        ]
    },
    "budgeting": {
        "title": "Budgeting",
        "landing": "/budgeting-quiz.html",
        "questions": [
            {"q": "What is the 50/30/20 rule?", "opts": ["Investment strategy", "Budget allocation: needs/wants/savings", "Debt repayment plan", "Tax strategy"], "correct": 1, "expl": "50% needs, 30% wants, 20% savings/debt - a simple framework for budgeting after-tax income."},
            {"q": "What is discretionary income?", "opts": ["Total income", "Income after taxes and necessities", "Investment income", "Side hustle income"], "correct": 1, "expl": "Discretionary income is what's left after paying for essential needs like housing, food, and utilities."},
            {"q": "What is a zero-based budget?", "opts": ["No spending allowed", "Every dollar has a job, income minus expenses equals zero", "Budget with no savings", "Emergency budget"], "correct": 1, "expl": "Zero-based budgeting assigns every dollar to a category so income - expenses = $0 (including savings)."},
            {"q": "What is an emergency fund?", "opts": ["Investment account", "Savings for unexpected expenses", "Insurance policy", "Credit card"], "correct": 1, "expl": "An emergency fund covers unexpected costs like job loss or medical bills - aim for 3-6 months of expenses."},
            {"q": "What is the envelope method?", "opts": ["Mailing cash", "Using physical envelopes for budget categories", "Online banking", "Auto-pay system"], "correct": 1, "expl": "The envelope method puts cash in labeled envelopes for each spending category. When it's gone, spending stops."},
            {"q": "What does 'pay yourself first' mean?", "opts": ["Treat yourself to shopping", "Save before spending on wants", "Get a raise", "Invest in yourself"], "correct": 1, "expl": "Pay yourself first means automatically saving/investing before spending on discretionary items."},
            {"q": "What is a sinking fund?", "opts": ["Emergency fund", "Savings for planned future expenses", "Retirement account", "Debt payoff fund"], "correct": 1, "expl": "Sinking funds save gradually for predictable expenses like car repairs, holidays, or annual insurance."},
            {"q": "What is lifestyle creep?", "opts": ["Moving to a better neighborhood", "Increasing spending as income rises", "Downsizing", "Frugal living"], "correct": 1, "expl": "Lifestyle creep is when increased income leads to increased spending instead of increased saving."},
            {"q": "What is the difference between gross and net income?", "opts": ["Same thing", "Gross is before taxes, net is after", "Net is higher", "Gross includes investments"], "correct": 1, "expl": "Gross income is your total earnings before taxes and deductions. Net is your take-home pay."},
            {"q": "How often should you review your budget?", "opts": ["Once a year", "Monthly", "Only when in debt", "Never"], "correct": 1, "expl": "Review your budget monthly to track progress, adjust for changes, and stay on target with goals."},
        ]
    },
    "banking": {
        "title": "Banking",
        "landing": "/banking-quiz.html",
        "questions": [
            {"q": "What is the difference between a bank and credit union?", "opts": ["No difference", "Credit unions are member-owned nonprofits", "Banks have better rates", "Credit unions are online only"], "correct": 1, "expl": "Credit unions are not-for-profit cooperatives owned by members, often offering better rates and lower fees."},
            {"q": "What is FDIC insurance?", "opts": ["Investment protection", "Bank deposit insurance up to $250,000", "Credit card protection", "Loan guarantee"], "correct": 1, "expl": "FDIC insures bank deposits up to $250,000 per depositor, per bank. Credit unions have NCUA insurance."},
            {"q": "What is an overdraft fee?", "opts": ["Monthly account fee", "Charge for spending more than your balance", "ATM fee", "Wire transfer fee"], "correct": 1, "expl": "Overdraft fees (often $35+) are charged when you spend more than your available balance."},
            {"q": "What is APY?", "opts": ["Annual Payment Yield", "Annual Percentage Yield", "Applied Percentage Yearly", "Average Payment Yield"], "correct": 1, "expl": "APY is Annual Percentage Yield - the real rate of return on savings including compound interest."},
            {"q": "What is a certificate of deposit (CD)?", "opts": ["Savings account with unlimited access", "Time deposit with fixed rate and term", "Checking account", "Investment fund"], "correct": 1, "expl": "CDs lock your money for a set term (months to years) in exchange for a guaranteed interest rate."},
            {"q": "What is a money market account?", "opts": ["Stock market investment", "Savings account with check-writing", "Checking account", "Retirement account"], "correct": 1, "expl": "Money market accounts are savings accounts that may offer check-writing and debit card access with higher rates."},
            {"q": "What is a wire transfer?", "opts": ["Electronic transfer between banks", "Physical cash transfer", "Check deposit", "ATM withdrawal"], "correct": 0, "expl": "Wire transfers electronically move money between banks, often same-day, with fees typically $15-30."},
            {"q": "What is direct deposit?", "opts": ["Cash deposit", "Electronic payment to your account", "Check deposit", "Mobile deposit"], "correct": 1, "expl": "Direct deposit electronically transfers paychecks or benefits directly into your bank account."},
            {"q": "What is a routing number?", "opts": ["Your account number", "Bank identifier for transfers", "SWIFT code", "Credit score"], "correct": 1, "expl": "Routing numbers identify your bank for ACH transfers, direct deposits, and wire transfers."},
            {"q": "What is mobile check deposit?", "opts": ["Mailing a check", "Depositing via phone camera", "ATM deposit", "In-person deposit"], "correct": 1, "expl": "Mobile deposit lets you deposit checks by photographing them with your banking app."},
        ]
    },
    "make-money-online": {
        "title": "Make Money Online",
        "landing": "/make-money-online-quiz.html",
        "questions": [
            {"q": "What is freelancing?", "opts": ["Working for one company", "Independent contract work", "Unpaid internship", "Government job"], "correct": 1, "expl": "Freelancing is working independently on projects for multiple clients rather than as an employee."},
            {"q": "What is dropshipping?", "opts": ["Shipping packages yourself", "Selling without holding inventory", "Retail arbitrage", "Wholesale buying"], "correct": 1, "expl": "Dropshipping lets you sell products that are shipped directly from supplier to customer - no inventory needed."},
            {"q": "What is affiliate marketing?", "opts": ["Creating products", "Earning commission promoting others' products", "Social media ads", "Email marketing"], "correct": 1, "expl": "Affiliate marketing earns you commission when people buy through your referral links."},
            {"q": "What is a common red flag for online job scams?", "opts": ["Requires specific skills", "Asks you to pay to start working", "Has a website", "Requires resume"], "correct": 1, "expl": "Legitimate jobs never ask you to pay upfront. Be wary of 'pay $99 to start earning thousands' schemes."},
            {"q": "What is passive income?", "opts": ["Salary from job", "Earnings requiring little ongoing effort", "Side hustle income", "Investment losses"], "correct": 1, "expl": "Passive income continues earning with minimal active work, like dividends, royalties, or rental income."},
            {"q": "What is print-on-demand?", "opts": ["Printing at home", "Products printed when ordered", "Bulk printing", "Newspaper delivery"], "correct": 1, "expl": "Print-on-demand creates custom products (t-shirts, mugs) only when customers order, eliminating inventory risk."},
            {"q": "What is a digital product?", "opts": ["Physical electronics", "Downloadable items like ebooks or courses", "Online ads", "Website hosting"], "correct": 1, "expl": "Digital products (ebooks, templates, courses, software) can be sold infinitely with no inventory costs."},
            {"q": "What is Fiverr?", "opts": ["Investment platform", "Freelance services marketplace", "Social network", "Banking app"], "correct": 1, "expl": "Fiverr is a marketplace where freelancers offer services ('gigs') starting at $5 in categories like design, writing, and programming."},
            {"q": "What is user testing?", "opts": ["Software development", "Getting paid to test websites/apps", "Product manufacturing", "Quality control"], "correct": 1, "expl": "User testing pays you to provide feedback on websites and apps, typically $10 per 20-minute test."},
            {"q": "What is the most important factor for online success?", "opts": ["Luck", "Consistency and providing value", "Having money to start", "Being first to market"], "correct": 1, "expl": "Consistently showing up and genuinely helping your audience beats get-rich-quick schemes every time."},
        ]
    },
    "credit-rewards": {
        "title": "Credit Card Rewards",
        "landing": "/quiz-credit-rewards.html",
        "questions": [
            {"q": "What is a credit card signup bonus?", "opts": ["Annual fee waiver", "Reward for spending threshold", "Lower APR", "Higher credit limit"], "correct": 1, "expl": "Signup bonuses reward you with points/cash back after spending a certain amount in the first months."},
            {"q": "Which type of reward is most flexible?", "opts": ["Airline miles", "Hotel points", "Cash back", "Store credit"], "correct": 2, "expl": "Cash back is the most flexible - you can use it for anything, not just travel or specific stores."},
            {"q": "What is the typical value of 1 credit card point?", "opts": ["$0.01", "$0.05", "$0.10", "$1.00"], "correct": 0, "expl": "Most points are worth about 1 cent each, though travel redemptions can increase this value."},
            {"q": "What is a rotating category card?", "opts": ["Card with fixed rewards", "Card with changing bonus categories", "Card with no rewards", "Card for rotating balances"], "correct": 1, "expl": "Rotating category cards offer 5% back in categories that change quarterly, like gas, groceries, or Amazon."},
            {"q": "What is point devaluation?", "opts": ["Points gaining value", "Points losing value over time", "Points expiring", "Points being stolen"], "correct": 1, "expl": "Point devaluation occurs when issuers increase redemption costs, making your points worth less."},
            {"q": "What is the best strategy for maximizing rewards?", "opts": ["Use one card for everything", "Use multiple cards for different categories", "Only use debit cards", "Avoid credit cards entirely"], "correct": 1, "expl": "Using multiple cards strategically - like 5% on groceries, 3% on dining, 2% on everything else - maximizes rewards."},
            {"q": "What is a statement credit?", "opts": ["A loan", "Money applied to your credit card bill", "A late fee", "An annual fee"], "correct": 1, "expl": "Statement credits reduce your credit card balance - it's like getting cash back applied directly to your bill."},
            {"q": "Do credit card rewards expire?", "opts": ["Never", "Always after 1 year", "It depends on the program", "Only cash back expires"], "correct": 2, "expl": "Some rewards never expire, others expire after periods of inactivity or fixed timeframes - check your program terms."},
            {"q": "What is transfer partner optimization?", "opts": ["Moving balances between cards", "Transferring points to airline/hotel programs for better value", "Selling points", "Buying points"], "correct": 1, "expl": "Transferring points to partners like airlines can increase value from 1 cent to 2+ cents per point."},
            {"q": "What should you do before canceling a rewards card?", "opts": ["Nothing", "Use or transfer all your points", "Max out the credit limit", "Apply for a new card first"], "correct": 1, "expl": "Before canceling, use or transfer your points - you typically lose them when you close the account."},
        ]
    },
    "fed-rates": {
        "title": "Fed Rates & Your Money",
        "landing": "/quiz-fed-rates.html",
        "questions": [
            {"q": "What does the Federal Reserve control?", "opts": ["Stock prices", "The federal funds rate", "Tax rates", "Mortgage rates directly"], "correct": 1, "expl": "The Fed controls the federal funds rate - the rate banks charge each other for overnight loans."},
            {"q": "How do Fed rate changes affect credit cards?", "opts": ["No effect", "APR changes with prime rate", "Only affects new cards", "Only affects business cards"], "correct": 1, "expl": "Most credit cards have variable APRs tied to the prime rate, which follows Fed rate changes."},
            {"q": "What happens to savings rates when the Fed raises rates?", "opts": ["They decrease", "They typically increase", "Nothing changes", "They become taxable"], "correct": 1, "expl": "When the Fed raises rates, banks usually increase savings account and CD rates to compete for deposits."},
            {"q": "How quickly do Fed rate changes affect mortgage rates?", "opts": ["Immediately", "Within days", "Mortgage rates are more influenced by long-term bonds", "Only affects new mortgages"], "correct": 2, "expl": "Mortgage rates follow 10-year Treasury yields more closely than the Fed funds rate - it's an indirect relationship."},
            {"q": "What is the prime rate?", "opts": ["The best interest rate available", "The rate banks charge their best customers", "The Fed funds rate", "The inflation rate"], "correct": 1, "expl": "The prime rate is what banks charge their most creditworthy customers, typically 3% above the Fed funds rate."},
            {"q": "Why does the Fed change interest rates?", "opts": ["To control inflation and employment", "To help the stock market", "To set mortgage rates", "To increase bank profits"], "correct": 0, "expl": "The Fed's dual mandate is to maintain price stability (control inflation) and maximum employment."},
            {"q": "What happens to car loans when rates rise?", "opts": ["Rates decrease", "Rates increase, making payments higher", "Only used cars are affected", "No effect on auto loans"], "correct": 1, "expl": "Auto loan rates typically rise with Fed rates, increasing monthly payments for the same car price."},
            {"q": "How often does the Federal Reserve meet?", "opts": ["Monthly", "8 times per year", "Quarterly", "Annually"], "correct": 1, "expl": "The Federal Open Market Committee (FOMC) meets 8 times per year to set monetary policy."},
            {"q": "What is quantitative easing?", "opts": ["Raising interest rates", "The Fed buying bonds to lower rates", "Increasing taxes", "Reducing the money supply"], "correct": 1, "expl": "Quantitative easing is when the Fed buys government bonds to increase money supply and lower long-term rates."},
            {"q": "Should you pay off debt faster when rates rise?", "opts": ["No, keep minimum payments", "Yes, especially variable-rate debt", "Only pay off mortgages", "Wait for rates to fall again"], "correct": 1, "expl": "When rates rise, paying off variable-rate debt (credit cards, HELOCs) faster saves more money."},
        ]
    },
    "auto-loans": {
        "title": "Auto Loans",
        "landing": "/auto-loans-quiz.html",
        "questions": [
            {"q": "What is the typical auto loan term?", "opts": ["12-24 months", "36-72 months", "84-96 months", "120+ months"], "correct": 1, "expl": "Most auto loans range from 36-72 months (3-6 years). Longer terms mean lower payments but more interest paid overall."},
            {"q": "What is a good credit score for the best auto loan rates?", "opts": ["600-650", "660-719", "720+", "500-599"], "correct": 2, "expl": "Credit scores of 720+ typically qualify for the best auto loan rates, often below 5% APR."},
            {"q": "What does 'being upside down' on a car loan mean?", "opts": ["You owe more than the car is worth", "Your car is parked incorrectly", "You missed payments", "You have excellent credit"], "correct": 0, "expl": "Being upside down means you owe more on the loan than the car's current value - common with new cars that depreciate quickly."},
            {"q": "Should you get pre-approved for an auto loan before shopping?", "opts": ["No, it hurts your credit", "Yes, it gives you negotiating power", "Only for used cars", "Only if you have bad credit"], "correct": 1, "expl": "Pre-approval shows dealers you're serious and gives you a rate to compare against their financing offers."},
            {"q": "What is a captive lender?", "opts": ["A bank that only loans to prisoners", "A finance company owned by the car manufacturer", "A credit union", "An online lender"], "correct": 1, "expl": "Captive lenders like Toyota Financial or Ford Credit are owned by manufacturers and often offer promotional rates."},
            {"q": "How much should your monthly car payment be relative to income?", "opts": ["Less than 10% of gross monthly income", "15-20% of gross income", "25-30% of gross income", "As much as you can afford"], "correct": 0, "expl": "Financial experts recommend keeping total car costs (payment, insurance, gas) under 10-15% of gross monthly income."},
            {"q": "What is gap insurance?", "opts": ["Insurance for gaps in employment", "Coverage that pays the difference between loan balance and car value if totaled", "Extended warranty", "Theft protection"], "correct": 1, "expl": "Gap insurance covers the difference if your car is totaled and you owe more than the insurance payout - valuable for new cars with large loans."},
            {"q": "Is it better to finance through a dealer or your bank?", "opts": ["Always the dealer", "Always your bank", "Compare both to get the best rate", "It doesn't matter"], "correct": 2, "expl": "Always compare rates. Dealers may offer promotional rates, but banks and credit unions often have competitive or better rates."},
            {"q": "What happens if you miss an auto loan payment?", "opts": ["Nothing for 90 days", "Late fee and credit score damage", "Car is immediately repossessed", "Loan is forgiven"], "correct": 1, "expl": "Missing payments results in late fees (typically $25-50), credit score damage, and after 60-90 days, risk of repossession."},
            {"q": "Should you make a down payment on a car?", "opts": ["No, put $0 down", "Yes, at least 10-20% for new cars", "Only for used cars", "Only if you have bad credit"], "correct": 1, "expl": "A 10-20% down payment reduces your loan amount, lowers monthly payments, and helps avoid being upside down on the loan."},
        ]
    },
    "car-shopping": {
        "title": "Shopping for a Car",
        "landing": "/car-shopping-quiz.html",
        "questions": [
            {"q": "What is the biggest factor in a car's depreciation?", "opts": ["Color", "Brand reputation", "Mileage and age", "Number of previous owners"], "correct": 2, "expl": "Mileage and age are the biggest depreciation factors. A new car loses 20-30% of value in the first year alone."},
            {"q": "When is the best time to buy a new car?", "opts": ["January", "End of the month/quarter", "Summer", "It doesn't matter"], "correct": 1, "expl": "End of month, quarter, or model year when dealers need to meet sales quotas and clear inventory for new models."},
            {"q": "What does MSRP stand for?", "opts": ["Minimum Sale Retail Price", "Manufacturer's Suggested Retail Price", "Monthly Sale Rate Payment", "Maximum Sale Retail Price"], "correct": 1, "expl": "MSRP is the sticker price set by the manufacturer - the starting point for negotiations, not the final price."},
            {"q": "Should you buy new or used?", "opts": ["Always new for reliability", "Always used for value", "Depends on your budget and needs", "Leasing is always better"], "correct": 2, "expl": "New cars offer latest features and warranties but depreciate fast. Used cars offer better value but may have higher maintenance costs."},
            {"q": "What is a certified pre-owned (CPO) vehicle?", "opts": ["Any used car", "A used car with manufacturer warranty and inspection", "A car with cosmetic damage", "A rental car"], "correct": 1, "expl": "CPO vehicles are late-model used cars that pass manufacturer inspections and come with extended warranties - a middle ground between new and used."},
            {"q": "How much should you budget for maintenance?", "opts": ["Nothing for the first 5 years", "$500-1,000 per year", "$100 per month", "Only oil changes"], "correct": 1, "expl": "Budget $500-1,000 annually for maintenance. New cars cost less initially, while older cars may need more repairs."},
            {"q": "What is the out-the-door price?", "opts": ["Just the car's sticker price", "Total price including taxes, fees, and extras", "The monthly payment", "The trade-in value"], "correct": 1, "expl": "Out-the-door price is the total you'll actually pay including car price, taxes, registration, documentation fees, and any add-ons."},
            {"q": "Should you trade in your old car or sell it privately?", "opts": ["Always trade in for convenience", "Always sell privately for more money", "Compare offers - private sales often get 10-20% more", "It doesn't matter"], "correct": 2, "expl": "Private sales typically yield 10-20% more than trade-ins, but trading in is more convenient and reduces sales tax in some states."},
            {"q": "What is the 20/4/10 rule for car buying?", "opts": ["20% down, 4-year loan, 10% of income on transportation", "20% interest rate, 4 payments, 10 years", "$20k car, $4k down, $10k loan", "20 mpg, 4 cylinders, 10-year warranty"], "correct": 0, "expl": "20% down payment, 4-year maximum loan term, and transportation costs under 10% of gross income."},
            {"q": "What should you check during a test drive?", "opts": ["Only the radio", "Acceleration, brakes, steering, comfort, and visibility", "Just the exterior", "Only the price"], "correct": 1, "expl": "Test acceleration, braking, steering response, seat comfort, visibility, noise levels, and how it handles bumps and turns."},
        ]
    },
    "auto-insurance": {
        "title": "Auto Insurance",
        "landing": "/auto-insurance-quiz.html",
        "questions": [
            {"q": "What is liability insurance?", "opts": ["Coverage for your own car damage", "Coverage for damage you cause to others", "Coverage for theft", "Coverage for medical bills only"], "correct": 1, "expl": "Liability covers damage/injuries you cause to others. It's required in most states but doesn't cover your own vehicle."},
            {"q": "What is a deductible?", "opts": ["Your monthly premium", "Amount you pay before insurance kicks in", "The insurance company's profit", "Your agent's commission"], "correct": 1, "expl": "A deductible is what you pay out-of-pocket before insurance covers the rest. Higher deductibles mean lower premiums."},
            {"q": "What does comprehensive coverage protect against?", "opts": ["Only collision damage", "Theft, vandalism, weather, fire, hitting animals", "Medical bills", "Other drivers' mistakes"], "correct": 1, "expl": "Comprehensive covers non-collision damage: theft, vandalism, fire, weather damage, and hitting animals."},
            {"q": "What factors affect your insurance premium?", "opts": ["Only your car's color", "Driving record, age, location, car type, credit score", "Only your income", "Only the car's age"], "correct": 1, "expl": "Premiums are based on driving record, age, location, vehicle type, credit score, mileage, and coverage levels."},
            {"q": "What is uninsured motorist coverage?", "opts": ["Insurance for your uninsured car", "Protection if hit by a driver without insurance", "Coverage for rental cars", "Minimum required coverage"], "correct": 1, "expl": "Uninsured motorist coverage pays for your injuries/damages if hit by a driver with no insurance or in a hit-and-run."},
            {"q": "Should you get gap insurance?", "opts": ["Always for any car", "Only if you owe more than the car is worth", "Never, it's a scam", "Only for luxury cars"], "correct": 1, "expl": "Gap insurance is valuable if you have a large loan on a new car that depreciates faster than you pay it off."},
            {"q": "How often should you shop for new insurance rates?", "opts": ["Never, stay loyal to one company", "Every 6-12 months", "Only when you buy a new car", "Every 5 years"], "correct": 1, "expl": "Comparing rates annually or when your policy renews can save hundreds, as rates change and new discounts become available."},
            {"q": "What is a no-fault state?", "opts": ["A state with no insurance requirements", "A state where your insurance pays regardless of who caused the accident", "A state with free insurance", "A state with no accidents"], "correct": 1, "expl": "In no-fault states, your own insurance covers your injuries regardless of who caused the accident, reducing lawsuits."},
            {"q": "What does collision coverage pay for?", "opts": ["Medical bills", "Damage to your car from accidents you cause", "Damage from theft", "Other people's cars"], "correct": 1, "expl": "Collision covers damage to your vehicle from accidents you cause, regardless of fault. Usually required for financed cars."},
            {"q": "What discount can you get for good grades?", "opts": ["None, grades don't matter", "Good student discount (typically 10-25% off)", "Only for college graduates", "Only for teachers"], "correct": 1, "expl": "Many insurers offer good student discounts (10-25% off) for full-time students with B averages or higher, as they're seen as more responsible."},
        ]
    },
    "ai-skills": {
        "title": "AI Skills for Career Growth",
        "landing": "/ai-skills-quiz.html",
        "questions": [
            {"q": "Which AI tool is best for writing and content creation?", "opts": ["Only Photoshop", "ChatGPT, Claude, or Gemini", "Only Excel", "Only programming tools"], "correct": 1, "expl": "ChatGPT, Claude, and Gemini are leading AI writing assistants that can help with emails, reports, creative writing, and more."},
            {"q": "What is prompt engineering?", "opts": ["Building physical machines", "Crafting effective instructions for AI tools", "Only for software engineers", "A type of engineering degree"], "correct": 1, "expl": "Prompt engineering is the skill of writing clear, specific instructions to get the best results from AI tools."},
            {"q": "Which AI tool creates images from text descriptions?", "opts": ["Only Word", "Midjourney, DALL-E, or Stable Diffusion", "Only calculators", "Only spreadsheets"], "correct": 1, "expl": "Midjourney, DALL-E, and Stable Diffusion are popular AI image generators that create visuals from text prompts."},
            {"q": "How can AI help with job searching?", "opts": ["It can't help at all", "Resume optimization, interview prep, and finding opportunities", "Only for tech jobs", "Only for writing cover letters"], "correct": 1, "expl": "AI can optimize resumes for ATS systems, prepare interview answers, research companies, and identify relevant job postings."},
            {"q": "What is the best way to learn AI tools?", "opts": ["Only formal college courses", "Hands-on practice with real projects", "Reading about them only", "Avoiding them entirely"], "correct": 1, "expl": "The best way to learn AI tools is hands-on practice. Start with free versions, experiment daily, and apply them to real tasks."},
            {"q": "Which skill is most valuable with AI tools?", "opts": ["Only coding", "Critical thinking and problem-solving", "Only graphic design", "Only writing"], "correct": 1, "expl": "Critical thinking and problem-solving are most valuable. AI is a tool - you need to know what to ask, how to evaluate answers, and when to use it."},
            {"q": "Can AI replace your job?", "opts": ["Yes, all jobs immediately", "It can automate tasks but creates new opportunities for those who adapt", "No, AI is useless", "Only manual labor jobs"], "correct": 1, "expl": "AI automates specific tasks but creates demand for people who can use it effectively. Adaptability and AI literacy are key career skills."},
            {"q": "What is GitHub Copilot?", "opts": ["A social media app", "AI pair programmer that suggests code", "A video game", "A type of insurance"], "correct": 1, "expl": "GitHub Copilot is an AI coding assistant that suggests code completions, helping programmers write faster and learn new languages."},
            {"q": "How much do AI skills increase earning potential?", "opts": ["No impact", "Studies show 10-50% salary increases for AI-proficient workers", "Only affects minimum wage jobs", "Only affects CEOs"], "correct": 1, "expl": "Workers with AI skills command 10-50% higher salaries in many fields, as they can accomplish more in less time."},
            {"q": "What is the first AI tool you should learn?", "opts": ["Only the most complex one", "ChatGPT - it's versatile and user-friendly", "Only industry-specific tools", "None, avoid AI"], "correct": 1, "expl": "ChatGPT is the best starting point - it's free, versatile for writing/analysis/coding help, and teaches you how to work with AI."},
        ]
    },
    "glp1-effects": {
        "title": "GLP-1 Effects on Mind & Finances",
        "landing": "/glp1-effects-quiz.html",
        "questions": [
            {"q": "What are GLP-1 drugs primarily used for?", "opts": ["Only diabetes", "Type 2 diabetes and weight management", "Only heart disease", "Only cosmetic purposes"], "correct": 1, "expl": "GLP-1 drugs like Ozempic and Wegovy are used for Type 2 diabetes management and weight loss, with growing off-label use for obesity."},
            {"q": "What is the monthly cost of GLP-1 medications without insurance?", "opts": ["$10-50", "$100-200", "$800-1,400+", "$50-100"], "correct": 2, "expl": "Without insurance, GLP-1 drugs can cost $800-1,400+ per month, making them a significant financial consideration for most people."},
            {"q": "How can GLP-1 drugs affect food spending?", "opts": ["Increase food costs", "Reduce food spending by 10-30% due to decreased appetite", "No effect on spending", "Only increase restaurant spending"], "correct": 1, "expl": "Many users report spending 10-30% less on food due to reduced appetite, potentially offsetting some medication costs."},
            {"q": "What mental health benefit have some GLP-1 users reported?", "opts": ["Only anxiety", "Reduced food noise/obsessive thoughts about eating", "Only depression", "No mental effects"], "correct": 1, "expl": "Many users report reduced 'food noise' - the constant obsessive thoughts about eating - leading to improved mental well-being."},
            {"q": "What happens if you stop taking GLP-1 drugs?", "opts": ["Weight stays off permanently", "Most people regain weight within a year", "No changes occur", "You immediately gain double the weight"], "correct": 1, "expl": "Studies show most people regain significant weight within a year of stopping, as appetite returns and metabolic adaptations reverse."},
            {"q": "How might GLP-1 drugs affect clothing expenses?", "opts": ["No change", "Initial increase as sizes change, then stabilization", "Only decrease", "Only increase"], "correct": 1, "expl": "Rapid weight loss often requires buying new clothes multiple times, creating a temporary but significant expense."},
            {"q": "What percentage of weight loss is typical with GLP-1 drugs?", "opts": ["1-5%", "10-15%", "15-20% of body weight on average", "50%+"], "correct": 2, "expl": "Clinical trials show average weight loss of 15-20% of body weight, with some losing more and some less."},
            {"q": "What hidden cost should GLP-1 users budget for?", "opts": ["Only the medication", "New wardrobes, potential supplements, and higher protein food costs", "Only gym memberships", "Only doctor visits"], "correct": 1, "expl": "Beyond medication, budget for new clothes, potentially higher protein food costs, supplements, and more frequent medical monitoring."},
            {"q": "How do GLP-1 drugs affect productivity?", "opts": ["No effect", "Many report increased energy and productivity after initial adjustment", "Always decrease productivity", "Only affect physical work"], "correct": 1, "expl": "After initial adjustment period, many users report increased energy, better focus, and improved productivity from weight loss and better metabolic health."},
            {"q": "What is 'food noise' that GLP-1 users mention?", "opts": ["Loud eating sounds", "Constant obsessive thoughts about food and eating", "Restaurant background music", "Cooking sounds"], "correct": 1, "expl": "Food noise refers to persistent, intrusive thoughts about food, eating, and cravings that many people experience - often reduced by GLP-1 medications."},
        ]
    }
}

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{quiz_title} Quiz - Question {q_num} of {total}</title>
    <meta name="description" content="{quiz_title} Quiz - Test your knowledge. Question {q_num} of {total}.">
    <meta name="robots" content="noindex, nofollow">
    <link rel="stylesheet" href="/styles.css">
    <style>
        .quiz-page {{ padding: 40px 0; min-height: calc(100vh - 200px); }}
        .quiz-container {{ max-width: 700px; margin: 0 auto; background: white; border-radius: 16px; padding: 40px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }}
        .quiz-header {{ text-align: center; margin-bottom: 32px; }}
        .category-tag {{ display: inline-block; background: #6366f1; color: white; padding: 6px 16px; border-radius: 20px; font-size: 0.875rem; font-weight: 600; margin-bottom: 16px; }}
        .progress-container {{ margin-bottom: 32px; }}
        .progress-bar-bg {{ background: #e2e8f0; height: 8px; border-radius: 4px; overflow: hidden; }}
        .progress-bar {{ background: linear-gradient(90deg, #6366f1, #8b5cf6); height: 100%; border-radius: 4px; }}
        .progress-text {{ font-size: 0.875rem; color: #64748b; margin-top: 8px; text-align: center; }}
        .question-container h2 {{ font-size: 1.5rem; margin-bottom: 24px; line-height: 1.5; }}
        .options-list {{ display: flex; flex-direction: column; gap: 12px; }}
        .option {{ background: white; border: 2px solid #e2e8f0; padding: 16px 20px; border-radius: 12px; cursor: pointer; transition: all 0.2s; font-size: 1rem; text-align: left; }}
        .option:hover {{ border-color: #6366f1; background: #f8fafc; }}
        .explanation {{ margin-top: 24px; padding: 20px; border-radius: 12px; display: none; }}
        .explanation.correct {{ background: #d1fae5; border: 1px solid #10b981; display: block; }}
        .explanation.incorrect {{ background: #fee2e2; border: 1px solid #ef4444; display: block; }}
        .next-btn {{ margin-top: 16px; background: #6366f1; color: white; border: none; padding: 14px 28px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 1rem; text-decoration: none; display: inline-block; }}
        .ad-container {{ max-width: 700px; margin: 32px auto; text-align: center; }}
        .ad-label {{ font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-bottom: 8px; }}
        .error-message {{ background: #fee2e2; border: 1px solid #ef4444; color: #b91c1c; padding: 20px; border-radius: 12px; text-align: center; display: none; }}
    </style>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
    <script src="/quiz-token.js"></script>
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <a href="/" class="logo">💳 Credit Gamer Area</a>
        </div>
    </nav>

    <div id="error-msg" class="error-message" style="max-width: 700px; margin: 40px auto;">
        <h3>⚠️ Invalid Access</h3>
        <p>Please start the quiz from the beginning.</p>
        <a href="{landing_page}" class="next-btn">Go to Quiz Start</a>
    </div>

    <section class="quiz-page" id="quiz-content">
        <div class="container">
            <div class="quiz-container">
                <div class="quiz-header">
                    <span class="category-tag">{quiz_title} - Question {q_num} of {total}</span>
                </div>
                
                <div class="progress-container">
                    <div class="progress-bar-bg">
                        <div class="progress-bar" style="width: {progress}%;"></div>
                    </div>
                    <div class="progress-text">Question {q_num} of {total}</div>
                </div>
                
                <div class="question-container">
                    <h2>{question}</h2>
                    <div class="options-list">
                        <button class="option" onclick="selectAnswer(0, {correct})">{opt0}</button>
                        <button class="option" onclick="selectAnswer(1, {correct})">{opt1}</button>
                        <button class="option" onclick="selectAnswer(2, {correct})">{opt2}</button>
                        <button class="option" onclick="selectAnswer(3, {correct})">{opt3}</button>
                    </div>
                    
                    <div id="explanation" class="explanation">
                        <h4 id="result-text"></h4>
                        <p>{explanation}</p>
                        <button id="next-btn" class="next-btn" onclick="goToNext()">{next_text}</button>
                    </div>
                </div>
            </div>
            
            <div class="ad-container">
                <div class="ad-label">Advertisement</div>
                <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins>
                <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
            </div>
        </div>
    </section>

    <footer class="footer" style="background: #1e1b4b; color: white; padding: 40px 0; text-align: center;">
        <div class="container">
            <p>&copy; 2026 Credit Gamer Area. All rights reserved.</p>
        </div>
    </footer>

    <script>
        const QUIZ_NAME = '{quiz_id}';
        const QUESTION_NUM = {q_num};
        const IS_LAST = {is_last};
        
        // Validate token on page load
        document.addEventListener('DOMContentLoaded', function() {{
            const params = QuizToken.getParams();
            
            // First question doesn't need token
            if (QUESTION_NUM === 1) {{
                sessionStorage.setItem('{quiz_abbr}_score', '0');
                return;
            }}
            
            // Validate token for subsequent questions
            if (!params.token || !QuizToken.validate(params.token, QUIZ_NAME, QUESTION_NUM - 1, params.score)) {{
                document.getElementById('quiz-content').style.display = 'none';
                document.getElementById('error-msg').style.display = 'block';
            }} else {{
                // Update score from token
                sessionStorage.setItem('{quiz_abbr}_score', params.score.toString());
            }}
        }});
        
        let answered = false;
        let currentScore = parseInt(sessionStorage.getItem('{quiz_abbr}_score') || '0');
        
        function selectAnswer(selected, correct) {{
            if (answered) return;
            answered = true;
            
            const isCorrect = selected === correct;
            const explanation = document.getElementById('explanation');
            const resultText = document.getElementById('result-text');
            
            document.querySelectorAll('.option').forEach((btn, idx) => {{
                btn.style.pointerEvents = 'none';
                if (idx === correct) {{
                    btn.style.borderColor = '#10b981';
                    btn.style.background = '#d1fae5';
                }} else if (idx === selected && !isCorrect) {{
                    btn.style.borderColor = '#ef4444';
                    btn.style.background = '#fee2e2';
                }}
            }});
            
            explanation.className = 'explanation ' + (isCorrect ? 'correct' : 'incorrect');
            resultText.textContent = isCorrect ? '✓ Correct!' : '✗ Incorrect';
            
            if (isCorrect) {{
                currentScore++;
                sessionStorage.setItem('{quiz_abbr}_score', currentScore.toString());
            }}
        }}
        
        function goToNext() {{
            if (IS_LAST) {{
                // Go to completion page with token
                window.location.href = QuizToken.buildUrl('/quiz-complete.html', QUIZ_NAME, 'complete', currentScore);
            }} else {{
                // Go to next question with token
                window.location.href = QuizToken.buildUrl('{next_page}', QUIZ_NAME, QUESTION_NUM + 1, currentScore);
            }}
        }}
    </script>
</body>
</html>'''

def generate_quiz(quiz_id):
    """Generate all question pages for a quiz."""
    if quiz_id not in QUIZ_DATA:
        print(f"Unknown quiz: {quiz_id}")
        print(f"Available: {', '.join(QUIZ_DATA.keys())}")
        return False
    
    quiz = QUIZ_DATA[quiz_id]
    quiz_dir = f"/root/.openclaw/workspace/triviacaptain-website/quiz/{quiz_id}"
    os.makedirs(quiz_dir, exist_ok=True)
    
    questions = quiz["questions"]
    total = len(questions)
    quiz_abbr = quiz_id.replace("-", "")[:4]
    
    for i, q in enumerate(questions):
        q_num = i + 1
        next_q = q_num + 1
        progress = q_num * 10
        is_last = "true" if q_num == total else "false"
        next_page = "/quiz-complete.html" if q_num == total else f"q{next_q}.html"
        next_text = "See Results →" if q_num == total else "Next Question →"
        
        html = HTML_TEMPLATE.format(
            quiz_title=quiz["title"],
            quiz_id=quiz_id,
            quiz_abbr=quiz_abbr,
            landing_page=quiz["landing"],
            q_num=q_num,
            total=total,
            progress=progress,
            question=q["q"],
            opt0=q["opts"][0],
            opt1=q["opts"][1],
            opt2=q["opts"][2],
            opt3=q["opts"][3],
            correct=q["correct"],
            explanation=q["expl"],
            is_last=is_last,
            next_page=next_page,
            next_text=next_text
        )
        
        filepath = os.path.join(quiz_dir, f"q{q_num}.html")
        with open(filepath, 'w') as f:
            f.write(html)
        print(f"Created {filepath}")
    
    print(f"\nAll {total} question pages created for {quiz['title']}!")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate-quiz.py <quiz-id>")
        print(f"Available quizzes: {', '.join(QUIZ_DATA.keys())}")
        sys.exit(1)
    
    quiz_id = sys.argv[1]
    success = generate_quiz(quiz_id)
    sys.exit(0 if success else 1)

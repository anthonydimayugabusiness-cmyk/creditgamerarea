#!/bin/bash
# Generate quiz question pages

QUIZ_DIR="/root/.openclaw/workspace/triviacaptain-website/quiz/credit-basics"
mkdir -p "$QUIZ_DIR"

# Question data
questions=(
    "What is the most commonly used credit scoring model?|VantageScore|FICO Score|Experian Score|TransUnion Score|1|FICO Score is used by 90% of top lenders. It ranges from 300-850."
    "What percentage of your credit score is based on payment history?|15%|35%|50%|65%|1|Payment history makes up 35% of your FICO score - the single biggest factor."
    "How long do negative items stay on your credit report?|3 years|5 years|7 years|10 years|2|Most negative items stay for 7 years. Bankruptcies can stay for 10."
    "What is the recommended credit utilization ratio?|Under 10%|Under 30%|Under 50%|Under 70%|1|Keep utilization under 30% (ideally under 10%) for best scores."
    "How often can you get a free credit report from each bureau?|Monthly|Every 6 months|Annually|Every 3 years|2|AnnualCreditReport.com gives you one free report per bureau per year."
    "What is a 'hard inquiry' on your credit report?|Checking your own score|A lender checking your credit|A soft credit check|An error on your report|1|Hard inquiries happen when you apply for credit and can lower your score slightly."
    "How long does it take to build credit from scratch?|1 month|3-6 months|1 year|2 years|1|It takes 3-6 months of credit activity to generate a FICO score."
    "What is the best first credit card for beginners?|Premium travel card|Secured credit card|Business credit card|Store credit card|1|Secured cards require a deposit and are designed for building credit."
    "Does closing a credit card help your credit score?|Yes, always|Yes, if it has a balance|No, it usually hurts|No effect|2|Closing cards reduces available credit and can hurt your utilization ratio."
    "What is the average credit score in the US?|650|700|718|750|2|The average FICO score is around 718 as of 2024."
)

total=${#questions[@]}

for i in "${!questions[@]}"; do
    q_num=$((i + 1))
    next_q=$((q_num + 1))
    progress=$((q_num * 10))
    
    IFS='|' read -r qtext opt1 opt2 opt3 opt4 correct expl <<< "${questions[$i]}"
    
    if [ $q_num -eq $total ]; then
        next_link="/quiz-complete.html?quiz=credit-basics"
        next_text="See Results"
    else
        next_link="q${next_q}.html"
        next_text="Next Question →"
    fi
    
    cat > "$QUIZ_DIR/q${q_num}.html" << EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Credit Basics Quiz - Question ${q_num} of ${total}</title>
    <meta name="description" content="Credit Basics Quiz - Test your knowledge. Question ${q_num} of ${total}.">
    <meta name="robots" content="noindex, follow">
    <link rel="stylesheet" href="/styles.css">
    <style>
        .quiz-page { padding: 40px 0; min-height: calc(100vh - 200px); }
        .quiz-container { max-width: 700px; margin: 0 auto; background: white; border-radius: 16px; padding: 40px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
        .quiz-header { text-align: center; margin-bottom: 32px; }
        .category-tag { display: inline-block; background: #6366f1; color: white; padding: 6px 16px; border-radius: 20px; font-size: 0.875rem; font-weight: 600; margin-bottom: 16px; }
        .progress-container { margin-bottom: 32px; }
        .progress-bar-bg { background: #e2e8f0; height: 8px; border-radius: 4px; overflow: hidden; }
        .progress-bar { background: linear-gradient(90deg, #6366f1, #8b5cf6); height: 100%; border-radius: 4px; }
        .progress-text { font-size: 0.875rem; color: #64748b; margin-top: 8px; text-align: center; }
        .question-container h2 { font-size: 1.5rem; margin-bottom: 24px; line-height: 1.5; }
        .options-list { display: flex; flex-direction: column; gap: 12px; }
        .option { background: white; border: 2px solid #e2e8f0; padding: 16px 20px; border-radius: 12px; cursor: pointer; transition: all 0.2s; font-size: 1rem; text-align: left; }
        .option:hover { border-color: #6366f1; background: #f8fafc; }
        .explanation { margin-top: 24px; padding: 20px; border-radius: 12px; display: none; }
        .explanation.correct { background: #d1fae5; border: 1px solid #10b981; display: block; }
        .explanation.incorrect { background: #fee2e2; border: 1px solid #ef4444; display: block; }
        .next-btn { margin-top: 16px; background: #6366f1; color: white; border: none; padding: 14px 28px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 1rem; text-decoration: none; display: inline-block; }
        .ad-container { max-width: 700px; margin: 32px auto; text-align: center; }
        .ad-label { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-bottom: 8px; }
    </style>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <a href="/" class="logo">💳 Credit Gamer Area</a>
        </div>
    </nav>

    <section class="quiz-page">
        <div class="container">
            <div class="quiz-container">
                <div class="quiz-header">
                    <span class="category-tag">Credit Basics - Question ${q_num} of ${total}</span>
                </div>
                
                <div class="progress-container">
                    <div class="progress-bar-bg">
                        <div class="progress-bar" style="width: ${progress}%"></div>
                    </div>
                    <div class="progress-text">Question ${q_num} of ${total}</div>
                </div>
                
                <div class="question-container">
                    <h2>${qtext}</h2>
                    <div class="options-list">
                        <button class="option" onclick="selectAnswer(0, ${correct})">${opt1}</button>
                        <button class="option" onclick="selectAnswer(1, ${correct})">${opt2}</button>
                        <button class="option" onclick="selectAnswer(2, ${correct})">${opt3}</button>
                        <button class="option" onclick="selectAnswer(3, ${correct})">${opt4}</button>
                    </div>
                    
                    <div id="explanation" class="explanation">
                        <h4 id="result-text"></h4>
                        <p>${expl}</p>
                        <a href="${next_link}" class="next-btn">${next_text}</a>
                    </div>
                </div>
            </div>
            
            <div class="ad-container">
                <div class="ad-label">Advertisement</div>
                <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins>
                <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
            </div>
        </div>
    </section>

    <footer class="footer" style="background: #1e1b4b; color: white; padding: 40px 0; text-align: center;">
        <div class="container">
            <p>&copy; 2026 Credit Gamer Area. All rights reserved.</p>
        </div>
    </footer>

    <script>
        let answered = false;
        
        function selectAnswer(selected, correct) {
            if (answered) return;
            answered = true;
            
            const isCorrect = selected === correct;
            const explanation = document.getElementById('explanation');
            const resultText = document.getElementById('result-text');
            
            document.querySelectorAll('.option').forEach((btn, idx) => {
                btn.style.pointerEvents = 'none';
                if (idx === correct) {
                    btn.style.borderColor = '#10b981';
                    btn.style.background = '#d1fae5';
                } else if (idx === selected && !isCorrect) {
                    btn.style.borderColor = '#ef4444';
                    btn.style.background = '#fee2e2';
                }
            });
            
            explanation.className = 'explanation ' + (isCorrect ? 'correct' : 'incorrect');
            resultText.textContent = isCorrect ? '✓ Correct!' : '✗ Incorrect';
            
            let score = parseInt(sessionStorage.getItem('cb_score') || '0');
            if (isCorrect) score++;
            sessionStorage.setItem('cb_score', score);
        }
    </script>
</body>
</html>
EOF
    
    echo "Created q${q_num}.html"
done

echo "All ${total} question pages created!"

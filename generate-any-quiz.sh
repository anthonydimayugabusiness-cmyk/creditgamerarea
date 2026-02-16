#!/bin/bash
# Generate token-protected quiz pages for any quiz

QUIZ_NAME=$1
QUIZ_DIR=$2
DISPLAY_NAME=$3

mkdir -p "$QUIZ_DIR"

# Define questions for each quiz
case $QUIZ_NAME in
    "credit-cards")
        questions=(
            "What is a credit card 'statement balance'?|Your total credit limit|What you owe at the end of billing cycle|Your minimum payment|Your available credit|1|The statement balance is what you owe when the billing cycle closes. Pay this to avoid interest."
            "How much should you spend on a \$1,000 limit card?|\$900-1000|\$500-700|\$100-300|As much as possible|2|Keep utilization under 30% (\$300 on \$1,000 limit) for best credit scores."
            "What happens if you only pay the minimum?|Nothing, that's fine|You pay interest on the remaining balance|Your credit score goes up|You get rewards bonus|1|Paying minimum means you carry a balance and pay interest on the rest—often 20%+ APR."
            "What is a 'secured' credit card?|A card with fraud protection|A card requiring a deposit|A card with high limits|A card for businesses only|1|Secured cards require a security deposit, making them accessible for building credit."
            "How many credit cards should a beginner have?|0|1-2|5-10|As many as possible|1|Start with 1-2 cards to build credit without overwhelming yourself."
            "What is a cash advance?|Free money from ATM|Withdrawing cash with high fees and interest|Cashback rewards|Balance transfer|1|Cash advances have high fees (3-5%) and immediate interest accrual. Avoid them."
            "When do you pay interest on purchases?|Immediately|If you don't pay full statement balance|Never with credit cards|Only on cash advances|1|Pay your full statement balance by the due date to avoid interest charges."
            "What is a 'grace period'?|Time to return purchases|Interest-free period between purchase and due date|Late payment forgiveness|Annual fee waiver|1|The grace period (21-25 days) lets you pay without interest if you pay in full."
            "Does applying for a card hurt your credit?|No, never|Yes, slightly via hard inquiry|Only if denied|Only if approved|1|Each application creates a hard inquiry that can temporarily lower your score 5-10 points."
            "What is the best way to use credit cards?|Max them out and pay minimum|Pay in full every month|Only use for emergencies|Never use them|1|Pay in full monthly to build credit, earn rewards, and pay zero interest."
        )
        ;;
    "prediction-markets")
        questions=(
            "What is a prediction market?|A weather forecasting service|An exchange for trading on event outcomes|A stock market for tech companies|A sports betting app|1|Prediction markets are exchanges where participants trade contracts whose payoff depends on the outcome of future events."
            "Which platform became the first regulated US prediction market?|Polymarket|Kalshi|PredictIt|Betfair|1|Kalshi won legal approval from the CFTC to offer regulated event contracts in the United States."
            "How do prediction market contracts work?|They pay \$1 if the event happens, \$0 if not|They pay double your bet if you win|They work like traditional stock shares|They only pay on election outcomes|0|Most prediction markets use binary contracts that pay \$1 if the event occurs and \$0 if it doesn't."
            "What does it mean if 'Yes' shares trade at \$0.75?|The market thinks there's a 75% chance|You pay \$0.75 to place a bet|The event is 75% complete|You win \$0.75 if correct|0|The price reflects the market's collective belief about probability—a \$0.75 price implies 75% likelihood."
            "How is Polymarket different from Kalshi?|Polymarket is crypto-based and international|Polymarket only does sports|Kalshi has higher fees|They're identical|0|Polymarket uses cryptocurrency and operates internationally, while Kalshi is USD-based and US-regulated."
            "What is 'hedging' in prediction markets?|Trimming garden hedges|Using bets to offset real-world risks|Betting on multiple outcomes|Avoiding taxes|1|Hedging means using prediction markets as insurance—profiting from outcomes that would hurt you financially."
            "What is the 'wisdom of crowds'?|A group of smart people|The idea that collective predictions often beat experts|A prediction market strategy|A type of contract|1|The wisdom of crowds theory suggests that aggregate predictions from many people often outperform individual experts."
            "What is a major risk of prediction markets?|They're guaranteed to make money|Most participants lose money|They're illegal everywhere|They only trade during business hours|1|Like all gambling, most participants lose money. Markets can also be manipulated and are inherently uncertain."
            "What happened to prediction markets in 2024?|They became illegal|They exploded in popularity during elections|They were banned by the SEC|Nothing significant|1|2024 saw massive growth in prediction market trading, especially around elections, with billions in volume."
            "How should you treat prediction markets?|As a primary investment strategy|As entertainment/hedging only|As a guaranteed income source|As a replacement for savings|1|Prediction markets should be treated as entertainment or hedging tools—not reliable investments. Never risk more than you can afford to lose."
        )
        ;;
    *)
        echo "Unknown quiz: $QUIZ_NAME"
        exit 1
        ;;
esac

total=${#questions[@]}

for i in "${!questions[@]}"; do
    q_num=$((i + 1))
    next_q=$((q_num + 1))
    progress=$((q_num * 10))
    
    IFS='|' read -r qtext opt1 opt2 opt3 opt4 correct expl <<< "${questions[$i]}"
    
    if [ $q_num -eq $total ]; then
        next_page="/quiz-complete.html"
        is_last="true"
    else
        next_page="q${next_q}.html"
        is_last="false"
    fi
    
    cat > "$QUIZ_DIR/q${q_num}.html" << EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${DISPLAY_NAME} Quiz - Question ${q_num} of ${total}</title>
    <meta name="description" content="${DISPLAY_NAME} Quiz - Test your knowledge. Question ${q_num} of ${total}.">
    <meta name="robots" content="noindex, nofollow">
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
        .error-message { background: #fee2e2; border: 1px solid #ef4444; color: #b91c1c; padding: 20px; border-radius: 12px; text-align: center; display: none; }
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
        <a href="/${QUIZ_NAME}-quiz.html" class="next-btn">Go to Quiz Start</a>
    </div>

    <section class="quiz-page" id="quiz-content">
        <div class="container">
            <div class="quiz-container">
                <div class="quiz-header">
                    <span class="category-tag">${DISPLAY_NAME} - Question ${q_num} of ${total}</span>
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
                        <button id="next-btn" class="next-btn" onclick="goToNext()">${is_last == "true" ? "See Results" : "Next Question →"}</button>
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
        const QUIZ_NAME = '${QUIZ_NAME}';
        const QUESTION_NUM = ${q_num};
        const IS_LAST = ${is_last};
        
        document.addEventListener('DOMContentLoaded', function() {
            const params = QuizToken.getParams();
            
            if (QUESTION_NUM === 1) {
                sessionStorage.setItem('${QUIZ_NAME}_score', '0');
                return;
            }
            
            if (!params.token || !QuizToken.validate(params.token, QUIZ_NAME, QUESTION_NUM - 1, params.score)) {
                document.getElementById('quiz-content').style.display = 'none';
                document.getElementById('error-msg').style.display = 'block';
            } else {
                sessionStorage.setItem('${QUIZ_NAME}_score', params.score.toString());
            }
        });
        
        let answered = false;
        let currentScore = parseInt(sessionStorage.getItem('${QUIZ_NAME}_score') || '0');
        
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
            
            if (isCorrect) {
                currentScore++;
                sessionStorage.setItem('${QUIZ_NAME}_score', currentScore.toString());
            }
        }
        
        function goToNext() {
            if (IS_LAST) {
                window.location.href = QuizToken.buildUrl('${next_page}', QUIZ_NAME, 'complete', currentScore);
            } else {
                window.location.href = QuizToken.buildUrl('${next_page}', QUIZ_NAME, QUESTION_NUM + 1, currentScore);
            }
        }
    </script>
</body>
</html>
EOF
    
    echo "Created ${QUIZ_NAME} q${q_num}.html"
done

echo "All ${total} ${QUIZ_NAME} question pages created!"

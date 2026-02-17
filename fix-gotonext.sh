#!/bin/bash
# Fix broken goToNext functions in all quiz pages

for file in /root/.openclaw/workspace/triviacaptain-website/quiz/*/q*.html; do
    # Remove the broken else clause
    sed -i '/^        } else {$/,/^            }$/{/^        } else {$/d; /^            }$/d; /^                \/\/ Go to next question with token$/d}' "$file"
done

echo "Fixed goToNext functions in all quiz pages"

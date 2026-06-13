# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

Problem 1:
I needed to do the opposite of what the game said. When the game showed me to go lower, I guessed a higher number.
When the game showed me to go higher, I picked a lower number.
The first guess I submitted was 50
Game showed me 📉 Go LOWER!
I submit guess: 75
Game showed me 📈 Go HIGHER!
I submit guess: 62
Game showed me 📉 Go LOWER!
I submit guess: 69
Game showed me: "🎉 Correct! You won! The secret was 69. Final score: 25"

Started guess at 50
Hint told me "📉 Go LOWER!"
I repeatedly kept going lower to 1 and got:
Actual: Out of attempts! The secret was 56. Score: -35
Expected: Why didn't the game show me "📈 Go HIGHER!" when my guess was lower than the correct answer?

Started guess at 50
Hint told me "📈 Go HIGHER!"
I repeatedly kept going higher to 100:
Actual: Out of attempts! The secret was 11. Score: -5
Expected: Why didn't the game show me "📉 Go LOWER!" when my guess was higher than the correct answer?

Problem 2: After running out of guesses, or guessing the correct number, clicking "New Game 🔁" does not remove "Game over. Start a new game to try again." and I cannot guess again.

Problem 3: changing difficult does not change this message: "Guess a number between 1 and 100." and numbers higher than 20 are able to be the secret on Easy difficulty.

Problem 4: Guessing the correct secret should show a positive final score.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input                 | Expected Behavior                     | Actual Behavior          | Console Output / Error |
|-----------------------|---------------------------------------|--------------------------|------------------------|
| Guess number < secret | Go LOWER!                             | Go HIGHER!               |                        |
| Change difficulty     | Number range and label changes.       | Max number stays 100     |                        |
| click "New Game"      | I can guess again + Game over removed | Game over stays          |                        |
| correct secret        | Final score is positive               | Final score: -10         |                        |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

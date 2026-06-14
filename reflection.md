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
| Change difficulty     | Number range and label changes        | Max number stays 100     |                        |
| click "New Game"      | I can guess again + Game over removed | Game over stays          |                        |
| correct secret        | Final score is positive               | Final score: -10         |                        |
| wrong guess           | Does not reward points                | Rewards points           |                        |
| Non-whole number      | Guess is rejected                     | Guess is accepted        |                        |
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I used Claude.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - When prompted with "Move the parse_guess function to logic_utils.py, update the logic to fix the string/integer bug, and update the import in app.py.", Claude gave suggestion to update parse_guess in logic_utils to first check for None, check the guess for empty string, then use a try except to parse the guess for an integer. I verified the result by playing the game/guessing with an empty string, letters, and letters + numbers; I saw that empty guesses show error "Enter a guess.", and guesses with letters/punctuation show error "That is not a number.". These guesses correctly did not decrement attempts.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - When prompted with "generate a pytest case in tests/test_game_logic.py that specifically targets the bug Final score is positive after guessing nultiple number of attempts including maximum number of attempts.", Claude gave suggestion: "test_losing_game_final_score_is_not_positive" which is a misleading name for a test. I wanted to assert the final score is always positive or not negative. The name for this test is misleading and can imply final scores can be negative when they can't.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I manually played the game and tried the same input causing the bug.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  - One test I ran using pytest was test_easy_difficulty_updates_range_label_and_secret. This test verifies the range is updated after changing difficulty and also changed the label. It showed me the starter code had multiple instances of hard-coded values e.g. 1 for low and 100 for high.
- Did AI help you design or understand any tests? How?
  - Yes, when prompting Claude "generate a pytest case in /tests/test_game_logic.py that specifically targets the bug Final score is positive after guessing nultiple number of attempts including maximum number of attempts.", Claude found the bug that update_score adds 5 points for a "Too High" wrong guess on even-numbered attempts. This helped me to understand the scoring logic more and why previously I would end up with a higher than expected final score.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  - I want to reuse moving functions to a separate file so the functions are easier to test.
- What is one thing you would do differently next time you work with AI on a coding task?
  - I would commit more frequently to mark checkpoints that are easier to revert.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - AI generated code can be a lot better when given proper context and examples. Scoping prompts to a specific bug, file, function, and test will make the overall code more maintainable.
  
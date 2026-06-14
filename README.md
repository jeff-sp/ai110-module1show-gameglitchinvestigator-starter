# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [X] Describe the game's purpose.
The purpose of the game is the user is supposed to guess the secret number picked by the computer. The difficulty determines the number of guesses the user can make and the range of the secret number i.e. Easy: 1-20 with 6 attempts, Normal: 1-100 with 8 attempts, and Hard: 1-200 with 5 attemps. When the player guesses too low, the computer should tell the user to go higher. When the player guesses too high, the computer should tell the user to go lower. The fewer attempts used to guess the number will result in a higher score and vice versa.

- [X] Detail which bugs you found.
Bugs I found include:
1. When user guesses a number too low, computer tells user to go lower. When user guesses a number too high, computer tells user to go higher.
2. Changing difficulty has no effect on the range from where the secret number is chosen, and the label range stays the same (1-100).
3. Clicking "New Game 🔁" does not start a new game. The secret number is not reset, and user cannot guess again.
4. Guesing the correct secret can still result in a negative final score.
5. Guessing the wrong number should not reward points to the user.
6. Empty guess or guessing with alphabet characters or punctuation is accepted as a valid guess.

- [X] Explain what fixes you applied.
1. `check_guess` now returns the correct direction: a guess higher than the secret → `"Too High"` → "📉 Go LOWER!", and a guess lower → `"Too Low"` → "📈 Go HIGHER!".
2. `get_range_for_difficulty` returns Easy 1–20, Normal 1–100, Hard 1–200 instead of a hard-coded 1–100. The info label now interpolates `low/high` instead of the hard-coded "1 and 100", and the secret is drawn from the active range.
3. Clicking New Game now resets attempts, picks a fresh secret in range, sets `status` back to `"playing"`, clears history, zeroes the score, and reruns. Previously `status` stayed `"lost"`, so the `st.stop()` at app.py:103 kept blocking input and the "Game over" message persisted.
4. `update_score` clamps the result with `if new_score < 0: new_score = 0`, so a losing run can't drop below 0.
5. Both `"Too High"` and `"Too Low"` now subtract 5. The original glitch added 5 on even-numbered "Too High" attempts, which let a losing player finish with points.
6. `parse_guess` rejects `None`, empty/whitespace strings ("Enter a guess."), and anything that isn't a whole number ("That is not a whole number.").

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User enters a guess of 50
2. Game returns "Too Low", shows hint "📈 Go HIGHER!", and decrements attempts
3. User enters a guess of 75
4. Game returns "Too High", shows hint "📉 Go LOWER!", and decrements attempts
5. Game ends after the correct guess or until user runs out of attempts

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]

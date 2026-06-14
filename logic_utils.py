#FIX: Refactored logic into logic_utils.py using Claude. Changing difficulty updates High value instead of always 100.
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    elif difficulty == "Normal":
        return 1, 100
    elif difficulty == "Hard":
        return 1, 200
    else:
        return 1, 100

#FIX: Refactored logic into logic_utils.py using Claude. Rejects non-whole number guesses.
def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    text = raw.strip()
    if text == "":
        return False, None, "Enter a guess."

    try:
        guess_int = int(text)
    except ValueError:
        return False, None, "That is not a whole number."

    return True, guess_int, None

#FIX: Refactored logic into logic_utils.py using Claude. Return "📉 Go LOWER!" when guess is Too High. Return "📈 Go HIGHER!" when guess is Too Low.
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"

#FIX: Refactored logic into logic_utils.py using Claude and prevent negative scores.
def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number.

    Score is never allowed to go below 0.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        new_score = current_score + points
    elif outcome == "Too High":
        new_score = current_score - 5
    elif outcome == "Too Low":
        new_score = current_score - 5
    else:
        new_score = current_score

    if new_score < 0:
        new_score = 0
    return new_score

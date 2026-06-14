import os
import random

from streamlit.testing.v1 import AppTest

from logic_utils import check_guess, get_range_for_difficulty, update_score

APP_PATH = os.path.join(os.path.dirname(__file__), "..", "app.py")
GAME_OVER_MSG = "Game over. Start a new game to try again."


def _start_app():
    """Boot app.py inside Streamlit's test harness and run the first pass."""
    at = AppTest.from_file(APP_PATH)
    at.run()
    return at


def _button(at, label_fragment):
    """Return the button whose label contains label_fragment (emojis included)."""
    for btn in at.button:
        if label_fragment in btn.label:
            return btn
    raise AssertionError(f"button containing {label_fragment!r} not found")


def _error_texts(at):
    return [e.value for e in at.error]


def _success_texts(at):
    return [s.value for s in at.success]

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_lower_guess_shows_go_higher():
    # Bug target: guessing a number LOWER than the secret must tell the
    # player to go HIGHER. check_guess returns (outcome, message), so we
    # assert on the message specifically.
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"

def test_higher_guess_shows_go_lower():
    # Bug target: guessing a number HIGHER than the secret must tell the
    # player to go LOWER. check_guess returns (outcome, message), so we
    # assert on the message specifically.
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"


def _range_label(low, high):
    # Mirrors the sidebar/info label produced in app.py from the active range.
    return f"Range: {low} to {high}"


def test_easy_difficulty_updates_range_label_and_secret():
    # Bug target: switching difficulty to "Easy" must update the active number
    # range to 1-20, update the displayed label, and produce a secret that is
    # between 1 and 20 inclusive.
    low, high = get_range_for_difficulty("Easy")
    assert (low, high) == (1, 20)

    # The displayed label must reflect the new range.
    assert _range_label(low, high) == "Range: 1 to 20"

    # The secret (random.randint(low, high)) must fall within 1-20 inclusive,
    # including both boundaries. Sample many times so a range glitch surfaces.
    for _ in range(2000):
        secret = random.randint(low, high)
        assert 1 <= secret <= 20

    # Both inclusive boundaries must be reachable.
    assert low == 1
    assert high == 20

def test_normal_difficulty_updates_range_label_and_secret():
    # Bug target: switching difficulty to "Normal" must update the active number
    # range to 1-100, update the displayed label, and produce a secret that is
    # between 1 and 100 inclusive.
    low, high = get_range_for_difficulty("Normal")
    assert (low, high) == (1, 100)

    # The displayed label must reflect the new range.
    assert _range_label(low, high) == "Range: 1 to 100"

    # The secret (random.randint(low, high)) must fall within 1-20 inclusive,
    # including both boundaries. Sample many times so a range glitch surfaces.
    for _ in range(2000):
        secret = random.randint(low, high)
        assert 1 <= secret <= 100

    # Both inclusive boundaries must be reachable.
    assert low == 1
    assert high == 100


def test_hard_difficulty_updates_range_label_and_secret():
    # Bug target: switching difficulty to "Hard" must update the active number
    # range to 1-200, update the displayed label, and produce a secret that is
    # between 1 and 200 inclusive.
    low, high = get_range_for_difficulty("Hard")
    assert (low, high) == (1, 200)

    # The displayed label must reflect the new range.
    assert _range_label(low, high) == "Range: 1 to 200"

    # The secret (random.randint(low, high)) must fall within 1-200 inclusive,
    # including both boundaries. Sample many times so a range glitch surfaces.
    for _ in range(2000):
        secret = random.randint(low, high)
        assert 1 <= secret <= 200

    # Both inclusive boundaries must be reachable.
    assert low == 1
    assert high == 200


def test_new_game_clears_game_over_and_allows_fresh_guess():
    # Bug target: while the app is in the "lost" state it shows
    # "Game over. Start a new game to try again." and st.stop()s. Clicking
    # "New Game" MUST:
    #   1. clear that Game-over message,
    #   2. reset status back to "playing",
    #   3. generate a brand-new secret within the active range, and
    #   4. accept a fresh guess that is evaluated against the NEW secret.
    # If the status reset line in app.py is missing, status stays "lost",
    # the Game-over message persists, st.stop() blocks input, and this fails.
    at = _start_app()

    # Force the app into a lost game so the Game-over message is rendered.
    at.session_state.status = "lost"
    at.run()
    assert GAME_OVER_MSG in _error_texts(at)

    # Click "New Game 🔁".
    _button(at, "New Game").click().run()

    # (1)+(2): the message is gone and we are playing again.
    assert at.session_state.status == "playing"
    assert GAME_OVER_MSG not in _error_texts(at)

    # (3): a fresh secret was generated inside the Normal range (1..100).
    new_secret = at.session_state.secret
    assert 1 <= new_secret <= 100

    # (4): submitting a guess equal to the NEW secret is accepted (input is
    # not blocked) and evaluated as a win against that new secret. The win
    # banner echoes the secret, proving the new value was the one compared.
    at.text_input[0].set_value(str(new_secret))
    _button(at, "Submit Guess").click().run()

    assert at.session_state.status == "won"
    assert any(f"The secret was {new_secret}" in msg for msg in _success_texts(at))


def test_new_game_guess_evaluated_against_new_secret_when_wrong():
    # Complements the win case: after New Game, a guess that does NOT match the
    # new secret must still be processed (not blocked by a stale Game-over /
    # st.stop()) and evaluated against the NEW secret, yielding the correct
    # directional hint from check_guess.
    at = _start_app()
    at.session_state.status = "lost"
    at.run()

    _button(at, "New Game").click().run()
    assert at.session_state.status == "playing"

    new_secret = at.session_state.secret
    # Pick an in-range guess guaranteed to differ from the new secret.
    wrong_guess = 1 if new_secret != 1 else 2
    expected_outcome, expected_hint = check_guess(wrong_guess, new_secret)

    at.text_input[0].set_value(str(wrong_guess))
    _button(at, "Submit Guess").click().run()

    # The guess was accepted (recorded in history) and is still "playing".
    assert wrong_guess in at.session_state.history
    assert at.session_state.status == "playing"

    # The hint shown matches evaluating the guess against the NEW secret.
    warnings = [w.value for w in at.warning]
    assert expected_hint in warnings


def test_losing_game_final_score_is_zero():
    # Bug target: a player who NEVER wins and burns through every attempt
    # (up to and including the maximum allowed) should never finish with a
    # positive score. Wrong guesses must not reward points.
    #
    # update_score has a glitch: a "Too High" outcome on an even-numbered
    # attempt ADDS 5 instead of subtracting. So a losing run made up entirely
    # of wrong guesses still ends with a positive final score, which is wrong.
    #
    # Normal difficulty allows 8 attempts (see attempt_limit_map in app.py).
    # app.py increments attempts BEFORE scoring, so the attempt_number values
    # passed to update_score are 1..8.
    attempt_limit = 8

    score = 0
    for attempt_number in range(1, attempt_limit + 1):
        # Every guess is wrong; "Too High" is what exposes the even-attempt
        # scoring glitch.
        score = update_score(score, "Too High", attempt_number)

    # A game lost on only wrong guesses must not leave the player with points.
    assert score == 0, (
        f"Losing game ended with a positive final score of {score}; "
        f"wrong guesses must never increase the score."
    )


def test_winning_game_final_score_is_positive():
    # A player who wins should always finish with a positive final score,
    # regardless of how many attempts it took. update_score awards points on
    # a "Win" outcome, with a guaranteed floor of 10 points (see logic_utils).
    #
    # app.py increments attempts BEFORE scoring, so attempt_number is 1-based.
    # Normal difficulty allows 8 attempts; check a win on each attempt 1..8.
    attempt_limit = 8

    for winning_attempt in range(1, attempt_limit + 1):
        score = update_score(0, "Win", winning_attempt)
        assert score > 0, (
            f"Winning on attempt {winning_attempt} produced a non-positive "
            f"final score of {score}; a win must always award points."
        )

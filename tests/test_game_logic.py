from pathlib import Path

from streamlit.testing.v1 import AppTest

from logic_utils import check_guess, get_range_for_difficulty, parse_guess

APP_PATH = str(Path(__file__).resolve().parent.parent / "app.py")

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result[0] == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result[0] == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result[0] == "Too Low"

def test_hint_messages_point_toward_secret():
    # Hint messages used to be swapped, so a guess that was too high said "Go HIGHER!"
    _, high_message = check_guess(60, 50)
    _, low_message = check_guess(40, 50)
    assert "LOWER" in high_message
    assert "HIGHER" in low_message

def test_string_secret_compared_as_number():
    # app.py passes the secret as a string on even attempts; it used to be compared as text,
    # so "9" > "50" made a guess of 9 count as too high
    assert check_guess(9, "50")[0] == "Too Low"
    assert check_guess(60, "50")[0] == "Too High"
    assert check_guess(50, "50")[0] == "Win"

def test_range_grows_with_difficulty():
    # Normal and Hard ranges used to be swapped, so Hard (1-50) was easier than Normal (1-100)
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert easy_high < normal_high < hard_high

def test_whitespace_guess_asks_for_a_guess():
    # Whitespace-only input used to say "That is not a number." instead of "Enter a guess."
    assert parse_guess("   ") == (False, None, "Enter a guess.")

def test_guess_with_surrounding_spaces_is_accepted():
    assert parse_guess(" 7 ") == (True, 7, None)

def test_decimal_guess_is_rejected():
    # Decimals used to be silently truncated, so "4.9" became a guess of 4
    ok, value, _ = parse_guess("4.9")
    assert not ok
    assert value is None

def test_guess_outside_range_is_rejected():
    # Guesses outside the difficulty range used to be accepted
    assert not parse_guess("0", 1, 50)[0]
    assert not parse_guess("51", 1, 50)[0]
    assert parse_guess("1", 1, 50) == (True, 1, None)
    assert parse_guess("50", 1, 50) == (True, 50, None)

def test_invalid_guess_does_not_use_an_attempt():
    # Attempts used to be counted before parse_guess checked the input,
    # so submitting an empty guess still used up an attempt (row 3 of bug log)
    at = AppTest.from_file(APP_PATH).run()
    for bad_input in ["", "abc", "4.9", "500"]:
        at.text_input[0].input(bad_input)
        at.button[0].click().run()
        assert at.session_state.attempts == 0

    at.text_input[0].input("10")
    at.button[0].click().run()
    assert at.session_state.attempts == 1

from logic_utils import check_guess, get_range_for_difficulty

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

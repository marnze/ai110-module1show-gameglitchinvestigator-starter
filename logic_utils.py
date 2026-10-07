def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    #FIX: Moved from app.py using agent mode. I noticed Normal and Hard ranges were
    #     swapped; the AI corrected them so the range grows with difficulty (Easy < Normal < Hard)
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 50


def parse_guess(raw: str, low: int = None, high: int = None):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    #FIX: Moved from app.py using agent mode. The AI found that whitespace-only input
    #     was reported as "not a number", decimals like "4.9" were silently truncated
    #     to 4, and guesses outside the difficulty range were accepted. Input is now
    #     stripped, only whole numbers are allowed, and the range is checked.
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        value = int(raw.strip())
    except ValueError:
        return False, None, "Please enter a whole number."

    if low is not None and high is not None and not (low <= value <= high):
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    #FIX: Moved from app.py using agent mode. The AI found the hint messages were swapped
    #     (too high said "Go HIGHER!"), row 2 of bug log fixed. It also found the TypeError
    #     fallback compared strings, so "9" > "50" counted as too high. Both values are now
    #     compared as ints.
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")

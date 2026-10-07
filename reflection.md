# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  The game looked fine from a visual perspective, except for the Attempts left being at 7 instead of 8. There are a multitude of bugs I found while playing that I have listed below.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  I expected pressing Enter in the textbox after inputting my guess would make the guess go through. It did not. I had to
  press the "Submit Guess" button to actually submit the guess, not sure if that's the only intended way to submit the guess. If pressing Enter was intended to submit the guess, I suspect the code related to that would go somewhere in app.py parse_guess. 
  
  The hints are wrong. Looks like the code for this is in app.py Lines 38 and 40, go higher and go lower messages should be swapped.

  If you don't enter any guess and keep clicking "Submit Guess", the attempt counter keeps decreasing and goes into the negatives. There is a check for empty guess with the message "Enter a guess" but the attempt counter should not be decreasing. The culprit for this is likely line app.py line 148 where the attempts counter is incremented after each submit without a check. 

  "New Game" button does not work correctly after a game ends. The attempts left are reset but my guesses are not read nor do any hints appear. The only thing that changes is the secret number, as seen in the developer debug info. It seems to work fine if the button is pressed mid-game, but not after a game ends whether it's due to winning or losing. app.py line 148 in the else statement where the player lost is where I think this happens.

  Checking "Show hint" only makes the hint appear after submitting a guess. It does not show the hint for the current guess. app.py Line 165 and 166 seems to be where the hint is shown, but it looks like this only happens after clicking the submit button. 

  "Attempts left" shows one attempt less than the total attemps allowed for each mode. For example, in Normal mode, Attemps left starts out at 7 when it should be 8. When I submit my first guess, Attempts left stays at 7 and only starts decreasing after my 2nd guess. Then the game ends even though I had 1 attempt left. app.py Line 111 is where these attempts are shown it seems, and Line 96 seems to set attempts to 1 at the beginning of a game.


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input          | Expected Behavior | Actual Behavior | Console Output / Error | Suspected Code Location |
|----------------|-------------------|-----------------|------------------------|-------------------------|
| Enter on guess textbox| Guess is submitted | Nothing happens | None | app.py, parse_guess |
| Guess of 50 | Too Low hint | Too high hint | None | app.py, lines 38 and 40 |
| Submit empty Guess | Only "Enter a guess" message shown | Attempts left decremented | "Enter a guess" | app.py, line 148|
| New Game button pressed after lost game | New guess submissions are accepted and hints appear | Only the Attempts left and secret number are reset | "Game over. Start a new game to try again." doesn't go away | app.py, from line 148|
| Checking "Show hint" | Hint appears for current guess | Hint is not shown | None | app.py, lines 165 and 166|
| None | Attempts left is 8 when starting Normal mode | Attempts left shows 7 for Normal mode | None | app.py, lines 96 and 111|

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

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

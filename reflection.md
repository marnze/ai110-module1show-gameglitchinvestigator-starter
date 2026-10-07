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

  "Attempts left" shows one attempt less than the total attempts allowed for each mode. For example, in Normal mode, Attempts left starts out at 7 when it should be 8. When I submit my first guess, Attempts left stays at 7 and only starts decreasing after my 2nd guess. Then the game ends even though I had 1 attempt left. app.py Line 111 is where these attempts are shown it seems, and Line 96 seems to set attempts to 1 at the beginning of a game.


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
  
  Claude Opus 5.5 Medium (I know Sonnet uses less tokens but I really wanted to see the hype with Opus 5.5)

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  One suggestion that was correct was when moving parse_guess to logic_utils.py, the AI noticed whitespace-only input was reported as "not a number" when it thought it should give a warning message of "Enter a guess". Technically whitespace still counts as "not a number" but the AI wanted to be more specific in telling the user to type in an actual guess, be it a string number or anything else, and I agreed. It also pointed out some other bugs while moving the function like decimals being truncated silently. I verified the changes by making it write and pass pytest cases in tests/test_game_logic.py and also manually deploying the game and checking, for example on a whitespace-only guess it should show "Enter a guess."

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
  
  When asking AI to move the core logic from app.py to logic_utils.py and to update the logic to fix any bugs, it suggested changing the Hard difficulty range from 1,50 to 1,200 in get_range_for_difficulty since it felt the old range was too easy. The fix it should've done is swapped the Normal (1,100) and Hard ranges. I stopped it and clarified I want the ranges swapped instead of a new range being suggested. I'm not sure if it suggested that because I asked it to move every function that logic_utils.py was expecting into it (might have overwhelmed it?), but I ended up doing a separate chat message for each function instead so it focuses on each function more carefully.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

  Pytest cases, manually redeploying the app after the fixes and checking for intended behavior, and just reading through the new code and seeing how it fits together with the rest of the code and if it makes sense.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

  I did a manual test for the New Game button fix where I couldn't start a new game after the current game was over, whether I won or lost. It would get locked in the win/loss message. I purposefully lost by spamming the same wrong guess until my attempts ran out and was met with the game over message. I pressed the New Game button and was able to start a new game. This proved that the new code worked.

- Did AI help you design or understand any tests? How?

  Yes, AI worked through the design and implementation of all the tests. After it implemented each fix, I asked it to "Create a pytest case or cases in @tests/test_game_logic.py that specifically targets the bug or bugs you just fixed". It created the tests, checked that they passed, and then explained to me what each test tested for. It's quite phenomenal how useful AI is for testing.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  Every time you click a button, type in a box, or tick a checkbox, Streamlit runs the whole script again from top to bottom. Variables start fresh on every run. st.session_state is like a notebook that survives those reruns. Anything that needs to persist, like the secret number, attempts, score, status has to go there. This is necessary so the secret number you need to guess doesn't change every time you click something. 

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

  I'm not sure if it's the optimal way to do things, but I really like the workflow I got into with each problem or mini code fix. It was 
  1. Ask the AI to fix the thing and explain the fix but don't commit anything yet
  2. Once I made sure I understood the fix, make it go through with it.
  3. Write test(s) to validate the fix or fixes
  4. Write a commit message detailing the fixes
  Also, this would be for each little problem or fix in a separate Claude chat. That way the AI can focus on only that small problem and not go too crazy trying to fix everything at once (overwhelms me and probably the model as well(?))

- What is one thing you would do differently next time you work with AI on a coding task?

  I'd want to be more specific in giving AI instructions. I feel like a lot of times I just said "fix the thing" and it went overboard or didn't do the fix I wanted. Also I wish I started on this project sooner. I'll probably be submitting this with the bare minimum since there's only 30 min left on the 48-hr extension, but I'm planning on coming back and implementing the challenge features. Awesome job on the team who made this.


- In one or two sentences, describe how this project changed the way you think about AI generated code.

  AI generated code is amazing and I am scared for my future career. The possibilities it brings in time-saving and creating awesome things makes me think it's worth it though.

# Plan for Implementing "Easy" and "Hard" Game Modes

This document outlines the steps to implement two distinct game modes: "easy" and "hard".

- **Hard Mode:** The current behavior. Players get one attempt per question. An incorrect answer immediately moves to the result screen.
- **Easy Mode:** A more forgiving mode. If a player chooses an incorrect answer, it will be marked red, but they can keep trying other answers on the same question. The game only proceeds to the result screen when the correct answer is selected.

**⚠️ Important Note:** As stated in the `README.md`, all tests run against the packed `index.html` file. The `run_tests.sh` script handles this by running `pack_project.py` before executing the tests. Always use `bash run_tests.sh` to ensure you are testing the latest code changes.

---

## Implementation Checklist

- [x] **1. Update Schema and Data Files**
  - [x] Add a `"mode"` attribute to the `"metadata"` object in `data/schema.json`. This attribute should accept either `"easy"` or `"hard"`.
  - [x] Update `data/questions_kids_12plus.json` to include `"mode": "easy"` in its metadata.
  - [x] Update all other question data files (`questions.json`, `questions_citizenship_level.json`, etc.) to include `"mode": "hard"` in their metadata.
  - [x] **Verification:** Run `bash run_tests.sh`. The `unit_test_json_validation` test should pass, confirming all data files conform to the new schema.

- [x] **2. Refactor the Hard Mode Integration Test**
  - [x] Rename the existing game integration test: `git mv tests/integration_test_game.py tests/integration_test_game_hard.py`.
  - [x] Update `run_tests.sh` to find test files matching `integration_test_game_*.py`.
  - [x] Modify `tests/integration_test_game_hard.py` to explicitly select and test a "hard" mode question set (e.g., "UK Citizenship Level"). This ensures its independence from the "easy" mode changes.
  - [x] **Verification:** Run `bash run_tests.sh`. All tests, including the renamed `integration_test_game_hard.py`, should pass.

- [x] **3. Create the Easy Mode Integration Test**
  - [x] Create a new test file: `tests/integration_test_game_easy.py`.
  - [x] This test must specifically select the "Kids (12+)" question set, which is configured for "easy" mode.
  - [x] The test needs to be sophisticated:
    - It will load `data/questions_kids_12plus.json` at the start to create a map of correct answers for each question.
    - The test will iterate through the questions, alternating its strategy:
      1. For one question, it will deliberately select a *wrong* answer first. It will assert that the chosen answer turns red and that the game *does not* advance to the result screen. Then, it will select the correct answer.
      2. For the next question, it will select the *correct* answer on the first try.
    - When the correct answer is selected (either on the first or subsequent attempt), the test must assert that the choice turns green, there is a brief pause, and then the result screen is displayed.
  - [x] **Verification:** Run `bash run_tests.sh`. The new `integration_test_game_easy.py` is expected to **fail** because the game logic has not been implemented yet. (Note: This is now failing as expected).

- [ ] **4. Implement the "Easy" and "Hard" Mode Logic**
  - [x] Modify `js/game-engine.js` to differentiate game state progression based on the question set's `mode`. (This is complete).
  - [ ] Refactor `js/ui.js` to handle the different outcomes from the game engine. The `selectAnswer` function will be the focus.
    - **If `mode` is "easy" and the answer is incorrect:**
      - Mark the selected choice as red and do nothing else. The other choices should remain active.
    - **If `mode` is "hard" OR the answer is correct:**
      - The existing logic remains: disable all choices, highlight correct/incorrect answers, and proceed to the result screen after a short delay.
  - [ ] **Verification:** Continuously run `bash run_tests.sh` while developing until all tests, including the new easy mode test, pass.

- [ ] **5. Final Review and Cleanup**
  - [ ] Once all tests pass, perform a final review of the code changes.
  - [ ] Ensure the `PlanMode.md` is fully checked off.
  - [ ] Remove any temporary debug code.
  - [ ] The feature is complete.

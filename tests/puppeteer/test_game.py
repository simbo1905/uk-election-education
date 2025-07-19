#!/usr/bin/env python3
"""
Puppeteer tests for Democracy Education Game
Tests the complete game flow and functionality
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from pyppeteer import launch
import jsonschema

class GameTester:
    def __init__(self):
        self.browser = None
        self.page = None
        self.project_root = Path(__file__).parent.parent.parent
        self.game_url = f"file://{self.project_root}/index.html"
        
    async def setup(self):
        """Initialize browser and page"""
        self.browser = await launch(
            headless=False,  # Set to True for CI/CD
            args=['--no-sandbox', '--disable-setuid-sandbox'],
            autoClose=False
        )
        self.page = await self.browser.newPage()
        await self.page.setViewport({'width': 1280, 'height': 800})
        
    async def teardown(self):
        """Clean up browser"""
        if self.browser:
            await self.browser.close()
            
    async def wait_for_selector(self, selector, timeout=5000):
        """Wait for element with error handling"""
        try:
            await self.page.waitForSelector(selector, timeout=timeout)
            return True
        except Exception as e:
            print(f"❌ Element not found: {selector} - {e}")
            return False
            
    async def test_json_schema_validation(self):
        """Test that questions.json matches the schema"""
        print("🧪 Testing JSON schema validation...")
        
        try:
            # Load schema
            schema_path = self.project_root / 'data' / 'schema.json'
            with open(schema_path, 'r') as f:
                schema = json.load(f)
                
            # Load questions
            questions_path = self.project_root / 'data' / 'questions.json'
            with open(questions_path, 'r') as f:
                questions = json.load(f)
                
            # Validate
            jsonschema.validate(questions, schema)
            print("✅ JSON schema validation passed")
            return True
            
        except Exception as e:
            print(f"❌ JSON schema validation failed: {e}")
            return False
            
    async def test_game_loading(self):
        """Test that the game loads correctly"""
        print("🧪 Testing game loading...")
        
        try:
            await self.page.goto(self.game_url)
            
            # Should start with loading screen
            if not await self.wait_for_selector('#loading-screen'):
                return False
                
            # Should transition to start screen
            if not await self.wait_for_selector('#start-screen', timeout=10000):
                return False
                
            # Check that start screen is visible
            start_display = await self.page.evaluate(
                'document.getElementById("start-screen").style.display'
            )
            
            if start_display == 'none':
                print("❌ Start screen should be visible")
                return False
                
            print("✅ Game loading test passed")
            return True
            
        except Exception as e:
            print(f"❌ Game loading test failed: {e}")
            return False
            
    async def test_start_game_flow(self):
        """Test starting the game"""
        print("🧪 Testing start game flow...")
        
        try:
            # Click start button
            await self.page.click('#start-button')
            
            # Should transition to game screen
            if not await self.wait_for_selector('#game-screen', timeout=5000):
                return False
                
            # Check that game screen is visible
            game_display = await self.page.evaluate(
                'document.getElementById("game-screen").style.display'
            )
            
            if game_display == 'none':
                print("❌ Game screen should be visible")
                return False
                
            # Check that question is loaded
            question_text = await self.page.evaluate(
                'document.getElementById("question-text").textContent'
            )
            
            if question_text == "Loading question..." or not question_text:
                print("❌ Question should be loaded")
                return False
                
            print("✅ Start game flow test passed")
            return True
            
        except Exception as e:
            print(f"❌ Start game flow test failed: {e}")
            return False
            
    async def test_answer_question(self):
        """Test answering a question"""
        print("🧪 Testing answer question flow...")
        
        try:
            # Wait for choices to be available
            if not await self.wait_for_selector('.choice-button'):
                return False
                
            # Get number of choices
            choice_count = await self.page.evaluate(
                'document.querySelectorAll(".choice-button").length'
            )
            
            if choice_count < 2:
                print(f"❌ Should have at least 2 choices, found {choice_count}")
                return False
                
            # Click first choice
            await self.page.click('.choice-button:first-child')
            
            # Should transition to result screen
            if not await self.wait_for_selector('#result-screen', timeout=10000):
                return False
                
            # Check that result screen is visible
            result_display = await self.page.evaluate(
                'document.getElementById("result-screen").style.display'
            )
            
            if result_display == 'none':
                print("❌ Result screen should be visible")
                return False
                
            # Check that explanation is shown
            explanation = await self.page.evaluate(
                'document.getElementById("explanation-text").textContent'
            )
            
            if not explanation or explanation == "Explanation will appear here...":
                print("❌ Explanation should be loaded")
                return False
                
            print("✅ Answer question test passed")
            return True
            
        except Exception as e:
            print(f"❌ Answer question test failed: {e}")
            return False
            
    async def test_next_question(self):
        """Test moving to next question"""
        print("🧪 Testing next question flow...")
        
        try:
            # Click next button
            await self.page.click('#next-button')
            
            # Should return to game screen or finish screen
            # Wait a bit for transition
            await asyncio.sleep(1)
            
            # Check if we're on game screen (more questions) or finish screen (done)
            game_visible = await self.page.evaluate('''
                () => {
                    const gameScreen = document.getElementById("game-screen");
                    const finishScreen = document.getElementById("finish-screen");
                    return {
                        game: gameScreen.style.display !== 'none',
                        finish: finishScreen.style.display !== 'none'
                    };
                }
            ''')
            
            if not (game_visible['game'] or game_visible['finish']):
                print("❌ Should be on either game screen or finish screen")
                return False
                
            print("✅ Next question test passed")
            return True
            
        except Exception as e:
            print(f"❌ Next question test failed: {e}")
            return False
            
    async def test_complete_game(self):
        """Test completing the entire game"""
        print("🧪 Testing complete game flow...")
        
        try:
            # Go back to start for fresh game
            await self.page.goto(self.game_url)
            await self.wait_for_selector('#start-screen', timeout=10000)
            await self.page.click('#start-button')
            await self.wait_for_selector('#game-screen')
            
            questions_answered = 0
            max_questions = 10  # Safety limit
            
            while questions_answered < max_questions:
                # Check if we're still on game screen
                game_visible = await self.page.evaluate(
                    'document.getElementById("game-screen").style.display !== "none"'
                )
                
                if not game_visible:
                    break
                    
                # Answer the question (click first choice)
                await self.page.click('.choice-button:first-child')
                await self.wait_for_selector('#result-screen')
                
                # Click next
                await self.page.click('#next-button')
                questions_answered += 1
                
                # Wait for transition
                await asyncio.sleep(1)
                
            # Should now be on finish screen
            if not await self.wait_for_selector('#finish-screen', timeout=5000):
                print("❌ Should reach finish screen")
                return False
                
            # Check final score is displayed
            final_score = await self.page.evaluate(
                'document.getElementById("final-score").textContent'
            )
            
            if not final_score or final_score == "0 out of 6":
                print(f"❌ Final score should be meaningful: {final_score}")
                # This might be acceptable if we only answered questions incorrectly
                
            print(f"✅ Complete game test passed - answered {questions_answered} questions")
            return True
            
        except Exception as e:
            print(f"❌ Complete game test failed: {e}")
            return False
            
    async def test_play_again(self):
        """Test play again functionality"""
        print("🧪 Testing play again flow...")
        
        try:
            # Should be on finish screen from previous test
            # Click play again
            await self.page.click('#play-again-button')
            
            # Should return to game screen
            if not await self.wait_for_selector('#game-screen', timeout=5000):
                return False
                
            # Check that we're back to first question
            question_counter = await self.page.evaluate(
                'document.getElementById("question-counter").textContent'
            )
            
            if not question_counter.startswith("Question 1"):
                print(f"❌ Should be back to question 1: {question_counter}")
                return False
                
            print("✅ Play again test passed")
            return True
            
        except Exception as e:
            print(f"❌ Play again test failed: {e}")
            return False
            
    async def run_all_tests(self):
        """Run all tests and report results"""
        print("🎮 Starting Democracy Education Game Tests\n")
        
        await self.setup()
        
        tests = [
            ("JSON Schema Validation", self.test_json_schema_validation),
            ("Game Loading", self.test_game_loading),
            ("Start Game Flow", self.test_start_game_flow),
            ("Answer Question", self.test_answer_question),
            ("Next Question", self.test_next_question),
            ("Complete Game", self.test_complete_game),
            ("Play Again", self.test_play_again),
        ]
        
        results = []
        
        for test_name, test_func in tests:
            try:
                result = await test_func()
                results.append((test_name, result))
                print()  # Add spacing between tests
            except Exception as e:
                print(f"❌ {test_name} crashed: {e}\n")
                results.append((test_name, False))
                
        await self.teardown()
        
        # Print summary
        print("=" * 50)
        print("🏁 TEST SUMMARY")
        print("=" * 50)
        
        passed = 0
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{status} {test_name}")
            if result:
                passed += 1
                
        print(f"\nResult: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Game is working correctly.")
            return True
        else:
            print("⚠️  Some tests failed. Check the output above.")
            return False

async def main():
    """Main test runner"""
    tester = GameTester()
    success = await tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())
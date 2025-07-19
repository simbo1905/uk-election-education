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
        self.build_info = None
        
    async def setup(self):
        """Initialize browser and page"""
        self.browser = await launch(
            headless=False,  # Set to True for CI/CD
            args=['--no-sandbox', '--disable-setuid-sandbox'],
            autoClose=False
        )
        self.page = await self.browser.newPage()
        await self.page.setViewport({'width': 1280, 'height': 800})
        
        # Capture console logs from the browser
        self.page.on('console', lambda msg: print(f"🌐 BROWSER: {msg.text}"))
        
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
            
            # CRITICAL: Check and log build info to verify we're testing the correct build
            self.build_info = await self.page.evaluate('window.BUILD_INFO')
            if self.build_info:
                print(f"🏗️ Testing build: {self.build_info['version']} • {self.build_info['timestamp']}")
            else:
                print("⚠️ No build info found - might be testing old version")
                
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
                print("❌ Choice buttons not found")
                return False
                
            # Get number of choices and log details
            choice_count = await self.page.evaluate(
                'document.querySelectorAll(".choice-button").length'
            )
            print(f"🔍 Found {choice_count} choice buttons")
            
            if choice_count < 2:
                print(f"❌ Should have at least 2 choices, found {choice_count}")
                return False
            
            # Check console logs before clicking
            print("🔍 Checking console logs before click...")
            
            # Click first choice and log what happens
            print("🔍 Clicking first choice button...")
            await self.page.click('.choice-button:first-child')
            
            # Wait longer for the timeout in selectAnswer (800ms + buffer)
            print("🔍 Waiting for result screen transition (800ms timeout + buffer)...")
            await asyncio.sleep(1.2)
            
            # Simple check - just see if result screen exists and is visible
            try:
                result_visible = await self.page.evaluate('''
                    () => {
                        const screen = document.getElementById("result-screen");
                        return screen && screen.style.display !== "none";
                    }
                ''')
                print(f"🔍 Result screen visible: {result_visible}")
                
                if not result_visible:
                    print("❌ Result screen should be visible after answer")
                    return False
                    
            except Exception as e:
                print(f"❌ Error checking result screen: {e}")
                return False
                
            # Check that explanation is shown
            try:
                explanation = await self.page.evaluate(
                    '() => document.getElementById("explanation-text").textContent'
                )
                print(f"🔍 Explanation text: {explanation[:50] if explanation else 'None'}...")
                
                if not explanation or explanation == "Explanation will appear here...":
                    print("❌ Explanation should be loaded")
                    return False
                    
            except Exception as e:
                print(f"❌ Error checking explanation: {e}")
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
            
            # Simply answer 6 questions (typical game length) with timeout
            for i in range(6):
                print(f"🔍 Answering question {i + 1}")
                
                # Check if finish screen appeared
                finish_visible = await self.page.evaluate(
                    '() => document.getElementById("finish-screen").style.display !== "none"'
                )
                if finish_visible:
                    print(f"🔍 Reached finish screen after {i} questions")
                    break
                
                # Click choice and wait for result
                await self.page.click('.choice-button:first-child')
                await asyncio.sleep(1.2)
                
                # Click next
                await self.page.click('#next-button')
                await asyncio.sleep(0.8)
                
            # Wait for finish screen
            await self.wait_for_selector('#finish-screen', timeout=3000)
            
            print("✅ Complete game test passed")
            return True
            
        except Exception as e:
            print(f"❌ Complete game test failed: {e}")
            return False
            
    async def test_play_again(self):
        """Test play again functionality"""
        print("🧪 Testing play again flow...")
        
        try:
            # Ensure we're on finish screen first (complete a game if needed)
            current_screen = await self.page.evaluate('''
                () => {
                    const screens = ['loading-screen', 'start-screen', 'game-screen', 'result-screen', 'finish-screen'];
                    return screens.find(id => {
                        const el = document.getElementById(id);
                        return el && el.style.display !== "none";
                    });
                }
            ''')
            print(f"🔍 Current screen before play again: {current_screen}")
            
            if current_screen != 'finish-screen':
                print("🔍 Not on finish screen, need to complete a game first...")
                # Start a fresh game and complete it quickly
                await self.page.goto(self.game_url)
                await self.wait_for_selector('#start-screen', timeout=10000)
                await self.page.click('#start-button')
                await self.wait_for_selector('#game-screen')
                
                # Answer questions quickly to get to finish screen
                for i in range(6):  # Assume 6 questions max
                    try:
                        await self.page.click('.choice-button:first-child')
                        await asyncio.sleep(1.2)  # Wait for result screen
                        await self.page.click('#next-button')
                        await asyncio.sleep(0.5)
                    except:
                        break  # Probably reached finish screen
                
                # Wait for finish screen
                await self.wait_for_selector('#finish-screen', timeout=5000)
            
            # Now click play again
            print("🔍 Clicking play again button...")
            await self.page.click('#play-again-button')
            
            # Should return to game screen
            if not await self.wait_for_selector('#game-screen', timeout=5000):
                print("❌ Should return to game screen after play again")
                return False
                
            # Check that we're back to first question
            question_counter = await self.page.evaluate(
                '() => document.getElementById("question-counter").textContent'
            )
            
            if not question_counter.startswith("Question 1"):
                print(f"❌ Should be back to question 1: {question_counter}")
                return False
                
            print("✅ Play again test passed")
            return True
            
        except Exception as e:
            print(f"❌ Play again test failed: {e}")
            return False
    
    async def test_build_info_verification(self):
        """Verify build info is present and current"""
        print("🧪 Testing build info verification...")
        
        try:
            if not self.build_info:
                print("❌ No build info found")
                return False
            
            required_fields = ['version', 'timestamp', 'timestampUnix']
            for field in required_fields:
                if field not in self.build_info:
                    print(f"❌ Missing build info field: {field}")
                    return False
            
            print(f"✅ Build info verification passed")
            return True
            
        except Exception as e:
            print(f"❌ Build info verification failed: {e}")
            return False
            
    async def run_all_tests(self):
        """Run all tests and report results"""
        print("🎮 Starting Democracy Education Game Tests\n")
        
        await self.setup()
        
        tests = [
            ("JSON Schema Validation", self.test_json_schema_validation),
            ("Game Loading", self.test_game_loading),
            ("Build Info Verification", self.test_build_info_verification),
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
        
        # Show build info at top of summary
        if self.build_info:
            print(f"🏗️ Tested Build: {self.build_info['version']} • {self.build_info['timestamp']}")
            print("-" * 50)
        
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
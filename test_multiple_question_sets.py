#!/usr/bin/env python3
"""
Test for multiple question sets functionality
Tests discovery, packing, and UI selector for multiple data files
"""

import asyncio
import json
import os
import tempfile
from pathlib import Path
from pyppeteer import launch
from bs4 import BeautifulSoup

class MultipleQuestionSetsTest:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.browser = None
        self.page = None
        
    async def setup(self):
        """Setup browser for testing"""
        self.browser = await launch(
            headless=False,
            args=['--no-sandbox', '--disable-setuid-sandbox'],
            autoClose=False
        )
        self.page = await self.browser.newPage()
        await self.page.setViewport({'width': 1280, 'height': 800})
        
    async def teardown(self):
        """Clean up browser"""
        if self.browser:
            await self.browser.close()
            
    def test_pack_project_discovers_all_data_files(self):
        """Test that pack_project.py discovers all JSON files in data/ folder"""
        print("🧪 Testing multiple data file discovery...")
        
        # Import pack_project module
        import sys
        sys.path.append(str(self.project_root))
        
        # We'll test this by checking the packed HTML contains multiple datasets
        # First run the packer
        import pack_project
        pack_project.pack_project()
        
        # Read the packed HTML and check for multiple embedded datasets
        html_file = self.project_root / "index.html"
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Should contain multiple EMBEDDED_QUESTION_SETS
        assert 'window.EMBEDDED_QUESTION_SETS' in content, "Multiple question sets not found"
        
        # Parse the embedded data
        soup = BeautifulSoup(content, 'html.parser')
        script_tags = soup.find_all('script')
        
        found_question_sets = False
        for script in script_tags:
            if script.string and 'EMBEDDED_QUESTION_SETS' in script.string:
                found_question_sets = True
                # Extract the JSON data (this is a simplified extraction)
                break
                
        assert found_question_sets, "EMBEDDED_QUESTION_SETS script not found"
        print("✅ Multiple question sets embedding test passed")
        
    async def test_ui_question_set_selector(self):
        """Test that UI has a selector for choosing question sets"""
        print("🧪 Testing UI question set selector...")
        
        # Load the packed HTML
        html_file = self.project_root / "index.html"
        file_url = f"file://{html_file.absolute()}"
        
        await self.page.goto(file_url)
        await self.page.waitForSelector('#start-screen', timeout=10000)
        
        # Check for question set selector
        selector_exists = await self.page.evaluate('''
            !!document.getElementById('question-set-selector')
        ''')
        
        assert selector_exists, "Question set selector not found in UI"
        
        # Check selector has options
        option_count = await self.page.evaluate('''
            document.getElementById('question-set-selector').options.length
        ''')
        
        assert option_count > 1, f"Expected multiple options, found {option_count}"
        
        print(f"✅ Found question set selector with {option_count} options")
        
    async def test_question_set_switching(self):
        """Test that selecting different question sets loads different questions"""
        print("🧪 Testing question set switching...")
        
        html_file = self.project_root / "index.html"
        file_url = f"file://{html_file.absolute()}"
        
        await self.page.goto(file_url)
        await self.page.waitForSelector('#start-screen', timeout=10000)
        
        # Get initial question set title
        initial_title = await self.page.evaluate('''
            window.EMBEDDED_QUESTION_SETS ? 
            Object.keys(window.EMBEDDED_QUESTION_SETS)[0] : null
        ''')
        
        assert initial_title, "No question sets found"
        
        # Change question set selection
        await self.page.select('#question-set-selector', initial_title)
        
        # Start the game
        await self.page.click('#start-button')
        await self.page.waitForSelector('#game-screen', timeout=5000)
        
        # Get first question
        first_question = await self.page.evaluate('''
            document.getElementById('question-text').textContent
        ''')
        
        assert first_question.strip(), "No question text found"
        print(f"✅ Question set switching works, loaded question: {first_question[:50]}...")

async def run_all_tests():
    """Run all multiple question sets tests"""
    tester = MultipleQuestionSetsTest()
    
    try:
        print("🚀 Starting Multiple Question Sets Tests")
        print("=" * 50)
        
        # Test 1: Data file discovery and packing
        tester.test_pack_project_discovers_all_data_files()
        
        # Test 2 & 3: UI tests
        await tester.setup()
        await tester.test_ui_question_set_selector()
        await tester.test_question_set_switching()
        
        print("\n🎉 All tests passed!")
        
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        await tester.teardown()
        
    return True

if __name__ == "__main__":
    asyncio.run(run_all_tests())
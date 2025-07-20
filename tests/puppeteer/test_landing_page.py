#!/usr/bin/env python3
"""
Puppeteer tests for the new landing page design with tiles.
Tests the tile layout, hover effects, and game start functionality.
"""

import asyncio
import sys
from pathlib import Path
from pyppeteer import launch

# Add project root to sys.path to allow importing pack_project
project_root_for_import = Path(__file__).parent.parent.parent
sys.path.append(str(project_root_for_import))
import pack_project

class LandingPageTester:
    def __init__(self):
        self.browser = None
        self.page = None
        self.project_root = Path(__file__).parent.parent.parent
        self.game_url = f"file://{self.project_root}/index.html"
        self.build_info = None

    async def setup(self):
        """Initialize browser and page"""
        print("🚀 Setting up browser for landing page tests...")
        self.browser = await launch(
            headless=False,
            args=['--no-sandbox', '--disable-setuid-sandbox'],
            autoClose=False
        )
        self.page = await self.browser.newPage()
        await self.page.setViewport({'width': 1280, 'height': 800})
        
        # Capture console logs from the browser
        self.page.on('console', lambda msg: print(f"🌐 BROWSER: {msg.text}"))
        print("✅ Browser setup complete.")

    async def teardown(self):
        """Clean up browser"""
        if self.browser:
            print("🔚 Closing browser.")
            await self.browser.close()

    async def wait_for_selector(self, selector, timeout=5000):
        """Wait for element with error handling"""
        try:
            await self.page.waitForSelector(selector, {'timeout': timeout})
            print(f"✅ Found selector: '{selector}'")
            return await self.page.querySelector(selector)
        except Exception as e:
            print(f"❌ Failed to find selector: '{selector}'")
            print(f"   Error: {e}")
            return None

    async def test_pack_project(self):
        """Ensure the project packs correctly before testing."""
        print("\n🧪 Testing project packing...")
        try:
            pack_project.pack_project()
            print("✅ Project packed successfully.")
            return True
        except Exception as e:
            print(f"❌ Failed to pack project: {e}")
            return False

    async def test_game_loading_and_tile_presence(self):
        """Test that the game loads and question set tiles are present."""
        print("\n🧪 Testing game loading and tile presence...")
        try:
            await self.page.goto(self.game_url, {'waitUntil': 'networkidle0'})
            print(f"🌐 Navigated to {self.game_url}")

            start_screen = await self.wait_for_selector('#start-screen')
            if not start_screen:
                return False

            tile_container = await self.wait_for_selector('#question-set-tiles')
            if not tile_container:
                print("❌ Question set tile container not found.")
                return False

            tiles = await self.page.querySelectorAll('.question-set-tile')
            print(f"✅ Found {len(tiles)} question set tiles.")
            if len(tiles) < 2:
                print(f"⚠️  Expected more than 1 tile, but found {len(tiles)}. Check data folder.")
            
            return len(tiles) > 0
        except Exception as e:
            print(f"❌ An error occurred during game loading test: {e}")
            return False

    async def test_tile_content_and_hover_effect(self):
        """Test that tiles have titles and descriptions appear on hover."""
        print("\n🧪 Testing tile content and hover effect...")
        try:
            tile = await self.wait_for_selector('.question-set-tile')
            if not tile:
                return False

            title = await self.page.evaluate('(element) => element.querySelector(".tile-title").textContent', tile)
            print(f"✅ First tile title: '{title.strip()}'")
            if not title.strip():
                print("❌ Tile title is empty.")
                return False

            description = await self.page.evaluate('(element) => element.querySelector(".tile-description").textContent', tile)
            print(f"✅ Tile description found: '{description.strip()[:50]}...'")
            if not description.strip():
                print("❌ Tile description is empty.")
                return False

            # Check if description is initially hidden (or has opacity 0, etc.)
            # This depends on the CSS implementation. We'll check for opacity.
            initial_opacity = await self.page.evaluate('(element) => getComputedStyle(element.querySelector(".tile-description")).opacity', tile)
            print(f"✅ Initial description opacity: {initial_opacity}")
            
            # Hover over the tile
            await tile.hover()
            print("🖱️ Hovering over tile.")
            await self.page.waitFor(1000) # wait for transition

            # Check opacity after hover
            hover_opacity = await self.page.evaluate('(element) => getComputedStyle(element.querySelector(".tile-description")).opacity', tile)
            print(f"✅ Description opacity on hover: {hover_opacity}")

            if float(hover_opacity) <= float(initial_opacity):
                 print("❌ Description did not become visible on hover.")
                 return False
            
            print("✅ Hover effect test passed.")
            return True
        except Exception as e:
            print(f"❌ An error occurred during tile content/hover test: {e}")
            return False

    async def test_tile_click_starts_game(self):
        """Test that clicking a tile starts the game with the correct question set."""
        print("\n🧪 Testing that clicking a tile starts the game...")
        try:
            tiles = await self.page.querySelectorAll('.question-set-tile')
            if not tiles:
                return False
            
            # Get the title of the second tile to click it
            second_tile = tiles[1]
            tile_title_to_click = await self.page.evaluate('(element) => element.querySelector(".tile-title").textContent', second_tile)
            tile_title_to_click = tile_title_to_click.strip()
            print(f"🖱️ Will click on tile with title: '{tile_title_to_click}'")

            await second_tile.click()
            print("✅ Clicked on the second tile.")

            game_screen = await self.wait_for_selector('#game-screen')
            if not game_screen:
                print("❌ Game screen did not appear after clicking tile.")
                return False
            
            print("✅ Game screen is visible.")

            # Verify that the correct game is loaded by checking the title in the UI, if available
            # Or by checking some internal state. For now, just starting is a good sign.
            # We can enhance this if UI shows which set is active.
            question_text_element = await self.wait_for_selector('#question-text')
            question_text = await self.page.evaluate('(element) => element.textContent', question_text_element)
            print(f"✅ First question loaded: '{question_text[:50]}...'")

            if not question_text or "Loading" in question_text:
                print("❌ Question text seems incorrect.")
                return False

            return True
        except Exception as e:
            print(f"❌ An error occurred during tile click test: {e}")
            return False

    async def run_all_tests(self):
        """Run all tests and report results"""
        print("🎮 Starting Landing Page Tests\n")
        
        await self.setup()
        
        tests = [
            ("Project Packing", self.test_pack_project),
            ("Game Loading and Tile Presence", self.test_game_loading_and_tile_presence),
            ("Tile Content and Hover Effect", self.test_tile_content_and_hover_effect),
            ("Tile Click Starts Game", self.test_tile_click_starts_game),
        ]
        
        results = []
        
        for test_name, test_func in tests:
            try:
                success = await test_func()
                results.append((test_name, "✅ PASSED" if success else "❌ FAILED"))
                if not success:
                    print(f"🛑 Halting tests due to failure in: {test_name}")
                    break 
            except Exception as e:
                results.append((test_name, f"💥 ERROR: {e}"))
                break
                
        await self.teardown()
        
        print("\n" + "=" * 50)
        print("🏁 LANDING PAGE TEST SUMMARY")
        print("=" * 50)
        
        passed = 0
        total = len(tests)
        
        for i, (test_name, result) in enumerate(results):
            print(f"{i+1}. {test_name}: {result}")
            if "PASSED" in result:
                passed += 1
        
        # Fill in missing results if tests were halted
        missing = len(tests) - len(results)
        if missing > 0:
            for i in range(len(results), len(tests)):
                print(f"{i+1}. {tests[i][0]}: ⏭️ SKIPPED")


        print(f"\nResult: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 All landing page tests passed!")
            return True
        else:
            print("\n🔥 Some landing page tests failed.")
            return False

async def main():
    """Main test runner"""
    tester = LandingPageTester()
    success = await tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())

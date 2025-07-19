#!/usr/bin/env python3
"""
Pack all external resources into a single index.html file
This creates a truly standalone HTML file that can be opened directly
"""

import json
import os
from pathlib import Path
from bs4 import BeautifulSoup

def pack_project():
    """Pack CSS, JS, and JSON data into a single HTML file"""
    
    root_dir = Path(__file__).parent
    html_file = root_dir / "index.html"
    
    print(f"📦 Packing project from: {root_dir}")
    print(f"📄 Reading HTML from: {html_file}")
    
    # Read the original HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    # 1. Embed JSON data as a global variable
    data_file = root_dir / "data" / "questions.json"
    print(f"📋 Embedding data from: {data_file}")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        game_data = json.load(f)
    
    # Create script tag with embedded data
    data_script = soup.new_tag("script")
    data_script.string = f"window.EMBEDDED_GAME_DATA = {json.dumps(game_data, indent=2)};"
    
    # Insert before other scripts
    head = soup.find('head')
    head.insert(0, data_script)
    
    # 2. Inline CSS files
    print("🎨 Inlining CSS files...")
    for link in soup.find_all('link', {'rel': 'stylesheet'}):
        href = link.get('href')
        if href:
            css_path = root_dir / href
            if css_path.exists():
                print(f"  ✅ Inlining: {href}")
                with open(css_path, 'r', encoding='utf-8') as f:
                    css_content = f.read()
                
                # Create style tag
                style_tag = soup.new_tag('style')
                style_tag.string = css_content
                link.replace_with(style_tag)
            else:
                print(f"  ⚠️  File not found: {css_path}")
    
    # 3. Inline JavaScript files
    print("⚙️  Inlining JavaScript files...")
    for script in soup.find_all('script', src=True):
        src = script.get('src')
        if src:
            js_path = root_dir / src
            if js_path.exists():
                print(f"  ✅ Inlining: {src}")
                with open(js_path, 'r', encoding='utf-8') as f:
                    js_content = f.read()
                
                # Remove src attribute and set content
                del script['src']
                script.string = js_content
            else:
                print(f"  ⚠️  File not found: {js_path}")
    
    # 4. Update the fetch call to use embedded data
    print("🔧 Updating fetch calls to use embedded data...")
    
    # Find the inline script that calls loadGame
    for script in soup.find_all('script'):
        if script.string and 'uiController.loadGame()' in script.string:
            # Replace the loadGame call to use embedded data
            new_script_content = script.string.replace(
                'uiController.loadGame()',
                'uiController.loadEmbeddedGame()'
            )
            script.string = new_script_content
            break
    
    # 5. Write the packed HTML back to index.html
    print(f"💾 Writing packed file to: {html_file}")
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
    
    print("✨ Project packed successfully!")
    print("🎯 You can now open index.html directly in any browser")

if __name__ == "__main__":
    pack_project()
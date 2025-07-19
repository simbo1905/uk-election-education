#!/usr/bin/env python3
"""
Simple test runner for the Democracy Education Game
Activates virtual environment and runs Puppeteer tests
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    project_root = Path(__file__).parent
    venv_path = project_root / "venv"
    test_script = project_root / "tests" / "puppeteer" / "test_game.py"
    
    # Check if virtual environment exists
    if not venv_path.exists():
        print("❌ Virtual environment not found. Please run:")
        print("   python3 -m venv venv")
        print("   source venv/bin/activate")
        print("   pip install pyppeteer jsonschema")
        sys.exit(1)
    
    # Determine activation script path
    if sys.platform == "win32":
        activate_script = venv_path / "Scripts" / "activate"
        python_exe = venv_path / "Scripts" / "python"
    else:
        activate_script = venv_path / "bin" / "activate"
        python_exe = venv_path / "bin" / "python"
    
    if not python_exe.exists():
        print("❌ Python executable not found in virtual environment")
        sys.exit(1)
    
    print("🚀 Running Democracy Education Game Tests")
    print(f"📁 Project root: {project_root}")
    print(f"🐍 Using Python: {python_exe}")
    print("=" * 50)
    
    try:
        # Run the test script using the virtual environment's Python
        result = subprocess.run([str(python_exe), str(test_script)], 
                              cwd=project_root,
                              check=False)
        sys.exit(result.returncode)
        
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
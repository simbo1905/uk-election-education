# UK Democracy Education Game

This educational app is now live at [https://simbo1905.github.io/uk-election-education/](https://simbo1905.github.io/uk-election-education/)

A vanilla JavaScript flash-card game to teach children (12+) about democracy and the democratic process in the UK.

## Features

- Multi-choice flash-card game format
- Serverless - runs as a single HTML file
- Separates knowledge base (JSON) from game engine
- Compatible with Chrome OS, macOS, Windows, and mobile devices
- Minimal dependencies, modern web standards

## Project Structure

```
/
├── index.html          # Main game interface
├── js/
│   ├── game-engine.js  # Core game logic
│   └── ui.js          # User interface handlers
├── data/
│   ├── schema.json    # JSON schema for knowledge base
│   └── questions.json # Game questions and answers
├── css/
│   └── style.css      # Basic styling
└── tests/
    └── puppeteer/     # Automated tests
```

## Development

Setup development environment:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install pyppeteer jinja2 jsonschema
```

Run Puppeteer web browser tests using chrome dev tools:
```bash
python tests/puppeteer/test_game.py
```

Build project:
```bash
python pack_project.py
```

Verify build worked:
```bash
python test_build_info.py
```

The pack script embeds build timestamps and version info to verify the build process is working correctly. Check the bottom-right corner of the generated HTML page for build info, and browser console for debug logs.

## Usage

Open `index.html` in any modern web browser.
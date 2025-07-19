# UK Democracy Education Game

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

Run tests with Puppeteer:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install pyppeteer
python tests/puppeteer/test_game.py
```

## Usage

Open `index.html` in any modern web browser.
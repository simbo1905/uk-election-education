# Quick Start Guide

## Running the Democracy Education Game

### Option 1: Direct Browser Access
1. Open `index.html` in any modern web browser
2. The game will load automatically
3. Click "Start Learning" to begin

### Option 2: Local Web Server (Recommended)
If you have Python installed:
```bash
# Python 3
python3 -m http.server 8000

# Then open: http://localhost:8000
```

If you have Node.js installed:
```bash
npx serve .

# Or install globally:
npm install -g serve
serve .
```

### Option 3: Live Server (VS Code)
If using VS Code:
1. Install "Live Server" extension
2. Right-click on `index.html`
3. Select "Open with Live Server"

## Manual Testing Checklist

✅ **Game Loading**
- [ ] Loading screen appears briefly
- [ ] Start screen loads with game title and description
- [ ] Start button is clickable

✅ **Game Flow**
- [ ] Clicking "Start Learning" transitions to first question
- [ ] Question counter shows "Question 1 of 6"
- [ ] Score display shows "Score: 0/0"
- [ ] Question text loads properly
- [ ] Multiple choice buttons appear (2-4 options)

✅ **Answer Interaction**
- [ ] Clicking an answer disables all buttons
- [ ] Correct answer turns green
- [ ] Wrong answer (if selected) turns red
- [ ] Result screen shows ✅ for correct or ❌ for incorrect
- [ ] Explanation text appears
- [ ] "Next Question" button works

✅ **Game Completion**
- [ ] After answering all questions, finish screen appears
- [ ] Final score displays correctly (e.g., "4 out of 6")
- [ ] Percentage is calculated correctly
- [ ] "Play Again" button restarts the game

✅ **Responsive Design**
- [ ] Game works on desktop browsers
- [ ] Game works on tablet/mobile browsers
- [ ] Text is readable at different screen sizes
- [ ] Buttons are easily clickable on touch devices

## Troubleshooting

**Game doesn't load:**
- Check browser console for errors (F12)
- Ensure you're accessing via HTTP (not file://) if possible
- Try a different browser

**Questions don't appear:**
- Check that `data/questions.json` exists
- Verify JSON syntax is valid
- Check browser network tab for failed requests

**Styling looks wrong:**
- Ensure `css/style.css` is loading
- Check for CSS syntax errors
- Try hard refresh (Ctrl+F5 or Cmd+Shift+R)

## Customizing Content

To add your own questions:
1. Edit `data/questions.json` following the schema
2. Validate against `data/schema.json`
3. Refresh the browser to see changes

The game automatically shuffles questions for variety on each playthrough.
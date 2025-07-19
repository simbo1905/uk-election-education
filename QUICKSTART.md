# Quick Start Guide

## Running the Democracy Education Game

### ✅ Recommended: Direct File Access (Truly Standalone)
The game is now packed into a single HTML file that works perfectly when opened directly:

1. **Double-click on `index.html`** in your file manager
2. **Or right-click → "Open with" → choose your browser**
3. The game loads immediately with no server required!

This works on:
- ✅ macOS (Safari, Chrome, Firefox)
- ✅ Windows (Edge, Chrome, Firefox) 
- ✅ Chrome OS
- ✅ Linux (Firefox, Chrome)
- ✅ Mobile browsers (when transferred to device)

### Development Mode (Optional)
If you want to modify the game and use separate files:

1. Run the "unpacked" version with a local server:
```bash
# Python 3
python3 -m http.server 8000
# Then open: http://localhost:8000

# Or with Node.js
npx serve .
```

2. After making changes, repack the game:
```bash
# Activate Python environment
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Repack into standalone file
python pack_project.py
```

## Game Features

✅ **Truly Serverless** - No web server needed
✅ **Single File** - Everything embedded in `index.html`
✅ **6 Sample Questions** about UK democracy
✅ **Responsive Design** - Works on all screen sizes
✅ **Educational Explanations** - Learn after each answer
✅ **Question Shuffling** - Different order each time
✅ **Progress Tracking** - Score and completion percentage

## Manual Testing Checklist

✅ **File Loading**
- [ ] Double-click `index.html` opens in browser
- [ ] Loading screen appears briefly
- [ ] Start screen loads with game title
- [ ] No console errors (F12 → Console tab)

✅ **Game Flow**
- [ ] "Start Learning" button works
- [ ] Question counter shows "Question 1 of 6"
- [ ] Score display shows "Score: 0/0"
- [ ] Question text loads properly
- [ ] 4 choice buttons appear

✅ **Answer Interaction**
- [ ] Clicking an answer disables all buttons
- [ ] Correct answer turns green
- [ ] Wrong answer (if selected) turns red
- [ ] Result screen shows ✅ or ❌
- [ ] Explanation text appears
- [ ] "Next Question" button works

✅ **Game Completion**
- [ ] After 6 questions, finish screen appears
- [ ] Final score displays correctly
- [ ] Percentage is calculated correctly
- [ ] "Play Again" button restarts the game

✅ **Mobile/Responsive**
- [ ] Game works on phone browsers
- [ ] Buttons are touch-friendly
- [ ] Text is readable on small screens

## Customizing Content

The game uses embedded data, so to add your own questions:

1. Edit `data/questions.json` with your questions
2. Run the packing script: `python pack_project.py`
3. The new `index.html` will include your updated questions

### Question Format
```json
{
  "id": "q007",
  "question": "Your question here?",
  "choices": [
    "Option A",
    "Option B", 
    "Option C",
    "Option D"
  ],
  "correctAnswer": 1,
  "explanation": "Educational explanation here...",
  "category": "Topic Name",
  "difficulty": "easy",
  "tags": ["tag1", "tag2"]
}
```

## Testing

Run automated tests:
```bash
source venv/bin/activate
python test_file_url.py  # Test file:// URL functionality
```

## Sharing the Game

To share with others:
1. Send them just the `index.html` file
2. They double-click to open it
3. No installation or setup required!

Perfect for:
- 📧 Email attachments
- 💾 USB drives  
- 📱 Transfer to mobile devices
- 🏫 School environments with restricted internet
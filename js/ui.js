/**
 * UI Controller for Democracy Education Game
 * Handles all user interface interactions and updates
 */

class UIController {
    constructor(gameEngine) {
        this.game = gameEngine;
        this.elements = {};
        this.init();
    }

    /**
     * Initialize UI elements and event listeners
     */
    init() {
        // Cache DOM elements
        this.elements = {
            gameContainer: document.getElementById('game-container'),
            loadingScreen: document.getElementById('loading-screen'),
            startScreen: document.getElementById('start-screen'),
            gameScreen: document.getElementById('game-screen'),
            resultScreen: document.getElementById('result-screen'),
            finishScreen: document.getElementById('finish-screen'),
            
            // Start screen
            gameTitle: document.getElementById('game-title'),
            gameDescription: document.getElementById('game-description'),
            startButton: document.getElementById('start-button'),
            
            // Game screen
            questionCounter: document.getElementById('question-counter'),
            scoreDisplay: document.getElementById('score-display'),
            questionText: document.getElementById('question-text'),
            choicesContainer: document.getElementById('choices-container'),
            
            // Result screen
            resultIcon: document.getElementById('result-icon'),
            resultText: document.getElementById('result-text'),
            explanationText: document.getElementById('explanation-text'),
            nextButton: document.getElementById('next-button'),
            
            // Finish screen
            finalScore: document.getElementById('final-score'),
            finalPercentage: document.getElementById('final-percentage'),
            playAgainButton: document.getElementById('play-again-button')
        };

        this.bindEvents();
    }

    /**
     * Bind event listeners
     */
    bindEvents() {
        if (this.elements.startButton) {
            this.elements.startButton.addEventListener('click', () => this.startGame());
        }
        
        if (this.elements.nextButton) {
            this.elements.nextButton.addEventListener('click', () => this.nextQuestion());
        }
        
        if (this.elements.playAgainButton) {
            this.elements.playAgainButton.addEventListener('click', () => this.restartGame());
        }
    }

    /**
     * Load game data and initialize
     */
    async loadGame() {
        this.showScreen('loading');
        
        try {
            const response = await fetch('./data/questions.json');
            const gameData = await response.json();
            
            const success = await this.game.loadQuestions(gameData);
            if (success) {
                this.updateStartScreen();
                this.showScreen('start');
            } else {
                this.showError('Failed to load game data');
            }
        } catch (error) {
            console.error('Error loading game:', error);
            this.showError('Failed to load game. Please check your connection.');
        }
    }

    /**
     * Load embedded game data (for packed version)
     */
    async loadEmbeddedGame() {
        this.showScreen('loading');
        
        try {
            // Use embedded data instead of fetching
            if (window.EMBEDDED_GAME_DATA) {
                const success = await this.game.loadQuestions(window.EMBEDDED_GAME_DATA);
                if (success) {
                    this.updateStartScreen();
                    this.showScreen('start');
                } else {
                    this.showError('Failed to load embedded game data');
                }
            } else {
                this.showError('No embedded game data found');
            }
        } catch (error) {
            console.error('Error loading embedded game:', error);
            this.showError('Failed to load embedded game data.');
        }
    }

    /**
     * Update start screen with game metadata
     */
    updateStartScreen() {
        const metadata = this.game.getMetadata();
        
        if (this.elements.gameTitle) {
            this.elements.gameTitle.textContent = metadata.title || 'Democracy Education Game';
        }
        
        if (this.elements.gameDescription) {
            this.elements.gameDescription.textContent = 
                metadata.description || 'Learn about democracy through interactive questions';
        }
    }

    /**
     * Start the game
     */
    startGame() {
        this.game.startGame();
        this.showQuestion();
        this.showScreen('game');
    }

    /**
     * Display current question
     */
    showQuestion() {
        const question = this.game.getCurrentQuestion();
        const stats = this.game.getStats();
        
        if (!question) {
            this.showFinishScreen();
            return;
        }

        // Update question counter and score
        if (this.elements.questionCounter) {
            this.elements.questionCounter.textContent = 
                `Question ${stats.answered + 1} of ${stats.total}`;
        }
        
        if (this.elements.scoreDisplay) {
            this.elements.scoreDisplay.textContent = 
                `Score: ${stats.score}/${stats.answered}`;
        }

        // Display question
        if (this.elements.questionText) {
            this.elements.questionText.textContent = question.question;
        }

        // Create choice buttons
        this.createChoiceButtons(question.choices);
    }

    /**
     * Create clickable choice buttons
     */
    createChoiceButtons(choices) {
        if (!this.elements.choicesContainer) return;

        this.elements.choicesContainer.innerHTML = '';
        
        choices.forEach((choice, index) => {
            const button = document.createElement('button');
            button.className = 'choice-button';
            button.textContent = choice;
            button.onclick = () => this.selectAnswer(index);
            
            this.elements.choicesContainer.appendChild(button);
        });
    }

    /**
     * Handle answer selection
     */
    selectAnswer(answerIndex) {
        // Disable all choice buttons
        const buttons = this.elements.choicesContainer.querySelectorAll('.choice-button');
        buttons.forEach(button => button.disabled = true);

        // Submit answer and get result
        const result = this.game.submitAnswer(answerIndex);
        
        // Highlight correct and incorrect answers
        buttons.forEach((button, index) => {
            if (index === result.correctAnswerIndex) {
                button.classList.add('correct');
            } else if (index === answerIndex && !result.correct) {
                button.classList.add('incorrect');
            }
        });

        // Show result after a brief delay
        setTimeout(() => {
            this.showResult(result);
        }, 1500);
    }

    /**
     * Show answer result and explanation
     */
    showResult(result) {
        if (this.elements.resultIcon) {
            this.elements.resultIcon.textContent = result.correct ? '✅' : '❌';
        }
        
        if (this.elements.resultText) {
            this.elements.resultText.textContent = result.correct 
                ? 'Correct!' 
                : `Incorrect. The correct answer was: ${result.correctAnswerText}`;
        }
        
        if (this.elements.explanationText) {
            this.elements.explanationText.textContent = result.explanation;
        }

        this.showScreen('result');
    }

    /**
     * Move to next question
     */
    nextQuestion() {
        const nextQ = this.game.nextQuestion();
        
        if (nextQ) {
            this.showQuestion();
            this.showScreen('game');
        } else {
            this.showFinishScreen();
        }
    }

    /**
     * Show final results
     */
    showFinishScreen() {
        const stats = this.game.getStats();
        
        if (this.elements.finalScore) {
            this.elements.finalScore.textContent = `${stats.score} out of ${stats.total}`;
        }
        
        if (this.elements.finalPercentage) {
            this.elements.finalPercentage.textContent = `${stats.percentage}%`;
        }

        this.showScreen('finish');
    }

    /**
     * Restart the game
     */
    restartGame() {
        this.game.reset();
        this.startGame();
    }

    /**
     * Show specific screen
     */
    showScreen(screenName) {
        // Hide all screens
        Object.values(this.elements).forEach(element => {
            if (element && element.classList && element.classList.contains('screen')) {
                element.style.display = 'none';
            }
        });

        // Show requested screen
        const screenMap = {
            'loading': this.elements.loadingScreen,
            'start': this.elements.startScreen,
            'game': this.elements.gameScreen,
            'result': this.elements.resultScreen,
            'finish': this.elements.finishScreen
        };

        const targetScreen = screenMap[screenName];
        if (targetScreen) {
            targetScreen.style.display = 'block';
        }
    }

    /**
     * Show error message
     */
    showError(message) {
        // Simple error display - could be enhanced with a proper error screen
        if (this.elements.loadingScreen) {
            this.elements.loadingScreen.innerHTML = `
                <div class="error">
                    <h2>Error</h2>
                    <p>${message}</p>
                    <button onclick="location.reload()">Retry</button>
                </div>
            `;
        }
    }
}
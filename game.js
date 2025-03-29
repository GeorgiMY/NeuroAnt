// Constants
const GRID_SIZE = 160;
const CELL_SIZE = 5;
const CANVAS_SIZE = GRID_SIZE * CELL_SIZE;

// Colors
const COLORS = [
    [255, 255, 255], // White
    [0, 0, 0],       // Black
    [255, 0, 0],     // Red
    [0, 255, 0],     // Green
    [0, 0, 255]      // Blue
];

// Directions (up, right, down, left)
const DIRECTIONS = [[0, -1], [1, 0], [0, 1], [-1, 0]];

// Get DOM elements
const gameStepsInput = document.getElementById('gameSteps');
const addRuleLeftBtn = document.getElementById('addRuleLeft');
const addRuleRightBtn = document.getElementById('addRuleRight');
const removeRuleBtn = document.getElementById('removeRule');
const startButton = document.getElementById('startButton');
const pauseButton = document.getElementById('pauseButton');
const resetButton = document.getElementById('resetButton');

// Function to enable/disable controls
function setControlsEnabled(enabled) {
    addRuleLeftBtn.disabled = !enabled;
    addRuleRightBtn.disabled = !enabled;
    removeRuleBtn.disabled = !enabled;
    gameStepsInput.disabled = !enabled;
}

class LangtonsAnt {
    constructor() {
        this.grid = Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(0));
        this.x = Math.floor(GRID_SIZE / 2);
        this.y = Math.floor(GRID_SIZE / 2);
        this.dir = 0;
        this.rules = { 0: 1, 1: 2, 2: 0 };
        this.turns = { 0: 1, 1: -1, 2: 1 };
        this.isRunning = false;
        this.animationFrame = null;
    }

    step() {
        const currentColor = this.grid[this.y][this.x];
        this.grid[this.y][this.x] = this.rules[currentColor];
        this.dir = (this.dir + this.turns[currentColor] + 4) % 4;
        const [dx, dy] = DIRECTIONS[this.dir];
        this.x = (this.x + dx + GRID_SIZE) % GRID_SIZE;
        this.y = (this.y + dy + GRID_SIZE) % GRID_SIZE;
    }

    addRuleLeft() {
        const newColor = Object.keys(this.rules).length;
        COLORS.push([
            Math.floor(Math.random() * 256),
            Math.floor(Math.random() * 256),
            Math.floor(Math.random() * 256)
        ]);

        this.rules[newColor] = 0;
        if (newColor > 0) {
            this.rules[newColor - 1] = newColor;
        }
        this.turns[newColor] = -1;
        this.updateRulesDisplay();
    }

    addRuleRight() {
        const newColor = Object.keys(this.rules).length;
        COLORS.push([
            Math.floor(Math.random() * 256),
            Math.floor(Math.random() * 256),
            Math.floor(Math.random() * 256)
        ]);

        this.rules[newColor] = 0;
        if (newColor > 0) {
            this.rules[newColor - 1] = newColor;
        }
        this.turns[newColor] = 1;
        this.updateRulesDisplay();
    }

    removeRule() {
        if (Object.keys(this.rules).length > 0) {
            const lastColor = Object.keys(this.rules).length - 1;
            delete this.rules[lastColor];
            delete this.turns[lastColor];

            if (Object.keys(this.rules).length > 0) {
                this.rules[Object.keys(this.rules).length - 1] = 0;
            }

            COLORS.pop();
            this.updateRulesDisplay();
        }
    }

    reset() {
        this.grid = Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(0));
        this.x = Math.floor(GRID_SIZE / 2);
        this.y = Math.floor(GRID_SIZE / 2);
        this.dir = 0;
        this.rules = { 0: 1, 1: 2, 2: 0 };
        this.turns = { 0: 1, 1: -1, 2: 1 };
        COLORS.length = 5; // Reset to initial colors
        this.updateRulesDisplay();
        setControlsEnabled(true);
    }

    updateRulesDisplay() {
        const rulesList = document.getElementById('rulesList');
        rulesList.innerHTML = '';
        Object.keys(this.rules).forEach(key => {
            const ruleItem = document.createElement('div');
            ruleItem.className = 'rule-item';
            ruleItem.textContent = `Rule ${key} → ${this.rules[key]} (Turn: ${this.turns[key] === 1 ? 'Right' : 'Left'})`;
            rulesList.appendChild(ruleItem);
        });
    }

    draw(ctx) {
        // Draw grid
        for (let y = 0; y < GRID_SIZE; y++) {
            for (let x = 0; x < GRID_SIZE; x++) {
                const color = COLORS[this.grid[y][x]];
                ctx.fillStyle = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
                ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
            }
        }
    }
}

// Initialize canvas and game
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
canvas.width = CANVAS_SIZE;
canvas.height = CANVAS_SIZE;

const game = new LangtonsAnt();

// Animation loop
function animate() {
    if (game.isRunning) {
        const steps = parseInt(gameStepsInput.value) || 100;
        for (let i = 0; i < steps; i++) {
            game.step();
        }
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        game.draw(ctx);
        game.animationFrame = requestAnimationFrame(animate);
    }
}

// Event listeners
addRuleLeftBtn.addEventListener('click', () => {
    if (!game.isRunning) {
        game.addRuleLeft();
    }
});

addRuleRightBtn.addEventListener('click', () => {
    if (!game.isRunning) {
        game.addRuleRight();
    }
});

removeRuleBtn.addEventListener('click', () => {
    if (!game.isRunning) {
        game.removeRule();
    }
});

startButton.addEventListener('click', () => {
    game.isRunning = true;
    startButton.style.display = 'none';
    pauseButton.style.display = 'block';
    setControlsEnabled(false);
    animate();
});

pauseButton.addEventListener('click', () => {
    game.isRunning = false;
    cancelAnimationFrame(game.animationFrame);
    startButton.style.display = 'block';
    pauseButton.style.display = 'none';
    setControlsEnabled(true);
});

resetButton.addEventListener('click', () => {
    game.isRunning = false;
    cancelAnimationFrame(game.animationFrame);
    game.reset();
    startButton.style.display = 'block';
    pauseButton.style.display = 'none';
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    game.draw(ctx);
});

// Initial draw
game.draw(ctx);
game.updateRulesDisplay(); 

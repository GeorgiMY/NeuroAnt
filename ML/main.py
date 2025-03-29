import gymnasium as gym
import numpy as np
import pygame
import random
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from datetime import datetime

# Constants
GRID_SIZE = 100
CELL_SIZE = 5
STEPS_BEFORE_CHECK = 50000  # Check for highway after this many steps

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [WHITE, BLACK]
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

class LangtonsAntEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)
        self.x, self.y = GRID_SIZE // 2, GRID_SIZE // 2
        self.dir = 0
        self.rules = {0: 1, 1: 0}  # Initial rule: flip black <-> white
        self.turns = {0: 1, 1: -1}  # Right turn for white, left turn for black
        self.previous_positions = set()
        self.steps = 0
        self.highway_detected = False
        
        self.action_space = gym.spaces.Discrete(2)  # 0: add rule, 1: remove rule
        # Flatten the observation space to 1D
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(GRID_SIZE * GRID_SIZE,), dtype=np.uint8)
    
    def step(self, action):
        if action == 0:
            self.add_rule()
        elif action == 1:
            self.remove_rule()
        
        for _ in range(100):  # Simulate 100 steps per action
            self._move_ant()
        
        self.steps += 100
        reward = 0
        
        # Check for highway formation
        if self.detect_highway():
            reward += 50  # Large reward for highway
            self.highway_detected = True
            self.save_successful_rules()
        
        if self.steps >= STEPS_BEFORE_CHECK and not self.highway_detected:
            reward -= 20  # Penalize for failing to create a highway
        
        terminated = self.steps >= STEPS_BEFORE_CHECK
        truncated = False  # We don't truncate episodes early
        
        return self.grid.flatten(), reward, terminated, truncated, {}
    
    def reset(self, seed=None):
        super().reset(seed=seed)
        self.grid.fill(0)
        self.x, self.y = GRID_SIZE // 2, GRID_SIZE // 2
        self.dir = 0
        self.rules = {0: 1, 1: 0}
        self.turns = {0: 1, 1: -1}
        self.previous_positions.clear()
        self.steps = 0
        self.highway_detected = False
        return self.grid.flatten(), {}
    
    def _move_ant(self):
        current_color = self.grid[self.y, self.x]
        self.grid[self.y, self.x] = self.rules[current_color]
        self.dir = (self.dir + self.turns[current_color]) % 4
        dx, dy = DIRECTIONS[self.dir]
        self.x = (self.x + dx) % GRID_SIZE
        self.y = (self.y + dy) % GRID_SIZE
        self.previous_positions.add((self.x, self.y))
    
    def add_rule(self):
        if len(self.rules) < 2:  # Keep only binary values in the grid
            new_color = len(self.rules)
            COLORS.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            self.rules[new_color] = 0
            self.rules[new_color - 1] = new_color
            self.turns[new_color] = random.choice([-1, 1])
    
    def remove_rule(self):
        if len(self.rules) > 2:
            last_color = len(self.rules) - 1
            # Convert all cells with the last color to 0
            self.grid[self.grid == last_color] = 0
            del self.rules[last_color]
            del self.turns[last_color]
            COLORS.pop()
    
    def detect_highway(self):
        last_positions = list(self.previous_positions)[-50:]
        if len(set(last_positions)) == 1:
            return True  # If the last 50 positions are the same, it's a highway
        return False
    
    def save_successful_rules(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("successful_rules.txt", "a") as file:
            file.write(f"\n=== Successful Rules Found at {timestamp} ===\n")
            file.write(f"Steps taken: {self.steps}\n")
            file.write("Rules:\n")
            for color, next_color in self.rules.items():
                file.write(f"  Color {color} -> {next_color} (Turn: {self.turns[color]})\n")
            file.write("=" * 50 + "\n")

# Initialize and check environment
env = LangtonsAntEnv()
check_env(env)

# Train RL Model
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# Save the trained model
model.save("langtons_ant_rl")

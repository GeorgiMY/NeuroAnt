import random
import numpy as np
from datetime import datetime
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
import gymnasium as gym

# Constants
GRID_SIZE = 160
STEPS_BEFORE_CHECK = 50000  # Check for highway after this many steps
MAX_HIGHWAYS = 10  # Maximum number of different highways to find

# Directions (up, right, down, left)
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

class LangtonsAntEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.action_space = gym.spaces.Discrete(2)  # 0: add rule, 1: remove rule
        # Flatten the observation space to 1D
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(GRID_SIZE * GRID_SIZE,), dtype=np.uint8)
        # Initialize all instance variables
        self.grid = None
        self.x = None
        self.y = None
        self.dir = None
        self.rules = None
        self.turns = None
        self.previous_positions = None
        self.steps = None
        self.highway_detected = None
        # Reset the environment
        self.reset()
    
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
            # Reset the environment to search for a new highway
            self.reset()
        
        if self.steps >= STEPS_BEFORE_CHECK and not self.highway_detected:
            reward -= 20  # Penalize for failing to create a highway
            # Reset the environment to try again
            self.reset()
        
        terminated = self.steps >= STEPS_BEFORE_CHECK
        truncated = False  # We don't truncate episodes early
        
        # Normalize the grid values to stay within observation space bounds
        normalized_grid = np.clip(self.grid, 0, 1)
        return normalized_grid.flatten(), reward, terminated, truncated, {}
    
    def reset(self, seed=None):
        super().reset(seed=seed)
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)
        self.x, self.y = GRID_SIZE // 2, GRID_SIZE // 2
        self.dir = 0
        self.rules = {0: 1, 1: 0}
        self.turns = {0: 1, 1: -1}
        self.previous_positions = set()  # Initialize as empty set
        self.steps = 0
        self.highway_detected = False
        return self.grid.flatten(), {}
    
    def _move_ant(self):
        current_color = int(self.grid[self.y, self.x])  # Convert to int to ensure valid key
        if current_color in self.rules:  # Only proceed if color exists in rules
            self.grid[self.y, self.x] = self.rules[current_color]
            self.dir = (self.dir + self.turns[current_color]) % 4
            dx, dy = DIRECTIONS[self.dir]
            self.x = (self.x + dx) % GRID_SIZE
            self.y = (self.y + dy) % GRID_SIZE
            self.previous_positions.add((self.x, self.y))
    
    def add_rule(self):
        if len(self.rules) < 10:  # Limit to 10 rules
            new_color = len(self.rules)
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


def main():
    # Initialize and check environment
    env = LangtonsAntEnv()
    check_env(env)

    # Create and train the model
    model = PPO("MlpPolicy", env, verbose=1)
    
    # Train until we find MAX_HIGHWAYS different highways
    highways_found = 0
    total_timesteps = 0
    max_timesteps = 1000000  # Maximum total training steps
    
    while highways_found < MAX_HIGHWAYS and total_timesteps < max_timesteps:
        # Train for a batch of steps
        model.learn(total_timesteps=100000)
        total_timesteps += 100000
        
        # Test the current model
        obs, _ = env.reset()
        done = False
        while not done:
            action, _ = model.predict(obs)
            obs, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
        
        # Count highways found
        with open("successful_rules.txt", "r") as file:
            highways_found = file.read().count("=== Successful Rules Found")
        
        print(f"Highways found: {highways_found}/{MAX_HIGHWAYS}")
        print(f"Total timesteps: {total_timesteps}")

    # Save the final trained model
    model.save("langtons_ant_rl")
    print(f"Training completed. Found {highways_found} different highways.")

if __name__ == "__main__":
    main() 

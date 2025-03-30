import pygame
import random
from datetime import datetime

# Constants
STEPS_PER_FRAME = 0
GRID_SIZE = 160
CELL_SIZE = 5
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE + 200, GRID_SIZE * CELL_SIZE 

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [WHITE, BLACK, RED, GREEN, BLUE]

# Directions (up, right, down, left)
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

class LangtonsAnt:
    def __init__(self):
        # Initialize the grid with zeros (white cells)
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        # Start the ant in the center of the grid
        self.x, self.y = GRID_SIZE // 2, GRID_SIZE // 2
        self.dir = 0  # Start facing upward
        # Rules for color changes: current color -> next color
        self.rules = {0: 1, 1: 2, 2: 0}
        # Turn rules: 1 = turn right, -1 = turn left
        self.turns = {0: 1, 1: -1, 2: 1}
    
    def step(self):
        # Get current cell color
        current_color = self.grid[self.y][self.x]
        # Update cell color based on rules
        self.grid[self.y][self.x] = self.rules[current_color]
        # Update direction based on turn rules
        self.dir = (self.dir + self.turns[current_color]) % 4
        # Move ant in current direction
        dx, dy = DIRECTIONS[self.dir]
        self.x = (self.x + dx) % GRID_SIZE
        self.y = (self.y + dy) % GRID_SIZE

    def add_rule_left(self):
        # Add a new color to the sequence
        new_color = len(self.rules)
        
        # Add a random new color to the COLORS list
        COLORS.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        # Update rules to maintain the cycle
        self.rules[new_color] = 0  # New color returns to start (0)
        
        # Update the previous rule to point to the new color
        if new_color > 0:
            self.rules[new_color - 1] = new_color  

        # Set the turn direction to left (-1)
        self.turns[new_color] = -1

    def add_rule_right(self):
        # Add a new color to the sequence
        new_color = len(self.rules)
        
        # Add a random new color to the COLORS list
        COLORS.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        # Update rules to maintain the cycle
        self.rules[new_color] = 0  # New color returns to start (0)
        
        # Update the previous rule to point to the new color
        if new_color > 0:
            self.rules[new_color - 1] = new_color  

        # Set the turn direction to right (1)
        self.turns[new_color] = 1

    def remove_rule(self):
        if len(self.rules) > 0:
            # Remove the last element from rules and turns
            last_color = len(self.rules) - 1
            del self.rules[last_color]
            del self.turns[last_color]
            
            # Update the cycle in rules if there are remaining elements
            if len(self.rules) > 0:
                # Last added color should point to the first color
                self.rules[len(self.rules) - 1] = 0
            
            # Remove the last color from COLORS
            COLORS.pop()

    def reser_simulatin(self):
        # Reset the simulation to initial state
        self.__init__()

    def draw_rules_and_turns(self, screen, font):
        # Calculate position for rule display
        x_offset = GRID_SIZE * CELL_SIZE + 10  # Offset to the right of the grid
        y_offset = 10  # Initial offset from top

        # Draw each rule and its corresponding turn direction
        for key in self.rules.keys():
            rule_text = f"Rule {key} -> {self.rules[key]}"
            turn_text = f"{'Right' if self.turns[key] == 1 else 'Left'}"

            # Render the text
            rule_rendered = font.render(rule_text, True, BLACK)
            turn_rendered = font.render(turn_text, True, BLACK)

            # Display text side by side (100px spacing between them)
            screen.blit(rule_rendered, (x_offset, y_offset))
            screen.blit(turn_rendered, (x_offset + 120, y_offset))  

            # Move down for the next line
            y_offset += 30

    def save_successful_rules(self):
        # Save the current rules configuration to a file with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("successful_rules.txt", "a") as file:
            file.write(f"\n=== Successful Rules Found at {timestamp} ===\n")
            file.write(f"Steps taken: {self.steps}\n")
            file.write("Rules:\n")
            for color, next_color in self.rules.items():
                file.write(f"  Color {color} -> {next_color} (Turn: {self.turns[color]})\n")
            file.write("=" * 50 + "\n")

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
ant = LangtonsAnt()
running = True
font = pygame.font.Font(None, 24)

def start_simulation():
    # Start the simulation by setting steps per frame
    global STEPS_PER_FRAME
    STEPS_PER_FRAME = 100

def pause_simulation():
    # Pause the simulation by setting steps per frame to 0
    global STEPS_PER_FRAME
    STEPS_PER_FRAME = 0

def draw_buttons_add_rul_left():
    # Draw the "Add Rule Left" button
    pygame.draw.rect(screen, BLUE, (10, HEIGHT - 40, 100, 30))
    small_font = pygame.font.Font(None, 18)
    text = small_font.render("Add Rule Left", True, WHITE)
    screen.blit(text, (20, HEIGHT - 35))

def draw_buttons_add_rul_right():
    # Draw the "Add Rule Right" button
    pygame.draw.rect(screen, BLUE, (120, HEIGHT - 40, 100, 30))
    small_font = pygame.font.Font(None, 18)
    text = small_font.render("Add Rule Right", True, WHITE)
    screen.blit(text, (130, HEIGHT - 35))

def draw_buttons_remove_rule():
    # Draw the "Remove Rule" button
    pygame.draw.rect(screen, RED, (240, HEIGHT - 40, 100, 30))
    text = font.render("Remove Rule", True, WHITE)
    screen.blit(text, (250, HEIGHT - 35))

def draw_buttons_start():
    # Draw the "Start" button
    pygame.draw.rect(screen, GREEN, (350, HEIGHT - 40, 100, 30))
    small_font = pygame.font.Font(None, 18)
    text = small_font.render("Start", True, WHITE)
    screen.blit(text, (360, HEIGHT - 35))

def draw_buttons_pause():
    # Draw the "Pause" button
    pygame.draw.rect(screen, (255, 255, 0), (350, HEIGHT - 40, 100, 30))
    small_font = pygame.font.Font(None, 18)
    text = small_font.render("Pause", True, WHITE)
    screen.blit(text, (360, HEIGHT - 35))

def draw_buttons_reset_button():
    # Draw the "Reset" button
    pygame.draw.rect(screen, BLUE, (460, HEIGHT - 40, 100, 30))
    text = font.render("Reset", True, WHITE)
    screen.blit(text, (470, HEIGHT - 35))

def draw_on_no_play_buttons():
    # Draw all buttons when simulation is paused
    draw_buttons_add_rul_left()
    draw_buttons_add_rul_right()
    draw_buttons_remove_rule()
    draw_buttons_start()
    draw_buttons_reset_button()

def draw_on_play_buttons():
    # Draw only the pause button when simulation is running
    draw_buttons_pause()

# Main game loop
while running:
    screen.fill(WHITE)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:  # Check for clicks
            x, y = event.pos  # Get mouse coordinates
            
            if STEPS_PER_FRAME == 0:
                # Handle button clicks when simulation is paused
                if 10 <= x <= 110 and HEIGHT - 40 <= y <= HEIGHT - 10:
                    ant.add_rule_left()  # Add new left turn rule
                                       
                if 120 <= x <= 220 and HEIGHT - 40 <= y <= HEIGHT - 10:
                    ant.add_rule_right()  # Add new right turn rule

                if 240 <= x <= 340 and HEIGHT - 40 <= y <= HEIGHT - 10:
                    ant.remove_rule()  # Remove last rule
                    
                if 360 <= x <= 460 and HEIGHT - 40 <= y <= HEIGHT - 10:
                    start_simulation()  # Start the simulation

                if 480 <= x <= 580 and HEIGHT - 40 <= y <= HEIGHT - 10:
                    ant.reser_simulatin()  # Reset the simulation
            else:
                if 360 <= x <= 460 and HEIGHT - 40 <= y <= HEIGHT - 10:
                    pause_simulation()  # Pause the simulation

    # Update ant position multiple times per frame
    for _ in range(STEPS_PER_FRAME):
        ant.step()

    # Draw the grid
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            pygame.draw.rect(screen, COLORS[ant.grid[y][x]], (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Display rules and turns on the side
    ant.draw_rules_and_turns(screen, font)

    # Draw appropriate buttons based on simulation state
    if STEPS_PER_FRAME == 0:
        draw_on_no_play_buttons()
    else:
        draw_on_play_buttons()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

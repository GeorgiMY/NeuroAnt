import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Start Scene")
clock = pygame.time.Clock()

# Load background image
try:
    background = pygame.image.load(os.path.join("assets", "bg.png"))
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
except pygame.error as e:
    print(f"Couldn't load background image: {e}")
    background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    background.fill(WHITE)

def run_start_scene():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse position
                mouse_pos = pygame.mouse.get_pos()
                # Check if click is within screen bounds
                if (0 <= mouse_pos[0] <= WINDOW_WIDTH and 0 <= mouse_pos[1] <= WINDOW_HEIGHT):
                    return "ant-scene"

        # Draw background
        screen.blit(background, (0, 0))
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    run_start_scene()

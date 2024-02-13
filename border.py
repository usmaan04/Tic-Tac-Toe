import pygame
import sys

pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Rectangle with Border")

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up rectangle properties
rect_x, rect_y, rect_width, rect_height = 50, 50, 200, 100
border_thickness = 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(white)

    # Draw border
    pygame.draw.rect(screen, black, (rect_x, rect_y, rect_width, rect_height))

    # Draw fill (inner rectangle)
    inner_rect = pygame.Rect(rect_x + border_thickness, rect_y + border_thickness,
                             rect_width - 2 * border_thickness, rect_height - 2 * border_thickness)
    pygame.draw.rect(screen, white, inner_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()

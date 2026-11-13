# runs all lower classes

# import pygame package
import pygame
from renderer import Renderer

# initializing imported module
pygame.init()
screen = pygame.display.set_mode((750, 700))

# Setting name for window
pygame.display.set_caption('Platformer')
# Game should be in a game folder to run properly
original_image = pygame.image.load("Game/Sprites/background.png").convert_alpha()
background_image = pygame.transform.scale(original_image, (750, 700))
# creating a bool value which checks 
# if game is running
running = True
clock = pygame.time.Clock()

while running:
  
    # Check for event if user has pushed 
    # any event in queue
    for event in pygame.event.get():
      
        # if event is of type quit then set
        # running bool to false
        if event.type == pygame.QUIT:
            running = False
    screen.blit(background_image, (0,0))
    pygame.display.flip()
    clock.tick(60)

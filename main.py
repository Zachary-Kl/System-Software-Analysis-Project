# runs all lower classes

# import pygame package
import pygame
from renderer import draw

# initializing imported module
pygame.init()

# displaying a window of height
# 500 and width 400
pygame.display.set_mode((750, 700))

# Setting name for window
pygame.display.set_caption('Platformer')

# creating a bool value which checks 
# if game is running
running = True
while running:
  
    # Check for event if user has pushed 
    # any event in queue
    for event in pygame.event.get():
      
        # if event is of type quit then set
        # running bool to false
        if event.type == pygame.QUIT:
            running = False

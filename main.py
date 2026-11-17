# runs all lower classes

# import pygame package
import pygame

# initializing imported module
pygame.init()
XScale = 750
YScale = 700
screen = pygame.display.set_mode((XScale, YScale))

# Setting name for window
pygame.display.set_caption('Platformer')
# Game should be in a game folder to run properly
original_image = pygame.image.load("Game/Sprites/Background.png").convert_alpha()
background_image = pygame.transform.scale(original_image, (XScale, YScale))
player_original_image = pygame.image.load("Game/Sprites/PlayerModel.png")
player_image = pygame.transform.scale(player_original_image, (40, 80))
platform_original_image = pygame.image.load("Game/Sprites/Platform.png")
platform_image = pygame.transform.scale(platform_original_image, (160, 40))
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
    screen.blit(player_image, (400,400))
    screen.blit(platform_image, (500,500))
    pygame.display.flip()
    clock.tick(60)

# Game should be in a game folder to run properly
import pygame
XScale = 800
YScale = 600

class Player(pygame.sprite.Sprite):
    #Creating Player
    def __init__(self):
        super().__init__()
        #Load Player Image and Set Size of it
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        player_original_image = pygame.image.load("Game/Sprites/PlayerModel.png")
        player_image = pygame.transform.scale(player_original_image, (width, height))
        self.image = player_image
        self.rect = self.image.get_rect()
        #Set Speed to 0
        self.change_x = 0
        self.change_y = 0
        self.level = None
        
    #Player Movement
    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x
        #Collision Detection
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0
            
    #Gravity Calculations
    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
        if self.rect.y >= YScale - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = YScale - self.rect.height
            
    #Jump
    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        if len(platform_hit_list) > 0 or self.rect.bottom >= YScale:
            self.change_y = -10
    
    #Sideways Movement
    def go_left(self):
        self.change_x = -6
        
    def go_right(self):
        self.change_x = 6
        
    def stop(self):
        self.change_x = 0


#Platform
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        platform_original_image = pygame.image.load("Game/Sprites/Platform.png")
        platform_image = pygame.transform.scale(platform_original_image, (width, height))
        self.image = platform_image
        self.rect = self.image.get_rect()
        
        
#Level Loader
class Level():
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
        self.world_shift = 0
        
    def update(self):
        self.platform_list.update()
        self.enemy_list.update()
        
    def draw(self, screen):
        original_image = pygame.image.load("Game/Sprites/Background.png").convert_alpha()
        background_image = pygame.transform.scale(original_image, (XScale, YScale))
        screen.blit(background_image, (0,0))
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        
    def shift_world(self, shift_x):
        self.world_shift += shift_x
        for platform in self.platform_list:
            platform.rect.x += shift_x
 
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x


#Test Levels
class Level_Test_1(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        self.level_limit = -1000
        #Platform Locations
        level = [[210, 70, 500, 500],
                 [210, 70, 800, 400],
                 [210, 70, 1000, 500],
                 [210, 70, 1120, 280],
                 ]
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
class Level_Test_2(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        self.level_limit = -1000
        #Platform Locations
        level = [[210, 30, 450, 570],
                 [210, 30, 850, 420],
                 [210, 30, 1000, 520],
                 [210, 30, 1120, 280],
                 ]
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        
    
#Main Program
def main():
    pygame.init()
    size = [XScale, YScale]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Platformer')
    player = Player()
    #Level Import
    level_list = []
    level_list.append(Level_Test_1(player))
    level_list.append(Level_Test_2(player))
    current_level_no = 0
    current_level = level_list[current_level_no]
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    player.rect.x = 340
    player.rect.y = YScale - player.rect.height
    active_sprite_list.add(player)
    running = True
    clock = pygame.time.Clock()
    
    #Main Program
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            #Movement Key Presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
        
        active_sprite_list.update()
        current_level.update()
        
        #Move Map if close to sides
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)
            
        #Next Level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
                
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()
    
if __name__ == "__main__":
    main()

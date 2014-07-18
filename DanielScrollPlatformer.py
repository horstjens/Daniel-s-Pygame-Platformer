"""
Python3 Pygame Platform game
2014 by Daniel-Eichler

Based on Tutorials of:
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

supported by:
http://spielend-programmieren.at

"""
import pygame
import random

# Global constants

# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)



# Screen dimensions
SCREEN_WIDTH  = 1800
SCREEN_HEIGHT = 900

class Alien(pygame.sprite.Sprite):
    """
    This is an alien enemy
    """

    # -- Class Attributes
    images=[]
    try:
       images.append(pygame.image.load("alien100.bmp"))
    except:
       alienimage=pygame.Surface((60,60))
       alienimage.set_colorkey((0,0,0))
       pygame.draw.circle(alienimage,GREEN,(30,30),30,1)
       #alienimage.convert_alpha()
       images.append(alienimage)
       #alienimage.set_colorkey=((0,0,0))
    
  

    # -- Methods
    def __init__(self,x,y):
        """ Constructor function """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.boundary_top = 0
        self.boundary_bottom = SCREEN_HEIGHT
        self.boundary_left = 0
        self.boundary_right = 0
        self.change_x=0
        self.change_y=0
        self.image=Alien.images[0]
        self.rect=self.image.get_rect()
        self.rect.centerx=self.x
        self.rect.centery=self.y
        self.hitpoints=100
        self.hitpointsfull=100
        

      

       
        

    def update(self, seconds):
        pass
        
class Player(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player controls.
    """

    # -- Attributes
    # Set speed vector of player
    #change_x = 0
    #change_y = 0

    # List of sprites we can bump against
    #level = None

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60
        self.hitpointsfull=600.0
        self.hitpoints=600.0
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        self.moving_with_platform = False
        self.change_x = 0
        self.change_y = 0

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
        

    def update(self, seconds):
        """ Move the player. """
        
        if self.moving_with_platform:
            pass
        else: 
           self.calc_grav() # Gravity

           # Move left/right
           self.rect.x += self.change_x*seconds

           # See if we hit anything
           block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
           for block in block_hit_list:
                # If we are moving right,
                # set our right side to the left side of the item we hit
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                elif self.change_x < 0:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right

           # Move up/down
           self.rect.y += self.change_y*seconds

           # Check and see if we hit anything
           block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
           for block in block_hit_list:

                # Reset our position based on the top/bottom of the object.
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                    #lava? is the current block where the player stands on made out of lava?
                    if self.level.lava_list.has(block):
                        self.hitpoints-=50000*seconds # player looses one hitpoint
                    #spikes?  is the current block, where the player stands on made out of spikes?
                    if self.level.spike_list.has(block):
                        self.hitpoints-=90000*seconds
                    #teleporter? is the current block ,where the playre stands on made out of active teleporters???
                    if self.level.teleporter_list.has(block):
                        if block.target != None:
                            #beam player to target teleporter
                            self.rect.x= block.target.rect.x
                            self.rect.y =block.target.rect.y-120  # above the target teleporter
                    if self.level.moving_list.has(block):
                        self.rect.centerx = block.rect.centerx
                            
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom

                # Stop our vertical movement
                self.change_y = 0

           

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 25.35

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -1500

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -1400

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 1500

    def stop(self):
        """ Called when the user lets off the keyboard. """
        #if not self.moving_with_platform
        self.change_x = 0
        
        
class Lifebar(pygame.sprite.Sprite):
    """shows a bar with the hitpoints of player sprite
    """
    def __init__(self, boss):
            #self.groups = allgroup
            self.boss = boss
            #self._layer = self.boss._layer
            pygame.sprite.Sprite.__init__(self)
            self.oldpercent = 0
            self.paint()
            
            
    def paint(self):
            self.image = pygame.Surface((self.boss.rect.width,7))
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.rect(self.image, (0,255,0), (0,0,self.boss.rect.width,7),1)
            self.rect = self.image.get_rect()
            
    def update(self, time):
            self.percent = self.boss.hitpoints / self.boss.hitpointsfull * 1.0
            if self.percent != self.oldpercent:
                self.paint() # important ! boss.rect.width may have changed (because rotating)
                pygame.draw.rect(self.image, (0,0,0), (1,1,self.boss.rect.width-2,5)) # fill black
                pygame.draw.rect(self.image, (0,255,0), (1,1,
                                 int(self.boss.rect.width * self.percent),5),0) # fill green
            self.oldpercent = self.percent
            self.rect.centerx = self.boss.rect.centerx
            self.rect.centery = self.boss.rect.centery - self.boss.rect.height /2 - 10
            if self.boss.hitpoints < 1: #check if boss is still alive
                self.kill() # kill the hitbar

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.change_x = 0
        self.change_y = 0

        self.boundary_top = 0
        self.boundary_bottom = SCREEN_HEIGHT
        self.boundary_left = 0
        self.boundary_right = 0

        self.rect = self.image.get_rect()
        
class SpikePlatform(pygame.sprite.Sprite):
    """ Platform where the player dies """

    def __init__(self, width, height):
        """ Platform constructor.Spike's width must be >10
            """
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        for x in range(10,width,10):
             # line(Surface, color, start_pos, end_pos, width=1) -> Rect
             pygame.draw.line(self.image, BLACK, (x-10,height),(x-5,0), 3)
             pygame.draw.line(self.image, BLACK, (x-5,0),(x,height), 3)
            

        self.rect = self.image.get_rect()


class TeleporterPlatform(pygame.sprite.Sprite):
    """ Platform, which teleports the player to the target TeleporterPlatform """

    def __init__(self, width, height):
        """ Platform constructor.
            """
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
        self.green= 0
        self.deltagreen=1
        self.target=None

        self.rect = self.image.get_rect()
        
    def update(self, seconds):
        """ Paint the platform blue with color cycle. """
        self.image.fill((0,self.green,255))
        self.green+=self.deltagreen
        if self.green==200:
            self.deltagreen=-1
        if self.green==0:
            self.deltagreen=1

class LavaPlatform(Platform):
    """ Platform, which burns the player """

    def __init__(self, width, height):
        """ Platform constructor.
            """
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        
    def update(self, seconds):
        """ Paint the platform red. """
        self.image.fill((random.randint(128,255),0,0))


class MovingPlatform(Platform):
    """ This is a fancier platform that can actually move. """
    

    def update(self,seconds):
        """ Move the platform.
            If the player is in the way, it will shove the player
            out of the way. This does NOT handle what happens if a
            platform shoves a player into another object. Make sure
            moving platforms have clearance to push the player around
            or add code to handle what happens if they don't. """

        # Move left/right
        self.rect.x += self.change_x*seconds

        # See if we hit the player
        #hit = pygame.sprite.collide_rect(self, self.player)
        #self.player.travelplatform = False
        #if hit:
            #self.player.travelplatform = True
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # If we are moving right, set our right side
            # to the left side of the item we hit
        #    if self.change_x < 0:
                #self.player.rect.right = self.rect.left
                #self.player.rect.centerx = self.rect.centerx - self.change_x * seconds
        #        self.player.change_x = self.change_x
                
        #    else:
                # Otherwise if we are moving left, do the opposite.
                #self.player.rect.left = self.rect.right
                #self.player.rect.centerx = self.rect.centerx + self.cange_x * seconds
        #        self.player.change_x = self.change_x
      
      
        # Move up/down
        self.rect.y += self.change_y*seconds

        # Check and see if we hit the player
        #hit = pygame.sprite.collide_rect(self, self.player)
        #if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # Reset our position based on the top/bottom of the object.
        #    if self.change_y < 0:
        #        self.player.rect.bottom = self.rect.top
        #    else:
        #        self.player.rect.top = self.rect.bottom

        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom >= self.boundary_bottom:
            self.rect.bottom = self.boundary_bottom-1
            self.change_y *= -1
        
        if self.rect.top <= self.boundary_top:
            self.rect.top = self.boundary_top+1
            self.change_y *= -1
           
        # world shift
        cur_pos = self.rect.x - self.level.world_shift
        
        # left right boundary ?
        if cur_pos <= self.boundary_left:
            cur_pos = self.boundary_left
            self.change_x *= -1
        
        if cur_pos >= self.boundary_right:
            cur_pos = self.boundary_right
            self.change_x *= -1

class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    # Lists of sprites used in all levels. Add or remove
    # lists as needed for your game. """
    platform_list = None
    enemy_list = None

    # Background image
    background = None

    # How far this world has been scrolled left/right
    world_shift = 0
    level_limit = -1000

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.lava_list = pygame.sprite.Group()
        self.spike_list = pygame.sprite.Group()
        self.teleporter_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.moving_list = pygame.sprite.Group()
        self.alien_lilst  =pygame.sprite.Group()
        self.player = player

    # Update everythign on this level
    def update(self, seconds):
        """ Update everything in this level."""
        self.seconds = seconds
        self.platform_list.update(self.seconds)
        self.enemy_list.update(self.seconds)

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(WHITE)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything:
        """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -3000

        # Array with width, height, x, and y of platform
        level = [[210, 70, 500, 700],
                 [210, 70, 1000,600],
                 [210, 70, 1300, 450],
                 [70, 50, 270, 600],
                 [70, 50, 2060, 500],
                 [500, 50, 30, 480],
                 [240, 50, 2300, 530],
                 [240,50, 3200, 500],
                 [240, 50, 3850, 100],
                 ] 

        self.alien_list=[]
        a1=Alien(100, 100)
        self.alien_list.append(a1)
        self.platform_list.add(a1)
        
         # Add a up, down moving platform
        block = MovingPlatform(70, 70)
        block.rect.x = 360#3600
        block.rect.y = 200
        block.boundary_top = 10
        block.boundary_bottom = 550
        block.change_y = -500
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
        
        
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
            
        #Now we add the Ground LavaPlatform :D
        block= LavaPlatform(400, 50)
        block.rect.x = 50
        block.rect.y = 800
        block.player = self.player
        self.platform_list.add(block)
        self.lava_list.add(block)
        
        #Now we add the 2nd Ground LavaPlatform :D
        block= LavaPlatform(40, 50)
        block.rect.x = 2900
        block.rect.y = 600
        block.player = self.player
        self.platform_list.add(block)
        self.lava_list.add(block)
       
        
        #Now we add the SpikePlatform :D
        block= SpikePlatform(4330,50)
        block.rect.x = 0
        block.rect.y =SCREEN_HEIGHT-50
        block.player = self.player
        self.platform_list.add(block)
        self.spike_list.add(block)
        
        #Now we add the 1st active TeleporterPlatform :D
        tele1= TeleporterPlatform(100, 70)
        tele1.rect.x = 30
        tele1.rect.y = 600
        tele1.player = self.player
        self.platform_list.add(tele1)
        self.teleporter_list.add(tele1)
        
        #Now we add the 1st passive TeleporterPlatform :D
        tele2= TeleporterPlatform(100, 70)
        tele2.rect.x = 1400
        tele2.rect.y = 100
        tele2.player = self.player
        self.platform_list.add(tele2)
        self.teleporter_list.add(tele2)
        
        #Connect Teleporters
        tele1.target=tele2
        #tele2.target=tele1

        # Add a left, right moving platform
        #block = MovingPlatform(70, 40)
       # block.rect.x = 1600
        #block.rect.y = 500
       # block.boundary_left = 1000
        #block.boundary_right = 2000
       # block.change_x = 700
        #block.player = self.player
        #block.level = self
       # self.platform_list.add(block)
       # self.moving_list.add(block)


# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1000

        # Array with type of platform, and x, y location of the platform.
        level = [[210, 70, 500, 790],
                 [210, 70, 800, 700],
                 [210, 70, 1000, 600],
                 [210, 70, 1120, 500],]
                 


        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = MovingPlatform(70, 70)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

class Level_03(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1000

        # Array with type of platform, and x, y location of the platform.
        level = [[210, 70, 700, 890],
                 [210, 70, 600, 730],
                 [210, 70, 900, 625],
                 [210, 70, 1020, 540],]
                 


        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = MovingPlatform(70, 70)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
        
        # Add a custom moving platform
        block = MovingPlatform(70, 70)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)








def main():
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Platformer with moving platforms")

    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
    level_list.append(Level_03(player))
    
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height-500
    active_sprite_list.add(player)
    lifebar1=Lifebar (player)
    active_sprite_list.add(lifebar1)
    #Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    playtime = 0.00000
    FPS= 1000
    # -------- Main Program Loop -----------
    while not done:
        milliseconds = clock.tick(FPS) # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
        playtime += seconds
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

            #if event.type == pygame.KEYDOWN:
            #    if event.key == pygame.K_LEFT:
            #        player.go_left()
            #    if event.key == pygame.K_RIGHT:
            #        player.go_right()
            #    if event.key == pygame.K_UP:
            #        player.jump()

            #if event.type == pygame.KEYUP:
            #    if event.key == pygame.K_LEFT and player.change_x < 0:
            #        player.stop()
            #    if event.key == pygame.K_RIGHT and player.change_x > 0:
            #        player.stop()
            
        # player movement ( CONTROLLER )
        # check if key is pressed at this moment
        pressedkeys = pygame.key.get_pressed()
        
        player.stop() 
        if pressedkeys[pygame.K_LEFT]:
             player.go_left()
        
        if pressedkeys[pygame.K_RIGHT]:
             player.go_right()
        
        if pressedkeys[pygame.K_UP]:
             player.jump()  

        # Update the player.
        active_sprite_list.update(seconds)
       
        # Update items in the level
        current_level.update(seconds)
        #update aliens
        for enemy in current_level.alien_list:
            
            enemy.update(seconds)

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)
            
        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            if current_level_no < len(level_list)-1:
                player.rect.x = 120
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
            else:
                # Out of levels. This just exits the program.
                # You'll want to do something better.
                done = True
        
        #check if player is alive
        if player.hitpoints<1:
            done=True
        
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        pygame.display.set_caption("player1.hitpoints {} FPS: {:.2f}".format(player.hitpoints, clock.get_fps()))

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

if __name__ == "__main__":
    main()

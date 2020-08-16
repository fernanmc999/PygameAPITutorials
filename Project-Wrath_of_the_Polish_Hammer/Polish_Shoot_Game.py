import pygame
import sys

class Missile:
    def __init__(self, screen, x, y):
        # Store the data.  Initialize:   y to 591   and   has_exploded to False.
        self.screen=screen
        self.x=x
        self.y=y
        self.has_exploded=False

    def move(self):
        # Make self.y 5 smaller than it was (which will cause the Missile to move UP).
        self.y-=10
        pass

    def draw(self):
        # Draw a vertical, 4 pixels thick, 8 pixels long, red (or green) line on the screen,
        # where the line starts at the current position of this Missile.
        pygame.draw.line(self.screen, (0,255,255), (self.x,self.y), (self.x, self.y+8), 4)


class Fighter:
    def __init__(self, screen, x, y):
        self.screen=screen
        self.x=x
        self.y=y
        self.image=pygame.image.load("fighter.png")
        self.image.set_colorkey((255,255,255))
        self.missiles=[]
        self.fire_sound=pygame.mixer.Sound("pew.wav")
        self.health=5
        self.died=False
        pass

    def draw(self):
        # Draw this Fighter, using its image at its current (x, y) position.
        self.screen.blit(self.image, (self.x,self.y))
        # API --> pygame.draw.rect(screen, (r,g,b), (x, y, width, height), thickness)
        pygame.draw.rect(self.screen, (255, 0, 0), (10, 600, 100, 30))
        pygame.draw.rect(self.screen, (124, 252, 0), (10, 600, 100 - (20 * (5 - self.health)), 30))
        pass

    def fire(self):
        # Construct a new Missile 50 pixels to the right of this Fighter.
        # Append that Missile to this Fighter's list of Missile objects.
        new_Missile=Missile(self.screen, self.x+self.image.get_width()//2,
                            self.screen.get_height()-self.image.get_height()+1)
        self.missiles.append(new_Missile)
        self.fire_sound.play()

    def remove_exploded_missiles(self):
        # Already complete
        for k in range(len(self.missiles) - 1, -1, -1):
            if self.missiles[k].has_exploded or self.missiles[k].y < 0:
                del self.missiles[k]

    def wound(self, lasers):
        hitbox = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        return hitbox.collidepoint(lasers.x, lasers.y)


class Badguy:
    def __init__(self, screen, x, y, speed):
        self.screen=screen
        self.x=x
        self.original_x=x
        self.y=y+200
        self.speed=speed
        self.is_dead= False
        self.image=pygame.image.load("badguy.png")

    def move(self):
        # Move 2 units in the current direction.
        # Switch direction if this Badguy's position is more than 100 pixels from its original position.
        self.x += self.speed
        if abs(self.x-self.original_x) > 100:
            self.speed = -self.speed

    def draw(self):
        # Draw this Badguy, using its image at its current (x, y) position.
        self.screen.blit(self.image, (self.x,self.y))

    def hit_by(self, missile):
        # Make a Badguy hitbox rect.
        # Return True if that hitbox collides with the xy point of the given missile.
        hitbox=pygame.Rect(self.x,self.y,self.image.get_width(),self.image.get_height())
        return hitbox.collidepoint(missile.x,missile.y)

class EnemyFleet:
    def __init__(self, screen, enemy_rows):
        # Already done.  Prepares the list of Badguys.
        self.badguys = []
        self.explosion_sound=pygame.mixer.Sound("explosion.wav")
        self.sound=pygame.mixer.Sound("idied.wav")
        for j in range(enemy_rows):
            for k in range(13):
                self.badguys.append(Badguy(screen, 80 * k, 55 * j + 20, enemy_rows))

    @property
    def is_defeated(self):
        # Return True if the number of badguys in this Enemy Fleet is 0,
        # otherwise return False.
        return len(self.badguys)==0

    def move(self):
        # Make each badguy in this EnemyFleet move.
        for badguy in self.badguys:
            badguy.move()

    def draw(self):
        # Make each badguy in this EnemyFleet draw itself.
        for badguy in self.badguys:
            badguy.draw()

    def remove_dead_badguys(self):
        for k in range(len(self.badguys) - 1, -1, -1):
            if self.badguys[k].is_dead:
                del self.badguys[k]
                self.sound.play()
                self.explosion_sound.play()

class Scoreboard:

    def __init__(self, screen):
        self.screen = screen
        self.score=0
        self.font=pygame.font.Font(None,30)

    def draw(self):
        score_string="Score:"+str(self.score)
        score_image=self.font.render(score_string, True, (255,255,255))
        self.screen.blit(score_image, (5,5))

class Mothership:
    def __init__(self, screen, x, y):
        self.screen=screen
        self.x=x
        self.original_x=x
        self.y=y
        self.image=pygame.image.load("MotherShip.jpg")
        self.speed=8
        self.health=100
        self.death=False
        self.lasers=[]
        self.automation=0
        self.fire_sound=pygame.mixer.Sound("pew.wav")
        pass

    def draw(self):
        # Draw this ship, using its image at its current (x, y) position.
        image1 = pygame.transform.scale(self.image, (500,150))
        self.screen.blit(image1, (self.x,self.y))
        # API --> pygame.draw.rect(screen, (r,g,b), (x, y, width, height), thickness)
        pygame.draw.rect(self.screen, (255, 0, 0), (350, 10, 400,30))
        pygame.draw.rect(self.screen, (124, 252, 0), (350, 10, 400-(4*(100-self.health)), 30))
        pass

    def move(self):
        self.x = self.x+self.speed
        if abs(self.x-self.original_x) > 400:
            self.speed = -self.speed

    def hit(self, missile):
        # Make a hitbox rect.
        # Return True if that hitbox collides with the xy point of the given missile.
        hitbox=pygame.Rect(self.x,self.y,self.image.get_width(),self.image.get_height())
        return hitbox.collidepoint(missile.x,missile.y)

    def charge(self):
        # Construct a new Missile 50 pixels to the right of this Fighter.
        # Append that Missile to this Fighter's list of Missile objects.
        image1 = pygame.transform.scale(self.image, (500, 150))
        new_Laser=Laser(self.screen, self.x+image1.get_width()//2,
                            image1.get_height()+1)
        self.lasers.append(new_Laser)
        self.fire_sound.play()

    def remove_exploded_laser(self):
        # Already complete
        for k in range(len(self.lasers) - 1, -1, -1):
            if self.lasers[k].has_exploded or self.lasers[k].y > 650:
                del self.lasers[k]

    def automated_laser(self):
        self.automation+=1
        if self.automation==60:
            self.charge()
            self.automation=0

class Laser:
    def __init__(self, screen, x, y):
        # Store the data.  Initialize:   y to 591   and   has_exploded to False.
        self.screen=screen
        self.x=x
        self.y=y
        self.has_exploded=False

    def move(self):
        # Make self.y 5 smaller than it was (which will cause the Missile to move UP).
        self.y+=10
        pass

    def draw(self):
        # Draw a vertical, 10 pixels thick, 20 pixels long, red (or green) line on the screen,
        # where the line starts at the current position of this Missile.
        pygame.draw.line(self.screen, (124,252,0), (self.x,self.y), (self.x, self.y+100), 30)

def main():
    pygame.init()
    pygame.display.set_caption("Polish Hammer")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1000, 650))

    enemy_rows=6
    enemy_fleet= EnemyFleet(screen,enemy_rows)
    fighter = Fighter(screen, 400, screen.get_height() - 60)
    ship=Mothership(screen,200,20)
    scoreboard = Scoreboard(screen)
    Not_Yet = pygame.mixer.Sound("lose.wav")
    ship_hit=pygame.mixer.Sound("damage.wav")
    fighter_hit=pygame.mixer.Sound("expl06.wav")
    is_game_over=False
    game_over_image=pygame.image.load("Polish_Hammered.jpeg")
    victory_sound=pygame.mixer.Sound("battle explosion.wav")
    victory_image=pygame.image.load("Super Victory.jpeg")
    heat_death=pygame.mixer.Sound("aaa.wav")

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()
            # DONE 5: If the event type is KEYDOWN and pressed_keys[pygame.K_SPACE] is True, then fire a missile
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_SPACE]:
                fighter.fire()
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0, 0, 0))
        ship.draw()
        scoreboard.draw()
        if is_game_over:
            image1 = pygame.transform.scale(game_over_image, (1000, 650))
            screen.blit(image1, (0,0))
            pygame.display.update()
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_e]:
                main()
            continue

        pressed_keys=pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT] and fighter.x > -fighter.image.get_width() / 2:
            fighter.x -= 5
        if pressed_keys[pygame.K_RIGHT] and fighter.x < screen.get_width() - fighter.image.get_width() / 2:
            fighter.x += 5

        fighter.draw()
        enemy_fleet.draw()

        enemy_fleet.move()
        ship.move()
        ship.automated_laser()
        for laser in ship.lasers:
            laser.move()
            laser.draw()
        for missile in fighter.missiles:
            missile.move()
            missile.draw()
        for badguy in enemy_fleet.badguys:
            for missile in fighter.missiles:
                if badguy.hit_by(missile):
                    scoreboard.score += 100
                    badguy.is_dead=True
                    missile.has_exploded=True
        for missile in fighter.missiles:
            if ship.hit(missile):
                if ship.health>0:
                    scoreboard.score+=500
                    ship.health-=1
                    ship_hit.play()
                    missile.has_exploded=True
                else:
                    ship.death=True
                    missile.has_exploded=True
        if ship.death==True:
            victory_sound.play()
            image1 = pygame.transform.scale(victory_image, (1000, 650))
            screen.blit(image1, (0, 0))
            pygame.display.update()
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_e]:
                main()
            continue
        for laser in ship.lasers:
            if fighter.wound(laser):
                if fighter.health>0:
                    scoreboard.score-=100
                    fighter.health-=1
                    fighter_hit.play()
                    laser.has_exploded=True
                else:
                    fighter.died=True
                    laser.has_exploded=True
        if fighter.died==True:
            heat_death.play()
            image1 = pygame.transform.scale(game_over_image, (1000, 650))
            screen.blit(image1, (0, 0))
            pygame.display.update()
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_e]:
                main()
            continue
        fighter.remove_exploded_missiles()
        enemy_fleet.remove_dead_badguys()
        ship.remove_exploded_laser()
        if enemy_fleet.is_defeated:
            Not_Yet.play()
            enemy_rows+=1
            enemy_fleet=EnemyFleet(screen,enemy_rows)

        for badguy in enemy_fleet.badguys:
            if badguy.y>screen.get_height()-fighter.image.get_height()-badguy.image.get_height():
                is_game_over=True
        pygame.display.update()
# main()
def start():
    pygame.init()
    pygame.display.set_caption("Let's Save the World!")
    screen = pygame.display.set_mode((1000, 650))
    Beginning_Image=pygame.image.load("Beginning.jpeg")
    while True:
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()
            print(event)  # Used for an example here
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_e]:
                main()
                pass
            # Additional interactions

        # Draw things on the screen
        screen.fill((0,0,0))
        initiation = pygame.transform.scale(Beginning_Image, (1000, 650))
        screen.blit(initiation, (0, 0))
        pygame.display.update()

start()
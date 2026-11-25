
from pygame import *
from random import *

#load functions for working w fonts separately
font.init()
game_font = font.Font(None, 36)

#step 1: prepare music
mixer.init()
mixer.music.load('back_music.ogg')
mixer.music.set_volume(1)
mixer.music.play(-1)

destroy_effect = mixer.Sound('destroy_sound.ogg')

#step 2: prepare window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
FPS = 60

#enemy spawn settings
spawn_counter = 0
spawn_delay = randint(30, 60)
MAX_ENEMIES = 6
score = 0

#zombie progression system
zombie_level = 1 #current zombie lvl (1, 2 or 3)
zombies_killed = 0 #track total zombies killed
ZOMBIES_PER_LEVEL = 10 #zombies needed to advance to next level

#step 3: prepare imgs
img_back = transform.scale(image.load('map1.png'), (win_width, win_height))
img_pistol = transform.scale(image.load('gun1.png'), (50, 70))
img_bazooka = transform.scale(image.load('gun2.png'), (50, 70))
img_minigun = transform.scale(image.load('gun3.png'), (50, 70))
img_zombie1 = transform.scale(image.load('zombie1.png'), (50, 50))
img_zombie2 = transform.scale(image.load('zombie2.png'), (50, 50))
img_zombie3 = transform.scale(image.load('zombie3.png'), (50, 50))
img_bullet = transform.scale(image.load('bullet.png'), (15, 20))

#step 4: create classes
class Healthbar:
    def __init__(self, x, y, width, height, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.background_color = (128, 128, 128) #gray
        self.health_color = (255, 0, 0) #red
        self.current_health = max_health

    def draw(self, surface):
        draw.rect(surface, self.background_color, (self.x, self.y, self.width, self.height))
        current_health_width = (self.current_health / self.max_health) * self.width
        draw.rect(surface, self.health_color, (self.x, self.y, current_health_width, self.height))

    def decrease_health(self, amount=1):
        self.current_health = max(0, self.current_health - amount)
        return self.current_health <= 0

    def reset(self):
        self.current_health = self.max_health


def draw_gui():
    #score display
    score_text = game_font.render("Score: " + str(score), True, (255, 255, 255)) #create the text
    score_rect = score_text.get_rect()
    score_rect.topright = (win_width - 10, 10)
    window.blit(score_text, score_rect)

    #weapon display
    weapon_text = game_font.render("Weapon: " + player.current_weapon, True, (255, 255, 255))
    window.blit(weapon_text, (10, 10))

    #zombie lvl display
    level_text = game_font.render("Level: " + str(zombie_level), True, (255, 255, 255))
    window.blit(level_text, (10, 50))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self) #inheritance
        self.speed = player_speed
        self.image = player_image

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y)) #put the sprite at the beginning


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.shift_x = -8
        self.shift_y = -5 #let the bullet know where to go
        self.bullet_speed = -10
        self.reload_time = 30 #0.5s
        self.reload_counter = 0
        self.current_weapon = 'pistol'
        self.weapon_damage = 1

    def update(self): #set the movement
        keys = key.get_pressed() #logs

        if keys[K_a] and self.rect.x > 5: #make sure the sprite doesn't go out of the window
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 50:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 75:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 70:
            self.rect.y += self.speed

        #change the weapon
        if keys[K_1]:
            self.image = img_pistol
            self.shift_x = -8
            self.shift_y = -5 #let the bullet know where to go
            self.bullet_speed = -10
            self.reload_time = 30 #0.5s
            self.current_weapon = 'pistol'
            self.weapon_damage = 1

        elif keys[K_2]:
            self.image = img_bazooka
            self.shift_x = -22
            self.shift_y = -15 #let the bullet know where to go
            self.bullet_speed = -5
            self.reload_time = 60 #1s
            self.current_weapon = 'bazooka'
            self.weapon_damage = 3

        elif keys[K_3]:
            self.image = img_minigun
            self.shift_x = -13
            self.shift_y = -11 #let the bullet know where to go
            self.bullet_speed = -8
            self.reload_time = 15 #0.25s
            self.current_weapon = 'minigun'
            self.weapon_damage = 1

        if self.reload_counter > 0:
            self.reload_counter -= 1

    def fire(self):
        if self.reload_counter <= 0: #only fire if reload
            bullet = Bullet(img_bullet, self.rect.x + self.shift_x, self.rect.top + self.shift_y, 15, 20, self.bullet_speed)
            bullets.add(bullet)
            self.reload_counter = self.reload_time #reset the counter for next shoot


class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, zombie_type=1):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.zombie_type = zombie_type
        self.health = zombie_type

    def update(self):
        self.rect.y += self.speed #upd the position

        if self.rect.y > win_height:
            self.rect.x = randint(40, win_width - 50)
            self.rect.y = 0 #spawn the enemy to the top

    def take_damage(self):
        self.health -= 1
        return self.health <= 0


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed #the speed is negative
        if self.rect.y <= 0:
            self.kill()


#step 5: create objects
player = Player(img_pistol, 350, 400, 50, 70, 8)
health_bar = Healthbar(100, 475, 500, 20, 10)

monsters = sprite.Group()
bullets = sprite.Group()

finish = False

clock = time.Clock()
run = True

#step 6: game loop

while run:
    for e in event.get():
        if e.type == QUIT: #when the user click the quit button
            run = False #stop the game loop
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not finish:
                player.fire()

    if not finish:
        window.blit(img_back, (0, 0)) #make the background appear
        player.update()
        player.reset()
        health_bar.draw(window) #draw the healthbar
        bullets.draw(window)
        bullets.update()

        spawn_counter += 1
        if spawn_counter >= spawn_delay and len(monsters) < MAX_ENEMIES:
            if zombies_killed >= ZOMBIES_PER_LEVEL and zombie_level < 3:
                zombie_level += 1
                zombies_killed = 0 #make sure can not skip levels

            if zombie_level == 1:
                zombie_type = 1
                zombie_img = img_zombie1

            elif zombie_level == 2:
                if randint(1, 10) <= 7: #70% chance
                    zombie_type = 2
                    zombie_img = img_zombie2
                else: #30% chance
                    zombie_type = 1
                    zombie_img = img_zombie1

            else:
                rand = randint(1, 10)
                if rand <= 5:
                    zombie_type = 3
                    zombie_img = img_zombie3
                elif rand <= 8:
                    zombie_type = 2
                    zombie_img = img_zombie2
                else:
                    zombie_type = 1
                    zombie_img = img_zombie1

            monster = Enemy(zombie_img, randint(40, win_width - 50), -30, 50, 50, randint(1, 2), zombie_type)
            monsters.add(monster) #use the monsters list to know how many enemies are on the screen
            spawn_counter = 0
            spawn_delay = randint(30, 60)

        monsters.draw(window)
        monsters.update()

        for monster in list(monsters):
            if monster.rect.bottom >= win_height - 40:
                if health_bar.decrease_health(): #if health decrease to 0 or less
                    finish = True

                monster.kill()

        #check collision bullet - monster
        for bullet in list(bullets):
            for monster in list(monsters):
                if sprite.collide_rect(bullet, monster):
                    bullet.kill()
                    monster.health -= player.weapon_damage

                    if monster.health <= 0: #check when the zombie die
                        destroy_effect.play()
                        monster.kill()
                        zombies_killed += 1
                        score += monster.zombie_type #upd score by zombie type

                    break

        #check collision player - monster
        for monster in list(monsters):
            if sprite.collide_rect(player, monster):
                player.rect.x = 350
                player.rect.y = 400 #respawn player
                monster.kill()

                if health_bar.decrease_health():
                    finish = True

        draw_gui()

    #draw game over screen when player loses
    if finish:
        window.fill((255, 255, 255)) #white bg

        #draw 'YOU LOSE' text
        lose_text = game_font.render("YOU LOSE", True, (0, 0, 255)) #text color
        lose_rect = lose_text.get_rect()
        lose_rect.center = (win_width // 2, win_height // 2)
        window.blit(lose_text, lose_rect)

        #draw final score
        final_score_text = game_font.render("Final score: " + str(score), True, (0, 0, 255)) #text color
        final_score_rect = final_score_text.get_rect()
        final_score_rect.center = (win_width // 2, win_height // 2 + 50)
        window.blit(final_score_text, final_score_rect)

    display.update()
    clock.tick(FPS)

mixer.music.stop()
quit()

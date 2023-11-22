from pygame import *

class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
           self.rect.x -= self.speed
        if keys[K_UP]:
            self.rect.y -= self.speed
        if keys[K_DOWN]:
            self.rect.y += self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed

class Enemy(GameSprite):
    def update(self):
        if self.rect.x >= win_width - 85:
            self.direction = 'left'
        if self.rect.x <= 470:
            self.direction = "right"
        if self.direction == 'right':
            self.rect.x += self.speed
        if self.direction == 'left':
            self.rect.x -= self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height ):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.y = wall_y
        self.rect.x = wall_x
    def  draw_wall(self):
        window.blit(self.image,(self.rect.x, self.rect.y))


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Maze')
background = transform.scale(image.load("background.jpg"), (win_width, win_height))

player = Player('hero.png', 5, win_height - 80, 4)
monster = Enemy('cyborg.png', win_width - 80, 280, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)
w1 = Wall(154, 205, 50, 100, 20, 450, 10)

FPS=60
font.init()
font = font.Font(None, 70)
win = font.render(
    'YOU WIN', True, (255, 215, 0)
)
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
kick=mixer.Sound("kick.ogg")
money=mixer.Sound("money.ogg")
game = True
finish = False
clock = time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        if sprite.collide_rect(player, final):
            window.blit(win, (200, 200))
            finish = True
            money.play()
        if sprite.collide_rect(player, monster) or sprite.collide_rect(player, final):
            finish = True
            kick.play()

        window.blit(background, (0, 0)) 
        player.update()
        w1.draw_wall()
        monster.update()
        player.reset()
        monster.reset()
        final.reset()
    display.update()    
    clock.tick(FPS) 



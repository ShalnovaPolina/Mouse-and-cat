from pygame import*
from time import perf_counter

class GameSprite(sprite.Sprite):
    def __init__(self,image_path, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(image_path), (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def show(self):
        window.blit(self.image, (self.rect.x,self.rect.y))
    def restart(self,x,y):
        self.rect.x = x
        self.rect.y = y
        self.show()

class Player(GameSprite):
    def __init__(self, image_path, w, h, x, y, speed):
        super().__init__(image_path, w, h, x, y)
        self.speed = speed
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if key_pressed[K_DOWN] and self.rect.y < 900:
            self.rect.y += self.speed
        if key_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < 1500:
            self.rect.x += self.speed
    
class Enemy(GameSprite):
    def __init__(self, image_path, w, h, x, y, speed, path):
        super().__init__(image_path, w, h, x, y)
        self.speed = speed
        self.path = path
    def do_left(self):
        self.rect.x -= self.speed
    def do_right(self):
        self.rect.x += self.speed
    def do_up(self):
        self.rect.y -= self.speed
    def do_down(self):
        self.rect.y += self.speed
    def cat_way(self):
        if cat.rect.x > 1000 and cat.rect.y == 750 and self.path == 1:
            cat.do_left()
        elif cat.rect.x == 1000 and cat.rect.y > 600 and self.path == 1:
            cat.do_up()
        elif cat.rect.x < 1330 and cat.rect.y == 600 and self.path == 1:
            cat.do_right()
        elif cat.rect.x == 1330 and cat.rect.y > 450 and self.path == 1:
            cat.do_up()
        elif cat.rect.x > 1000 and cat.rect.y == 450 and self.path == 1:
            cat.do_left()
            if cat.rect.x == 1000:
                self.path = 2
        if cat.rect.x >= 1000  and cat.rect.y == 450 and self.path == 2:
            cat.do_right()
        if cat.rect.x == 1330 and cat.rect.y <= 600 and cat.rect.y >=450 and self.path == 2:
            cat.do_down()
        if cat.rect.x >= 1000 and cat.rect.y == 600 and self.path == 2:
            cat.do_left()
        if cat.rect.x == 1000 and cat.rect.y <= 750 and cat.rect.y >=600 and self.path == 2:
            cat.do_down()
        if cat.rect.x >= 1000 and cat.rect.y == 750 and self.path == 2:
            cat.do_right()
            if cat.rect.x == 1330:
                self.path = 1
        
class Wall(sprite.Sprite):
    def __init__(self,width,height,x,y,color):
        super().__init__()
        self.color = color
        self.w = width
        self.h = height
        self.image = Surface((self.w,self.h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

init()
mixer.init()
mixer.music.load('music_game.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.1)

window = display.set_mode((1600, 1000))
display.set_caption('Догонялки')
background = GameSprite('background.png', 1600,1000,0,0)
mouse = Player('mouse.png', 120,95,125,100, 5)
cat = Enemy('cat.png', 140,100,1330, 750, 10, 1)
cheese = GameSprite('cheese.png', 100,100,1200,870)
#препятствия
RED = (168,84,0)
wall_1= Wall(20, 1000, 100,0, RED )
wall_2 = Wall(20, 850, 300, 0, RED)
wall_3 = Wall(20, 850, 500, 150, RED)
wall_4 = Wall(20, 850, 700, 0, RED)
wall_5 = Wall(20, 850, 950, 150, RED)
wall_6 = Wall(400,20, 950,150, RED)
wall_7 = Wall(20,1000,1500,0, RED)
wall_8 = Wall(1400,20,100,0, RED)
wall_9 = Wall(1400,20,100,980, RED)

text = ''
cat_win = ''
mouse_win = ''
cat_way = True
seconds = 60


clock = time.Clock()

game = True
start = int(perf_counter())
while game:
    background.show()
    if cat_way:
        wall_1.draw_wall()
        wall_2.draw_wall()
        wall_3.draw_wall()
        wall_4.draw_wall()
        wall_5.draw_wall()
        wall_6.draw_wall()
        wall_7.draw_wall()
        wall_8.draw_wall()
        wall_9.draw_wall()
    cheese.show()
    mouse.show()
    cat.show()
    
    win_text = font.SysFont('verdana', 68).render(text, True, (0,0,0))
    window.blit(win_text, (500,400))
    
    for ev in event.get(): #перебираем все события из списка event.get() там записываются все события клавиш
        if ev.type == QUIT: #если событие - нажатие на крестик
            game = False
    if seconds != -1:            
        mouse.update()
    # касания
    if mouse.rect.colliderect(cat.rect) or mouse.rect.colliderect(wall_1.rect) or mouse.rect.colliderect(wall_2.rect) or mouse.rect.colliderect(wall_3.rect) or mouse.rect.colliderect(wall_4.rect) or mouse.rect.colliderect(wall_5.rect) or mouse.rect.colliderect(wall_6.rect) or mouse.rect.colliderect(wall_7.rect) or mouse.rect.colliderect(wall_8.rect) or mouse.rect.colliderect(wall_9.rect):
        cat_win = 'win'
    if mouse.rect.colliderect(cheese.rect):
        mouse_win = 'win'
        music_mouse_cheese = mixer.Sound('music_mouse_sheese.mp3')
        music_mouse_cheese.play()
    #движение кота

    if cat_way:

        cat.cat_way()

    end = int(perf_counter())  
    if (end - start) > 0 and (seconds-(end-start)) >= 0 and cat_win != 'win':
        seconds_text = font.SysFont('verdana', 45).render(str(seconds-(end-start)), True, (0,0,0))
        window.blit(seconds_text, (20,20))
    if (seconds-(end-start)) <= 0 and seconds!= -1:
        cat_win = 'win' 

    if cat_win == 'win' and mouse_win == '':
        text = 'кошка победила'
        music_cat_win = mixer.Sound('music_cat_win.mp3')
        music_cat_win.play()
        cat_win = ''
        seconds = -1
        cat.restart(620,600)
        mouse.restart(830,600)
        cat_way= False
        
    if mouse_win == 'win' and cat_win == '':
        text = 'мышка победила'
        music_mouse_win = mixer.Sound('music_mouse_win.mp3')
        music_mouse_win.play()
        mouse_win = ''
        seconds = -1
        cat.restart(620,600)
        mouse.restart(830,600)
        cat_way= False

    display.update()
    clock.tick(60)
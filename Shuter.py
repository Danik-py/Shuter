from pygame import *
from random import randint

window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
clock = time.Clock()

mixer.init()
mixer.music.load('Sbornik_-_Kosmicheskaya_muzyka_77037474.mp3')
mixer.music.play()
mixer.music.set_volume(0.1)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed =key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 615:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15, 15, 20)
        bullets.add(bullet)
lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(100, 600)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
    
#groupcollide = метот который проверяет столкновение у групп спрайтов@       
#collides = список в котором хранятся спрайты которых коснулись между собой
#blit = отображает элементы
#rect = хитбокс == часть спрайта отвечающая за логику(перемещение, касание)
#update = изменения( работа перемещения моего спрайта)
#reset = отвечает за отрисовку на экране
#локальные = внутри функции
#глобальные = вне функции
#score = счётчик
#finish = игра пройдена или не пройдена
#game = не закрыли окно игры 
#Подписка на события = это запрос программы какое событие для неё важно
#Чтобы создать исполняемый файл нужно в терминале написать команду == pyinstaller --onefile название файла.py

finish = False
bullets = sprite.Group()


font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 70)
win_text = font2.render('Ты выиграл!!!', True, (0, 255, 0))
lose_text = font2.render('Ты проиграл!', True, (255, 0, 0))


score = 0

game = True
hero = Player('rocket (1).png', 250, 400, 10, 75, 90)
monsters = sprite.Group()
for i in range (5):
    monster = Enemy('ufo.png', randint(100, 600), -20, randint(1, 3), 90, 75)
    monsters.add(monster)

while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        if i.type == KEYDOWN:
            if i.key == K_SPACE:
                hero.fire()
    if finish != True:
        window.blit(background,(0,0))
        hero.update()
        monsters.update()
        hero.reset()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        text_lose = font1.render('Пропущено: ' + str(lost), True, (255, 255, 255)) 
        text_score = font1.render('Счет: ' + str(score), True, (255, 255, 255))
        window.blit(text_score, (10, 20))
        window.blit(text_lose, (10, 50))
        if sprite.spritecollide(hero, monsters, False) or lost >= 5:
            finish = True
            window.blit(lose_text, (200, 200))
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for i in collides:
            score += 1
            monster = Enemy('ufo.png', randint(100, 600), -20, randint(1, 3), 90, 75)
            monsters.add(monster)
        if score >= 10:
            finish = True
            window.blit(win_text, (200, 200))
   
    display.update()
    clock.tick(60)
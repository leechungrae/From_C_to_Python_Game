#-*- coding:utf-8 -*-
import pygame, random
import function

#----------------------------------## 게임 기본 설정 관련 ##---------------------------------------
pygame.init()

#게임 전체 스크린 사이즈
global widthSize, heightSize, imageSize
widthSize= 500
heightSize = 400
imageSize = 30

Enemycount = 9  #적군 숫자

#게임 스크린 사이즈와 게임 제목 설정
game_screen = pygame.display.set_mode((widthSize,heightSize))
pygame.display.set_caption("test")

#오디오 출력용
pygame.mixer.music.load('sound/ponyo.wav')
pygame.mixer.music.play(0)

#----------------------------------## 클래스 정 ##---------------------------------------
class Enemy:
    def __init__(self, screen, ex, ey, tx, ty):
        self.screen = screen
        self.x = ex
        self.y = ey
        self.vx = tx - ex
        self.vy = ty - ey
        self.check = False
        self.mImage = pygame.image.load("picture/enemy1.png")
        self.mImage = pygame.transform.scale(self.mImage, (30, 30))
        self.mVector = pygame.math.Vector2(self.vx, self.vy)
        self.mVector = pygame.math.Vector2.normalize(self.mVector)
    
    def update(self):
        self.x += self.mVector[0]
        self.y += self.mVector[1]
        
        if self.y < 0 or self.y > heightSize - imageSize:
            self.vy = -self.vy
        if self.x < 0 or self.x > widthSize - imageSize:
            self.vx = -self.vx
        
        self.mVector = pygame.math.Vector2(self.vx, self.vy)
        self.mVector = pygame.math.Vector2.normalize(self.mVector)
    
    def crush(self, cx, cy):
        if self.x+3 < cx + imageSize and self.x+3 > cx - imageSize:
            if self.y+3 < cy + imageSize and self.y+3 > cy - imageSize:
                self.check = True

def draw(self):  #나중에 부모클래스 하나 만들어서 상속받아도 될듯
    self.update()
        
        mRect = self.mImage.get_rect()
        mRect = mRect.fit((self.x, self.y, 50, 50))
        self.screen.blit(self.mImage, mRect)

class Missile:
    def __init__(self, screen, cx, cy, tx, ty):
        self.screen = screen
        self.x = cx + 10
        self.y = cy + 10
        self.vx = tx - cx
        self.vy = ty - cy
        self.check = False
        self.mImage = pygame.image.load("picture/coin.png")
        self.mImage = pygame.transform.scale(self.mImage, (10, 10))
        self.mVector = pygame.math.Vector2(self.vx, self.vy)
        self.mVector = pygame.math.Vector2.normalize(self.mVector)
    
    def update(self):
        global widthSize, heightSize
        self.x += self.mVector[0]
        self.y += self.mVector[1]
        if self.x < 0 or self.y < 0:
            self.check = True
        if self.x > widthSize or self.y > heightSize:
            self.check = True

def draw(self):
    self.update()
        mRect = self.mImage.get_rect()
        mRect = mRect.fit((self.x, self.y, 50, 50))
        self.screen.blit(self.mImage, mRect)

#-----------------------------------## 게임 사용 변수 ##---------------------------------------
#키보드 이동용 전역변수 초기위치지정용도
x = widthSize/2
y = heightSize/2

finish = False #나중에 게임루프를 벗어나고 싶을때 즉 종료하고 싶을때
makeEnemy = False  #처음에 2페이지 넘어가면 한번만 생성해주기위해서 판단하는 변수

enemyList = []
missileList = []
Page = 1

gametimecheck = False

#-----------------------------------## 게임 로직 시작 ##---------------------------------------
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True

pressd = pygame.key.get_pressed()  # 키 이벤트
    gametime = int(pygame.time.get_ticks()) # 게임 타이머
    
    
    
    if Page == 1:  #초기화면
        game_screen.fill((200, 200, 0))  # 배경색
        
        # 텍스트 출력용
        function.show_text(game_screen, "If you want to start game, Enter the Spacebar ", 20, 100)
        
        if pressd[pygame.K_SPACE]:   Page = 2
    
    elif Page == 2: #게임 시작화면
        game_screen.fill((0, 200, 0))  #배경색
        
        function.show_text(game_screen, "Gametime : " + str(gametime), 10, 10) # 텍스트 출력용
        function.show_img(game_screen, "picture/airplane.png", x, y)
        
        (x, y) = function.character_Control(pressd , widthSize, heightSize, imageSize, x, y)
        
        
        #------미사일 처리
        if pressd[pygame.K_SPACE]:
            missile = Missile(game_screen, x, y, x, y-1)
            missileList.append(missile)
        
        for m in missileList:
            m.draw()
            if m.check == True:
                missileList.remove(m)
    
        #------적군 처리---------------
        if makeEnemy == False:
            for i in range(Enemycount):
                random_x = random.randrange(0, 100)
                random_y = random.randrange(0, 100)  #heightSize - imageSize
                enemy = Enemy(game_screen,random_x, random_y, x, y)  #200,200 은 방향을 지정하는거니깐 내쪽으로 움직이게 해야겠다
                enemyList.append(enemy)
            makeEnemy = True

for e in enemyList:
    e.draw()
        e.crush(x,y)
            if e.check == True:     Page = 3
        
        for e in enemyList:
            for m in missileList:   # 1준게 적군의 반지름 사이즈이다
                if m.x < e.x + 1 and m.x > e.x-1 and m.y < e.y + 1 and m.y > e.y -1:
                    missileList.remove(m)
                    enemyList.remove(e)

elif Page == 3: #엔딩 화면
    game_screen.fill((200, 200, 200))  # 배경색
        
        if gametimecheck == False:
            gameovertime = gametime
            gametimecheck = True


    function.show_text(game_screen, "GameOver:  " + str(gameovertime) , widthSize/2, heightSize/2)

pygame.display.flip() #프레임 갱신

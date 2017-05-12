#-*- coding:utf-8 -*-
import pygame
import function

#----------------------------------## 클래스 정 ##---------------------------------------
class MoveEntity:
    def __init__(self, screen, ex, ey, tx, ty):
        self.screen = screen
        self.x = ex
        self.y = ey
        self.vx = tx - ex
        self.vy = ty - ey
        self.check = False
        self.mVector = pygame.math.Vector2(self.vx, self.vy)
        self.mVector = pygame.math.Vector2.normalize(self.mVector)
    
    def draw(self):
        mRect = self.mImage.get_rect()
        mRect = mRect.fit((self.x, self.y, 50, 50))
        self.screen.blit(self.mImage, mRect)


class Enemy(MoveEntity):  #상속
    def __init__(self, screen, ex, ey, tx, ty):
        MoveEntity.__init__(self, screen, ex, ey, tx, ty)
        self.mImage = pygame.image.load("picture/enemy1.png")
        self.mImage = pygame.transform.scale(self.mImage, (30, 30))

    def draw(self):
        self.update()
        MoveEntity.draw(self)


    def update(self):
        self.x += self.mVector[0]
        self.y += self.mVector[1]
        
        if self.y < 0 or self.y > heightSize - ememyImageSize:
            self.vy = -self.vy
        if self.x < 0 or self.x > widthSize - ememyImageSize:
            self.vx = -self.vx
        
        self.mVector = pygame.math.Vector2(self.vx, self.vy)
        self.mVector = pygame.math.Vector2.normalize(self.mVector)


    def crush(self, mx, my):
        if self.x+3 < mx + ememyImageSize and self.x+3 > mx - ememyImageSize:
            if self.y+3 < my + ememyImageSize and self.y+3 > my - ememyImageSize:
                self.check = True


class Missile:
    def __init__(self, screen, ex, ey, tx, ty):
        MoveEntity.__init__(self, screen, ex, ey, tx, ty)
        self.mImage = pygame.image.load("picture/coin.png")
        self.mImage = pygame.transform.scale(self.mImage, (10, 10))

    def draw(self):
        self.update()
        MoveEntity.draw(self)

    def update(self):
        global widthSize, heightSize
        self.x += self.mVector[0]
        self.y += self.mVector[1]
        if self.x < 0 or self.y < 0:                        self.check = True
        if self.x > widthSize or self.y > heightSize:       self.check = True

# ----------------------------------## 게임 기본 설정 관련 ##---------------------------------------
pygame.init()

# 게임 전체 스크린 사이즈
global widthSize, heightSize, ememyImageSize
widthSize = 500
heightSize = 400
ememyImageSize = 43

Enemycount = 14  # 적군 숫자

# 게임 스크린 사이즈와 게임 제목 설정
game_screen = pygame.display.set_mode((widthSize, heightSize))
pygame.display.set_caption("test")

# 오디오 출력용
pygame.mixer.music.load('sound/ponyo.wav')
pygame.mixer.music.play(0)

#-----------------------------------## 게임 사용 변수    ##---------------------------------------


finish = False      #나중에 게임루프를 벗어나고 싶을때 즉 종료하고 싶을때

makeEnemy = False   #처음에 2페이지 넘어가면 한번만 생성해주기위해서 판단하는 변수
enemyList = []
missileList = []
gametimecheck = False
# 키보드 이동용 전역변수 초기위치지정용도
m_x = widthSize / 2
m_y = heightSize / 2
Page = 1            #페이지 처리

#-----------------------------------## 게임 로직 시작 ##---------------------------------------
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True

    pressd = pygame.key.get_pressed()  # 키 이벤트
    gametime = int(pygame.time.get_ticks()) # 게임 타이머

    function.show_img(game_screen, "picture/bg.png", 0, 0)


    if Page == 1:


        function.show_text(game_screen, "If you want to start game, Enter the Spacebar ", 20, 100)
        if pressd[pygame.K_SPACE]:      Page = 2


    
    elif Page == 2:

        function.show_text(game_screen, "Gametime : " + str(gametime), 10, 10) # 텍스트 출력용

        # -----0 내 캐릭터 0 --------
        function.show_img(game_screen, "picture/airplane.png", m_x, m_y)
        (m_x, m_y) = function.character_Control(pressd , widthSize, heightSize, ememyImageSize, m_x, m_y)

        # -----0 적 캐릭터 0 --------
        if makeEnemy == False:
            for i in range(Enemycount):
                (random_x, random_y) = function.enemyRandomPosition(widthSize, heightSize, ememyImageSize)
                enemy = Enemy(game_screen, random_x, random_y, m_x, m_y)
                enemyList.append(enemy)
            makeEnemy = True
        for e in enemyList:
            e.draw()
            e.crush(m_x,m_y)
            if e.check == True:     Page = 3    #충돌시 엔딩화면


        #  ------미사일 처리
        if pressd[pygame.K_SPACE]:
            missile = Missile(game_screen, m_x, m_y, m_x, m_y-1)
            missileList.append(missile)
        for m in missileList:
            m.draw()
            if m.check == True:
                missileList.remove(m)

        #  -------적과 미사일 맞을 때 처리
        for e in enemyList:
            for m in missileList:   # 1준게 적군의 반지름 사이즈이다
                if m.x < e.x + 1 and m.x > e.x-1 and m.y < e.y + 1 and m.y > e.y -1:
                    missileList.remove(m)
                    enemyList.remove(e)



    elif Page == 3: #엔딩 화면

        if gametimecheck == False:
            gameovertime = gametime
            gametimecheck = True

        for i in range(1,5):
            function.show_text(game_screen, "GameOver:  " + str(gameovertime) , widthSize/i, heightSize/i)

        if pressd[pygame.K_p]:
            makeEnemy = False
            enemyList = []
            missileList = []
            gametimecheck = False
            m_x = widthSize / 2
            m_y = heightSize / 2
            Page = 1

    pygame.display.flip() #프레임 갱신

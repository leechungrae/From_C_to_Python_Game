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

Enemycount = 9 #적군 숫자

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
        self.mImage = pygame.image.load("picture/enemy3.png")
        self.mImage = pygame.transform.scale(self.mImage, (int(30), int(30)))
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

#-----------------------------------## 게임 사용 변수 ##---------------------------------------
#키보드 이동용 전역변수 초기위치지정용도
x = widthSize/2
y = heightSize/2

finish = False #나중에 게임루프를 벗어나고 싶을때 즉 종료하고 싶을때
makeEnemy = False  #처음에 2페이지 넘어가면 한번만 생성해주기위해서 판단하는 변수

enemyList = []
Page = 1

#-----------------------------------## 게임 로직 시작 ##---------------------------------------
while not finish:

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

        if pressd[pygame.K_RIGHT]:
            if x < widthSize-imageSize:     x += 5
        elif pressd[pygame.K_LEFT]:
            if x > 0:                       x -= 5
        elif pressd[pygame.K_UP]:
            if y > 0:                       y -= 5
        elif pressd[pygame.K_DOWN]:
            if y < heightSize-imageSize:    y += 5

        # ---------------------------적군 발사처리해주려고 ------
        if makeEnemy == False:
            for i in range(Enemycount):
                random_x = random.randrange(0, widthSize-imageSize)
                random_y = random.randrange(0, heightSize - imageSize)
                enemy = Enemy(game_screen,random_x, random_y, 100, 100)  #200,200 은 방향을 지정하는거니깐 내쪽으로 움직이게 해야겠다
                enemyList.append(enemy)
            makeEnemy = True

        for m in enemyList:
            m.draw()

        for m in enemyList:
            m.crush(x,y)
            if m.check == True: Page = 3


    elif Page == 3: #엔딩 화면
        game_screen.fill((200, 200, 200))  # 배경색
        function.show_text(game_screen, "GameOver", widthSize/2, heightSize/2)

    pygame.display.flip() #프레임 갱신
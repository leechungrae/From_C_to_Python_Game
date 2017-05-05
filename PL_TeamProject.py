#-*- coding:utf-8 -*-
import pygame, sys

pygame.init()

class Missile:
    def __init__(self, screen, cx, cy, tx, ty):
        self.screen = screen
        self.x = cx + 25
        self.y = cy + 25
        self.vx = tx - cx
        self.vy = ty - cy
        self.check = False
        self.mImage = pygame.image.load("picture/coin.png")
        self.mImage = pygame.transform.scale(self.mImage, (int(10), int(10)))
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
        mRect = self.mImage.get_rect()
        mRect = mRect.fit((self.x, self.y, 50, 50))
        self.screen.blit(self.mImage, mRect)

#----------------------------------## 게임 기본 설정 관련 ##---------------------------------------


#게임 전체 스크린 사이즈
widthSize = 500
heightSize = 400


#게임 스크린 사이즈와 게임 제목 설정
game_screen = pygame.display.set_mode((widthSize,heightSize))
pygame.display.set_caption("test")

#오디오 출력용
pygame.mixer.music.load('sound/ponyo.wav')
pygame.mixer.music.play(0)

#-----------------------------------## 게임 관련 함수 ##---------------------------------------


def show_img(ourScreen, img_name, x_Position,y_Position) :
    myimg = pygame.image.load(img_name)
    ourScreen.blit(myimg, (x_Position, y_Position))


def show_text(ourScreen,text,x_Position, y_Position):
    text_Font = pygame.font.Font("freesansbold.ttf", 20)
    textSurface = text_Font.render(text, True, (0, 100, 0))
    ourScreen.blit(textSurface, (x_Position, y_Position))


#-----------------------------------## 게임 사용 변수 ##---------------------------------------

#키보드 이동용 전역변수 초기위치지정용도
x = widthSize/2
y = heightSize/2


finish = False
Page = 1

missileList = []
#-----------------------------------## 게임 로직 시작 ##---------------------------------------
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True

    pressd = pygame.key.get_pressed()  # 키 이벤트
    gametime = int(pygame.time.get_ticks()) #게임 타이머

    if Page == 1:  #초기화면
        game_screen.fill((200, 200, 0))  # 배경색

        # 텍스트 출력용
        show_text(game_screen, "Gamestart", 100, 100)

        # 임시로 준것
        if pressd[pygame.K_UP]:   Page = 2




    elif Page == 2: #게임 시작화면
        game_screen.fill((0, 200, 0))  #배경색

        if pressd[pygame.K_RIGHT]:
            if x < widthSize-30:
                x += 5
        if pressd[pygame.K_LEFT]:
            if x > 0:
                x -= 5
        if pressd[pygame.K_UP]:
            if y > 0:
                y -= 5
        if pressd[pygame.K_DOWN]:
            if y < heightSize-30:
                y += 5




        # 임시로 준것
        if pressd[pygame.K_p]:   Page = 3


        show_img(game_screen, "picture/air.png", x, y)


        pos = pygame.mouse.get_pos()
        if pressd[pygame.K_SPACE]:
            missile = Missile(game_screen, x, y, pos[0], pos[1])
            missileList.append(missile)

        for m in missileList:
            m.update()
            m.draw()
            if m.check == True:
                missileList.remove(m)


        # 텍스트 출력용
        show_text(game_screen, "Gametime : " + str(gametime), 10, 10)


    elif Page == 3: #엔딩 화면
        game_screen.fill((200, 200, 200))  # 배경색
        show_text(game_screen, "GameOver", 100, 100)




    pygame.display.flip() #프레임 갱신
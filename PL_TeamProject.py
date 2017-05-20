import function
import pygame, math, random

# ----------------------------------## 클래스 정 ##---------------------------------------
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


class Enemy(MoveEntity):  # 상속
    def __init__(self, screen, ex, ey, tx, ty, gt):
        MoveEntity.__init__(self, screen, ex, ey, tx, ty)
        self.gameTime = gt
        self.mImage = pygame.image.load("picture/enemy1.png")
        self.mImage = pygame.transform.scale(self.mImage, (30, 30))

    def draw(self):
        self.update()
        MoveEntity.draw(self)

    def update(self):


        if self.y < 0 or self.y > heightSize - enemySize:
            self.vy = -self.vy
        if self.x < 0 or self.x > widthSize - enemySize:
            self.vx = -self.vx

        self.mVector = pygame.math.Vector2(self.vx, self.vy)
        self.mVector = pygame.math.Vector2.normalize(self.mVector)

        self.mVector[0] *= gameTime
        self.mVector[1] *= gameTime

        self.x += self.mVector[0]
        self.y += self.mVector[1]



        # ------------------------------------------------------------

    def crush(self, mx, my):
        if self.x + 15  < mx + enemySize and self.x - 15 > mx - enemySize:
            if self.y + 15  < my + enemySize and self.y - 15 > my - enemySize:
                self.check = True


class Missile:
    def __init__(self, screen, ex, ey, tx, ty):
        MoveEntity.__init__(self, screen, ex, ey, tx, ty)
        self.mImage = pygame.image.load("picture/bullet.png")
        self.mImage = pygame.transform.scale(self.mImage, (23, 35))

    def draw(self):
        self.update()
        MoveEntity.draw(self)

    def update(self):
        global widthSize, heightSize
        self.x += self.mVector[0]
        self.y += self.mVector[1] - 5   # 총알 속도
        if self.x < 0 or self.y < 0:                        self.check = True
        if self.x > widthSize or self.y > heightSize:       self.check = True


# ----------------------------------## 게임 기본 설정 관련 ##---------------------------------------

#게임 시작 및 초기화
pygame.init()

widthSize, heightSize = 500, 400
enemySize = 30

# 게임 스크린 사이즈와 게임 제목 설정
game_screen = pygame.display.set_mode((widthSize, heightSize))
pygame.display.set_caption("PL_Project")

# 오디오 출력용
pygame.mixer.music.load('sound/ponyo.wav')
pygame.mixer.music.play(0)

#----------------------------           # 게임 사용 변수    -----------------------------------


gameOverTimeCheck = False                   # 종료시 게임시간 체크
makeEnemy = False   # 처음에 2페이지 넘어가면 한번만 생성해주기위해서 판단하는 변수
gameStartTimeCheck = False
enemyList = []                          # 적군 리스트
missileList = []                        # 미사일 리스트
page = 1                                # 페이지 처리
enemyCount = 7                          # 적군 숫자
airplane_pos_x = widthSize / 2          # 내 캐릭터 초기 위치값
airplane_pos_y = heightSize / 2         # 내 캐릭터 초기 위치값
missileCheck = True

gameResult = []

#-----------------------------------## 게임 로직 시작 ##---------------------------------------
finish = False
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True

    pressed = pygame.key.get_pressed()           # 키 이벤트
    gameTotalTime = int(pygame.time.get_ticks()/1000)     # 게임 타이머

    if page == 1:
        function.show_img(game_screen, "picture/bg1.png", 0, 0)  # 배경 설정

        if pressed[pygame.K_SPACE]:      page = 2


    elif page == 2:
        if gameStartTimeCheck ==False:
            gameStartTime = gameTotalTime
            gameStartTimeCheck = True

        gameTime = gameTotalTime - gameStartTime
        function.show_img(game_screen, "picture/bg2.png", 0, 0)  # 배경 설정

        function.show_text(game_screen, "Gametime : " + str(gameTime), 10, 10)  # 텍스트 출력용




        # ----- 내 캐릭터 생성 --------
        function.show_img(game_screen, "picture/airplane.png", airplane_pos_x, airplane_pos_y)
        (airplane_pos_x, airplane_pos_y) = function.character_Control(pressed, widthSize, heightSize, enemySize, airplane_pos_x, airplane_pos_y)

        # ----- 적 캐릭터 생성 --------
        if makeEnemy == False:
            for i in range(enemyCount):
                (random_x, random_y) = function.enemyRandomPosition(widthSize, heightSize, enemySize)
                enemy = Enemy(game_screen, random_x, random_y, airplane_pos_x, airplane_pos_y, gameTime)
                enemyList.append(enemy)
            makeEnemy = True

        for e in enemyList:
            e.draw()
            e.crush(airplane_pos_x, airplane_pos_y)
            if e.check == True:     page = 3  # 충돌시 엔딩화면


        # ------미사일 처리
        if missileCheck == True:
            if pressed[pygame.K_SPACE]:
                missile = Missile(game_screen, airplane_pos_x-4, airplane_pos_y, airplane_pos_x-4, airplane_pos_y - 1)
                missileList.append(missile)

                missileCheck = False
                missileShotTime = gameTotalTime
        else:
            if gameTotalTime - missileShotTime > 1:
                missileCheck = True


        for m in missileList:
            m.draw()
            if m.check == True:
                missileList.remove(m)

        # -------적과 미사일 맞을 때 처리
        for e in enemyList:
            for m in missileList:  # 1준게 적군의 반지름 사이즈이다
                if m.x < e.x + 15 and m.x > e.x - 15 and m.y < e.y + 2 and m.y > e.y - 2:
                    missileList.remove(m)
                    enemyList.remove(e)


    elif page == 3:  # 엔딩 화면
        function.show_img(game_screen, "picture/bg3.png", 0, 0)  # 배경 설정

        if gameOverTimeCheck == False:
            gameOverTime = gameTime
            gameResult.append(gameOverTime)
            gameOverTimeCheck = True

        function.show_text(game_screen, "GameOver:  " + str(gameOverTime), widthSize / 2, heightSize / 2)

        if pressed[pygame.K_s]:
            gameTimeCheck = False  # 종료시 게임시간 체크
            makeEnemy = False  # 처음에 2페이지 넘어가면 한번만 생성해주기위해서 판단하는 변수
            gameStartTimeCheck = False
            gameOverTimeCheck = False
            enemyList = []  # 적군 리스트
            missileList = []  # 미사일 리스트
            page = 1  # 페이지 처리
            enemyCount = 7  # 적군 숫자
            airplane_pos_x = widthSize / 2  # 내 캐릭터 초기 위치값
            airplane_pos_y = heightSize / 2  # 내 캐릭터 초기 위치값

    pygame.display.flip()  # 프레임 갱신
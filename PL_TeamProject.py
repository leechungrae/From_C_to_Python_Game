import function, pygame
# ----------------------------------## 클래스 정의 ##---------------------------------------
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
    def __init__(self, screen, ex, ey, tx, ty, gt, picture):
        MoveEntity.__init__(self, screen, ex, ey, tx, ty)
        self.gameTime = gt
        self.mImage = pygame.image.load(picture)
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
        self.x += (self.mVector[0] * gameSpeed)
        self.y += (self.mVector[1] * gameSpeed)

    def crush(self, mx, my):
        if self.x + 15 < mx + enemySize and self.x - 15 > mx - enemySize:
            if self.y + 15 < my + enemySize and self.y - 15 > my - enemySize:
                collision_sound.play()
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
pygame.init()

widthSize, heightSize = 500, 400
enemySize = 30

maxGameSpeed = 5        #게임 최대 스피드
gameInitCheck = False   # 초기화변수들
gameResult = []         #게임 결과 저장용

# 게임 스크린 사이즈와 게임 제목 설정
game_screen = pygame.display.set_mode((widthSize, heightSize))
pygame.display.set_caption("PL_Project")

# 오디오 출력용
pygame.mixer.music.load('sound/bgm.wav')
pygame.mixer.music.play(-1) # -1 설정해서 무한 반복

# 미사일 효과음
bullet_sound = pygame.mixer.Sound("audio/bullet.wav")
bullet_sound.set_volume(0.6)

# 명중 시 폭발음
collision_sound = pygame.mixer.Sound("audio/explosion.wav")
collision_sound.set_volume(0.8)

#-----------------------------------## 게임 로직 시작 ##---------------------------------------
finish = False
while not finish:
    if gameInitCheck == False: #게임 초기화 체크용

        gameOverTimeCheck = False           # 종료시 게임시간 체크
        makeEnemyCheck = False              # 처음에 2페이지 넘어가면 한번만 생성해주기위해서 판단하는 변수
        enemyStage = 1
        gameStartTimeCheck = False          # 게임 시작 저장용
        enemyList = []                      # 적군 리스트
        missileList = []                    # 미사일 리스트
        page = 1                            # 페이지 처리
        enemyCount = 7                      # 적군 숫자
        gameSpeed = 0                       # 초기 게임 스피드
        airplane_pos_x = widthSize / 2      # 내 캐릭터 초기 위치값
        airplane_pos_y = heightSize / 2     # 내 캐릭터 초기 위치값
        missileCheck = True                 # 미사일 계속 발생안되게 만드는 것
        gameInitCheck = True                # 게임 초기화 설정용도
        missile_width = 4                   # 미사일 너비
        missile_height = 1                  # 미사일 높이
        enemy_width = 23                    # 적 개체 너비
        enemy_height = 5                    # 적 개체 높이

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True

    pressed = pygame.key.get_pressed()                      # 키 이벤트
    gameTotalTime = round((pygame.time.get_ticks()/1000),1)     # 게임 타이머

    if page == 1:
        function.show_img(game_screen, "picture/bg.jpg", 0, 0)  # 배경 설정
        if pressed[pygame.K_SPACE]:         page = 2

    elif page == 2:
        if gameStartTimeCheck == False:     # 게임시작누를때 게임시작시간 저장
            gameStartTime = gameTotalTime
            gameStartTimeCheck = True

        gameTime = round(gameTotalTime - gameStartTime, 2)

        #게임 최대 스피드 정리하기
        gameSpeed = gameTime
        if gameSpeed > maxGameSpeed:            gameSpeed = maxGameSpeed

        function.show_img(game_screen, "picture/bg2.png", 0, 0)  # 배경 설정
        function.show_text(game_screen, str(gameTime) + " Seconds", 10, 10)  # 텍스트 출력용

        # ----- 내 캐릭터 생성 --------
        function.show_img(game_screen, "picture/airplane.png", airplane_pos_x, airplane_pos_y)
        (airplane_pos_x, airplane_pos_y) = function.character_Control(pressed, widthSize, heightSize, enemySize, airplane_pos_x, airplane_pos_y)

        # ----- 적 캐릭터 생성 --------
        if makeEnemyCheck == False:
            if enemyStage == 1:                  picture = "picture/enemy1.png"
            elif enemyStage == 2:                picture = "picture/enemy2.png"
            else:                                picture = "picture/enemy3.png"

            for i in range(enemyCount):
                (random_x, random_y) = function.enemyRandomPosition(widthSize, heightSize, enemySize)
                enemy = Enemy(game_screen, random_x, random_y, airplane_pos_x, airplane_pos_y, gameTime, picture)
                enemyList.append(enemy)

            makeEnemyCheck = True

        if len(enemyList) < 5:
            makeEnemyCheck = False
            enemyStage +=1



        for e in enemyList:
            e.draw()
            e.crush(airplane_pos_x, airplane_pos_y)
            if e.check == True:     page = 3  # 충돌시 엔딩화면

        # ------미사일 처리
        if missileCheck == True:
            if pressed[pygame.K_SPACE]:
                bullet_sound.play()
                missile = Missile(game_screen, airplane_pos_x-missile_width, airplane_pos_y, airplane_pos_x-missile_width, airplane_pos_y - missile_height)
                missileList.append(missile)
                missileCheck = False
                missileShotTime = gameTotalTime - 1
        else:
            if gameTotalTime - missileShotTime > 1:
                missileCheck = True


        # ------미사일 보여주고 지워지게
        for m in missileList:
            m.draw()
            if m.check == True:
                missileList.remove(m)

        # -------적과 미사일 맞을 때 처리
        for e in enemyList:
            for m in missileList:  # 1준게 적군의 반지름 사이즈이다
                #if pygame.sprite.spritecollide(e, m ,True):
                if m.x < e.x + enemy_width and m.x > e.x - enemy_width and m.y < e.y + 1 and m.y > e.y - enemy_height:
                    collision_sound.play()
                    missileList.remove(m)
                    enemyList.remove(e)



    elif page == 3:  # 엔딩 화면
        function.show_img(game_screen, "picture/bg3.png", 0, 0)  # 배경 설정

        #게임 시간 체크
        if gameOverTimeCheck == False:
            gameOverTime = gameTime
            gameOverTimeCheck = True
            gameResult.append(gameOverTime)

        function.show_result(game_screen, widthSize, heightSize, gameResult)

        if pressed[pygame.K_s]:            gameInitCheck = False

    pygame.display.flip()  # 프레임 갱신
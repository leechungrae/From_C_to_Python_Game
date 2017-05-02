import pygame

pygame.init()

#오디오 출력용
pygame.mixer.music.load('sound/ponyo.wav')
pygame.mixer.music.play(0)

widthSize = 500
heightSize = 400

game_screen = pygame.display.set_mode((widthSize,heightSize))  #스크린 사이즈 지정
pygame.display.set_caption("test") #제목 지정


#키보드 이동용 전역변수 초기위치지정용도
x = widthSize/2
y = heightSize/2

def show_img(ourScreen, img_name, x_Position,y_Position) :
    myimg = pygame.image.load(img_name)
    ourScreen.blit(myimg, (x_Position, y_Position))

finish = False
Page = 1



while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True

    pressd = pygame.key.get_pressed()  # 키 이벤트



    if Page == 1:
        game_screen.fill((200, 200, 0))  # 배경색 갱신해줘야한다

        # 임시로 준것
        if pressd[pygame.K_UP]:   Page = 2




    elif Page == 2:
        #밑에 게임로직 설계
        game_screen.fill((0, 200, 0))  #배경색 갱신해줘야한다

        if pressd[pygame.K_RIGHT]:  x += 5
        if pressd[pygame.K_LEFT]:   x -= 5

        #pygame.draw.rect(game_screen, (255,20,20), pygame.Rect(x, y, 10, 10))  # 방향키 처리
        show_img(game_screen, "picture/coin.png", x, y)

        #임시로 준것
        if pressd[pygame.K_DOWN]:   Page = 3



    elif Page == 3:
        game_screen.fill((200, 200, 200))  # 배경색 갱신해줘야한다





    pygame.display.flip() #프레임 갱신

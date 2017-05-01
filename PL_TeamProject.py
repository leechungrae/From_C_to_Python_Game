import pygame

pygame.init()

widthSize = 500
heightSize = 400

game_screen = pygame.display.set_mode((widthSize,heightSize))  #스크린 사이즈 지정
pygame.display.set_caption("test") #제목 지정


#키보드 이동용 전역변수 초기위치지정용도
x = widthSize/2
y = heightSize/2


finish = False
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True


    #밑에 게임로직 설계
    game_screen.fill((0, 200, 0))  #배경색 갱신해줘야한다

    pressd = pygame.key.get_pressed()  #키 이벤트


    if pressd[pygame.K_RIGHT]:  x += 5
    if pressd[pygame.K_LEFT]:   x -= 5

    pygame.draw.rect(game_screen, (255,20,20), pygame.Rect(x, y, 10, 10))  # 방향키 처리

    pygame.display.flip() #프레임 갱신

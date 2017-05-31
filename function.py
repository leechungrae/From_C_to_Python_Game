import pygame,random

def show_img(ourScreen, img_name, x_Position,y_Position) :
    myimg = pygame.image.load(img_name)
    ourScreen.blit(myimg, (x_Position, y_Position))


def show_text(ourScreen,text,x_Position, y_Position):
    text_Font = pygame.font.Font("freesansbold.ttf", 20)
    textSurface = text_Font.render(text, True, (250, 250, 250))
    ourScreen.blit(textSurface, (x_Position, y_Position))

def character_Control(pressed, widthSize, heightSize, imageSize, x, y):
    if pressed[pygame.K_RIGHT] and x < widthSize - imageSize:  x += 5
    if pressed[pygame.K_LEFT] and x > 0:                       x -= 5
    if pressed[pygame.K_UP] and y > 0:                         y -= 5
    if pressed[pygame.K_DOWN] and y < heightSize - imageSize:  y += 5

    return x, y

def enemyRandomPosition(w, h, s):
    random_x = random.randrange(0, w-s)
    random_y = random.randrange(0, h-s)

    while random_x > w/3 and random_x < 2*(w/3) :
        random_x = random.randrange(0, w-s)

    return random_x, random_y


def show_result(game_screen,widthSize,heightSize,gameResult):
    gameResult.sort(reverse=True)
    if len(gameResult) > 4:
        for i in range(4):
            show_text(game_screen, "Score:  " + str(gameResult[i]), widthSize / 3 + 30, heightSize / 3 + (50 * i))
    else:
        for i in range(len(gameResult)):
            show_text(game_screen, "Score:  " + str(gameResult[i]), widthSize / 3 + 30, heightSize / 3 + (50 * i))
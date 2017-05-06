import pygame

def show_img(ourScreen, img_name, x_Position,y_Position) :
    myimg = pygame.image.load(img_name)
    ourScreen.blit(myimg, (x_Position, y_Position))


def show_text(ourScreen,text,x_Position, y_Position):
    text_Font = pygame.font.Font("freesansbold.ttf", 20)
    textSurface = text_Font.render(text, True, (0, 100, 0))
    ourScreen.blit(textSurface, (x_Position, y_Position))

def character_Control(pressd, widthSize, heightSize, imageSize, x, y):
    if pressd[pygame.K_RIGHT] and x < widthSize - imageSize:   x += 5
    if pressd[pygame.K_LEFT] and x > 0:                     x -= 5
    if pressd[pygame.K_UP] and y > 0:                     y -= 5
    if pressd[pygame.K_DOWN] and y < heightSize - imageSize:  y += 5

    return x, y
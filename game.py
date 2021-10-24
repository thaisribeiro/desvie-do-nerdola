import random
import time
import pygame

pygame.init()

FPS = 60
SCREENWIDTH = 800
SCREENHEIGHT = 600
display_width = 800
display_height = 600
pause = True
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
block_color = (53, 115, 255)

player_width = 68

# seta o tamanho inicial no nosso display
display = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Desvie do Nerdola')
clock = pygame.time.Clock()

# seta os audios que vamos usar nos jogos
crash = pygame.mixer.Sound("audios/batenerd.wav")
level = pygame.mixer.Sound("audios/level.wav")
gado = pygame.mixer.Sound("audios/bategado.wav")
gameover = pygame.mixer.Sound("audios/gameover.wav")
start = pygame.mixer.Sound("audios/start.wav")


BACKGROUND = pygame.image.load('icons/street.png').convert()
PLAYER = pygame.image.load('icons/user.png').convert_alpha()

# seta as imagens dos personagens
nerd = pygame.image.load('icons/sapo.png').convert_alpha()
like = pygame.image.load('icons/like.png').convert_alpha()
gado = pygame.image.load('icons/minion.png').convert_alpha()
user_icon = pygame.image.load('icons/user.png')

pygame.display.set_icon(user_icon)

def detour(count):
    font = pygame.font.SysFont("Britannic Bold", 40)
    text = font.render(f'PONTUAÇÃO {str(count)}', True, bright_red)
    display.blit(text, (12, 5))

def player(x, y):
    display.blit(PLAYER, (x, y))

def text_objects(text, font, color=black):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def crash_object():
    pygame.mixer.Sound.play(crash)
    pygame.mixer.music.stop()

    time.sleep(2)

    pygame.mixer.music.load('audios/gameover.wav')
    pygame.mixer.music.play(-1)

    bg = pygame.image.load("icons/gameover.png")
    display.blit(bg, (0,0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("Jogar Novamente", 150, 480, 160, 50, green, bright_green, game_loop)
        button("Sair", 550, 480, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(display, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(display, ic, (x, y, w, h))

    smallText = pygame.font.SysFont("Britannic Bold", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w/2)), (y + (h/2)))
    display.blit(textSurf, textRect)

def quit_game():
    pygame.quit()
    quit()

def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False

def paused():
    pygame.mixer.music.pause()

    largeText = pygame.font.SysFont("Britannic Bold", 115)
    TextSurf, TextRect = text_objects("Stoped", largeText)
    TextRect.center = ((display_width/2), (display_height/2))
    display.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    unpause()

        button("Continuar", 150, 480, 100, 50, green, bright_green, unpause)
        button("Sair", 550, 480, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)

def power():
    pygame.mixer.Sound.play(level)
    pygame.mixer.music.stop()

def gado_object():
    pygame.mixer.Sound.play(gado)
    pygame.mixer.music.stop()

def intro_game():
    intro = True
    while intro:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                quit_game()
                
        bg = pygame.image.load("icons/intro.png")
        display.blit(bg, (0,0))

        button("Entrar!", 150, 480, 100, 50, green, bright_green, game_loop)
        button("Sair", 550, 480, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)


def game_loop():
    global pause
    pygame.mixer.Sound.play(start)
    pygame.mixer.music.stop()

    time.sleep(1)

    pygame.mixer.music.load('audios/jogo.wav')
    pygame.mixer.music.play(-1)

    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 7
    thing_width = 90
    thing_height = 75

    thingCount = 1

    
    like_startx = random.randrange(0, display_width)
    like_starty = -600
    like_width = 52
    like_height = 74
    like_speed = 3

    gado_startx = random.randrange(0, display_width)
    gado_starty = -600
    gado_width = 52
    gado_height = 74
    gado_speed = 3


    dodged = 0


    gameExit = False
    bgY = 0
    player_safe = False
    like_checkpoint = 0
    like_status = False
    gado_status = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_SPACE:
                    pause = True
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change

        if bgY < BACKGROUND.get_width() * -1:
            bgY = 0

        display.blit(BACKGROUND, (0, bgY))
        bgY -= 2
        display.blit(nerd, (thing_startx, thing_starty))

        thing_starty += thing_speed

        if dodged % 7 == 0 and dodged != 0 and like_checkpoint == 0:
            like_status = True

        if like_status:
            display.blit(like, (like_startx, like_starty))

        like_starty += like_speed

        if dodged % 12 == 0 and dodged != 0:
            gado_status = True

    
        gado_starty += gado_speed
        player(x, y)
        detour(dodged)
        
        if x > display_width - player_width or x < 0:
            crash_object()

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            dodged += 1
            thing_speed += 0.5
            
        if like_starty > display_height:
            like_starty = 0 - like_height
            like_startx = random.randrange(0, display_width)
            like_speed -= 0.01
            if like_speed < 0:
                like_speed = 0

        if gado_starty > display_height:
            gado_starty = -600
            gado_startx = random.randrange(0, display_width)


        if y < thing_starty + thing_height:
            if x > thing_startx and x < thing_startx + thing_width and player_safe == False or x + player_width > thing_startx and x + player_width < thing_startx + thing_width and player_safe == False:
                crash_object()

        if y < gado_starty + gado_height:
            if x > gado_startx and x < gado_startx + gado_width and gado_status or x + player_width > gado_startx and x + player_width < gado_startx + gado_width and gado_status:
                gado_object()
                pygame.mixer.music.load('audios/jogo.wav')
                pygame.mixer.music.play(-1)
                dodged = int(dodged/1.5)
                gado_status = False
            
        if y < like_starty + like_height:
            if x > like_startx and x < like_startx + like_width and like_status or x + player_width > like_startx and x + player_width < like_startx + like_width and like_status:
                power()
                pygame.mixer.music.load('audios/jogo.wav')
                pygame.mixer.music.play(-1)
                
                player_safe = True
                like_checkpoint = dodged
                like_status = False
                
        if dodged - like_checkpoint > 4:
            player_safe = False
            like_checkpoint = 0
            like_speed = 3

        if like_checkpoint > 0:
            pygame.display.flip()
            time.sleep(0.01)
            display.blit(PLAYER, (x, y))
            pygame.display.flip()

        pygame.display.update()
        clock.tick(FPS)

intro_game()
game_loop()
quit_game()

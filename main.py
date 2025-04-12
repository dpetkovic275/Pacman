from pygame import *
from easy import App
from medium import App1
from hard import App2

init()
VELICINA = 610, 670
screen = display.set_mode(VELICINA)

CRNA = (0, 0, 0)
CRVENA = (255, 0, 0)
ROZA = (0, 153, 153)

running = True
fontPacman = font.SysFont("arial black",80)
fontHello = font.SysFont("arial black", 37)
text3 = fontPacman.render("PACMAN", 1, (ROZA))


def mainmenu(screen):
    draw.rect(screen, CRNA, (0, 0, 800, 800))
    draw.rect(screen, ROZA, (160, 125, 330, 100))
    text = fontHello.render("EASY", 1, (CRVENA))
    screen.blit(text, Rect(275, 150, 400, 100))

    draw.rect(screen, ROZA, (160, 275, 330, 100))
    text1 = fontHello.render("MEDIUM", 1, (CRVENA))
    screen.blit(text1, Rect(260, 300, 400, 100))

    draw.rect(screen, ROZA, (160, 425, 330, 100))
    text2 = fontHello.render("HARD", 1, (CRVENA))
    screen.blit(text2, Rect(275, 450, 400, 100))

    text3
    screen.blit(text3,Rect(145, 0, 400, 100))

    display.flip()

state = 0
while running:
    button = 0
    for evnt in event.get():
        if evnt.type == QUIT:
            running = False
        elif evnt.type == MOUSEBUTTONDOWN:
            mx, my = evnt.pos
            button = evnt.button
            if state == 0:
                if mx > 250 and mx < 580 and my > 125 and my < 225:
                    state = 1
                elif mx > 250 and mx < 580 and my > 275 and my < 375:
                    state = 2
                elif mx > 250 and mx < 580 and my > 425 and my < 525:
                    state = 3


    if state == 0:
        mainmenu(screen)

    elif state == 1:
            app = App()
            app.run()

    elif state == 2:
            app = App1()
            app.run()

    elif state == 3:
            app = App2()
            app.run()

quit()


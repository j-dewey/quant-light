import pygame as pg
from pygame.locals import QUIT, MOUSEBUTTONUP, MOUSEBUTTONDOWN
pg.init()

modes = ["column"]

def get_mode():
    while True:
        mode = input("What mode would you like? ")
        if not mode in modes:
            print("Unrecognized mode")
            print("The following modes are recognized: " + str(modes))
        else:
            return mode

if __name__ == "__main__":
    file_name = input("What would you like to name the file? ")
    img_width = int( input("What width would you like? ") )
    img_height = int( input("What height would you like? ") )
    mode = get_mode()
    image = pg.Surface((img_width, img_height))
    image.fill((255, 255, 255))

    mouse_down = False
    editor_view = pg.Surface((img_width, 50))
    window = pg.display.set_mode((img_width, img_height + 50))

    while True:
        for ev in pg.event.get():
            print(ev)
            if ev.type == QUIT:
                pg.quit()
                quit()
            elif ev.type == MOUSEBUTTONDOWN:
                mouse_down = True
            elif ev.type == MOUSEBUTTONUP:
                mouse_down = False

        # rendering
        window.fill((255, 255, 255))
        window.blit(image, (0,0))
        window.blit(editor_view, (0, img_height))
        pg.display.flip()

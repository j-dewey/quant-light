import pygame as pg
from pygame.locals import QUIT, MOUSEBUTTONUP, MOUSEBUTTONDOWN, KEYDOWN
pg.init()

modes = ["column"]

class PenDetails:
    def __init__(self, width: float, color: list[int]) -> None:
        self.width = width
        self.color = color

def get_mode():
    while True:
        mode = input("What mode would you like? ")
        if not mode in modes:
            print("Unrecognized mode")
            print("The following modes are recognized: " + str(modes))
        else:
            return mode

def save_image():
    global image, file_name, img_width
    pg.display.quit()
    # height doesn't matter, so save space by removing it
    reduced_image = pg.Surface((img_width, 1))
    reduced_image.blit(image, (0, 0))
    print('saving...')
    keep_name = ""
    while not keep_name in ["y", "n"]:
        keep_name = input("Keep name {" + file_name + "} (y/n)? ")
    if keep_name == "n":
        file_name = input("What is the new name? ")
    pg.image.save(reduced_image, "src/"+file_name+".png")
    pg.quit()
    quit()

if __name__ == "__main__":
    file_name = input("What would you like to name the file? ")
    img_width = int( input("What width would you like? ") )
    img_height = int( input("What height would you like? ") )
    # the actual mode isn't important, especialy since all it does
    # is clarify how the writing is going to work. This is why there
    # is only column mode
    mode = get_mode()
    image = pg.Surface((img_width, img_height))
    image.fill((255, 255, 255))

    mouse_down = False
    color_editor_channel = 0
    color_channel_names = ['red', 'green', 'blue']
    writing_color_value = False
    color_value = ""
    pen = PenDetails(10, [255, 0, 0])
    editor_view = pg.Surface((img_width, 50))
    window = pg.display.set_mode((img_width, img_height + 50))
    font = pg.font.SysFont("arial", 40)

    while True:
        for ev in pg.event.get():
            if ev.type == QUIT:
                pg.quit()
                quit()
            elif ev.type == MOUSEBUTTONDOWN:
                mouse_down = True
            elif ev.type == MOUSEBUTTONUP:
                mouse_down = False
            elif ev.type == KEYDOWN and writing_color_value:
                try:
                    val = int(ev.unicode)
                    color_value += str(val)
                    if len(color_value) == 3:
                        strength = int(color_value)
                        if strength > 255: strength = 255
                        pen.color[color_editor_channel] = strength
                        color_value = ""
                        writing_color_value = False
                except ValueError:
                    print('expected an int')

        keys = pg.key.get_pressed()
        if keys[pg.K_r]:
            color_editor_channel = 0
        elif keys[pg.K_g]:
            color_editor_channel = 1
        elif keys[pg.K_b]:
            color_editor_channel = 2
        if keys[pg.K_w]:
            writing_color_value = True
            print('writing color')
        if keys[pg.K_s]:
            save_image()

        if mouse_down:
            mcoords = pg.mouse.get_pos()
            pg.draw.rect(
                image,
                pen.color,
                pg.Rect(
                    mcoords[0],
                    0,
                    pen.width,
                    img_height
                ),

            )

        # rendering
        editor_view.fill((122, 122, 122))
        pg.draw.rect( editor_view, pen.color, pg.Rect(10, 10, 30, 30) )
        editor_view.blit(
            font.render(color_channel_names[color_editor_channel], False, (255, 255, 255)),
            (50, 5)
        )

        window.fill((255, 255, 255))
        window.blit(image, (0,0))
        window.blit(editor_view, (0, img_height))
        pg.display.flip()

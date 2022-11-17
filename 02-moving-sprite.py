#
# Wandering Hobo: control the sprite
#
import pygame

def make_img(buff, colors, pixel_size=1):
    """helper function to create sprite out of thin air (eh, of list of strings... ;])
       buff       list of strings, each char represents one pixel (space == transparent)
       colors     dict of char to RGB mappings ie. {'B': (0,0,0)}
       pixel_size int multiplying result image size
       @returns   pygame.Surface
    """
    maxLen = max([len(ln) for ln in buff])
    s = pygame.Surface((pixel_size*maxLen, pixel_size*len(buff)), )
    s.fill((255,0,255))
    for y,ln in enumerate(buff):
        for x,px in enumerate(ln):
            if px == ' ':
                continue
            if px in colors:
                c = colors[px]
            else:
                c = (0,0,0)
            s.fill(c, (x*pixel_size,y*pixel_size, pixel_size, pixel_size))
    s.set_colorkey((255, 0, 255), pygame.RLEACCEL)
    return s.convert()


# setup
pygame.init()
screen = pygame.display.set_mode((640,480), pygame.HWSURFACE|pygame.DOUBLEBUF)
clock = pygame.time.Clock()

palette = {
    'R': (255, 0, 0), # red
    'r': (128, 0, 0), # dark red
}

sprite = make_img([
'  RRRR  ',
'RRRRRRRR',
'  rrrr  ',
'   rr   ',
'RRRRRRRR',
'  rRRr  ',
'  R  R  ',
' rR  Rr ',
], palette, 3) # note pixel_size=3 making sprite bigger

cx = 200
cy = 100

# controls:
# keys
left = False
right = False
up = False
down = False
quit = False
# mouse coords
mx = my = -1

while not quit:
    # ---- update ----
    # read controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT: quit = True
        if event.type == pygame.KEYDOWN:
            key = event.key
            #print(key) # dbg
            if key==pygame.K_ESCAPE: quit = True
            if key==pygame.K_UP:     up = True
            if key==pygame.K_DOWN:   down = True
            if key==pygame.K_LEFT:   left = True
            if key==pygame.K_RIGHT:  right = True
        if event.type == pygame.KEYUP:
            key = event.key
            if key==pygame.K_UP:    up = False
            if key==pygame.K_DOWN:  down = False
            if key==pygame.K_LEFT:  left = False
            if key==pygame.K_RIGHT: right = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(pygame.mouse.get_pressed()) # dbg
            mx, my = pygame.mouse.get_pos()
    # update coordinates
    if up: cy -= 1
    if down: cy += 1
    if left: cx -= 1
    if right: cx += 1
    if mx > -1: cx = mx ; mx = -1
    if my > -1: cy = my ; my = -1

    # ---- render -----
    screen.fill((0,0,0))
    screen.blit(sprite, (cx, cy))
    pygame.display.flip()

    # sleep a while (run 30 frames per second max)
    clock.tick(30)


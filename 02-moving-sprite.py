import sys
import pygame

def make_img(buff, colors, pixel_size=1):
    """helper function to create sprite out of thin air (eh, of list of strings... ;])
       buff       list of strings, each char represents one pixel (space == transparent)
       colors     dict of char to RGB mappings ie. {'B': (0,0,0)}
       pixel_size int multiplying result image size
       @returns   pygame.Surface
    """
    maxLen = 0
    for ln in buff:
        if len(ln) > maxLen:
            maxLen = len(ln)
    s = pygame.Surface((pixel_size*maxLen, pixel_size*len(buff)), )
    s.fill((255,0,255))
    for y,ln in enumerate(buff):
        for x,px in enumerate(ln):
            if px == ' ':
                continue
            if colors.has_key(px):
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
' RRRRR  ',
'R  R  R ',
'RrrRrrR ',
'RRRRRRR ',
'rRRRRRr ',
'  RRRr  ',
'   RRR  ',
'    rRRr',
], palette, 2)

cx = 200
cy = 100

# controls:
# keys
left = False
right = False
up = False
down = False
# mouse coords
mx = my = -1

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit(0)
        if event.type == pygame.KEYDOWN:
            key = event.key
            #print key
            if key==27:  sys.exit(0) #Esc
            if key==273: up = True
            if key==274: down = True
            if key==276: left = True
            if key==275: right = True
#            if key==305: self.fire = True
        if event.type == pygame.KEYUP:
            key = event.key
            if key==273: up = False
            if key==274: down = False
            if key==276: left = False
            if key==275: right = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            #print pygame.mouse.get_pressed()
            mx, my = pygame.mouse.get_pos()
    #endfor

    # update
    if up: cy -= 1
    if down: cy += 1
    if left: cx -= 1
    if right: cx += 1
    if mx > -1: cx = mx ; mx = -1
    if my > -1: cy = my ; my = -1

    # render
    screen.fill((0,0,0))
    screen.blit(sprite, (cx, cy))
    pygame.display.flip()

    # sleep a while (run 30 frames per second max)
    clock.tick(30)


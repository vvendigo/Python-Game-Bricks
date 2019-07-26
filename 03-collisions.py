import pygame

def make_img(buff, colors, pixel_size=1):
    """helper function to create sprite out of thin air (eh, of list of strings... ;])
       buff       list of strings, each char represents one pixel (space == transparent)
       colors     dict of char to RGB mappings ie. {'B': (0,0,0), 'W': (255,255,255)}
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

def collides(x1, y1, sf1, x2, y2, sf2):
    # we have to set positions to obtained sprite (surface) rects
    r1 = sf1.get_rect()
    r1.left, r1.top = x1, y1
    r2 = sf2.get_rect()
    r2.left, r2.top = x2, y2
    # and then use build-in method
    return r1.colliderect(r2)

# setup
pygame.init()
screen = pygame.display.set_mode((640,480), pygame.HWSURFACE|pygame.DOUBLEBUF)
clock = pygame.time.Clock()

palette = {
    'R': (255, 0, 0),
    'G': (0, 255, 0),
}

sprite = make_img([
'rRRRRRRr',
'R  RR  R',
'R  RR  R',
'RRRRRRRR',
'R R R R ',
'        ',
' R R R R',
'  RRRRR ',
], palette, 2)

human = make_img([
'   GG   ',
'   GG   ',
' GGGGGG ',
'G GGGG G',
'G  GG  G',
'G G  G G',
'  G  G  ',
'  G  G  ',
], palette)

# game objects are represented just by coordinates

# monster ("hero")
cx, cy = 200, 100

# humans
humans = [
    (30, 30),
    (320, 110),
    (120, 300),
    (60, 350),
    (500, 200),
]

# controls:
# keys
left = False
right = False
up = False
down = False
quit = False
# mouse coords
mx = my = -1

r = sprite.get_rect()
r.top = 10

while not quit:
    # ---- update ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT: quit = True
        if event.type == pygame.KEYDOWN:
            key = event.key
            #print key
            if key==pygame.K_ESCAPE:  quit = True
            if key==pygame.K_UP:    up = True
            if key==pygame.K_DOWN:  down = True
            if key==pygame.K_LEFT:  left = True
            if key==pygame.K_RIGHT: right = True
        if event.type == pygame.KEYUP:
            key = event.key
            if key==pygame.K_UP:    up = False
            if key==pygame.K_DOWN:  down = False
            if key==pygame.K_LEFT:  left = False
            if key==pygame.K_RIGHT: right = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            #print pygame.mouse.get_pressed()
            mx, my = pygame.mouse.get_pos()

    # check collision, remove colliding (killed) humans
    i = 0
    while i < len(humans):
        x, y = humans[i]
        if collides(x, y, human, cx, cy, sprite):
            #print 'collision', x, y
            del humans[i]
        else:
            i += 1
    # update player coordinates
    if up: cy -= 1
    if down: cy += 1
    if left: cx -= 1
    if right: cx += 1
    if mx > -1: cx = mx ; mx = -1
    if my > -1: cy = my ; my = -1

    # ---- render ----
    screen.fill((0,0,0))
    for x, y in humans:
        screen.blit(human, (x, y))
    screen.blit(sprite, (cx, cy))
    pygame.display.flip()

    # sleep a while (run 30 frames per second max)
    clock.tick(30)


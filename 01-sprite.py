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

palette = {
    'G': (0, 255, 0), # just green color
}

sprite = make_img([
'   GG   ',
'   GG   ',
' GGGGGG ',
'G GGGG G',
'G  GG  G',
'G G  G G',
'  G  G  ',
'  G  G  ',
], palette)

# clear the screen
screen.fill((0,0,0))
# draw the sprite at x=200, y=100
screen.blit(sprite, (200, 100))
# draw the sprite multiple times
for x in (10, 20, 40, 80, 160):
    screen.blit(sprite, (x, 200))

pygame.display.flip()


# just wait for window close event or Esc
while 1:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        break
    if event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
        break



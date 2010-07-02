import pygame
import sys, math
from random import randint

pygame.init()

width = 300
height = 300

screen = pygame.display.set_mode((width,height), pygame.HWSURFACE|pygame.DOUBLEBUF)

clock = pygame.time.Clock()

left = False
right = False
up = False
down = False


R = 100
r = 20
O = 25

for t in xrange(0,256):
    t = t*math.pi/128
    #(moving circle outside the fixed circle)
    x = (R+r)*math.cos(t) - O*math.cos(((R+r)/r)*t)
    y = (R+r)*math.sin(t) - O*math.sin(((R+r)/r)*t)
    screen.set_at((width/2+int(x),height/2+int(y)), (255,0,0))
    #(moving circle inside the fixed circle)
    x = (R-r)*math.cos(t) + O*math.cos(((R-r)/r)*t)
    y = (R-r)*math.sin(t) - O*math.sin(((R-r)/r)*t)
    screen.set_at((width/2+int(x),height/2+int(y)), (0,0,255))

    pygame.display.flip()
#endfor

tickCnt = 0

while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit(0)
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key==27:  sys.exit(0) #self.exit = True
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


    pygame.display.flip()

    clock.tick(30)
    tickCnt += 1
    if tickCnt > 5:
#        for p in points:
#            p.behave()
        tickCnt = 0
    #endif
#endwhile

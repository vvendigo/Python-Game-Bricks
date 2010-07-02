import pygame
import sys, math
from random import randint, random

pygame.init()

width = 250
height = 250

screen = pygame.display.set_mode((width,height), pygame.HWSURFACE|pygame.DOUBLEBUF)

clock = pygame.time.Clock()

left = False
right = False
up = False
down = False

def interpolate(x0, x1, alpha):
    return (1.0 - alpha) * x0 + alpha * x1
#enddef


class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.bmp = pygame.Surface((w, h)).convert()

        self.generate()

        #self.generateOld(0,0,w,h,128)
        self.addWater()
    #enddef

    def generate(self):
        octaveCount = 6
        persistance = 0.6

        w = self.w
        h = self.h

        smooth = []
        baseNoise = self.generateBaseNoise(w, h)
        for i in xrange(0, octaveCount):
            smooth.append(self.generateSmoothNoise(baseNoise, octaveCount-i, w, h))
        #endfor

        perlinNoise = []
        for i in xrange(0, w):
            ln = []
            for j in xrange(0, h):
                ln.append(0.0)
            perlinNoise.append(ln)
        #endfor

        amplitude = 1.0
        #blend noise together
        for k in xrange(0, octaveCount):
            amplitude *= persistance

            for i in xrange(0, w):
                for j in xrange(0, h):
                    perlinNoise[i][j] += smooth[k][i][j] * amplitude
            #endfor
        #endfor
        # normalisation
        maxVal = 0.0
        for col in perlinNoise:
            for val in col:
                if val > maxVal:
                    maxVal = val
        for i in xrange(0, w):
            for j in xrange(0, h):
                perlinNoise[i][j] /= maxVal
        #endfor

        # draw
        for i in xrange(0, w):
            for j in xrange(0, h):
                c = int(255*perlinNoise[i][j])
                self.bmp.set_at((i,j), (c,c,c))
        #endfor
    #enddef

    def generateBaseNoise(self, w, h):
        baseNoise = []
        for i in xrange(0, w):
            ln = []
            for j in xrange(0, h):
                ln.append(random())
            baseNoise.append(ln)
        #endfor
        return baseNoise
    #endfor

    def generateSmoothNoise(self, baseNoise, k, w, h):

        smooth = []
        for i in xrange(0, w):
            ln = []
            for j in xrange(0, h):
                ln.append(0.0)
            smooth.append(ln)
        #endfor

        samplePeriod = 1 << k # calculates 2 ^ k
        sampleFrequency = 1.0 / samplePeriod
        for i in xrange(0, w):
            #calculate the horizontal sampling indices
            sample_i0 = (i / samplePeriod) * samplePeriod
            sample_i1 = (sample_i0 + samplePeriod) % w #wrap around
            horizontal_blend = (i - sample_i0) * sampleFrequency
            for j in xrange(0, h):
                #calculate the vertical sampling indices
                sample_j0 = (j / samplePeriod) * samplePeriod
                sample_j1 = (sample_j0 + samplePeriod) % h #wrap around
                vertical_blend = (j - sample_j0) * sampleFrequency
                #blend the top two corners
                top = interpolate(baseNoise[int(sample_i0)][int(sample_j0)],\
                    baseNoise[int(sample_i1)][int(sample_j0)], horizontal_blend)
                #blend the bottom two corners
                bottom = interpolate(baseNoise[int(sample_i0)][int(sample_j1)],\
                    baseNoise[int(sample_i1)][int(sample_j1)], horizontal_blend)
                #final blend
                smooth[i][j] = interpolate(top, bottom, vertical_blend)
            #endfor
        #endfor

        return smooth
        # draw
        for i in xrange(0, w):
            for j in xrange(0, h):
                c = int(255*smooth[i][j])
                self.bmp.set_at((i,j), (c,c,c))
        self.show()
    #enddef

    def addWater(self, level = 128):
        for x in xrange(0,self.w):
            for y in xrange(0,self.h):
                c = self.bmp.get_at((x,y))
                if c[0] < level:
                    self.bmp.set_at((x,y), (c[0],c[1],250))
    #enddef

    def addRivers(self):
        spillProb = 2
        seeds = []
        for i in xrange(0,(self.w*self.h)/500):
            seeds.append((randint(0,self.w-1), randint(0,self.h-1)))
        while len(seeds)>0:# and len(seeds)<20000:
            seeds2 = []
            for (x,y) in seeds:
                #print s
                c1 = self.bmp.get_at((x,y))
                if c1[2]==255:
                    continue
                self.bmp.set_at((x,y), (c1[0],c1[1],255))
                spill = randint(0,10) < spillProb
                if x>0:
                    c2 = self.bmp.get_at((x-1,y))
                    if c2[2]!=255 and (c2[0]<c1[0] or (c2[0]==c1[0] and spill)):
                        seeds2.append((x-1,y))
                spill = randint(0,10) < spillProb
                if y>0:
                    c2 = self.bmp.get_at((x,y-1))
                    if c2[2]!=255 and (c2[0]<c1[0] or (c2[0]==c1[0] and spill)):
                        seeds2.append((x,y-1))
                spill = randint(0,10) < spillProb
                if x+1<self.w:
                    c2 = self.bmp.get_at((x+1,y))
                    if c2[2]!=255 and (c2[0]<c1[0] or (c2[0]==c1[0] and spill)):
                        seeds2.append((x+1,y))
                spill = randint(0,10) < spillProb
                if y+1<self.h:
                    c2 = self.bmp.get_at((x,y+1))
                    if c2[2]!=255 and (c2[0]<c1[0] or (c2[0]==c1[0] and spill)):
                        seeds2.append((x,y+1))

            #endfor
            seeds = seeds2
            # dbg
            #print len(seeds)
            self.show()
        #endwhile
    #enddef

    def show(self):
        global screen
        self.draw(screen)
        pygame.display.flip()
    #enddef

    def draw(self, screen):
        screen.blit(self.bmp, (0,0))
    #enddef
#endclass


map = Map(width, height)

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

    if up: points[ctrP].my -= 1
    if down: points[ctrP].my += 1
    if left: points[ctrP].mx -= 1
    if right: points[ctrP].mx += 1


    #screen.fill((0,0,0))
    map.draw(screen)
    pygame.display.flip()

    clock.tick(30)
    tickCnt += 1
    if tickCnt > 100:
        map.generate()
        map.addWater(randint(50,200))
        #map.addRivers()
#        for p in points:
#            p.behave()
        tickCnt = 0
    #endif
#endwhile

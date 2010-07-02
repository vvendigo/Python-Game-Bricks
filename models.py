import pygame
import sys, math, random

pygame.init()


class Point:

    def __init__(self, x, y, d, col, leaders=[]):
        self.x = x
        self.y = y
        self.d = d
        self.c = col
        self.mx = self.amx = 0
        self.my = self.amy = 0
        self.setLeaders(leaders)
    #enddef

    def setLeaders(self, leaders):
        self.leaders = []
        distTotal = 0
        for l in leaders:
            self.leaders.append(l)
            distTotal += l.getDist(self.x, self.y)
        #endfor
        self.dists = []
        for l in self.leaders:
            self.dists.append( l.getDist(self.x, self.y) )
            #self.dists.append((1.0 - l.getDist(self.x, self.y)/float(distTotal)))
    #enddef

    def getDist(self, x, y):
        dx = self.x - x
        dy = self.y - y
        return math.sqrt(float(dx**2 + dy**2))
    #enddef

    def draw(self, to):
        if not self.c:
            return
        self.amx = self.mx
        self.amy = self.my
        for i, l in enumerate(self.leaders):
            a = self.dists[i]
            if a==0.0:
                continue
            mx = l.amx
            if math.fabs(mx) < a:
                mx = (mx/a)**2 * mx
            my = l.amy
            if math.fabs(my) < a:
                my = (my/a)**2 * my
            self.amx += mx
            self.amy += my
        #endfor
        x = self.x + self.amx
        y = self.y + self.amy

        to.fill(self.c, (x-self.d/2, y-self.d/2, self.d, self.d))
    #enddef

    def behave(self):
        pass
    #enddef
#endclass

class PointRandom(Point):

    def behave(self):
        self.mx = random.randint(-1,1)
        self.my = random.randint(-1,1)
    #enddef

#endclass


points = []
# leaders
#points.append(Point(150,100,4,(250,210,200, 200)))
points.append(Point(150,150,4,(250,210,200, 200)))
#points.append(Point(150,200,4,(250,210,200, 200)))
leads = [points[0]]


#points[1].setLeaders([points[0],points[2]])
ctrP = 0
# other
for i in xrange(0, 10):
    prev = [points[0]]
    for j in xrange(10, 60, 20):
        x = math.cos(math.pi/5*i) * j
        y = math.sin(math.pi/5*i) * j
        p = PointRandom(150+x,150+y,8,(200-j,200-j,200+random.randint(-20,20), 200), prev)
        points.append(p)
        prev = [p]

screen = pygame.display.set_mode((640,480), pygame.HWSURFACE|pygame.DOUBLEBUF)
clock = pygame.time.Clock()

left = False
right = False
up = False
down = False

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            #print pygame.mouse.get_pressed()
            (cx, cy) = pygame.mouse.get_pos()
    #endfor

    if up: points[ctrP].my -= 1
    if down: points[ctrP].my += 1
    if left: points[ctrP].mx -= 1
    if right: points[ctrP].mx += 1


    screen.fill((0,0,0))
    for p in points:
        p.draw(screen)
    #endfor
    pygame.display.flip()

    clock.tick(30)
    tickCnt += 1
    if tickCnt > 5:
        for p in points:
            p.behave()
        tickCnt = 0
    #endif

#endwhile

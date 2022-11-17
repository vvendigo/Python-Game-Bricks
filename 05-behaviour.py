#
# Nemesis Entering: advanced behaviour
#
import pygame

# setup
pygame.init()
screen = pygame.display.set_mode((640,480), pygame.HWSURFACE|pygame.DOUBLEBUF)
FPS = 30 # game frame rate
MSPF = int(1000/FPS) # millisec per frame


def make_img(buff, colors, pixel_size=1):
    """helper function to create sprite out of thin air (eh, of list of strings... ;])
       buff       list of strings, each char represents one pixel (space == transparent)
       colors     dict of char to RGB mappings ie. {'B': (0,0,0), 'W': (255,255,255)}
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

class Controls:
    def __init__(self):
        # keys
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.quit = False
        # mouse coords
        self.mx = -1
        self.my = -1

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.quit = True
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key==pygame.K_ESCAPE: self.quit = True
                if key==pygame.K_UP:     self.up = True
                if key==pygame.K_DOWN:   self.down = True
                if key==pygame.K_LEFT:   self.left = True
                if key==pygame.K_RIGHT:  self.right = True
            if event.type == pygame.KEYUP:
                key = event.key
                if key==pygame.K_UP:    self.up = False
                if key==pygame.K_DOWN:  self.down = False
                if key==pygame.K_LEFT:  self.left = False
                if key==pygame.K_RIGHT: self.right = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mx, self.my = pygame.mouse.get_pos()

controls = Controls()

class GameObject(object):
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.alive = True

    def get_rect(self):
        r = self.sprite.get_rect()
        r.left, r.top = self.x, self.y
        return r

    def collides(self, other_gobj):
        return other_gobj.alive and self.get_rect().colliderect(other_gobj.get_rect())

    def draw(self):
        screen.blit(self.sprite, (self.x, self.y))

    def die(self):
        self.alive = False

    def behave(self):
        pass

class Hero(GameObject):
    def behave(self):
        if controls.up:    self.y -= 1
        if controls.down:  self.y += 1
        if controls.left:  self.x -= 1
        if controls.right: self.x += 1
        if controls.mx > -1: self.x = controls.mx ; controls.mx = -1
        if controls.my > -1: self.y = controls.my ; controls.my = -1

    def die(self):
        game_objs.append(BouncingObject(120, 120, spr_gameover, 3, 0))
        super(Hero, self).die()

class Victim(GameObject):
    def behave(self):
        if self.collides(hero):
            self.die()

class BouncingObject(GameObject):
    def __init__(self, x, y, spr, dx, dy):
        super(BouncingObject, self).__init__(x, y, spr)
        self.dx = dx
        self.dy = dy

    def behave(self):
        if self.x + self.dx < 0 or self.x + self.dx + self.get_rect().width > screen.get_rect().width:
            self.dx *= -1
        if self.y + self.dy < 0 or self.y + self.dy + self.get_rect().height > screen.get_rect().height:
            self.dy *= -1
        self.x += self.dx
        self.y += self.dy

class Nemesis(BouncingObject):
    def behave(self):
        super(Nemesis, self).behave()
        if self.collides(hero):
            hero.die()


palette = {
    'R': (255, 0, 0),
    'G': (0, 255, 0),
    'Y': (255, 255, 0),
    'W': (255, 255, 255),
}

spr_monster = make_img([
'rRRRRRRr',
'R  RR  R',
'R  RR  R',
'RRRRRRRR',
'R R R R ',
'        ',
' R R R R',
'  RRRRR ',
], palette, 2)

spr_human = make_img([
'   GG   ',
'   GG   ',
' GGGGGG ',
'G GGGG G',
'G  GG  G',
'G G  G G',
'  G  G  ',
'  G  G  ',
], palette)

spr_nemesis = make_img([
'   YY   ',
'   YY   ',
' YYYYYY ',
'Y YYYY Y',
'Y  YY  Y',
'Y Y  Y Y',
'  Y  Y  ',
'  Y  Y  ',
], palette, 4)

spr_gameover = make_img([
' WW   WW  W   W WWW    WW  W   W WWW WWW ',
'W    W  W WW WW W     W  W W   W W   W  W',
'W WW WWWW W W W WWW   W  W  W W  WWW WWW',
'W  W W  W W   W W     W  W  W W  W   W  W',
' WW  W  W W   W WWW    WW    W   WWW W  W',
], palette, 4)

hero = Hero(200, 100, spr_monster) # preserve hero refference
game_objs = [
    hero,
    Victim(30, 30, spr_human),
    Victim(320, 110, spr_human),
    Victim(120, 300, spr_human),
    Victim(60, 350, spr_human),
    Victim(500, 200, spr_human),
    Nemesis(500, 400, spr_nemesis, 3, 4)
]

clock = pygame.time.Clock()
elapsed = 0

while not controls.quit:
    # ---- render ----
    screen.fill((0,0,0))
    for o in game_objs:
        o.draw()
    pygame.display.flip()

    # wait / update clock
    elapsed += clock.tick(FPS)

    # ---- update ----
    controls.update()
    while elapsed >= MSPF:
        elapsed -= MSPF
        i = 0
        while i < len(game_objs):
            o = game_objs[i]
            o.behave()
            if not o.alive:
                del game_objs[i]
            else:
                i += 1


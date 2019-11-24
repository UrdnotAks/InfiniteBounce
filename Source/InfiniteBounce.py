import pygame, random, sys, math
import pygame.gfxdraw
from time import *
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

fontColor = (0, 139, 139)
bgColor = (0, 0, 0)
(width, height) = (500, 500)
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("INFINITE BOUNCE")
font = pygame.font.Font(resource_path("digital-7.ttf"), 40)
crash_sound = pygame.mixer.Sound(resource_path("crash.wav"))
crash_sound.set_volume(0.5)
bounce_sound = pygame.mixer.Sound(resource_path("bounce.wav"))
bounce_sound.set_volume(0.5)

bounce = 0
score = 0
no_of_particles = 2


def gameover():
    gameover = font.render("!GAME OVER LOSER!", True, fontColor)
    scoretext = font.render(str(score), True, fontColor)
    restartimg = pygame.image.load(resource_path("restart.png"))
    imgx, imgy = ((width // 2) - 32, (height - (height // 4) - 32))
    rect = pygame.Rect((imgx, imgy), (imgx + 64, imgy + 64))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mp = pygame.mouse.get_pos()
                if rect.collidepoint(mp):
                    main()
        screen.fill(bgColor)
        screen.blit(gameover, ((width - gameover.get_width()) // 2, (height - gameover.get_height()) // 4))
        screen.blit(scoretext, ((width - scoretext.get_width()) // 2, (height - scoretext.get_height()) // 2))
        screen.blit(restartimg, rect)
        pygame.display.flip()


def findparticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x - x, p.y - y) <= p.size:
            return p


def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    distance = math.hypot(dx, dy)
    if distance < p1.size + p2.size:
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent
        angle1 = 2 * tangent - p1.angle
        angle2 = 2 * tangent - p2.angle
        p1.angle = angle1
        p2.angle = angle2
        p1.x += math.sin(angle)
        p1.y -= math.sin(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)
        crash_sound.play()
        sleep(1)
        gameover()


def create_particle():
    size = random.randint(15, 25)
    colour = (0, 0, 255)
    x = random.randint(100 + size, width - 100 - size)
    y = random.randint(100 + size, height - 100 - size)
    particle = Particle(x, y, size, colour)
    particle.speed = 0
    particle.angle = 0
    return particle


class Particle:
    def __init__(self, x, y, size, colour):
        self.x = x
        self.y = y
        self.size = size
        self.colour = colour
        self.speed = 1
        self.angle = 0

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size)
        pygame.gfxdraw.circle(screen, int(self.x), int(self.y), self.size, self.colour)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

    def bounce(self):
        if self.x > width - 100 - self.size:
            self.x = 2 * (width - 100 - self.size) - self.x
            self.angle = -self.angle
            bounce_sound.play()
            return 1

        elif self.x < 100 + self.size:
            self.x = 2 * (100 + self.size) - self.x
            self.angle = -self.angle
            bounce_sound.play()
            return 1

        if self.y > height - 100 - self.size:
            self.y = 2 * (height - 100 - self.size) - self.y
            self.angle = math.pi - self.angle
            bounce_sound.play()
            return 1

        elif self.y < 100 + self.size:
            self.y = 2 * (100 + self.size) - self.y
            self.angle = math.pi - self.angle
            bounce_sound.play()
            return 1

        else:
            return 0


def update_score():
    scoretext = font.render(str(score), True, fontColor)
    screen.fill((bgColor), rect=scoretext.get_rect(topleft=((width - (scoretext.get_width() * 2)), (scoretext.get_height()))))
    screen.blit(scoretext, ((width - scoretext.get_width()) // 2, scoretext.get_height() // 2))


def updateFtimer(time):
    pygame.gfxdraw.circle(screen, width // 4, height - 50, 32, (0, 0, 0))
    timertext = font.render(str(time), True, fontColor)
    screen.blit(timertext, ((width // 4) - (timertext.get_width() // 2), 450 - (timertext.get_height() // 2)))


def updateMtimer(time):
    pygame.gfxdraw.circle(screen, width - width // 4, height - 50, 32, (0, 0, 0))
    timertext = font.render(str(time), True, fontColor)
    screen.blit(timertext, (width - (width // 4) - (timertext.get_width() // 2), 450 - (timertext.get_height() // 2)))


def main():
    ptlist = [(100, 100), (100, height - 100), (width - 100, height - 100), (width - 100, 100)]

    freezeimg = pygame.image.load(resource_path("freeze.png"))
    freezex, freezey = ((width // 4) - 32, (height - 82))
    freeze = pygame.Rect((freezex, freezey), (freezex + 64, freezey + 64))

    mergeimg = pygame.image.load(resource_path("merge.png"))
    mergex, mergey = (width - (width // 4) - 32, (height - 82))
    merge = pygame.Rect((mergex, mergey), (mergex + 64, mergey + 64))
    clock = pygame.time.Clock()

    global no_of_particles
    no_of_particles = 2
    global score
    score = 0
    global bounce
    particles = []

    bounce = 0
    check_bounce = 0

    freezeStart = 0
    freezeSel = False

    mergeStart = 0
    mergeSel = False

    size = 10
    colour = (255, 0, 0)
    x = random.randint(100 + size, width - 100 - size)
    y = random.randint(100 + size, height - 100 - size)
    particle = Particle(x, y, size, colour)
    particle.speed = 2.5
    particle.angle = random.uniform(0, math.pi * 2)
    particles.append(particle)

    for i in range(no_of_particles):
        particles.append(create_particle())
    sel_particle = None

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                (mousex, mousey) = pygame.mouse.get_pos()
                if freeze.collidepoint((mousex, mousey)) and not freezeSel:
                    freezeStart = pygame.time.get_ticks() / 1000
                    freezeSel = True
                    particles[0].speed *= 0.5

                if merge.collidepoint((mousex, mousey)) and not mergeSel:
                    mergeStart = pygame.time.get_ticks() / 1000
                    mergeSel = True
                    index = no_of_particles // 2
                    del (particles[index + 1:])
                    for p in particles:
                        p.size += int(p.size / 2)

                sel_particle = findparticle(particles[1:], mousex, mousey)

            elif event.type == pygame.MOUSEBUTTONUP:
                sel_particle = None

        if sel_particle:
            (mousex, mousey) = pygame.mouse.get_pos()
            sel_particle.x = mousex
            sel_particle.y = mousey

        screen.fill(bgColor)
        pygame.draw.aalines(screen, fontColor, True, ptlist, 5)

        if not freezeSel:
            screen.blit(freezeimg, freeze)
        if not mergeSel:
            screen.blit(mergeimg, merge)

        if int((pygame.time.get_ticks() / 1000) - freezeStart) == 10 and freezeSel:
            particles[0].speed = 2.5

        if (pygame.time.get_ticks() // 1000) - freezeStart <= 20 and freezeSel:
            updateFtimer(int((pygame.time.get_ticks() / 1000) - freezeStart))
        else:
            freezeStart = 0
            freezeSel = False

        if (pygame.time.get_ticks() // 1000) - mergeStart <= 20 and mergeSel:
            updateMtimer(int((pygame.time.get_ticks() / 1000) - mergeStart))
        else:
            mergeStart = 0
            mergeSel = False

        update_score()

        for i, particle in enumerate(particles):
            particle.move()
            bounceval = particle.bounce()
            if i != 0 and bounceval == 1:
                sleep(1)
                gameover()
            bounce += bounceval
            for particle2 in particles[i + 1:]:
                collide(particles[0], particle2)
            particle.display()

        if bounce != check_bounce:
            score += 1
            if score != 0 and score % 5 == 0:
                no_of_particles += 1
                particles.append(create_particle())
            check_bounce = bounce
            update_score()
            pygame.display.flip()

        clock.tick(60)
        pygame.display.flip()


title = font.render("INFINITE BOUNCE", True, fontColor)
startimg = pygame.image.load(resource_path("start.png"))
imgx, imgy = ((width // 2) - 32, (height // 2 + 32))
rect = pygame.Rect((imgx, imgy), (imgx + 64, imgy + 64))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mp = pygame.mouse.get_pos()
            if rect.collidepoint(mp):
                main()
    screen.fill(bgColor)
    screen.blit(title, ((width - title.get_width()) // 2, height // 2 - title.get_height() - 64))
    screen.blit(startimg, rect)
    pygame.display.flip()

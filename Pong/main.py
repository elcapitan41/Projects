# Modules
import sys, pygame
from pygame.locals import *
from config import *
# from classes import *

 
# Constants

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(BALL, transparent=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.centery = SCREEN_HEIGHT / 2
        self.speed = [0.5, -0.5]
 
    def update(self, time, player, cpu, score):
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time
 
        if self.rect.left <= 0:
            score[1] += 1
        if self.rect.right >= SCREEN_WIDTH:
            score[0] += 1
 
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time
 
        if pygame.sprite.collide_rect(self, player):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
 
        if pygame.sprite.collide_rect(self, cpu):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
 
        return score
        
 
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(PADDLE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = SCREEN_HEIGHT / 2
        self.speed = .3 + LEVEL/25
 
    def move(self, time, keys):
        if self.rect.top >= 0:
            if keys[K_UP]:
                self.rect.centery -= self.speed * time
        if self.rect.bottom <= SCREEN_HEIGHT:
            if keys[K_DOWN]:
                self.rect.centery += self.speed * time
 
    def AI(self, time, ball):
        if ball.speed[0] >= 0 and ball.rect.centerx >= SCREEN_WIDTH/2:
            if self.rect.centery < ball.rect.centery:
                self.rect.centery += self.speed * time
            if self.rect.centery > ball.rect.centery:
                self.rect.centery -= self.speed * time
 
# ---------------------------------------------------------------------
 
# Functions
# ---------------------------------------------------------------------
 
def load_image(filename, width=None, height=None, transparent=False):
        try: image = pygame.image.load(filename)
        except pygame.error as message:
                raise SystemExit
        image = image.convert()
        if transparent:
                color = image.get_at((0,0))
                image.set_colorkey(color, RLEACCEL)
        if width and height:
            image = pygame.transform.scale(image, (width, height))
        return image
 
def text(text, posx, posy, color=FONT_COLOR):
    font = pygame.font.Font(FONT, 50)
    draw = pygame.font.Font.render(font, text, 1, color)
    draw_rect = draw.get_rect()
    draw_rect.centerx = posx
    draw_rect.centery = posy
    return draw, draw_rect
 
# ---------------------------------------------------------------------
 
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
 
    background_image = load_image(BACKGROUND, SCREEN_WIDTH, SCREEN_HEIGHT)
    ball = Ball()
    player = Paddle(SCREEN_WIDTH * .05)
    cpu = Paddle(SCREEN_WIDTH - SCREEN_WIDTH * .05)
 
    clock = pygame.time.Clock()
 
    score = [0, 0]
 
    while True:
        time = clock.tick(60)
        keys = pygame.key.get_pressed()
        for events in pygame.event.get():
            if events.type == QUIT:
                sys.exit(0)
 
        score = ball.update(time, player, cpu, score)
        player.move(time, keys)
        cpu.AI(time, ball)
 
        draw_score, draw_score_rect = text("{}  :  {}".format(score[0], score[1]), SCREEN_WIDTH/2, SCREEN_HEIGHT/6)
        
        screen.blit(background_image, (0, 0))
        screen.blit(draw_score, draw_score_rect)
        screen.blit(ball.image, ball.rect)
        screen.blit(player.image, player.rect)
        screen.blit(cpu.image, cpu.rect)
        pygame.display.flip()
    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()
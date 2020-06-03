import sys, pygame
from pygame.locals import *
from config import *

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
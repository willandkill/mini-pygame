# coding=utf-8

import sys
import pygame
import random
import math
import traceback

pygame.init()
size = width,height = 800,600
black = 1,0,0
transparent = 0,0,0
white = 255,255,255
blue = 20,10,125
red = 255,0,0
yellow = 255,255,0
green = 0,255,0
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pause = False

def RandBall():
    color = [random.randint(100,255),random.randint(100,255),random.randint(100,255)]
    radius = random.randint(10,100)
    pos = [random.randint(0,width-2*radius),random.randint(0,height-2*radius)]
    speed = [random.randint(-7,7),random.randint(-7,7)]
    return color,radius,pos,speed

class Ball(pygame.sprite.Sprite):
    cnt = 0
    def __init__(self,color,radius,pos,speed):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.radius = radius
        self.mass = math.pi*(self.radius**2)
        self.name = Ball.cnt
        if 0:
            self.image = pygame.Surface([2*self.radius]*2,pygame.SRCALPHA,32)
        else:
            self.image = pygame.Surface([2*self.radius]*2)
            self.image.set_colorkey(transparent)
        self.font = pygame.font.Font(None,30)
        self.draw_background()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.speed = speed
        Ball.cnt += 1
    def __str__(self):
        return "Ball %s %s %s"%(self.name,self.rect.center,self.radius)
    def draw_background(self):
        self.image.fill(transparent)
        pygame.draw.circle(self.image,self.color,[self.radius]*2,self.radius)
        text = self.font.render(u'%s'%self.name,True,black)
        text_rect = text.get_rect(center=[self.radius]*2)
        self.image.blit(text,text_rect)
    def update(self,_hitballs):
        global pause
        self.draw_background()
        pygame.draw.line(self.image,yellow,[self.radius]*2,[self.radius*(1+s if abs(s)>=1 else 1) for s in self.speed],4)
        for _ball in _hitballs:
            dx = _ball.rect.center[0] - self.rect.center[0]
            dy = _ball.rect.center[1] - self.rect.center[1]
            pygame.draw.aaline(self.image,[1,0,0],[self.radius]*2,[dx+self.radius,dy+self.radius])
            radian = math.atan2(dy,dx)
            print(self,"hit",_ball,dx,dy,math.degrees(radian))
            p_vx = self.speed[0]*math.cos(radian)
            v_vx = self.speed[0]*math.sin(radian)
            p_vy = self.speed[1]*math.sin(radian)
            v_vy = self.speed[1]*math.cos(radian)
            print("vx = %s, vector = %s, %s"%(self.speed[0],p_vx,v_vx))
            print("vy = %s, vector = %s, %s"%(self.speed[1],p_vy,v_vy))
            veloce_radian = math.atan2(self.speed[1],self.speed[0])
            reflect_radian = 2*(radian-veloce_radian)+math.pi
            reflect_en = False
            print("veloce  degree %s"%math.degrees(veloce_radian))
            print("radian  degree %s"%math.degrees(radian))
            print("reflect degree %s"%math.degrees(reflect_radian))
            print("reflect is %s"%reflect_en)
            if (abs(veloce_radian)<=math.pi/2) and ((radian <= math.pi/2+veloce_radian) and (radian >= -math.pi/2+veloce_radian)):
                reflect_en = True
            elif (veloce_radian>=math.pi/2) and ((radian >= -math.pi/2+veloce_radian) or (radian <= -math.pi/2+veloce_radian-math.pi)):
                reflect_en = True
            elif (veloce_radian<=-math.pi/2) and ((radian >= math.pi/2+veloce_radian+math.pi) or (radian <= math.pi/2+veloce_radian)):
                reflect_en = True
            if reflect_en:
                xf = self.speed[0]*math.cos(reflect_radian)-self.speed[1]*math.sin(reflect_radian)
                yf = self.speed[0]*math.sin(reflect_radian)+self.speed[1]*math.cos(reflect_radian)
            else:
                xf,yf = self.speed[0],self.speed[1]
            self.speed = [xf,yf]
            # pause = True
            print("---------")
        if self.rect.left < 0 or self.rect.right > width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speed[1] = -self.speed[1]
        self.rect = self.rect.move(self.speed)
        pygame.draw.line(self.image,green,[self.radius]*2,[self.radius*(1+s if abs(s)>=1 else 1) for s in self.speed],4)
        # print(self.rect.left,self.rect.top,self.rect.right,self.rect.bottom,self.speed)

class Board(pygame.sprite.Sprite):
    def __init__(self,target):
        pygame.sprite.Sprite.__init__(self)
        self.target = target
        self.color = self.target.color
        self.size = self.width,self.height = 80,50
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font(None,30)
        self.x = 0
        self.y = 0
    def update(self):
        self.image.fill(self.color)
        self.x = self.target.rect.center[0]
        self.y = self.target.rect.center[1]
        textx = self.font.render(u'x=%s'%self.x,True,self.color)
        texty = self.font.render(u'y=%s'%self.y,True,self.color)
        textx_rect = textx.get_rect(center=[self.width/2,self.height*0.3])
        texty_rect = texty.get_rect(center=[self.width/2,self.height*0.7])
        pygame.draw.rect(self.image,black,[5,5,self.width-10,self.height-10])
        self.image.blit(textx,textx_rect)
        self.image.blit(texty,texty_rect)
        self.rect.topleft = [pos+5 for pos in self.target.rect.center]

# stalin = pygame.image.load("D:\\DATA\\my_matlab\\stalin.jpg")
# stalin_rect = stalin.get_rect()
# ball = pygame.Surface((100,100))
# pygame.draw.circle(ball,white,[50,50],50)
# ballrect = ball.get_rect()
screen.fill(blue)
pygame.display.update()

balls = []
ball_list = [(white,50,[0,0],[3,3]),(red,30,[200,300],[-2,2])]
for _i in range(random.randint(2,4)):
    ball_list.append(RandBall())
for _color,_radius,_pos,_speed in ball_list:
    balls.append(Ball(_color,_radius,_pos,_speed))
ball_group = pygame.sprite.RenderUpdates()
board_group = pygame.sprite.RenderUpdates()
for ball in balls:
    ball_group.add(ball)
    board_group.add(Board(ball))

spacefont = pygame.font.SysFont("SimHei",50)
spacetext = spacefont.render(u'按空格键暂停',True,white)
spacerect = spacetext.get_rect(center=[width/2,height-25])

while True:
    while not pause:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = True
        # stalin_rect = stalin_rect.move(speed)
        # if stalin_rect.left < 0 or stalin_rect.right > width:
        #     speed[0] = -speed[0]
        # if stalin_rect.top < 0 or stalin_rect.bottom > height:
        #     speed[1] = -speed[1]
        # screen.blit(stalin,stalin_rect)
        # screen.blit(ball,ballrect)
        # pygame.display.flip()
        # pygame.display.update(ballrect)
        screen.fill(blue)
        screen.blit(spacetext,spacerect)
        hitballs = []
        for ball in balls:
            ball_group.remove(ball)
            hitballs.append(pygame.sprite.spritecollide(ball,ball_group,False,pygame.sprite.collide_circle))
            ball_group.add(ball)
        for ball in balls:
            ball.update(hitballs[0])
            hitballs.pop(0)
        for board in board_group:
            board.update()
        ball_rects = ball_group.draw(screen)
        board_rects = board_group.draw(screen)
        pygame.display.update(spacerect)
        pygame.display.update(ball_rects)
        pygame.display.update(board_rects)
    while pause:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = False
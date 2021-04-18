# coding=utf-8

import sys
import pygame
import random
import math

pygame.init()
pygame.font.init()

size = width,height = 800,600
transparent = 0,0,0
black = 1,0,0
white = 255,255,255
blue = 50,50,255
purple = 0xb1,0x5b,0xff
green = 50,255,50
yellow = 255,255,0
red = 255,0,0
orange = 255,100,0
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
screen.fill(black)
center_width = width/2
center_height = height/2

def draw_bg():
    screen.fill(black)
    pygame.draw.circle(screen,white,[center_width,center_height],10)
    pygame.draw.line(screen,white,[0,center_height],[width,center_height],5)
    pygame.draw.line(screen,white,[center_width,0],[center_width,height],5)
    bgfont = pygame.font.SysFont("SimHei",50)
    bgtext = bgfont.render(u'右键创建拖拽球，左键拖动',True,white)
    bgrect = bgtext.get_rect(center=[center_width,height - 25])
    screen.blit(bgtext,bgrect)

class DragBall(pygame.sprite.Sprite):
    def __init__(self,pos=None):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 5
        self.image = pygame.Surface([self.radius*2]*2)
        self.image.set_colorkey(transparent)
        self.rect = self.image.get_rect()
        self.rect.topleft = [width*0.75,height*0.25] if pos is None else pos
        self.color = [random.randint(50,200),random.randint(50,200),random.randint(50,200)]
        self.drag = False
        pygame.draw.circle(self.image,self.color,[self.radius]*2,self.radius)
    def update(self,pos):
        if math.sqrt((pos[0]-self.rect.center[0])**2+(pos[1]-self.rect.center[1])**2) <= self.radius or self.drag == True:
            self.rect.center = pos
            self.drag = True

class DragLine(pygame.sprite.Sprite):
    velocity = [[128,96],[-128,96],[128,-96],[-128,-96]]
    cnt = 0
    def __init__(self,target):
        pygame.sprite.Sprite.__init__(self)
        self.target = target
        self.color = self.target.color
        self.start = [center_width,center_height]
        self.vx,self.vy = DragLine.velocity[DragLine.cnt%4]
        self.x = 0
        self.y = 0
        DragLine.cnt += 1
    def update(self):
        _width = abs(self.target.rect.center[0]-self.start[0])
        _height = abs(self.target.rect.center[1]-self.start[1])
        self.image = pygame.Surface([_width,_height])
        self.image.set_colorkey(transparent)
        self.rect = self.image.get_rect()
        sop = []
        eop = []
        if self.target.rect.center[0]<=self.start[0] and self.target.rect.center[1]<=self.start[1]:
            self.rect.bottomright = self.start
            sop,eop = [0,0],[_width,_height]
        elif self.target.rect.center[0]<=self.start[0] and self.target.rect.center[1]>=self.start[1]:
            self.rect.topright = self.start
            sop,eop = [0,_height],[_width,0]
        elif self.target.rect.center[0]>=self.start[0] and self.target.rect.center[1]<=self.start[1]:
            self.rect.bottomleft = self.start
            sop,eop = [0,_height],[_width,0]
        elif self.target.rect.center[0]>=self.start[0] and self.target.rect.center[1]>=self.start[1]:
            self.rect.topleft = self.start
            sop,eop = [0,0],[_width,_height]
        pygame.draw.aaline(self.image,self.color,sop,eop,5) # 画出从中心点到target的连接线
        vlp = vlpw,vlph = (self.target.rect.center[0]+self.start[0])/2,(self.target.rect.center[1]+self.start[1])/2 # 连接线的中垂点
        if self.x != self.target.rect.center[0]-center_width or self.y != center_height-self.target.rect.center[1]:
            new_pos = True
        else:
            new_pos = False
        self.x = self.target.rect.center[0]-center_width
        self.y = center_height-self.target.rect.center[1]
        radian = math.atan2(self.y,self.x)
        p_vx = self.vx*math.cos(radian)
        p_vx_dx = p_vx*math.cos(radian)
        p_vx_dy = p_vx*math.sin(radian)
        v_vx = self.vx*math.sin(radian)
        v_vx_dx = v_vx*math.sin(radian)
        v_vx_dy = -v_vx*math.cos(radian)
        p_vy = self.vy*math.sin(radian)
        p_vy_dx = p_vy*math.cos(radian)
        p_vy_dy = p_vy*math.sin(radian)
        v_vy = self.vy*math.cos(radian)
        v_vy_dx = -v_vy*math.sin(radian)
        v_vy_dy = v_vy*math.cos(radian)
        veloce_radian = math.atan2(self.vy,self.vx)
        reflect_radian = 2*(radian - veloce_radian)+math.pi
        reflect_en = False
        if (abs(veloce_radian)<=math.pi/2) and ((radian <= math.pi/2+veloce_radian) and (radian >= -math.pi/2+veloce_radian)):
            reflect_en = True
        elif (veloce_radian>=math.pi/2) and ((radian >= -math.pi/2+veloce_radian) or (radian <= -math.pi/2+veloce_radian-math.pi)):
            reflect_en = True
        elif (veloce_radian<=-math.pi/2) and ((radian >= math.pi/2+veloce_radian+math.pi) or (radian <= math.pi/2+veloce_radian)):
            reflect_en = True
        if reflect_en:
            xf = self.vx*math.cos(reflect_radian)-self.vy*math.sin(reflect_radian)
            yf = self.vx*math.sin(reflect_radian)+self.vy*math.cos(reflect_radian)
        else:
            xf,yf = self.vx,self.vy
        # pygame.draw.line(screen,green,vlp,[vlp[0]+vx,vlp[1]-vy],4)
        pygame.draw.line(screen,green ,vlp,[vlp[0]+self.vx,vlp[1]],4) # x轴方向速度
        pygame.draw.line(screen,green ,vlp,[vlp[0],vlp[1]-self.vy],4) # y轴方向速度
        pygame.draw.line(screen,orange,vlp,[vlp[0]+p_vx_dx,vlp[1]-p_vx_dy],4)                     # x轴方向速度在平行于连接线方向上的分量
        pygame.draw.line(screen,orange,[vlp[0]+self.vx,vlp[1]],[vlp[0]+p_vx_dx,vlp[1]-p_vx_dy],1) # x轴方向速度到平行分量的垂线
        pygame.draw.line(screen,red   ,vlp,[vlp[0]+v_vx_dx,vlp[1]-v_vx_dy],4)                     # x轴方向速度在垂直于连接线方向上的分量
        pygame.draw.line(screen,red   ,[vlp[0]+self.vx,vlp[1]],[vlp[0]+v_vx_dx,vlp[1]-v_vx_dy],1) # x轴方向速度到垂直分量的垂线
        pygame.draw.line(screen,purple,vlp,[vlp[0]+p_vy_dx,vlp[1]-p_vy_dy],4)                     # y轴方向速度在平行于连接线方向上的分量
        pygame.draw.line(screen,purple,[vlp[0],vlp[1]-self.vy],[vlp[0]+p_vy_dx,vlp[1]-p_vy_dy],1) # y轴方向速度到平行分量的垂线
        pygame.draw.line(screen,blue  ,vlp,[vlp[0]+v_vy_dx,vlp[1]-v_vy_dy],4)                     # y轴方向速度在垂直于连接线方向上的分量
        pygame.draw.line(screen,blue  ,[vlp[0],vlp[1]-self.vy],[vlp[0]+v_vy_dx,vlp[1]-v_vy_dy],1) # y轴方向速度到垂直分量的垂线
        pygame.draw.line(screen,white ,vlp,[vlp[0]+xf,vlp[1]-yf],5)
        pygame.draw.line(screen,yellow,vlp,[vlp[0]+self.vx,vlp[1]-self.vy],5)
        dx,dy = vlpw-self.start[0],vlph-self.start[1]
        if new_pos:
            print("dx = %s, vx = %s, vector = %s, %s"%( dx,self.vx,[p_vx_dx,p_vx_dy],[v_vx_dx,v_vx_dy]))
            print("dy = %s, vy = %s, vector = %s, %s"%(-dy,self.vy,[p_vy_dx,p_vy_dy],[v_vy_dx,v_vy_dy]))
            print("veloce  degree %s"%math.degrees(veloce_radian))
            print("radian  degree %s"%math.degrees(radian))
            print("reflect degree %s"%math.degrees(reflect_radian))
            print("---------")
        if dx == 0:
            x0,y0 = 0,vlph
            x1,y1 = width,vlph
        elif dy == 0:
            x0,y0 = vlpw,0
            x1,y1 = vlpw,height
        else:
            k = dy/dx
            b = vlp[1]+vlp[0]/k # y = -x/k+b
            x0,y0 = 0,b
            x1,y1 = width,(-width)/k+b
        pygame.draw.aaline(screen,self.color,[x0,y0],[x1,y1],5) # 画出连接线的中垂线

class DragBoard(pygame.sprite.Sprite):
    def __init__(self,target):
        pygame.sprite.Sprite.__init__(self)
        self.target = target
        self.color = self.target.color
        self.size = self.width,self.height = 120,100
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()
        self.fontx = pygame.font.Font(None,30)
        self.fonty = pygame.font.Font(None,30)
        self.fonta = pygame.font.Font(None,30)
        self.x = 0
        self.y = 0
        self.r = 0
        self.a = 0
    def update(self):
        self.image.fill(self.color)
        self.x = self.target.rect.center[0]-center_width
        self.y = center_height-self.target.rect.center[1]
        self.r = math.atan2(self.y,self.x)
        self.a = math.degrees(self.r)
        textx = self.fontx.render(u'x=%s'%self.x,True,self.color)
        texty = self.fonty.render(u'y=%s'%self.y,True,self.color)
        textz = self.fonty.render(u'ζ=%.2f'%self.a,True,self.color)
        textt = self.fonty.render(u'θ=%.2f'%(90-self.a),True,self.color)
        textx_rect = textx.get_rect(center=[self.width/2.5,self.height*0.2])
        texty_rect = textx.get_rect(center=[self.width/2.5,self.height*0.4])
        textz_rect = textx.get_rect(center=[self.width/2.5,self.height*0.6])
        textt_rect = textx.get_rect(center=[self.width/2.5,self.height*0.8])
        pygame.draw.rect(self.image,black,[5,5,self.width-10,self.height-10])
        self.image.blit(textx,textx_rect)
        self.image.blit(texty,texty_rect)
        self.image.blit(textz,textz_rect)
        self.image.blit(textt,textt_rect)
        self.rect.topleft = self.target.rect.center
        if self.target.rect.center[0]<=center_width and self.target.rect.center[1]<=center_height:
            self.rect.bottomright = self.target.rect.center
        elif self.target.rect.center[0]<=center_width and self.target.rect.center[1]>=center_height:
            self.rect.topright = self.target.rect.center
        elif self.target.rect.center[0]>=center_width and self.target.rect.center[1]<=center_height:
            self.rect.bottomleft = self.target.rect.center
        elif self.target.rect.center[0]>=center_width and self.target.rect.center[1]>=center_height:
            self.rect.topleft = self.target.rect.center
        if self.rect.left < 0:
            self.rect.left = self.target.rect.center[0]
        if self.rect.right > width:
            self.rect.right = self.target.rect.center[0]
        if self.rect.top < 0:
            self.rect.top = self.target.rect.center[1]
        if self.rect.bottom > height:
            self.rect.bottom = self.target.rect.center[1]

class DragArc(pygame.sprite.Sprite):
    cnt = 0
    def __init__(self,target_board):
        pygame.sprite.Sprite.__init__(self)
        self.target_board = target_board
        self.color = self.target_board.color
        self.radius = 40+DragArc.cnt*10
        self.image = pygame.Surface([self.radius]*2)
        self.image.set_colorkey(transparent)
        self.rect = self.image.get_rect()
        self.rect.center = [center_width,center_height]
        self.arcrect = pygame.Rect(0,0,self.radius,self.radius)
        DragArc.cnt += 1
    def __del__(self):
        DragArc.cnt -= 1
    def update(self):
        self.image.fill(transparent)
        pygame.draw.arc(self.image,self.color,self.arcrect,0,self.target_board.r,width=5)

class DragTarget:
    def __init__(self,group,pos):
        self.dragball = DragBall(pos)
        self.dragline = DragLine(self.dragball)
        self.dragboard = DragBoard(self.dragball)
        self.dragarc = DragArc(self.dragboard)
        self.add(group)
    def add(self,group):
        group.add(self.dragball)
        group.add(self.dragline)
        group.add(self.dragboard)
        group.add(self.dragarc)
    def update(self):
        self.dragline.update()
        self.dragboard.update()
        self.dragarc.update()

dragtargets = []
sprite_group = pygame.sprite.RenderUpdates()
draw_bg()
pygame.display.update()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for dragtarget in dragtargets:
                    dragtarget.dragball.update([event.pos[0],event.pos[1]])
                    if dragtarget.dragball.drag: break
            elif event.button == 3:
                dragtargets.append(DragTarget(sprite_group,[event.pos[0],event.pos[1]]))
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for dragtarget in dragtargets:
                    dragtarget.dragball.drag = False
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0] == 1:
                for dragtarget in dragtargets:
                    if dragtarget.dragball.drag:
                        dragtarget.dragball.update([event.pos[0],event.pos[1]])
    draw_bg()
    for dragtarget in dragtargets:
        dragtarget.update()
    new_rect = sprite_group.draw(screen)
    pygame.display.update()
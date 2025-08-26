from math import *
import pygame as pg

class CO:
    def __init__(self,Name,X,Y,Mass,Radius,X_Velocity=0,Y_Velocity=0,color='white',feather = False, track_color='not_given',track_len=2500,pin=False):
        self.name = Name
        self.x = X
        self.y = Y
        self.m = Mass
        self.r = Radius
        self.x_v = X_Velocity
        self.y_v = Y_Velocity
        self.color=color
        self.trace = []
        self.track_len = track_len
        self.feather = feather #to make track or not
        self.pin = pin
        if track_color == 'not_given':
            self.track_color = color
        pg.draw.ellipse(Screen,self.color,(self.Sx()-width*(self.r)/(x_max-x_min),self.Sy()-height*(self.r)/(y_max-y_min),2*width*(self.r)/(x_max-x_min),2*height*(self.r)/(y_max-y_min)))
        CO_list.append(self)

    def move(self):
        self.x += speed*self.x_v/max_fps
        self.y += speed*self.y_v/max_fps

        if self.feather:
            if  speed:
                self.trace.append((self.x,self.y))
            if len(self.trace) == self.track_len+1:
                self.trace.pop(0)
            for cords in self.trace:
                pg.draw.circle(Screen,self.track_color,(Scords(cords)),1)
                
        pg.draw.ellipse(Screen,self.color,(self.Sx()-width*(self.r)/(x_max-x_min),self.Sy()-height*(self.r)/(y_max-y_min),2*width*(self.r)/(x_max-x_min),2*height*(self.r)/(y_max-y_min)))
                         
    def new_velocity(self):
        for obj in CO_list:
            if self != obj:
                R=sqrt((obj.x-self.x)**2+(obj.y-self.y)**2)
                self.x_v -=speed*((self.x-obj.x)*G*obj.m/R**3)/max_fps
                self.y_v -=speed*((self.y-obj.y)*G*obj.m/R**3)/max_fps

    def Sx(self):
        return(width*(self.x-x_min)/(x_max-x_min))
    
    def Sy(self):
        return(-height*(self.y-y_max)/(y_max-y_min))
    
    def del_trace(self):
        self.trace = []

def Scords(cords): return((width*(cords[0]-x_min)/(x_max-x_min),-height*(cords[1]-y_max)/(y_max-y_min)))

Screen_par=[800,800]
width = Screen_par[0]
height = Screen_par[1]
Shown_cords=[-400,-400,400,400]
x_min = Shown_cords[0]
y_min = Shown_cords[1]
x_max = Shown_cords[2]
y_max = Shown_cords[3]

G = 0.1
primordial_speed=10
speed=primordial_speed
max_fps = 140
cam_speed = 500

CO_list=[]

Screen = pg.display.set_mode((width,height))
pg.display.set_caption('Matrix')
clock = pg.time.Clock()

CO('Sun',0,0,300000,30,1,0,'yellow')
CO('Earth',300,0,100,10,1,10,'darkgreen',True,track_len=3000,)
#Moon  = CO(320,0,0.1,3,0,120,'white',True)
while True:
#event handler
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if not speed:
                    speed = primordial_speed
                else:
                    speed = 0
        elif event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[2]:
                for co in CO_list:
                    co.pin = False

            elif pg.mouse.get_pressed()[0]:
                for co in CO_list:
                    if pg.Rect(co.Sx()-width*(co.r)/(x_max-x_min),co.Sy()-height*(co.r)/(y_max-y_min),2*width*(co.r)/(x_max-x_min),2*height*(co.r)/(y_max-y_min)).collidepoint(pg.mouse.get_pos()):
                        for obj in CO_list:
                            obj.pin = False
                        co.pin = True
                        break
    #cam movement
    keys = pg.key.get_pressed()
    if keys[pg.K_UP] or keys[pg.K_DOWN] or keys[pg.K_RIGHT] or keys[pg.K_LEFT]:
        for obj in CO_list:
            obj.pin = False
        if keys[pg.K_UP]:
            y_min+=cam_speed/max_fps
            y_max+=cam_speed/max_fps
        if keys[pg.K_DOWN]:
            y_min-=cam_speed/max_fps
            y_max-=cam_speed/max_fps
        if keys[pg.K_RIGHT]:
            x_min+=cam_speed/max_fps
            x_max+=cam_speed/max_fps
        if keys[pg.K_LEFT]:
            x_min-=cam_speed/max_fps
            x_max-=cam_speed/max_fps

#game processes and graphics
    Screen.fill('black')
    for obj in CO_list:
        obj.new_velocity()
        if obj.pin:
            x_min = obj.x - (Shown_cords[2]-Shown_cords[0])/2
            y_min = obj.y - (Shown_cords[3]-Shown_cords[1])/2
            x_max = obj.x + (Shown_cords[2]-Shown_cords[0])/2
            y_max = obj.y + (Shown_cords[3]-Shown_cords[1])/2
    for obj in CO_list:
        obj.move()

#Screen update and other
    pg.display.flip()
    pg.display.set_caption('Matrix'+ str(round(clock.get_fps())))
    clock.tick(max_fps)
from math import *
import pygame as pg

class CO:
    def __init__(self,Name,X,Y,Mass,Radius,X_Velocity=0,Y_Velocity=0,color='white',feather = False, track_color='not_given',track_len=1000,collision=False):
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
        self.pin = False
        self.track_color = track_color
        if track_color == 'not_given':
            self.track_color = color
        self.rect_var=(width*(self.r)/(dx),height*(self.r)/(dy),2*width*(self.r)/(dx),2*height*(self.r)/(dy),width,height,dx,dy)
        pg.draw.ellipse(Screen,self.color,(self.Sx()-self.rect_var[0],self.Sy()-self.rect_var[1],self.rect_var[2],self.rect_var[3]))
        self.collision=collision
        CO_list.append(self)

    def move(self):
        self.x += self.x_v*pysc
        self.y += self.y_v*pysc
        if width != self.rect_var[4] or height != self.rect_var[5] or dx != self.rect_var[6] or dy != self.rect_var[7]:
            self.rect_var=(width*(self.r)/(dx),height*(self.r)/(dy),2*width*(self.r)/(dx),2*height*(self.r)/(dy),width,height,dx,dy)
        pg.draw.ellipse(Screen,self.color,(self.Sx()-self.rect_var[0],self.Sy()-self.rect_var[1],self.rect_var[2],self.rect_var[3]))
        
        if self.feather:
            self.track_draw()

    def new_velocity(self,num):
        i = 0
        Impact_list = []
        for obj in CO_list:
            i += 1
            if self != obj:
                R=sqrt((obj.x-self.x)**2+(obj.y-self.y)**2)
                accel = acceleration(obj.m,self.m,R)
                self.x_v -=accel*((self.x-obj.x)/R)*pysc
                self.y_v -=accel*((self.y-obj.y)/R)*pysc
                if i >= num and R <= self.r+obj.r:
                    if self.m >= obj.m:
                        Impact_list.append((self,obj))
                    else:
                        Impact_list.append((obj,self))
        if Impact_list != []:
            return(Impact_list)

    def Sx(self):
        return(width*(self.x-x_min)/(dx))

    def Sy(self):
        return(-height*(self.y-y_max)/(dy))

    def track_draw(self):
        if  speed != 0:
            self.trace.append((self.x,self.y))
        if len(self.trace) == self.track_len+1:
            self.trace.pop(0)
        for cords in (self.trace):
            pg.draw.circle(Screen,self.track_color,(Scords(cords)),1)

    def impact(self,obj):
        self.x = (self.x*self.m+obj.x*obj.m)/(self.m+obj.m)
        self.y = (self.y*self.m+obj.y*obj.m)/(self.m+obj.m)
        self.m = self.m+obj.m
        self.r = sqrt(self.r**2+obj.r**2)
        self.x_v = (self.m*self.x_v+obj.m*obj.x_v)/(self.m+obj.m)
        self.y_v = (self.m*self.y_v+obj.m*obj.y_v)/(self.m+obj.m)
        CO_list.remove(obj)
        del obj
        

def Scords(cords): return((width*(cords[0]-x_min)/(dx),-height*(cords[1]-y_max)/(dy)))

def List_rerange(List):
    Final_list = []
    for element in List:
        for object in element:
            Final_list.append(object)
    return(Final_list)


#screen_parametrs
Screen_par=[800,800]
width = Screen_par[0]
height = Screen_par[1]

Shown_cords=[-450,-450,450,450]
x_min = Shown_cords[0]
y_min = Shown_cords[1]
x_max = Shown_cords[2]
y_max = Shown_cords[3]
dx = x_max-x_min
dy = y_max-y_min

Screen = pg.display.set_mode((width,height))
clock = pg.time.Clock()

#constants
CO_list=[]
prim_speed=1
speed=prim_speed
G = 1
m=10000

#returns accleretion created by the gravity force 
def acceleration(M,m,R):
    f=(G*M*m/R**2)
    a=f/m
    return(a)

#screen_constants
cam_speed = 500
prim_max_fps = 500
max_fps=prim_max_fps
pysc=speed/max_fps

CO('0',0,0,100*m,15,X_Velocity=0 ,Y_Velocity=-0.5,color='red',feather=False)
CO('1',400,0,m,10,X_Velocity=0 ,Y_Velocity=50,color='blue',feather=True,track_len=10000)
CO('2',425,0,100,4,X_Velocity=0 ,Y_Velocity=68,color='green',feather=True,track_len=10000)

while True:
#event handler
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if not speed:
                    speed = prim_speed
                    pysc = speed/max_fps
                else:
                    speed = 0
                    pysc = 0
        elif event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[2]:
                for co in CO_list:
                    co.pin = False

            elif pg.mouse.get_pressed()[0]:
                for co in CO_list:
                    if pg.Rect(co.Sx()-width*(co.r)/(dx),co.Sy()-height*(co.r)/(dy),2*width*(co.r)/(dx),2*height*(co.r)/(dy)).collidepoint(pg.mouse.get_pos()):
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
        dx = x_max-x_min
        dy = y_max-y_min

#game processes and graphics
    Screen.fill('black')
    Collision_list = []
    celestial_object_number = 0
    for obj in CO_list:
        celestial_object_number += 1
        Collision_list.append(obj.new_velocity(celestial_object_number))
        if Collision_list[-1] == None: Collision_list.pop(-1)
        if obj.pin:
            x_min = obj.x - (Shown_cords[2]-Shown_cords[0])/2
            y_min = obj.y - (Shown_cords[3]-Shown_cords[1])/2
            x_max = obj.x + (Shown_cords[2]-Shown_cords[0])/2
            y_max = obj.y + (Shown_cords[3]-Shown_cords[1])/2
            dx = x_max-x_min
            dy = y_max-y_min
    if Collision_list != []:
        for imp in List_rerange(Collision_list):
            imp[0].impact(imp[1])
    for obj in CO_list: obj.move()
        
#Screen update and other

    fps = clock.get_fps()
    if fps <= prim_max_fps and fps != 0:
        max_fps=fps*1.1
        if max_fps > prim_max_fps: max_fps=prim_max_fps
        pysc=speed/max_fps

#Mass centre
    cord=[0,0]
    M=0
    for o in CO_list:
        cord[0]+=o.Sx()*o.m
        cord[1]+=o.Sy()*o.m
        M+=o.m
    cord=[cord[0]/M,cord[1]/M]
    pg.draw.circle(Screen,'white',cord,2)

    pg.display.flip()
    pg.display.set_caption('Matrix'+ str(round(fps)))
    clock.tick(max_fps)
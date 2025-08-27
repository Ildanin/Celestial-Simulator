from math import *
import pygame as pg
from random import randint

class CO:
    def __init__(self,Name,X,Y,Mass,Radius,X_Velocity=0,Y_Velocity=0, color=(255,255,255),feather=False,track_quality=20,track_color='not_given',track_len=10000,collision=True,color_mix=True):
        self.name = Name
        self.x = X
        self.y = Y
        self.m = Mass
        self.r = Radius
        self.x_v = X_Velocity
        self.y_v = Y_Velocity
        self.color = color
        self.trace = []
        self.track_len = track_len
        self.feather = feather
        self.prim_feather = feather
        self.quality = track_quality
        self.remainder = 0
        self.pin = False
        self.track_color = (track_color, 'given')
        if track_color == 'not_given':
            self.track_color = (color, 'not_given')
        self.rect_var=(width*(self.r)/dx,height*(self.r)/dy,2*width*(self.r)/dx,2*height*(self.r)/dy,self.r,width,height,dx,dy)
        pg.draw.ellipse(Screen,self.color,(self.Sx()-self.rect_var[0],self.Sy()-self.rect_var[1],self.rect_var[2],self.rect_var[3]))
        self.collision = collision
        self.color_mix = color_mix
        CO_list.append(self)

    def move(self):
        self.x += self.x_v*delta_time
        self.y += self.y_v*delta_time

    def co_draw(self):
        if self.r != self.rect_var[4] or width != self.rect_var[5] or height != self.rect_var[6] or dx != self.rect_var[7] or dy != self.rect_var[8]:
            self.rect_var=(width*(self.r)/dx,height*(self.r)/dy,2*width*(self.r)/dx,2*height*(self.r)/dy,self.r,width,height,dx,dy)
        if (x_min-self.r <= self.x <= x_max+self.r) and (y_min-self.r <= self.y <= y_max+self.r):
            pg.draw.ellipse(Screen,self.color,(self.Sx()-self.rect_var[0],self.Sy()-self.rect_var[1],self.rect_var[2],self.rect_var[3]))

    def new_velocity(self,num):
        i = 0
        for obj in CO_list:
            i += 1
            if self != obj:
                R=sqrt((obj.x-self.x)**2+(obj.y-self.y)**2)
                accel = acceleration(obj.m,self.m,R)
                self.x_v -=accel*((self.x-obj.x)/R)*delta_time
                self.y_v -=accel*((self.y-obj.y)/R)*delta_time
                if (self.collision and obj.collision) and (i >= num and R <= self.r+obj.r):
                    if self.m >= obj.m:
                        Collision_list.append((self,obj))
                    else:
                        Collision_list.append((obj,self))

    def Sx(self): 
        return(width*(self.x-x_min)/dx)

    def Sy(self): 
        return(-height*(self.y-y_max)/dy)

    def track_draw(self):
        if  speed != 0 and self.remainder + 1000*delta_time >= self.quality:
            self.remainder += 1000*delta_time - self.quality
            self.trace.insert(0,((self.x,self.y),self.track_color[0]))
        elif speed != 0:
            self.remainder += 1000*delta_time
        if len(self.trace) == self.track_len+1:
            self.trace.pop(self.track_len)
        if self.feather:
            if pinned_object == None or local_trace == False:
                if feather_type == 'line':
                    for i in range(len(self.trace)-1):
                        if (x_min <= self.trace[i][0][0] <= x_max) and (y_min <= self.trace[i][0][1] <= y_max):
                            pg.draw.line(Screen,self.trace[i][1],Scords(self.trace[i][0]),Scords(self.trace[i+1][0]))
                else:
                    for cords in self.trace:
                        if (x_min <= cords[0][0] <= x_max) and (y_min <= cords[0][1] <= y_max):
                            pg.draw.circle(Screen,cords[1],Scords(cords[0]),1)
            else:
                if feather_type == 'line':
                    next_x_point = self.trace[0][0][0]-pinned_object.trace[0][0][0]+pinned_object.x
                    next_y_point = self.trace[0][0][1]-pinned_object.trace[0][0][1]+pinned_object.y
                    for i in range(len(list(zip(self.trace, pinned_object.trace)))-1):
                        if self.name == '1':
                            print(len(list(zip(self.trace, pinned_object.trace)))-1)
                        x_point = next_x_point
                        y_point = next_y_point
                        next_x_point = self.trace[i+1][0][0]-pinned_object.trace[i+1][0][0]+pinned_object.x
                        next_y_point = self.trace[i+1][0][1]-pinned_object.trace[i+1][0][1]+pinned_object.y
                        if (x_min <= x_point <= x_max) and (y_min <= y_point <= y_max):
                            pg.draw.line(Screen,self.trace[i][1],Scords((x_point,y_point)),Scords((next_x_point,next_y_point)))
                elif self != pinned_object:
                    for i in range(len(list(zip(self.trace, pinned_object.trace)))-1):
                        x_point = self.trace[i][0][0]-pinned_object.trace[i][0][0]+pinned_object.x
                        y_point = self.trace[i][0][1]-pinned_object.trace[i][0][1]+pinned_object.y
                        if (x_min <= x_point <= x_max) and (y_min <= y_point <= y_max):
                            pg.draw.circle(Screen,self.trace[i][1],Scords((x_point,y_point)),1)
        
    def impact(self,obj):
        mass = self.m + obj.m
        if mass != 0:
            if self.color_mix:
                self.color = ((self.color[0]*self.r**2+obj.color[0]*obj.r**2)/(self.r**2+obj.r**2),(self.color[1]*self.r**2+obj.color[1]*obj.r**2)/(self.r**2+obj.r**2),(self.color[2]*self.r**2+obj.color[2]*obj.r**2)/(self.r**2+obj.r**2))
            if self.track_color[1] == 'not_given':
                self.track_color = (self.color,'not_given')
            self.x = (self.x*self.m+obj.x*obj.m)/mass
            self.y = (self.y*self.m+obj.y*obj.m)/mass
            self.r = sqrt(self.r**2+obj.r**2)
            self.x_v = (self.m*self.x_v+obj.m*obj.x_v)/mass
            self.y_v = (self.m*self.y_v+obj.m*obj.y_v)/mass
            self.m = mass
            if obj.pin:
                global pinned_object 
                pinned_object= self
                self.pin = True
        else:
            CO_list.remove(self)
            del self
        try:
            CO_list.remove(obj)
        except:
            pass
        del obj
        

def Scords(cords): return((width*(cords[0]-x_min)/dx,-height*(cords[1]-y_max)/dy))

def Rainbow_color(angle):
    red = 0
    green = 0
    blue = 0
    if   0 <= angle <= 60:
        red = 255
        green = 255/60*angle
        blue = 0
    elif 60 <= angle <= 120:
        red = 255-255/60*(angle-60)
        green = 255
        blue = 0
    elif 120 <= angle <= 180:
        red = 0
        green = 255
        blue = 255/60*(angle-120)
    elif 180 <= angle <= 240:
        red = 0
        green = 255-255/60*(angle-180)
        blue = 255
    elif 240 <= angle <= 300:
        red = 255/60*(angle-240)
        green = 0
        blue = 255
    elif 300 <= angle <= 360:
        red = 255
        green = 0
        blue = 255-255/60*(angle-300)
    return((red,green,blue))

#screen_parametrs
Screen_par=[800,800]
width=Screen_par[0]
height=Screen_par[1]

view = 450
Shown_cords=[-view,view,-view,view]
x_min=Shown_cords[0]
x_max=Shown_cords[1]
y_min=Shown_cords[2]
y_max=Shown_cords[3]
dx = x_max-x_min
dy = y_max-y_min

Screen = pg.display.set_mode((width,height))
clock = pg.time.Clock()

#constants
CO_list=[]
traces = False
feather_type = 'line'
local_trace = False
pinned_object = None
prim_speed=1
speed=prim_speed
G=100
m=10000

#returns accleretion created by the gravity force 
def acceleration(M,m,R):
    f=G*M*m/R
    a=f/m
    return(a)

#screen_constants
cam_speed = 0.4
prim_max_fps = 140
max_fps=prim_max_fps
delta_time=speed/max_fps

#Examples
example = 2
if   example == 0:
    pass
elif example == 1: #Star-Planet-Satelite          f=G*M*m/R**2
    G=1
    m=10000
    CO('0',0,0,100*m,15,X_Velocity=0 ,Y_Velocity=-0.5,color=(255,255,0),feather=False)
    CO('1',400,0,m,10,X_Velocity=0 ,Y_Velocity=50,color=(0,0,255),feather=True,track_len=100)
    CO('2',425,0,100,4,X_Velocity=0 ,Y_Velocity=68,color=(0,255,0),feather=True,track_len=100)
elif example == 2: #polygon n-body problem        f=Any
    #f=G*M*m/R is recommended
    G=10
    m=10000
    R=400
    v=500
    impacts = False
    n=8
    for i in range(n):
        angle = i*360/n
        CO(str(i+1),cos(angle*pi/180)*R, sin(angle*pi/180)*R,m,5,X_Velocity=-sin(angle*pi/180)*v, Y_Velocity=cos(angle*pi/180)*v,color=Rainbow_color(angle),feather=False,track_len=1000,collision=impacts)
elif example == 3: #Proto_solar_system-Black_hole f=G*M*m/R**2
    G=100
    m=10000
    n=21
    start=-3000
    end=3000
    CO('Star',0,0,400*m,300,X_Velocity=0,Y_Velocity=0,color=(255,255,0),feather=False)
    CO('Black_hole',10000,1000,10000*m,20,X_Velocity=0,Y_Velocity=0,color=(220,20,60),feather=False,color_mix=False)
    CO_list[-1].pin = True
    for i in range(1,n):
        for j in range(1,n):
            q = randint(1,3)
            k = sqrt(G*400*m/sqrt((start+(end-start)*i/n)**2+(start+(end-start)*j/n)**2))
            Vx = -k*(start + (end-start)*j/n)/sqrt((start+(end-start)*i/n)**2+(start+(end-start)*j/n)**2)
            Vy = k*(start + (end-start)*i/n)/sqrt((start+(end-start)*i/n)**2+(start+(end-start)*j/n)**2)
            CO('Proto_planet',start+(end-start)*i/n,start+(end-start)*j/n,m/q**2,15/q,X_Velocity=randint(80,120)/100*Vx,Y_Velocity=randint(80,120)/100*Vy,color=(randint(0,255),randint(0,255),randint(0,255)),feather=False)
elif example == 4: #Star-Planet                   f=G*M*m
    G=1
    CO('Star',0,0,2000,30,X_Velocity=0 ,Y_Velocity=-1,color=(255,255,0),feather=False)
    CO('Planet',400,0,10,10,X_Velocity=0 ,Y_Velocity=200,color=(0,0,255),feather=True,track_len=1000,track_quality=30)
elif example == 5: #Star-Planet                   f=G*M*m/R
    G=1
    CO('Star',0,0,1600,30,X_Velocity=0 ,Y_Velocity=-0.05,color=(255,255,0),feather=False)
    CO('Planet',400,0,1,10,X_Velocity=0 ,Y_Velocity=40,color=(0,0,255),feather=True,track_len=1000,track_quality=30)
    CO('Planet',200,0,1,10,X_Velocity=0 ,Y_Velocity=40,color=(0,0,255),feather=True,track_len=1000,track_quality=30)
elif example == 6: #Star-Planet                   f=G*M*m*R
    G=0.04
    CO('Star',0,0,1600,30,X_Velocity=0 ,Y_Velocity=-3,color=(255,255,0),feather=False)
    CO('Planet',200,0,1,10,X_Velocity=0 ,Y_Velocity=1600,color=(0,0,255),feather=True,track_len=1000,track_quality=10)
    CO('Planet',400,0,1,10,X_Velocity=0 ,Y_Velocity=3200,color=(0,0,255),feather=True,track_len=1000,track_quality=10)



while True:
#event handler
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
                if not speed:
                    speed = round(prim_speed,1)
                    delta_time = speed/max_fps
                else:
                    speed = 0
                    delta_time = 0
            elif event.key == pg.K_t:
                if traces:
                    traces = False
                    for obj in CO_list:
                        obj.feather = obj.prim_feather
                else:
                    traces = True
                    for obj in CO_list:
                        obj.feather = True
            elif event.key == pg.K_y:
                if feather_type == 'dot':
                    feather_type = 'line'
                else:
                    feather_type = 'dot'
            elif event.key == pg.K_u:
                if local_trace:
                    local_trace = False
                else:
                    local_trace = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[2]:
                for obj in CO_list:
                    obj.pin = False
                pinned_object = None
            elif pg.mouse.get_pressed()[0]:
                for obj in CO_list:
                    if pg.Rect(obj.Sx()-width*(obj.r)/dx,obj.Sy()-height*(obj.r)/dy,2*width*(obj.r)/dx,2*height*(obj.r)/dy).collidepoint(pg.mouse.get_pos()):
                        for co in CO_list:
                            co.pin = False
                        obj.pin = True
                        pinned_object = obj
                        x_min = obj.x - (Shown_cords[2]-Shown_cords[0])/2
                        y_min = obj.y - (Shown_cords[3]-Shown_cords[1])/2
                        x_max = obj.x + (Shown_cords[2]-Shown_cords[0])/2
                        y_max = obj.y + (Shown_cords[3]-Shown_cords[1])/2
                        break
        elif event.type == pg.MOUSEWHEEL:
            if dx >= 1 and dy >= 1:
                if event.y > 0:
                    x_min += dx*0.1
                    y_min += dy*0.1
                    x_max -= dx*0.1
                    y_max -= dy*0.1
                else:
                    x_min -= dx*0.1
                    y_min -= dy*0.1
                    x_max += dx*0.1
                    y_max += dy*0.1
            else: 
                if event.y < 0:
                    x_min -= dx*0.1
                    y_min -= dy*0.1
                    x_max += dx*0.1
                    y_max += dy*0.1
            dx=x_max-x_min
            dy=y_max-y_min


#cam movement
    keys = pg.key.get_pressed()
    if keys[pg.K_UP] or keys[pg.K_DOWN] or keys[pg.K_RIGHT] or keys[pg.K_LEFT]:
        for obj in CO_list:
            obj.pin = False
        pinned_object = None
        if keys[pg.K_UP]:
            y_min+=dy*cam_speed/max_fps
            y_max+=dy*cam_speed/max_fps
        if keys[pg.K_DOWN]:
            y_min-=dy*cam_speed/max_fps
            y_max-=dy*cam_speed/max_fps
        if keys[pg.K_RIGHT]:
            x_min+=dx*cam_speed/max_fps
            x_max+=dx*cam_speed/max_fps
        if keys[pg.K_LEFT]:
            x_min-=dx*cam_speed/max_fps
            x_max-=dx*cam_speed/max_fps
        dx=x_max-x_min
        dy=y_max-y_min
    elif keys[pg.K_COMMA] or keys[pg.K_PERIOD]:
        if keys[pg.K_COMMA]:
            prim_speed -= 1/max_fps
        if keys[pg.K_PERIOD]:
            prim_speed += 1/max_fps
        if prim_speed < 0:
            prim_speed = 0
        speed = round(prim_speed,1)

#game processes and graphics
    Screen.fill('black')
    Collision_list = []
    celestial_object_number = 0
    for obj in CO_list:
        celestial_object_number += 1
        obj.new_velocity(celestial_object_number)
        if obj.pin:
            x_min = obj.x+obj.x_v*delta_time-dx/2
            y_min = obj.y+obj.y_v*delta_time-dy/2
            x_max = obj.x+obj.x_v*delta_time+dx/2
            y_max = obj.y+obj.y_v*delta_time+dy/2
    if Collision_list != []:
        for collision in Collision_list:
            collision[0].impact(collision[1])
    for obj in CO_list:
        obj.move()
    for obj in CO_list:
        obj.track_draw()
    for obj in CO_list:
        obj.co_draw()
        
#Screen update and other
    fps = clock.get_fps()
    if fps <= prim_max_fps and fps != 0:
        max_fps=1.05*fps
        if max_fps > prim_max_fps: max_fps=prim_max_fps
        delta_time=speed/max_fps

#Mass centre
    cord=[0,0]
    M=0
    for obj in CO_list:
        cord[0]+=obj.x*obj.m
        cord[1]+=obj.y*obj.m
        M+=obj.m
    if M != 0:
        cord=[cord[0]/M,cord[1]/M]
    pg.draw.circle(Screen,'white',Scords(cord),2)

#object lineization(looks good for a n-body problem)
    '''for i in range(len(CO_list)):
        for j in range(i+1,len(CO_list)):
            pg.draw.line(Screen,'white',Scords((CO_list[i].x,CO_list[i].y)),Scords((CO_list[j].x,CO_list[j].y)))'''

    pg.display.flip()
    pg.display.set_caption('Celestial system' + ' | Fps:' + str(round(fps)) + ' | Speed:' + str(speed))
    clock.tick(max_fps)
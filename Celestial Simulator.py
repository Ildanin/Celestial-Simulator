from math import *
import pygame as pg
from random import randint

class CO:
    def __init__(self,Astronomic_type,X,Y,Mass,Radius,X_Velocity=0,Y_Velocity=0, color=(255,255,255),feather=False,track_performance=10,track_color='not_given',track_len=10000,collision=True):
        self.astro_type = Astronomic_type
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
        self.performance = track_performance
        self.remainder = 0
        self.pin = False
        self.track_color = (track_color, 'given')
        if track_color == 'not_given':
            self.track_color = (color, 'not_given')
        self.rect_var=(width*(self.r)/dx,height*(self.r)/dy,2*width*(self.r)/dx,2*height*(self.r)/dy,self.r,width,height,dx,dy)
        pg.draw.ellipse(Screen,self.color,(self.Sx()-self.rect_var[0],self.Sy()-self.rect_var[1],self.rect_var[2],self.rect_var[3]))
        self.collision=collision
        CO_list.append(self)

    def move(self):
        self.x += self.x_v*delta_time
        self.y += self.y_v*delta_time
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
        if  speed != 0 and self.remainder + 1000*delta_time >= self.performance:
            self.remainder += 1000*delta_time - self.performance
            self.trace.append((self.x,self.y))
        elif speed != 0:
            self.remainder += 1000*delta_time
        if len(self.trace) == self.track_len+1:
            self.trace.pop(0)
        if self.feather:
            if feather_type == 'dot':
                for cords in self.trace:
                    if (x_min <= cords[0] <= x_max) and (y_min <= cords[1] <= y_max):
                        pg.draw.circle(Screen,self.track_color[0],Scords(cords),1)
            else:
                for i in range(len(self.trace)-1):
                    if (x_min <= self.trace[i][0] <= x_max) and (y_min <= self.trace[i][1] <= y_max):
                        pg.draw.line(Screen,self.track_color[0],Scords(self.trace[i]),Scords(self.trace[i+1]))

    def impact(self,obj):
        #if self.m > 50*obj.m:
        if True:
            mass = self.m + obj.m
            if mass != 0:
                self.color = ((self.color[0]*self.r**2+obj.color[0]*obj.r**2)/(self.r**2+obj.r**2),(self.color[1]*self.r**2+obj.color[1]*obj.r**2)/(self.r**2+obj.r**2),(self.color[2]*self.r**2+obj.color[2]*obj.r**2)/(self.r**2+obj.r**2))
                if self.track_color[1] == 'not_given':
                    self.track_color = (self.color,'not_given')
                self.x = (self.x*self.m+obj.x*obj.m)/mass
                self.y = (self.y*self.m+obj.y*obj.m)/mass
                self.r = sqrt(self.r**2+obj.r**2)
                self.x_v = (self.m*self.x_v+obj.m*obj.x_v)/mass
                self.y_v = (self.m*self.y_v+obj.m*obj.y_v)/mass
                self.m = mass
            else:
                CO_list.remove(self)
                del self
            try:
                CO_list.remove(obj)
            except:
                pass
            del obj
        else:
            mass = self.m + obj.m
            if mass != 0:
                k = obj.m/(self.m)
                Sx = obj.x*obj.m + self.x*self.m
                Sy = obj.y*obj.m + self.y*self.m
                q = 0.9

                new_mass = k*obj.m
                new_Mass = obj.m+(1-k)*self.m
                new_radius = sqrt(k)*obj.r
                new_Radius = sqrt(self.r**2 +(1-k)*(obj.r)**2)
                new_Vx = q*obj.x_v
                new_Vy = q*obj.y_v
                new_VY = (obj.m*obj.y_v+self.m*self.y_v-new_mass*new_Vy)/new_Mass
                new_VX = (obj.m*obj.x_v+self.m*self.x_v-new_mass*new_Vx)/new_Mass
                if obj.x_v != 0:
                    p = obj.y_v/obj.x_v
                    a = (1+p**2)*(mass)
                    b = 2*(p*mass*(obj.y-p*obj.x)-(Sx+p*Sy))
                    c = (obj.y-p*obj.x)*(mass*(obj.y-p*obj.x)-2*Sy)-((new_Mass*(new_Radius+new_radius))**2-(Sx**2+Sy**2))/mass
                    if obj.x_v >= 0:
                        new_x = (-b+sqrt(b**2-4*a*c))/(2*a)
                    else:
                        new_x = (-b-sqrt(b**2-4*a*c))/(2*a)
                    new_y = p*(new_x-obj.x)+obj.y
                else:
                    p = 0
                    a = mass
                    b = -2*Sy
                    c = (obj.x)*(mass*(obj.x)-2*Sx)-((new_Mass*(new_Radius+new_radius))**2-(Sx**2+Sy**2))/mass
                    if obj.y_v >= 0:
                        new_y = (-b+sqrt(b**2-4*a*c))/(2*a)
                    else:
                        new_y = (-b-sqrt(b**2-4*a*c))/(2*a)
                    new_x = p*(new_y-obj.y)+obj.x
                new_X = (Sx-new_x*new_mass)/new_Mass
                new_Y = (Sy-new_y*new_mass)/new_Mass
                
                self.x = new_X
                self.y = new_Y
                self.m = new_Mass
                self.r = new_Radius
                self.x_v = new_VX
                self.y_v = new_VY

                obj.x = new_x
                obj.y = new_y
                obj.m = new_mass
                obj.r = new_radius
                obj.x_v = new_Vx
                obj.y_v = new_Vy
            else:
                CO_list.remove(self)
                CO_list.remove(obj)
                del self
                del obj
        

def Scords(cords): return((width*(cords[0]-x_min)/dx,-height*(cords[1]-y_max)/dy))


#screen_parametrs
Screen_par=[800,800]
width=Screen_par[0]
height=Screen_par[1]

view = 450
Shown_cords=[-view,-view,view,view]
x_min=Shown_cords[0]
y_min=Shown_cords[1]
x_max=Shown_cords[2]
y_max=Shown_cords[3]
dx=x_max-x_min
dy=y_max-y_min

Screen = pg.display.set_mode((width,height))
clock = pg.time.Clock()

#constants
CO_list=[]
traces = False
feather_type = 'dot'
prim_speed=0.1
speed=prim_speed
G=100
m=10000

#returns accleretion created by the gravity force 
def acceleration(M,m,R):
    f=(G*M*m/R**2)
    a=f/m
    return(a)

#screen_constants
cam_speed = 0.4
prim_max_fps = 100
max_fps=prim_max_fps
delta_time=speed/max_fps

#Star-planet-satelite
'''CO('0',0,0,100*m,15,X_Velocity=0 ,Y_Velocity=-1,color='yellow',feather=False)
CO('1',400,0,m,10,X_Velocity=0 ,Y_Velocity=50,color='blue',feather=True,track_len=1000)
CO('2',425,0,100,4,X_Velocity=0 ,Y_Velocity=68,color='green',feather=True,track_len=1000)'''

n = 21
start = -3000
end = 3000
CO('Star',0,0,400*m,300,X_Velocity=0,Y_Velocity=0,color=(255,255,0),feather=False)
CO('Primordial_black_hole',10000,1000,10000*m,20,X_Velocity=0,Y_Velocity=0,color=(220,20,60),feather=False)
CO_list[-1].pin = True
for i in range(1,n):
    for j in range(1,n):
        q = randint(1,3)
        k = sqrt(G*400*m/sqrt((start+(end-start)*i/n)**2+(start+(end-start)*j/n)**2))
        Vx = -k*(start + (end-start)*j/n)/sqrt((start+(end-start)*i/n)**2+(start+(end-start)*j/n)**2)
        Vy = k*(start + (end-start)*i/n)/sqrt((start+(end-start)*i/n)**2+(start+(end-start)*j/n)**2)
        CO('n',start+(end-start)*i/n,start+(end-start)*j/n,m/q**2,15/q,X_Velocity=randint(80,120)/100*Vx,Y_Velocity=randint(80,120)/100*Vy,color=(randint(0,255),randint(0,255),randint(0,255)),feather=False)
        
while True:
#event handler
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if not speed:
                    speed = prim_speed
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
        elif event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[2]:
                for co in CO_list:
                    co.pin = False
            elif pg.mouse.get_pressed()[0]:
                for co in CO_list:
                    if pg.Rect(co.Sx()-width*(co.r)/dx,co.Sy()-height*(co.r)/dy,2*width*(co.r)/dx,2*height*(co.r)/dy).collidepoint(pg.mouse.get_pos()):
                        for obj in CO_list:
                            obj.pin = False
                        co.pin = True
                        x_min = obj.x - (Shown_cords[2]-Shown_cords[0])/2
                        y_min = obj.y - (Shown_cords[3]-Shown_cords[1])/2
                        x_max = obj.x + (Shown_cords[2]-Shown_cords[0])/2
                        y_max = obj.y + (Shown_cords[3]-Shown_cords[1])/2
                        dx=x_max-x_min
                        dy=y_max-y_min
                        break
        elif event.type == pg.MOUSEWHEEL:
            if dx >= 1 and dy >= 1:
                if event.y > 0:
                    Shown_cords[0]=x_min+dx*0.1
                    Shown_cords[1]=y_min+dy*0.1
                    Shown_cords[2]=x_max-dx*0.1
                    Shown_cords[3]=y_max-dy*0.1
                else:
                    Shown_cords[0]=x_min-dx*0.1
                    Shown_cords[1]=y_min-dy*0.1
                    Shown_cords[2]=x_max+dx*0.1
                    Shown_cords[3]=y_max+dy*0.1
            else: 
                if event.y < 0:
                    Shown_cords[0]=x_min-dx*0.1
                    Shown_cords[1]=y_min-dy*0.1
                    Shown_cords[2]=x_max+dx*0.1
                    Shown_cords[3]=y_max+dy*0.1
            x_min=Shown_cords[0]
            y_min=Shown_cords[1]
            x_max=Shown_cords[2]
            y_max=Shown_cords[3]
            dx=x_max-x_min
            dy=y_max-y_min


#cam movement
    keys = pg.key.get_pressed()
    if keys[pg.K_UP] or keys[pg.K_DOWN] or keys[pg.K_RIGHT] or keys[pg.K_LEFT]:
        for obj in CO_list:
            obj.pin = False
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

#game processes and graphics
    Screen.fill('black')
    Collision_list = []
    celestial_object_number = 0
    for obj in CO_list:
        celestial_object_number += 1
        obj.new_velocity(celestial_object_number)
        if obj.pin:
            x_min = obj.x - (Shown_cords[2]-Shown_cords[0])/2
            y_min = obj.y - (Shown_cords[3]-Shown_cords[1])/2
            x_max = obj.x + (Shown_cords[2]-Shown_cords[0])/2
            y_max = obj.y + (Shown_cords[3]-Shown_cords[1])/2
    if Collision_list != []:
        for collision in Collision_list:
            collision[0].impact(collision[1])
    for obj in CO_list: 
        obj.track_draw()
    for obj in CO_list:
        obj.move()
        
#Screen update and other
    fps = clock.get_fps()
    if fps <= prim_max_fps and fps != 0:
        max_fps=fps*1.1
        if max_fps > prim_max_fps: max_fps=prim_max_fps
        delta_time=speed/max_fps

#Mass centre
    cord=[0,0]
    M=0
    for obj in CO_list:
        cord[0]+=obj.Sx()*obj.m
        cord[1]+=obj.Sy()*obj.m
        M+=obj.m
    if M != 0:
        cord=[cord[0]/M,cord[1]/M]
    pg.draw.circle(Screen,'white',cord,2)

    pg.display.flip()
    pg.display.set_caption('Matrix'+ str(round(fps)))
    clock.tick(max_fps)
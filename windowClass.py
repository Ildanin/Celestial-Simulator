import pygame as pg
from utiles import GMm_d_r2

class Window:
    def __init__(self, width: float, height: float, background_color, x_min: float, x_max: float, y_min: float, y_max: float, gravity_constant: float, preserve_speed: bool, original_speed: float, original_delta_time: float, camera_speed: float, scaling_speed: float, speed_changing_speed: float, speed_changing_delta_time: float):
        #Screen par
        self.screen = pg.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.background_color = background_color

        #Simulation view
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.dx = self.x_max - self.x_min
        self.dy = self.y_max - self.y_min
        self.x_scale = self.width / self.dx
        self.y_scale = self.height / self.dy
        if self.x_scale == self.y_scale:
            self.similar_sides = True
        else:
            self.similar_sides = False

        #Simulation tweakables and variables
        self.force_equation = GMm_d_r2
        self.gravity_constant = gravity_constant

        self.preserve_speed = preserve_speed

        self.paused = False
        self.saved_speed = original_speed
        self.speed = self.saved_speed
        self.fps = 1000
        if preserve_speed:
            self.saved_delta_time = self.speed / self.fps
        else:
            self.saved_delta_time = original_delta_time
        self.delta_time = self.saved_delta_time

        self.camera_speed = camera_speed
        self.scaling_speed = scaling_speed
        self.speed_changing_speed = speed_changing_speed
        self.speed_changing_delta_time = speed_changing_delta_time

        self.traces = False
        self.local_traces = False
        self.traces_shortage = False
        self.feather_type = True
        self.pinned_object = False
        self.show_mass_center = True
        self.show_connecting_lines = False

    def camera_move_up(self):
        self.pinned_object = False
        self.y_min += self.dy * self.camera_speed / self.fps
        self.y_max += self.dy * self.camera_speed / self.fps

    def camera_move_down(self):
        self.pinned_object = False
        self.y_min -= self.dy * self.camera_speed / self.fps
        self.y_max -= self.dy * self.camera_speed / self.fps

    def camera_move_right(self):
        self.pinned_object = False
        self.x_min += self.dx * self.camera_speed / self.fps
        self.x_max += self.dx * self.camera_speed / self.fps

    def camera_move_left(self):
        self.pinned_object = False
        self.x_min -= self.dx * self.camera_speed / self.fps
        self.x_max -= self.dx * self.camera_speed / self.fps

    def camera_move_to(self, x: float, y: float):
        self.x_min = x - self.dx / 2
        self.y_min = y - self.dy / 2
        self.x_max = x + self.dx / 2
        self.y_max = y + self.dy / 2

    def camera_move_to_pinned_object(self):
        if self.pinned_object:
            self.x_min = self.pinned_object.x - self.dx / 2
            self.y_min = self.pinned_object.y - self.dy / 2
            self.x_max = self.pinned_object.x + self.dx / 2
            self.y_max = self.pinned_object.y + self.dy / 2

    def view_rescale(self, wheel_rotation: float):
        if self.dx >= 1 and self.dy >= 1:
            x_change = self.dx * self.scaling_speed
            y_change = self.dy * self.scaling_speed
            if wheel_rotation > 0:
                self.x_min += x_change
                self.y_min += y_change
                self.x_max -= x_change
                self.y_max -= y_change
            else:
                self.x_min -= x_change
                self.y_min -= y_change
                self.x_max += x_change
                self.y_max += y_change
        else: 
            if wheel_rotation < 0:
                self.x_min -= x_change
                self.y_min -= y_change
                self.x_max += x_change
                self.y_max += y_change
        self.dx = self.x_max - self.x_min
        self.dy = self.y_max - self.y_min
        self.x_scale = self.width / self.dx
        self.y_scale = self.height / self.dy

    def lower_speed(self):
        if self.paused:
            self.unpause()
        self.speed -= self.speed_changing_speed / self.fps
        if self.speed < 0:
            self.speed = 0
        self.delta_time = self.speed / self.fps

    def increase_speed(self):
        if self.paused:
            self.unpause()
        self.speed += self.speed_changing_speed / self.fps
        self.delta_time = self.speed / self.fps

    def lower_delta_time(self):
        if self.paused:
            self.unpause()
        self.delta_time -= self.speed_changing_delta_time / self.fps
        if self.delta_time < 0:
            self.delta_time = 0
        self.speed = self.delta_time * self.fps

    def increase_delta_time(self):
        if self.paused:
            self.unpause()
        self.delta_time += self.speed_changing_delta_time / self.fps
        self.speed = self.delta_time * self.fps

    def pause(self):
        self.paused = True
        self.saved_speed = self.speed
        self.saved_delta_time = self.delta_time
        self.speed = 0
        self.delta_time = 0
    
    def unpause(self):
        self.paused = False
        if self.preserve_speed:
            self.speed = self.saved_speed
            self.delta_time = self.speed / self.fps
        else:
            self.delta_time = self.saved_delta_time
            self.speed = self.delta_time * self.fps

    def update_fps(self, current_fps: float):
        if current_fps != 0:
            self.fps = current_fps
            if self.preserve_speed:
                self.saved_delta_time = self.speed / self.fps
                self.delta_time = self.saved_delta_time
            else:
                self.saved_speed = self.delta_time * self.fps
                self.speed = self.saved_speed

    def sx(self, x): 
        return(self.x_scale * (x - self.x_min))

    def sy(self, y): 
        return(-self.y_scale * (y - self.y_max))

    def scords(self, cords):
        return((self.x_scale * (cords[0] - self.x_min), -self.y_scale * (cords[1] - self.y_max)))
    
    def clear(self):
        self.screen.fill(self.background_color)
    
    def draw_mass_center(self, Celestial_Object_list : list):
        x = 0
        y = 0
        collective_mass = 0
        for obj in Celestial_Object_list:
            x += obj.x * obj.m
            y += obj.y * obj.m
            collective_mass += obj.m
        if collective_mass != 0:
            x /= collective_mass
            y /= collective_mass
            pg.draw.circle(self.screen, (255, 255, 255), self.scords((x, y)), 2)

    def draw_connecting_lines(self, Celestial_Object_list):
        for i in range(len(Celestial_Object_list)):
            for j in range(i+1, len(Celestial_Object_list)):
                pg.draw.line(self.screen, (255, 255 ,255), self.scords((Celestial_Object_list[i].x, Celestial_Object_list[i].y)), self.scords((Celestial_Object_list[j].x, Celestial_Object_list[j].y)))
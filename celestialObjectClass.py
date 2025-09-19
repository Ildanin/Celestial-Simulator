from math import sqrt
import pygame as pg
from windowClass import Window

class Celestial_Object:
    def __init__(self, x: float, y: float, mass: float, radius: float, x_velocity: float = 0, y_velocity: float = 0, color=(255, 255, 255), feather: bool = False, trace_quality: float = 20, trace_color = None, trace_len: float = 100, trace_shortage_significance: float = 0.1, collision: bool = True, color_mix: bool = True, material_mix_type: str= 'volume'):
        self.x = x
        self.y = y
        self.m = mass
        self.r = radius
        self.x_v = x_velocity
        self.y_v = y_velocity
        self.color = color
        self.trace = []
        self.trace_len = trace_len
        self.feather = feather
        self.trace_quality = trace_quality
        self.trace_shortage_significance = trace_shortage_significance
        self.remainder = 0  
        if trace_color == None:
            self.trace_color = color
            self.trace_color_given = False
        else:
            self.trace_color = trace_color
            self.trace_color_given = True
        self.collision = collision
        self.color_mix = color_mix
        self.material_mix_type = material_mix_type
        Celestial_Object_list.append(self)

    def move(self, win: Window):
        self.x += self.x_v * win.delta_time
        self.y += self.y_v * win.delta_time

    def draw(self, win: Window):
        if (win.x_min - self.r <= self.x <= win.x_max + self.r) and (win.y_min - self.r <= self.y <= win.y_max + self.r):
            pg.draw.ellipse(win.screen, self.color, (win.sx(self.x) - (win.x_scale * self.r), win.sy(self.y) - (win.y_scale * self.r), 2 * win.x_scale * self.r, 2 * win.y_scale * self.r))
            #if win.similar_sides:
            #    pg.draw.circle(win.screen, self.color, (win.sx(self.x), win.sy(self.y)), win.x_scale * self.r)
            #else:
            #    pg.draw.ellipse(win.screen, self.color, (win.sx(self.x) - (win.x_scale * self.r), win.sy(self.y) - (win.y_scale * self.r), 2 * win.x_scale * self.r, 2 * win.y_scale * self.r))

    def new_velocity(self, win: Window, celestial_object_number: int, Collision_list: list):
        for i, obj in enumerate(Celestial_Object_list):
            if i > celestial_object_number:
                distance = sqrt((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2)
                main_body_acceleration, second_body_acceleration = acceleration(win.force_equation, win.gravity_constant, self.m, obj.m, distance)
                force_radius_vector_x = ((self.x - obj.x) / distance) * win.delta_time
                force_radius_vector_y = ((self.y - obj.y) / distance) * win.delta_time
                self.x_v -= main_body_acceleration   * force_radius_vector_x
                self.y_v -= main_body_acceleration   * force_radius_vector_y
                obj.x_v  += second_body_acceleration * force_radius_vector_x
                obj.y_v  += second_body_acceleration * force_radius_vector_y
                if (self.collision and obj.collision) and (distance <= self.r + obj.r):
                    if self.m >= obj.m:
                        Collision_list.append((self, obj))
                    else:
                        Collision_list.append((obj, self))

    def trace_update(self, win: Window):
        if  win.speed != 0 and self.remainder + 1000 * win.delta_time >= self.trace_quality:
            self.remainder += 1000 * win.delta_time - self.trace_quality
            self.trace.insert(0, ((self.x, self.y), self.trace_color))
        elif win.speed != 0:
            self.remainder += 1000 * win.delta_time
        if len(self.trace) == self.trace_len + 1:
            self.trace.pop(self.trace_len)

    def trace_draw(self, win: Window):
        if win.pinned_object == False or win.local_traces == False:
            if win.feather_type == True:
                if win.traces_shortage:
                    for i in range(min(len(self.trace), round(self.trace_len * self.trace_shortage_significance)) - 1):
                        if (win.x_min <= self.trace[i+1][0][0] <= win.x_max) and (win.y_min <= self.trace[i+1][0][1] <= win.y_max):
                            pg.draw.line(win.screen, self.trace[i][1], win.scords(self.trace[i][0]), win.scords(self.trace[i+1][0]))
                else:
                    for i in range(len(self.trace) - 1):
                        if (win.x_min <= self.trace[i+1][0][0] <= win.x_max) and (win.y_min <= self.trace[i+1][0][1] <= win.y_max):
                            pg.draw.line(win.screen, self.trace[i][1], win.scords(self.trace[i][0]), win.scords(self.trace[i+1][0]))
            else:
                if win.traces_shortage:
                    for i in range(min(len(self.trace), round(self.trace_len * self.trace_shortage_significance))):
                        if (win.x_min <= self.trace[i][0][0] <= win.x_max) and (win.y_min <= self.trace[i][0][1] <= win.y_max):
                            pg.draw.circle(win.screen, self.trace[i][1], win.scords(self.trace[i][0]), 1)
                else:
                    for cords in self.trace:
                        if (win.x_min <= cords[0][0] <= win.x_max) and (win.y_min <= cords[0][1] <= win.y_max):
                            pg.draw.circle(win.screen, cords[1], win.scords(cords[0]), 1)
        else:
            if win.traces_shortage:
                number_of_included_points = min(len(self.trace), len(win.pinned_object.trace), round(self.trace_len * self.trace_shortage_significance), round(win.pinned_object.trace_len * self.trace_shortage_significance))
            else:
                number_of_included_points = min(len(self.trace), len(win.pinned_object.trace))
            if win.feather_type == True:
                next_x_point = self.trace[0][0][0] - win.pinned_object.trace[0][0][0] + win.pinned_object.x
                next_y_point = self.trace[0][0][1] - win.pinned_object.trace[0][0][1] + win.pinned_object.y
                for i in range(number_of_included_points - 1):
                    x_point = next_x_point
                    y_point = next_y_point
                    next_x_point = self.trace[i+1][0][0] - win.pinned_object.trace[i+1][0][0] + win.pinned_object.x
                    next_y_point = self.trace[i+1][0][1] - win.pinned_object.trace[i+1][0][1] + win.pinned_object.y
                    if (win.x_min <= next_x_point <= win.x_max) and (win.y_min <= next_y_point <= win.y_max):
                        pg.draw.line(win.screen, self.trace[i][1], win.scords((x_point, y_point)), win.scords((next_x_point, next_y_point)))
            elif self != win.pinned_object:
                for i in range(number_of_included_points):
                    x_point = self.trace[i][0][0] - win.pinned_object.trace[i][0][0] + win.pinned_object.x
                    y_point = self.trace[i][0][1] - win.pinned_object.trace[i][0][1] + win.pinned_object.y
                    if (win.x_min <= x_point <= win.x_max) and (win.y_min <= y_point <= win.y_max):
                        pg.draw.circle(win.screen, self.trace[i][1], win.scords((x_point, y_point)), 1)
        
    def impact(self, win: Window, obj):
        mass = self.m + obj.m
        if mass != 0:
            if self.color_mix:
                self.color = ((self.color[0] * self.r ** 2 + obj.color[0] * obj.r ** 2) / (self.r ** 2 + obj.r ** 2), (self.color[1] * self.r ** 2 + obj.color[1] * obj.r ** 2) / (self.r ** 2 + obj.r ** 2), (self.color[2] * self.r ** 2 + obj.color[2] * obj.r ** 2) / (self.r ** 2 + obj.r ** 2))
            if self.trace_color_given == False:
                self.trace_color = self.color
            if self.material_mix_type == 'volume':
                self.r = sqrt(self.r ** 2 + obj.r ** 2)
            elif self.material_mix_type == 'density':
                self.r = self.r * sqrt(mass / self.m)
            self.x = (self.x * self.m + obj.x * obj.m) / mass
            self.y = (self.y * self.m + obj.y * obj.m) / mass
            self.x_v = (self.m * self.x_v + obj.m * obj.x_v) / mass
            self.y_v = (self.m * self.y_v + obj.m * obj.y_v) / mass
            self.m = mass
            if obj == win.pinned_object:
                win.pinned_object = self
        else:
            Celestial_Object_list.remove(self)
            del self
        try:
            Celestial_Object_list.remove(obj)
        except:
            pass
        del obj

Celestial_Object_list = []

#returns Major and minor acceleration created by the gravity force
def acceleration(force_equasion, gravity_cosntant: float, main_mass: float, second_mass: float, distance: float):
    force = force_equasion(gravity_cosntant, main_mass, second_mass, distance)
    main_body_acceleration = force / main_mass
    second_body_acceleration = force / second_mass
    return(main_body_acceleration, second_body_acceleration)
from math import sqrt
import pygame as pg
from utiles import *

class Celestial_Object:
    def __init__(self, windwow, x: float, y: float, mass: float, radius: float, x_velocity: float = 0, y_velocity: float = 0,
                color: tuple[float, float, float] = (255, 255, 255), feather: bool = False, trace_quality: int = 20, trace_color = None, 
                trace_len: int = 100, trace_shortage_significance: float = 0.1, collision: bool = True, color_mix: bool = True, material_mix_type: str= 'volume'):
        self.win = windwow
        self.x = x
        self.y = y
        self.m = mass
        self.r = radius
        self.x_v = x_velocity
        self.y_v = y_velocity
        self.color = color
        self.feather = feather
        self.collision = collision
        self.color_mix = color_mix
        self.material_mix_type = material_mix_type

        if trace_color == None:
            trace_color = color
            self.trace_color_given = False
        else:
            self.trace_color_given = True
        self.trace_handler = Celestial_Object.Trace_handler(self, trace_len, trace_color, trace_quality, trace_shortage_significance)
        Celestial_Object_list.append(self)
        self.index = len(Celestial_Object_list) - 1

    def __str__(self) -> str:
        return(f"ID: {self.index} | Mass: {round(self.m, 2)} | Radius: {round(self.r, 2)} | Coords: {round(self.x, 2), round(self.y, 2)} ")
    
    def remove(self) -> None:
        Celestial_Object_list.pop(self.index)
        for obj in Celestial_Object_list[self.index:]:
            obj.index -= 1
        del self
    
    def move(self) -> None:
        self.x += self.x_v * self.win.delta_time
        self.y += self.y_v * self.win.delta_time

    def draw(self) -> None:
        if (self.win.x_min - self.r <= self.x <= self.win.x_max + self.r) and (self.win.y_min - self.r <= self.y <= self.win.y_max + self.r):
            pg.draw.ellipse(self.win.screen, self.color, 
                            (self.win.sx(self.x) - (self.win.x_scale * self.r), 
                            self.win.sy(self.y) - (self.win.y_scale * self.r),
                            2 * self.win.x_scale * self.r,
                            2 * self.win.y_scale * self.r))

    def update_velocity_not_using_distance_list(self) -> list[float]:
        Distances = []
        for obj in Celestial_Object_list[self.index+1:]:
            distance = sqrt((self.x - obj.x)**2 + (self.y - obj.y)**2)
            Distances.append(distance)
            force = self.win.force_equation(self.win.gravity_constant, self.m, obj.m, distance)
            main_body_acceleration = force / self.m
            second_body_acceleration = force / obj.m
            force_radius_vector_x = ((self.x - obj.x) / distance) * self.win.delta_time
            force_radius_vector_y = ((self.y - obj.y) / distance) * self.win.delta_time
            self.x_v -= main_body_acceleration   * force_radius_vector_x
            self.y_v -= main_body_acceleration   * force_radius_vector_y
            obj.x_v  += second_body_acceleration * force_radius_vector_x
            obj.y_v  += second_body_acceleration * force_radius_vector_y
        return(Distances)

    def update_velocity(self, Distance_list) -> None:
        for obj, distance in zip(Celestial_Object_list[self.index+1:], Distance_list[self.index]):
            force = self.win.force_equation(self.win.gravity_constant, self.m, obj.m, distance)
            main_body_acceleration = force / self.m
            second_body_acceleration = force / obj.m
            force_radius_vector_x = ((self.x - obj.x) / distance) * self.win.delta_time
            force_radius_vector_y = ((self.y - obj.y) / distance) * self.win.delta_time
            self.x_v -= main_body_acceleration   * force_radius_vector_x
            self.y_v -= main_body_acceleration   * force_radius_vector_y
            obj.x_v  += second_body_acceleration * force_radius_vector_x
            obj.y_v  += second_body_acceleration * force_radius_vector_y

    def collision_check(self, Distance_lsit) -> list[tuple]:
        Collsiions = []
        for obj in Celestial_Object_list[self.index+1:]:
            if Distance_lsit[self.index][obj.index - self.index - 1] < obj.r + self.r:
                Collsiions.append((self, obj))
        return(Collsiions)

    def impact(self, obj) -> None:
        mass = self.m + obj.m
        if self.m < obj.m:
            self.color_mix         = obj.color_mix
            self.material_mix_type = obj.material_mix_type
            self.trace_color_given = obj.trace_color_given
        if mass != 0:
            if self.color_mix or self.material_mix_type == 'volume':
                squared_new_radius = self.r ** 2 + obj.r ** 2
            if self.color_mix:
                self.color = ((self.color[0] * self.r ** 2 + obj.color[0] * obj.r ** 2) / squared_new_radius, 
                              (self.color[1] * self.r ** 2 + obj.color[1] * obj.r ** 2) / squared_new_radius, 
                              (self.color[2] * self.r ** 2 + obj.color[2] * obj.r ** 2) / squared_new_radius)
                if self.trace_color_given == False:
                    self.trace_handler.trace_color = self.color
            if self.material_mix_type == 'volume':
                self.r = sqrt(squared_new_radius)
            elif self.material_mix_type == 'density':
                self.r = self.r * sqrt(mass / self.m)
            self.x   = (self.x * self.m   + obj.x * obj.m  ) / mass
            self.y   = (self.y * self.m   + obj.y * obj.m  ) / mass
            self.x_v = (self.m * self.x_v + obj.m * obj.x_v) / mass
            self.y_v = (self.m * self.y_v + obj.m * obj.y_v) / mass
            self.m = mass
            if obj == self.win.pinned_object:
                self.win.pinned_object = self
            obj.remove()
        else:
            obj.remove()
            self.remove()

    class Trace_handler:
        def __init__(self, celestial_object, trace_len: int, trace_color: tuple[float, float, float], trace_quality: int, trace_shortage_significance: float):
            self.celestial_object = celestial_object
            self.win = celestial_object.win
            self.trace: list[tuple[tuple[float, float], tuple[float, float, float]]] = []
            self.remainder: float = 0
            self.trace_len = trace_len
            self.trace_color = trace_color
            self.trace_quality = trace_quality
            self.trace_shortage_significance = trace_shortage_significance

        def trace_update(self) -> None:
            self.remainder += 1000 * self.win.delta_time
            if  self.remainder >= self.trace_quality:
                self.remainder -= self.trace_quality
                self.trace.insert(0, ((self.celestial_object.x, self.celestial_object.y), self.trace_color))
                #self.trace.insert(0, (self.celestial_object.x, self.celestial_object.y))
                if len(self.trace) == self.trace_len + 1:
                    self.trace.pop(-1)

        def trace_draw_local_with_lines_shorted(self) -> None:
            next_x_point = self.trace[0][0][0] - self.win.pinned_object.trace_handler.trace[0][0][0] + self.win.pinned_object.x
            next_y_point = self.trace[0][0][1] - self.win.pinned_object.trace_handler.trace[0][0][1] + self.win.pinned_object.y
            for i in range( min(len(self.trace), len(self.win.pinned_object.trace_handler.trace), round(self.trace_len * self.trace_shortage_significance), round(self.win.pinned_object.trace_handler.trace_len * self.trace_shortage_significance)) - 1):
                x_point = next_x_point
                y_point = next_y_point
                next_x_point = self.trace[i+1][0][0] - self.win.pinned_object.trace_handler.trace[i+1][0][0] + self.win.pinned_object.x
                next_y_point = self.trace[i+1][0][1] - self.win.pinned_object.trace_handler.trace[i+1][0][1] + self.win.pinned_object.y
                if (self.win.x_min <= next_x_point <= self.win.x_max) and (self.win.y_min <= next_y_point <= self.win.y_max):
                    pg.draw.line(self.win.screen, self.trace[i][1], self.win.scords((x_point, y_point)), self.win.scords((next_x_point, next_y_point)))

        def trace_draw_local_with_lines(self) -> None:
            next_x_point = self.trace[0][0][0] - self.win.pinned_object.trace_handler.trace[0][0][0] + self.win.pinned_object.x
            next_y_point = self.trace[0][0][1] - self.win.pinned_object.trace_handler.trace[0][0][1] + self.win.pinned_object.y
            for i in range(min(len(self.trace), len(self.win.pinned_object.trace_handler.trace)) - 1):
                x_point = next_x_point
                y_point = next_y_point
                next_x_point = self.trace[i+1][0][0] - self.win.pinned_object.trace_handler.trace[i+1][0][0] + self.win.pinned_object.x
                next_y_point = self.trace[i+1][0][1] - self.win.pinned_object.trace_handler.trace[i+1][0][1] + self.win.pinned_object.y
                if (self.win.x_min <= next_x_point <= self.win.x_max) and (self.win.y_min <= next_y_point <= self.win.y_max):
                    pg.draw.line(self.win.screen, self.trace[i][1], self.win.scords((x_point, y_point)), self.win.scords((next_x_point, next_y_point)))

        def trace_draw_local_with_circles_shorted(self) -> None:
            for i in range( min(len(self.trace), len(self.win.pinned_object.trace_handler.trace), round(self.trace_len * self.trace_shortage_significance), round(self.win.pinned_object.trace_handler.trace_len * self.trace_shortage_significance))):
                x_point = self.trace[i][0][0] - self.win.pinned_object.trace_handler.trace[i][0][0] + self.win.pinned_object.x
                y_point = self.trace[i][0][1] - self.win.pinned_object.trace_handler.trace[i][0][1] + self.win.pinned_object.y
                if (self.win.x_min <= x_point <= self.win.x_max) and (self.win.y_min <= y_point <= self.win.y_max):
                    pg.draw.circle(self.win.screen, self.trace[i][1], self.win.scords((x_point, y_point)), 1)

        def trace_draw_local_with_circles(self) -> None:
            for i in range(min(len(self.trace), len(self.win.pinned_object.trace_handler.trace))):
                x_point = self.trace[i][0][0] - self.win.pinned_object.trace_handler.trace[i][0][0] + self.win.pinned_object.x
                y_point = self.trace[i][0][1] - self.win.pinned_object.trace_handler.trace[i][0][1] + self.win.pinned_object.y
                if (self.win.x_min <= x_point <= self.win.x_max) and (self.win.y_min <= y_point <= self.win.y_max):
                    pg.draw.circle(self.win.screen, self.trace[i][1], self.win.scords((x_point, y_point)), 1)

        def trace_draw_absolute_with_lines_shorted(self) -> None:
            for i in range(min(len(self.trace), round(self.trace_len * self.trace_shortage_significance)) - 1):
                if (self.win.x_min <= self.trace[i+1][0][0] <= self.win.x_max) and (self.win.y_min <= self.trace[i+1][0][1] <= self.win.y_max):
                    pg.draw.line(self.win.screen, self.trace[i][1], self.win.scords(self.trace[i][0]), self.win.scords(self.trace[i+1][0]))

        def trace_draw_absolute_with_lines(self) -> None:
            for i in range(len(self.trace) - 1):
                if (self.win.x_min <= self.trace[i+1][0][0] <= self.win.x_max) and (self.win.y_min <= self.trace[i+1][0][1] <= self.win.y_max):
                    pg.draw.line(self.win.screen, self.trace[i][1], self.win.scords(self.trace[i][0]), self.win.scords(self.trace[i+1][0]))
            #pg.draw.lines(self.win.screen, self.trace_color, False, list(map(self.win.scords, self.trace)))

        def trace_draw_absolute_with_circles_shorted(self) -> None:
            for i in range(min(len(self.trace), round(self.trace_len * self.trace_shortage_significance))):
                if (self.win.x_min <= self.trace[i][0][0] <= self.win.x_max) and (self.win.y_min <= self.trace[i][0][1] <= self.win.y_max):
                    pg.draw.circle(self.win.screen, self.trace[i][1], self.win.scords(self.trace[i][0]), 1)

        def trace_draw_absolute_with_circles(self) -> None:
            for cords in self.trace:
                if (self.win.x_min <= cords[0][0] <= self.win.x_max) and (self.win.y_min <= cords[0][1] <= self.win.y_max):
                    pg.draw.circle(self.win.screen, cords[1], self.win.scords(cords[0]), 1)
                #if (self.win.x_min <= cords[0] <= self.win.x_max) and (self.win.y_min <= cords[0] <= self.win.y_max):
                #    pg.draw.circle(self.win.screen, self.trace_color, self.win.scords(cords), 1)


Celestial_Object_list: list[Celestial_Object] = []
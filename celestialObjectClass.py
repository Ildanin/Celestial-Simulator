import pygame as pg
from utiles import *
from math import sqrt
from parameters import COLOR, FEATHER, COLLIDABLE, TRACE_COLOR, TRACE_LEN, TRACE_SHORTAGE_SIGNIFICANCE, COLOR_MIX, MATERIAL_MIX_TYPE

class Celestial_Object:
    def __init__(self, window, x: float, y: float, mass: float, radius: float, x_velocity: float = 0, y_velocity: float = 0,
                color: tuple[int, int, int] = COLOR, feather: bool = FEATHER, collidable: bool = COLLIDABLE, trace_color = TRACE_COLOR, 
                trace_len: int = TRACE_LEN, trace_shortage_significance: float = TRACE_SHORTAGE_SIGNIFICANCE, color_mix: bool = COLOR_MIX, material_mix_type: str = MATERIAL_MIX_TYPE):
        self.win = window
        self.parameters_handler = window.parameters_handler
        self.x = x
        self.y = y
        self.m = mass
        self.r = radius
        self.x_v = x_velocity
        self.y_v = y_velocity
        self.color = color
        self.feather = feather
        self.collidable = collidable
        self.color_mix = color_mix
        self.material_mix_type = material_mix_type

        if trace_color == None:
            trace_color = color
            self.trace_color_given = False
        else:
            self.trace_color_given = True
        self.trace_handler = Celestial_Object.Trace_handler(self, trace_len, trace_color, trace_shortage_significance)
        Celestial_Object_list.append(self)
        self.index = len(Celestial_Object_list) - 1

    def __str__(self) -> str:
        return(f"ID: {self.index} | Mass: {round(self.m, 2)} | Radius: {round(self.r, 2)} | Coords: {round(self.x, 2), round(self.y, 2)} ")
    
    def reindex(self, new_index) -> None:
        Celestial_Object_list.pop(self.index)
        for obj in Celestial_Object_list[self.index:]:
            obj.index -= 1
        Celestial_Object_list.insert(new_index, self)
        self.index = new_index
        for obj in Celestial_Object_list[self.index+1:]:
            obj.index += 1

    def remove(self) -> None:
        Celestial_Object_list.pop(self.index)
        for obj in Celestial_Object_list[self.index:]:
            obj.index -= 1
        del self
    
    def move(self) -> None:
        self.x += self.x_v * self.parameters_handler.delta_time
        self.y += self.y_v * self.parameters_handler.delta_time

    def draw(self) -> None:
        if self.win.camera.check_visibility(self.x, self.y, self.r):
            pg.draw.ellipse(self.win.screen, self.color, (self.win.sx(self.x) - (self.win.camera.x_scale * self.r), self.win.sy(self.y) - (self.win.camera.y_scale * self.r),
                             2 * self.win.camera.x_scale * self.r, 2 * self.win.camera.y_scale * self.r))
    
    def update_velocity(self, x_acceleration: float, y_acceleration: float) -> None:
        self.x_v += x_acceleration * self.parameters_handler.delta_time
        self.y_v += y_acceleration * self.parameters_handler.delta_time

    def impact(self, obj) -> None:
        mass = self.m + obj.m
        if self.m < obj.m:
            self.color_mix         = obj.color_mix
            self.material_mix_type = obj.material_mix_type
            self.trace_color_given = obj.trace_color_given
            self.trace_handler.inherit(obj.trace_handler)
        if mass != 0:
            if self.color_mix or self.material_mix_type == 'volume':
                squared_new_radius = self.r ** 2 + obj.r ** 2
            if self.color_mix:
                self.color = ((self.color[0] * self.r ** 2 + obj.color[0] * obj.r ** 2) / squared_new_radius, 
                              (self.color[1] * self.r ** 2 + obj.color[1] * obj.r ** 2) / squared_new_radius, 
                              (self.color[2] * self.r ** 2 + obj.color[2] * obj.r ** 2) / squared_new_radius)
            elif self.m < obj.m:
                self.color = obj.color
            if self.trace_color_given == False:
                self.trace_handler.trace_color = self.color
            if self.material_mix_type == 'volume':
                self.r = sqrt(squared_new_radius)
            elif self.material_mix_type == 'density':
                if self.m > obj.m:
                    self.r = self.r * sqrt(mass / self.m)
                else:
                    self.r = obj.r * sqrt(mass / obj.m)
            self.x   = (self.x * self.m   + obj.x * obj.m  ) / mass
            self.y   = (self.y * self.m   + obj.y * obj.m  ) / mass
            self.x_v = (self.m * self.x_v + obj.m * obj.x_v) / mass
            self.y_v = (self.m * self.y_v + obj.m * obj.y_v) / mass
            self.m = mass
            if self.parameters_handler.is_pinned_object:
                if obj == self.parameters_handler.pinned_object:
                    self.parameters_handler.pinned_object = self
            obj.remove()
        else:
            obj.remove()
            self.remove()

    class Trace_handler:
        def __init__(self, celestial_object, trace_len: int, trace_color: tuple[int, int, int], trace_shortage_significance: float):
            self.celestial_object = celestial_object
            self.win = celestial_object.win
            self.parameters_handler = celestial_object.parameters_handler
            self.trace: list[tuple[float, float]] = []
            self.local_trace: list[tuple[float, float]] = []
            self.trace_len = trace_len
            self.trace_color = trace_color
            self.trace_shortage_significance = trace_shortage_significance
        
        def inherit(self, parent) -> None:
            self.trace = parent.trace.copy()
            self.local_trace = parent.local_trace.copy()
            self.trace_len = parent.trace_len
            self.trace_color = parent.trace_color
            self.trace_shortage_significance = parent.trace_shortage_significance

        def trace_update(self) -> None:
            self.trace.insert(0, (self.celestial_object.x, self.celestial_object.y))
            if len(self.trace) > self.trace_len:
                self.trace.pop(-1)

        def local_trace_generate(self) -> None:
            self.local_trace = [(coords[0] - pin_coords[0], coords[1] - pin_coords[1]) for coords, pin_coords in zip(self.trace, self.parameters_handler.pinned_object.trace_handler.trace)]
        
        def local_trace_reoriented(self, length = -1) -> list[tuple[float, float]]:
            if length == -1:
                return([(x + self.parameters_handler.pinned_object.x, y + self.parameters_handler.pinned_object.y) for x, y in self.local_trace])
            else:
                return([(x + self.parameters_handler.pinned_object.x, y + self.parameters_handler.pinned_object.y) for x, y in self.local_trace[:length]])

        def local_trace_update(self) -> None:
            self.local_trace.insert(0, (self.celestial_object.x - self.parameters_handler.pinned_object.x, self.celestial_object.y - self.parameters_handler.pinned_object.y))
            if len(self.local_trace) > min(self.trace_len, self.parameters_handler.pinned_object.trace_handler.trace_len):
                self.local_trace.pop(-1)
        
        def draw_local_with_lines_shorted(self) -> None:
            length = min(len(self.trace), len(self.parameters_handler.pinned_object.trace_handler.trace), round(self.trace_len * self.trace_shortage_significance), 
                        round(self.parameters_handler.pinned_object.trace_handler.trace_len * self.trace_shortage_significance))
            pg.draw.lines(self.win.screen, self.trace_color, False, list(map(self.win.scords, self.local_trace_reoriented(length))))

        def draw_local_with_lines(self) -> None:
            pg.draw.lines(self.win.screen, self.trace_color, False, list(map(self.win.scords, self.local_trace_reoriented())))

        def draw_local_with_circles_shorted(self) -> None:
            length = min(len(self.trace), len(self.parameters_handler.pinned_object.trace_handler.trace), round(self.trace_len * self.trace_shortage_significance), 
                        round(self.parameters_handler.pinned_object.trace_handler.trace_len * self.trace_shortage_significance))
            for x, y in self.local_trace_reoriented(length):
                if self.win.camera.check_visibility(x, y):
                    pg.draw.circle(self.win.screen, self.trace_color, self.win.scords((x, y)), 1)

        def draw_local_with_circles(self) -> None:
            for x, y in self.local_trace_reoriented(min(len(self.trace), len(self.parameters_handler.pinned_object.trace_handler.trace))):
                if self.win.camera.check_visibility(x, y):
                    pg.draw.circle(self.win.screen, self.trace_color, self.win.scords((x, y)), 1)

        def draw_absolute_with_lines_shorted(self) -> None:
            pg.draw.lines(self.win.screen, self.trace_color, False, list(map(self.win.scords, self.trace[:min(len(self.trace), round(self.trace_len * self.trace_shortage_significance))])))

        def draw_absolute_with_lines(self) -> None:
            pg.draw.lines(self.win.screen, self.trace_color, False, list(map(self.win.scords, self.trace)))

        def draw_absolute_with_circles_shorted(self) -> None:
            for i in range(min(len(self.trace), round(self.trace_len * self.trace_shortage_significance))):
                if self.win.camera.check_visibility(self.trace[i][0], self.trace[i][1]):
                    pg.draw.circle(self.win.screen, self.trace_color, self.win.scords(self.trace[i]), 1)

        def draw_absolute_with_circles(self) -> None:
            for cords in self.trace:
                if self.win.camera.check_visibility(cords[0], cords[1]):
                    pg.draw.circle(self.win.screen, self.trace_color, self.win.scords(cords), 1)


Celestial_Object_list: list[Celestial_Object] = []
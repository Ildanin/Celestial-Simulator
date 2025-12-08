import pygame as pg
from parameters import *
from celestialObjectClass import Celestial_Object

class Window:
    def __init__(self, width: float, height: float, background_color: tuple[float, float, float], x_min: float, x_max: float, y_min: float, y_max: float):
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

        #Simulation tweakables and variables
        self.force_equation = None
        self.gravity_constant = 1

        self.paused = False
        self.saved_speed = ORIGINAL_SPEED
        self.speed = self.saved_speed
        self.fps = 1000
        self.preserve_speed = PRESERVE_SPEED
        if self.preserve_speed:
            self.saved_delta_time = self.speed / self.fps
        else:
            self.saved_delta_time = ORIGINAL_DELTA_TIME
        self.delta_time = self.saved_delta_time

        self.camera_speed = CAMERA_SPEED
        self.scaling_speed = SCALING_SPEED
        self.speed_changing_speed = SPEED_CHANGING_SPEED
        self.speed_changing_delta_time = SPEED_CHANGING_DELTA_TIME

        self.traces = False
        self.local_traces = False
        self.traces_shortage = False
        self.feather_type = True
        self.pinned_object = False
        self.show_mass_center = True
        self.show_connecting_lines = False
        self.trace_draw_function = None
        self.update_trace_draw_method()

    def camera_move_up(self) -> None:
        if self.pinned_object:
            self.pinned_object = False
            self.update_trace_draw_method()
        self.y_min += self.dy * self.camera_speed / self.fps
        self.y_max += self.dy * self.camera_speed / self.fps

    def camera_move_down(self) -> None:
        if self.pinned_object:
            self.pinned_object = False
            self.update_trace_draw_method()
        self.y_min -= self.dy * self.camera_speed / self.fps
        self.y_max -= self.dy * self.camera_speed / self.fps

    def camera_move_right(self) -> None:
        if self.pinned_object:
            self.pinned_object = False
            self.update_trace_draw_method()
        self.x_min += self.dx * self.camera_speed / self.fps
        self.x_max += self.dx * self.camera_speed / self.fps

    def camera_move_left(self) -> None:
        if self.pinned_object:
            self.pinned_object = False
            self.update_trace_draw_method()
        self.x_min -= self.dx * self.camera_speed / self.fps
        self.x_max -= self.dx * self.camera_speed / self.fps

    def camera_move_to(self, x: float, y: float) -> None:
        self.x_min = x - self.dx / 2
        self.y_min = y - self.dy / 2
        self.x_max = x + self.dx / 2
        self.y_max = y + self.dy / 2

    def camera_move_to_pinned_object(self) -> None:
        if self.pinned_object:
            self.camera_move_to(self.pinned_object.x, self.pinned_object.y)

    def view_rescale(self, wheel_rotation: float) -> None:
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
                x_change = self.dx * self.scaling_speed
                y_change = self.dy * self.scaling_speed
                self.x_min -= x_change
                self.y_min -= y_change
                self.x_max += x_change
                self.y_max += y_change
        self.dx = self.x_max - self.x_min
        self.dy = self.y_max - self.y_min
        self.x_scale = self.width / self.dx
        self.y_scale = self.height / self.dy

    def lower_speed(self) -> None:
        if self.paused:
            self.unpause()
        self.speed -= self.speed_changing_speed / self.fps
        if self.speed < 0:
            self.speed = 0
            self.pause()
        self.delta_time = self.speed / self.fps

    def increase_speed(self) -> None:
        if self.paused:
            self.unpause()
        self.speed += self.speed_changing_speed / self.fps
        self.delta_time = self.speed / self.fps

    def lower_delta_time(self) -> None:
        if self.paused:
            self.unpause()
        self.delta_time -= self.speed_changing_delta_time / self.fps
        if self.delta_time < 0:
            self.delta_time = 0
            self.pause()
        self.speed = self.delta_time * self.fps

    def increase_delta_time(self) -> None:
        if self.paused:
            self.unpause()
        self.delta_time += self.speed_changing_delta_time / self.fps
        self.speed = self.delta_time * self.fps

    def pause(self) -> None:
        self.paused = True
    
    def unpause(self) -> None:
        self.paused = False
        if self.delta_time != 0:
            self.fps = self.speed / self.delta_time
    
    def update_trace_draw_method(self) -> None:
        if self.local_traces == True and self.pinned_object:
            if self.feather_type == True:
                if self.traces_shortage == True:
                    self.trace_draw_function = Celestial_Object.Trace_handler.trace_draw_local_with_lines_shorted
                else:
                    self.trace_draw_function = Celestial_Object.Trace_handler.trace_draw_local_with_lines
            else:
                if self.traces_shortage == True:
                    self.trace_draw_function = Celestial_Object.Trace_handler.trace_draw_local_with_circles_shorted
                else:
                    self.trace_draw_function = Celestial_Object.Trace_handler.trace_draw_local_with_circles
        else:
            if self.feather_type == True:
                if self.traces_shortage == True:
                    self.trace_draw_function = Celestial_Object.Trace_handler.trace_draw_absolute_with_lines_shorted
                else:
                    self.trace_draw_function = Celestial_Object.Trace_handler.trace_draw_absolute_with_lines
            else:
                if self.traces_shortage == True:
                    self.trace_draw_function = Celestial_Object.Trace_handler.trace_draw_absolute_with_circles_shorted
                else:
                    self.trace_draw_function = Celestial_Object.Trace_handler.trace_draw_absolute_with_circles
    
    def update_fps(self, current_fps: float) -> None:
        if current_fps != 0:
            self.fps = current_fps
            if self.paused == False:
                if self.preserve_speed == True:
                    self.delta_time = self.speed / self.fps
                else:
                    self.speed = self.delta_time * self.fps 

    def sx(self, x: float) -> float: 
        return(self.x_scale * (x - self.x_min))

    def sy(self, y: float) -> float: 
        return(-self.y_scale * (y - self.y_max))

    def scords(self, cords) -> tuple[float, float]:
        return((self.x_scale * (cords[0] - self.x_min), -self.y_scale * (cords[1] - self.y_max)))
    
    def clear(self):
        self.screen.fill(self.background_color)
    
    def draw_traces(self, Celestial_Object_list: list[Celestial_Object]) -> None:
        for obj in Celestial_Object_list: 
            self.trace_draw_function(obj.trace_handler)

    def draw_mass_center(self, Celestial_Object_list : list[Celestial_Object]) -> None:
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

    def draw_connecting_lines(self, Celestial_Object_list: list[Celestial_Object]) -> None:
        for i in range(len(Celestial_Object_list)):
            for j in range(i+1, len(Celestial_Object_list)):
                pg.draw.line(self.screen, (255, 255 ,255), self.scords((Celestial_Object_list[i].x, Celestial_Object_list[i].y)), self.scords((Celestial_Object_list[j].x, Celestial_Object_list[j].y)))

    '''def draw_connecting_lines_with_distance_correlation(self, Celestial_Object_list: list, distance, color_if_more, color_if_less) -> None:
        for i in range(len(Celestial_Object_list)):
            for j in range(i+1, len(Celestial_Object_list)):
                if distance**2 < (Celestial_Object_list[i].x - Celestial_Object_list[j].x)**2 + (Celestial_Object_list[i].y - Celestial_Object_list[j].y)**2:
                    pg.draw.line(self.screen, color_if_more, self.scords((Celestial_Object_list[i].x, Celestial_Object_list[i].y)), self.scords((Celestial_Object_list[j].x, Celestial_Object_list[j].y)))
                else:
                    pg.draw.line(self.screen, color_if_less, self.scords((Celestial_Object_list[i].x, Celestial_Object_list[i].y)), self.scords((Celestial_Object_list[j].x, Celestial_Object_list[j].y)))'''
    
window = Window(WIDTH, HEIGHT, BACKGROUND_COLOR, X_MIN, X_MAX, Y_MIN, Y_MAX)
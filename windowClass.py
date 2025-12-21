import pygame as pg
from parameters import *
from utiles import rainbow_color
from math import atan2, sqrt, pi
from collections.abc import Callable
from celestialObjectClass import Celestial_Object

class Window:
    def __init__(self, width: float, height: float, background_color: tuple[int, int, int], x_min: float, x_max: float, y_min: float, y_max: float):
        self.width = width
        self.height = height
        self.background_color = background_color
        
        self.clock = pg.time.Clock()
        self.parameters_handler = Window.Parameters_handler(self, SPEED_SLIDER_SENSITIVITY, DELTA_TIME_SLIDER_SENSITIVITY, MASS_SLIDER_SENSITIVITY)
        self.screen = pg.display.set_mode((width, height))
        self.camera = Window.Camera(self, CAMERA_SPEED, ZOOMING_SPEED, x_min, x_max, y_min, y_max)
        self.object_generator = Window.Object_generator(self)

    class Camera:
        def __init__(self, window, camera_speed: float, zooming_speed: float, x_min: float, x_max: float, y_min: float, y_max: float):
            self.win = window
            self.moving_speed = camera_speed
            self.zooming_speed = zooming_speed
            self.x_min = x_min
            self.x_max = x_max
            self.y_min = y_min
            self.y_max = y_max
            self.dx = self.x_max - self.x_min
            self.dy = self.y_max - self.y_min
            self.x_scale = self.win.width / self.dx
            self.y_scale = self.win.height / self.dy

        def move_up(self) -> None:
            self.win.parameters_handler.unpin()
            self.y_min += self.dy * self.moving_speed / self.win.parameters_handler.fps
            self.y_max += self.dy * self.moving_speed / self.win.parameters_handler.fps

        def move_down(self) -> None:
            self.win.parameters_handler.unpin()
            self.y_min -= self.dy * self.moving_speed / self.win.parameters_handler.fps
            self.y_max -= self.dy * self.moving_speed / self.win.parameters_handler.fps

        def move_right(self) -> None:
            self.win.parameters_handler.unpin()
            self.x_min += self.dy * self.moving_speed / self.win.parameters_handler.fps
            self.x_max += self.dy * self.moving_speed / self.win.parameters_handler.fps

        def move_left(self) -> None:
            self.win.parameters_handler.unpin()
            self.x_min -= self.dy * self.moving_speed / self.win.parameters_handler.fps
            self.x_max -= self.dy * self.moving_speed / self.win.parameters_handler.fps

        def move_to(self, x: float, y: float) -> None:
            self.win.parameters_handler.unpin()
            self.x_min = x - self.dx / 2
            self.y_min = y - self.dy / 2
            self.x_max = x + self.dx / 2
            self.y_max = y + self.dy / 2

        def move_to_object(self, obj) -> None:
            self.move_to(obj.x, obj.y)
        
        def move_to_pinned_object(self) -> None:
            if self.win.parameters_handler.is_pinned_object:
                self.x_min = self.win.parameters_handler.pinned_object.x - self.dx / 2
                self.y_min = self.win.parameters_handler.pinned_object.y - self.dy / 2
                self.x_max = self.win.parameters_handler.pinned_object.x + self.dx / 2
                self.y_max = self.win.parameters_handler.pinned_object.y + self.dy / 2

        def zoom(self, wheel_rotation: float) -> None:
            if self.dx >= 1 and self.dy >= 1:
                x_change = self.dx * self.zooming_speed
                y_change = self.dy * self.zooming_speed
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
                    x_change = self.dx * self.zooming_speed
                    y_change = self.dy * self.zooming_speed
                    self.x_min -= x_change
                    self.y_min -= y_change
                    self.x_max += x_change
                    self.y_max += y_change
            self.dx = self.x_max - self.x_min
            self.dy = self.y_max - self.y_min
            self.x_scale = self.win.width / self.dx
            self.y_scale = self.win.height / self.dy

        def check_visibility(self, x, y, radius = 0) -> bool:
            if radius == 0:
                return(self.x_min <= x <= self.x_max) and (self.y_min <= y <= self.y_max)
            else:
                return(self.x_min - radius <= x <= self.x_max + radius) and (self.y_min - radius <= y <= self.y_max + radius)

    class Parameters_handler:
        def __init__(self, windwow, speed_slider_sensitivity: float, delta_time_slider_sensitivity: float, mass_slider_sensitivity):
            self.win = windwow
            self.speed_slider_sensitivity = speed_slider_sensitivity
            self.delta_time_slider_sensitivity = delta_time_slider_sensitivity
            self.mass_slider_sensitivity = mass_slider_sensitivity
            
            self.gravity_constant: float
            self.trace_quality = 20
            self.remainder: float = 0
            self.force_equation: Callable
            self.pinned_object: Celestial_Object

            self.paused = False
            self.fps = 1000
            self.preserve_speed = PRESERVE_SPEED
            if self.preserve_speed:
                self.speed = ORIGINAL_SPEED
                self.delta_time = self.speed / self.fps
            else:
                self.delta_time = ORIGINAL_DELTA_TIME
                self.speed = self.delta_time * self.fps

            self.traces = False
            self.local_traces = False
            self.traces_shortage = False
            self.feather_type = True
            self.is_pinned_object = False
            self.show_mass_center = True
            self.show_connecting_lines = False
            self.creation_mode = False
            self.update_trace_draw_method()

        def update_tumblers(self, key: int) -> None:
            if key == pg.K_p:
                if self.paused:
                    self.win.unpause()
                else:
                    self.win.pause()
            elif key == pg.K_t:
                self.traces = not self.traces
                self.update_trace_draw_method()
            elif key == pg.K_y:
                self.feather_type = not self.feather_type
                self.update_trace_draw_method()
            elif key == pg.K_u:
                self.local_traces = not self.local_traces
                self.update_trace_draw_method()
            elif key == pg.K_i:
                self.traces_shortage = not self.traces_shortage
                self.update_trace_draw_method()
            elif key == pg.K_k:
                self.preserve_speed = not self.preserve_speed
            elif key == pg.K_l:
                self.show_connecting_lines = not self.show_connecting_lines
            elif key == pg.K_m:
                self.show_mass_center = not self.show_mass_center
            elif key == pg.K_SLASH:
                self.creation_mode = not self.creation_mode
            elif key == pg.K_n:
                self.win.object_generator.collidable = not self.win.object_generator.collidable
            
        def update_sliders(self, keys) -> None:
            if keys[pg.K_UP]:
                self.win.camera.move_up()
            if keys[pg.K_DOWN]:
                self.win.camera.move_down()
            if keys[pg.K_RIGHT]:
                self.win.camera.move_right()
            if keys[pg.K_LEFT]:
                self.win.camera.move_left()
            if keys[pg.K_COMMA]:
                self.lower()
            if keys[pg.K_PERIOD]:
                self.increase()

        def lower(self):
            if self.creation_mode:
                self.win.object_generator.mass -= self.mass_slider_sensitivity / self.fps
            else:
                if self.preserve_speed:
                    self.lower_speed()
                else:
                    self.lower_delta_time()

        def increase(self):
            if self.creation_mode:
                self.win.object_generator.mass += self.mass_slider_sensitivity / self.fps
            else:
                if self.preserve_speed:
                    self.increase_speed()
                else:
                    self.increase_delta_time()
            
        def lower_speed(self) -> None:
            self.speed -= self.speed_slider_sensitivity / self.fps
            if self.speed < 0:
                self.speed = 0
                self.win.pause()
            self.delta_time = self.speed / self.fps

        def increase_speed(self) -> None:
            self.speed += self.speed_slider_sensitivity / self.fps
            self.delta_time = self.speed / self.fps

        def lower_delta_time(self) -> None:
            self.delta_time -= self.delta_time_slider_sensitivity / self.fps
            if self.delta_time < 0:
                self.delta_time = 0
                self.win.pause()
            self.speed = self.delta_time * self.fps

        def increase_delta_time(self) -> None:
            self.delta_time += self.delta_time_slider_sensitivity / self.fps
            self.speed = self.delta_time * self.fps
        
        def unpin(self) -> None:
            if self.is_pinned_object:
                self.is_pinned_object = False
                self.update_trace_draw_method()

        def update_trace_draw_method(self) -> None:
            if self.local_traces == True and self.is_pinned_object:
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
        
        def update_fps(self) -> None:
            current_fps = self.win.clock.get_fps()
            if current_fps != 0:
                self.fps = current_fps
                if self.paused == False:
                    if self.preserve_speed == True:
                        self.delta_time = self.speed / self.fps
                    else:
                        self.speed = self.delta_time * self.fps

    class Object_generator:
        def __init__(self, window):
            self.win = window
            self.velocity_multiplier = 2
            self.stage = 0
            self.mass = 100
            self.collidable = False

        def confirm(self, mouse_x: float, mouse_y: float) -> None:
            if self.stage == 0:
                self.set_coords(mouse_x, mouse_y)
                self.stage = 1
            elif self.stage == 1:
                self.set_radius(mouse_x, mouse_y)
                self.set_color(mouse_x, mouse_y)
                self.stage = 2
            elif self.stage == 2:
                self.set_velocity(mouse_x, mouse_y)
                self.create_object()
                self.stage = 0

        def get_radius(self, mouse_x, mouse_y) -> float:
            return(sqrt((mouse_x - self.x)**2 + (mouse_y - self.y)**2))
        
        def get_color(self, mouse_x: float, mouse_y: float) -> tuple[int, int, int]:
            angle = 180 / pi * atan2(mouse_y - self.y, mouse_x - self.x)
            if angle < 0:
                angle += 360
            return(rainbow_color(angle))
        
        def get_velocity(self, mouse_x: float, mouse_y: float) -> float:
            return(self.velocity_multiplier * sqrt((mouse_x - self.x)**2 + (mouse_y - self.y)**2))
        
        def set_coords(self, mouse_x: float, mouse_y: float) -> None:
            self.x = mouse_x
            self.y = mouse_y
        
        def set_radius(self, mouse_x: float, mouse_y: float) -> None:
            self.radius = sqrt((mouse_x - self.x)**2 + (mouse_y - self.y)**2)

        def set_color(self, mouse_x: float, mouse_y: float) -> None:
            self.color = self.get_color(mouse_x, mouse_y)

        def set_velocity(self, mouse_x: float, mouse_y: float) -> None:
            self.x_velocity = (mouse_x - self.x) * self.velocity_multiplier
            self.y_velocity = (mouse_y - self.y) * self.velocity_multiplier

        def create_object(self) -> None:
            Celestial_Object(self.win, self.x, self.y, self.mass, self.radius, self.x_velocity, self.y_velocity, self.color, collidable = self.collidable, trace_len = 1000)
            self.stage = 0
        
        def show_progress(self) -> None:
            mouse_x, mouse_y = self.win.inverse_scords(pg.mouse.get_pos())
            if self.stage == 1:
                radius = round(self.get_radius(mouse_x, mouse_y))
                color = self.get_color(mouse_x, mouse_y)
            else:
                radius = self.radius
                color = self.color
            if self.stage == 2:
                pg.draw.line(self.win.screen, color, self.win.scords((self.x, self.y)), (pg.mouse.get_pos()))
            pg.draw.ellipse(self.win.screen, color, (self.win.sx(self.x) - self.win.camera.x_scale * radius, self.win.sy(self.y) - self.win.camera.y_scale * radius,
                            2*self.win.camera.x_scale * radius, 2*self.win.camera.y_scale * radius))
        
        def get_caption(self) -> str:
            mouse_x, mouse_y = self.win.inverse_scords(pg.mouse.get_pos())
            if self.stage == 1:
                radius = round(self.get_radius(mouse_x, mouse_y))
            else:
                radius = round(self.radius)
            return(f'Creation mode | Mass: {round(self.mass)} | Radius: {radius} | Velocity: {round(self.get_velocity(mouse_x, mouse_y))} | Collision: {self.collidable}')
    
    def pause(self) -> None:
        self.parameters_handler.paused = True
    
    def unpause(self) -> None:
        if self.parameters_handler.paused:
            self.parameters_handler.paused = False
            if self.parameters_handler.delta_time != 0:
                self.parameters_handler.fps = self.parameters_handler.speed / self.parameters_handler.delta_time

    def sx(self, x: float) -> float: 
        return(self.camera.x_scale * (x - self.camera.x_min))

    def sy(self, y: float) -> float: 
        return(-self.camera.y_scale * (y - self.camera.y_max))

    def scords(self, cords) -> tuple[float, float]:
        return((self.camera.x_scale * (cords[0] - self.camera.x_min), -self.camera.y_scale * (cords[1] - self.camera.y_max)))
    
    def inverse_sx(self, sx: float) -> float: 
        return((sx / self.camera.x_scale + self.camera.x_min))

    def inverse_sy(self, sy: float) -> float: 
        return(-sy / self.camera.y_scale + self.camera.y_max)

    def inverse_scords(self, scords: tuple[float, float]) -> tuple[float, float]:
        return((scords[0] / self.camera.x_scale + self.camera.x_min), (-scords[1] / self.camera.y_scale + self.camera.y_max))
    
    def clear(self) -> None:
        self.screen.fill(self.background_color)
    
    def traces_update(self, Celestial_Object_list: list[Celestial_Object]) -> None: #
        self.parameters_handler.remainder += 1000 * self.parameters_handler.delta_time
        if  self.parameters_handler.remainder >= self.parameters_handler.trace_quality:
            self.parameters_handler.remainder -= self.parameters_handler.trace_quality
            for obj in Celestial_Object_list:
                obj.trace_handler.trace_update()

    def draw_traces(self, Celestial_Object_list: list[Celestial_Object]) -> None:
        for obj in Celestial_Object_list:
            if len(obj.trace_handler.trace) > 1:
                self.parameters_handler.trace_draw_function(obj.trace_handler)

    def draw_mass_center(self, Celestial_Object_list: list[Celestial_Object]) -> None:
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
        for i, obj1 in enumerate(Celestial_Object_list):
            for obj2 in Celestial_Object_list[i+1:]:
                pg.draw.line(self.screen, (255, 255 ,255), self.scords((obj1.x, obj1.y)), self.scords((obj2.x, obj2.y)))

    def update_caption(self) -> None:
        if self.parameters_handler.creation_mode and self.object_generator.stage != 0:
            pg.display.set_caption(self.object_generator.get_caption())
        elif self.parameters_handler.creation_mode:
            mouse_x, mouse_y = self.inverse_scords(pg.mouse.get_pos())
            pg.display.set_caption(f'Creation mode | X: {round(mouse_x)} | Y: {round(mouse_y)}')
        else:
            pg.display.set_caption(f'Celestial system | Speed: {round(self.parameters_handler.speed, 2)} | Delta Time: {round(self.parameters_handler.delta_time, 4)} | Fps: {round(self.parameters_handler.fps)}')
    
window = Window(WIDTH, HEIGHT, BACKGROUND_COLOR, X_MIN, X_MAX, Y_MIN, Y_MAX)
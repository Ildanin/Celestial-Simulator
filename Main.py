from math import *
import pygame as pg
from windowClass import Window
from parameters import *
from celestialObjectClass import *

import presetExamples

window = Window(WIDTH, HEIGHT, BACKGROUND_COLOR, X_MIN, X_MAX, Y_MIN, Y_MAX, GRAVITY_CONSTANT, PRESERVE_SPEED, ORIGINAL_SPEED, ORIGINAL_DELTA_TIME, CAMERA_SPEED, SCALING_SPEED, SPEED_CHANGING_SPEED, SPEED_CHANGING_DELTA_TIME)
clock = pg.time.Clock()

presetExamples.load_example_to_window(window, 2)

while True:
#event handler
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
                if window.paused:
                    window.unpause()
                else:
                    window.pause()
            elif event.key == pg.K_t:
                window.traces = not window.traces
            elif event.key == pg.K_y:
                window.feather_type = not window.feather_type
            elif event.key == pg.K_u:
                window.local_traces = not window.local_traces
            elif event.key == pg.K_i:
                window.traces_shortage = not window.traces_shortage
            elif event.key == pg.K_k:
                window.preserve_speed = not window.preserve_speed
            elif event.key == pg.K_l:
                window.show_connecting_lines = not window.show_connecting_lines
            elif event.key == pg.K_m:
                window.show_mass_center = not window.show_mass_center
        elif event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[2]:
                window.pinned_object = False
            elif pg.mouse.get_pressed()[0]:
                for obj in Celestial_Object_list:
                    if pg.Rect(window.sx(obj.x) - window.x_scale * obj.r, window.sy(obj.y) - window.y_scale * obj.r, 2 * window.x_scale * obj.r, 2 * window.y_scale * obj.r).collidepoint(pg.mouse.get_pos()):
                        window.pinned_object = obj
        elif event.type == pg.MOUSEWHEEL:
            window.view_rescale(event.y)


#cam movement
    keys = pg.key.get_pressed()
    if keys[pg.K_UP]:
        window.camera_move_up()
    if keys[pg.K_DOWN]:
        window.camera_move_down()
    if keys[pg.K_RIGHT]:
        window.camera_move_right()
    if keys[pg.K_LEFT]:
        window.camera_move_left()
    if keys[pg.K_COMMA]:
        if window.preserve_speed:
            window.lower_speed()
        else:
            window.lower_delta_time()
    if keys[pg.K_PERIOD]:
        if window.preserve_speed:
            window.increase_speed()
        else:
            window.increase_delta_time()

#game processes
    Collision_list = []
    for i, obj in enumerate(Celestial_Object_list):
        obj.new_velocity(window, i, Collision_list)
    if Collision_list:
        for collision in Collision_list:
            collision[0].impact(window, collision[1])
    for obj in Celestial_Object_list:
        obj.move(window)
        obj.trace_update(window)

#rendering
    window.clear()
    window.camera_move_to_pinned_object()

    if window.traces == True:
        for obj in Celestial_Object_list:
            obj.trace_draw(window)
    else:
        for obj in Celestial_Object_list:
            if obj.feather:
                obj.trace_draw(window)
    for obj in Celestial_Object_list:
        obj.draw(window)

#Screen update and other
    window.update_fps(clock.get_fps())
    if window.show_mass_center:
        window.draw_mass_center(Celestial_Object_list)
    if window.show_connecting_lines:
        window.draw_connecting_lines(Celestial_Object_list)

    pg.display.flip()
    pg.display.set_caption('Celestial system' + ' | Speed:' + str(round(window.speed, 2)) + ' | Delta Time:' + str(round(window.delta_time, 4)) + ' | Fps:' + str(round(window.fps)))
    clock.tick()
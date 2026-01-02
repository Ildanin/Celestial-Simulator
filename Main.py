if __name__ == '__main__':
    import pygame as pg
    import presetExamples
    from dataProcessing import Pool
    from windowClass import window
    from parameters import EXAMPLE_NUMBER, PARALEL_PROCESSES_USED
    from celestialObjectClass import *

    presetExamples.load_example_to_window(window, EXAMPLE_NUMBER)
    pool = Pool(PARALEL_PROCESSES_USED)
    pool.start()
    pool.send((window.parameters_handler.force_equation, window.parameters_handler.gravity_constant, [(obj.x, obj.y, obj.m, obj.r) for obj in Celestial_Object_list]))
    
    while True:
    #event handler
        keys = pg.key.get_pressed()
        window.camera.move(keys)
        window.parameters_handler.update_sliders(keys)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pool.kill()
                exit()
            elif event.type == pg.KEYDOWN:
                window.parameters_handler.update_tumblers(event.key)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed()[0]:
                    mouse_x, mouse_y = window.inverse_scords(pg.mouse.get_pos())
                    if window.parameters_handler.creation_mode == True:
                        window.object_editor.confirm(mouse_x, mouse_y)
                    else:
                        objs = [obj for obj in Celestial_Object_list if (mouse_x - obj.x)**2 + (mouse_y - obj.y)**2 < obj.r**2]
                        if len(objs) == 1:
                            window.parameters_handler.pin_object(objs[0])
                        elif len(objs) > 1:
                            window.parameters_handler.pin_object(min(((obj, (mouse_x - obj.x)**2 + (mouse_y - obj.y)**2) for obj in objs), key = lambda x: x[1])[0])
                        if window.parameters_handler.is_pinned_object:
                            for obj in Celestial_Object_list:
                                obj.trace_handler.local_trace_generate()
                elif pg.mouse.get_pressed()[2]:
                    window.parameters_handler.unpin()
                    window.object_editor.undo_progress()
            elif event.type == pg.MOUSEWHEEL:
                window.camera.zoom(event.y)

    #game processes
        if window.parameters_handler.paused == False and window.parameters_handler.speed != 0 and window.parameters_handler.delta_time != 0:
            X_accelerations, Y_accelerations, Collisions = pool.recv()

            for obj, x_acceleration, y_acceleration in zip(Celestial_Object_list, X_accelerations, Y_accelerations):
                obj.update_velocity(x_acceleration, y_acceleration)
            
            for obj1, obj2 in [(Celestial_Object_list[collision[0]], Celestial_Object_list[collision[1]]) for collision in Collisions.__reversed__()]:
                if obj1.collidable and obj2.collidable:
                    obj1.impact(obj2)
 
            for obj in Celestial_Object_list:
                obj.move()
            pool.send((window.parameters_handler.force_equation, window.parameters_handler.gravity_constant, [(obj.x, obj.y, obj.m, obj.r) for obj in Celestial_Object_list]))
            window.traces_update(Celestial_Object_list)

    #rendering
        window.clear()
        window.camera.move_to_pinned_object()

        if window.parameters_handler.traces == True:
            window.draw_traces(Celestial_Object_list)
        else:
            window.draw_traces([obj for obj in Celestial_Object_list if obj.feather])

        for obj in Celestial_Object_list:
            obj.draw()

    #Screen update and other
        window.parameters_handler.update_fps()
        if window.parameters_handler.show_mass_center:
            window.draw_mass_center(Celestial_Object_list)
        if window.parameters_handler.show_connecting_lines:
            window.draw_connecting_lines(Celestial_Object_list)
        if window.parameters_handler.creation_mode and window.object_editor.stage != 0:
            window.object_editor.show_progress()
        if window.parameters_handler.draw_vectors:
            window.draw_speed_vectors(Celestial_Object_list)

        pg.display.flip()
        window.update_caption()
        window.clock.tick()
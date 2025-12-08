if __name__ == '__main__':
    import pygame as pg
    from dataProcessing import Pool
    from windowClass import window
    from parameters import EXAMPLE_NUMBER, PARALEL_PROCESSES_USED
    from celestialObjectClass import *
    import presetExamples
    import time

    #load example function
    presetExamples.load_example_to_window(window, EXAMPLE_NUMBER)

    clock = pg.time.Clock()

    pool = Pool(PARALEL_PROCESSES_USED)
    pool.start(window.force_equation)

    while True:
    #event handler
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pool.kill()
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    if window.paused:
                        window.unpause()
                    else:
                        window.pause()
                elif event.key == pg.K_t:
                    window.traces = not window.traces
                    window.update_trace_draw_method()
                elif event.key == pg.K_y:
                    window.feather_type = not window.feather_type
                    window.update_trace_draw_method()
                elif event.key == pg.K_u:
                    window.local_traces = not window.local_traces
                    window.update_trace_draw_method()
                elif event.key == pg.K_i:
                    window.traces_shortage = not window.traces_shortage
                    window.update_trace_draw_method()
                elif event.key == pg.K_k:
                    window.preserve_speed = not window.preserve_speed
                elif event.key == pg.K_l:
                    window.show_connecting_lines = not window.show_connecting_lines
                elif event.key == pg.K_m:
                    window.show_mass_center = not window.show_mass_center
            elif event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed()[2]:
                    window.pinned_object = False
                    window.update_trace_draw_method()
                elif pg.mouse.get_pressed()[0]:
                    for obj in Celestial_Object_list:
                        if pg.Rect(window.sx(obj.x) - window.x_scale * obj.r, window.sy(obj.y) - window.y_scale * obj.r, 2 * window.x_scale * obj.r, 2 * window.y_scale * obj.r).collidepoint(pg.mouse.get_pos()):
                            window.pinned_object = obj
                            window.update_trace_draw_method()
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
        if window.paused == False:
            T1 = time.perf_counter()

            Distance_list = pool.process([(obj.x, obj.y) for obj in Celestial_Object_list])

            #T2 = time.perf_counter()
            #sprint("total", T2-T1)

            for obj in Celestial_Object_list[:-1]:
                obj.update_velocity(Distance_list)

            T2 = time.perf_counter()
            print("total", T2-T1)
        
            Collision_list: list[tuple[Celestial_Object, Celestial_Object]] = []
            for obj in [obj for obj in Celestial_Object_list if obj.collision == True]:
                Collision_list += obj.collision_check(Distance_list)
            if Collision_list:
                for obj1, obj2 in Collision_list.__reversed__():
                    obj1.impact(obj2)

            
            for obj in Celestial_Object_list:
                obj.move()
                obj.trace_handler.trace_update()

    #rendering
        window.clear()
        window.camera_move_to_pinned_object()

        if window.traces == True:
            window.draw_traces(Celestial_Object_list)
        else:
            window.draw_traces([obj for obj in Celestial_Object_list if obj.feather])

        for obj in Celestial_Object_list:
            obj.draw()

    #Screen update and other
        clock.get_time()
        window.update_fps(clock.get_fps())
        if window.show_mass_center:
            window.draw_mass_center(Celestial_Object_list)
        if window.show_connecting_lines:
            window.draw_connecting_lines(Celestial_Object_list)

        pg.display.flip()
        pg.display.set_caption('Celestial system' + ' | Speed:' + str(round(window.speed, 2)) + ' | Delta Time:' + str(round(window.delta_time, 4)) + ' | Fps:' + str(round(window.fps)))
        clock.tick()
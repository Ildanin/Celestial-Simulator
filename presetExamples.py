from celestialObjectClass import *
from random import randint
from windowClass import Window
from utiles import *


        
def load_example_to_window(win : Window, example_n : int, additional_info : list = []):
    if   example_n == 0:
        pass

    elif example_n == 1: #Star-Planet-Satelite          force=G*M*m/R**2
        win.force_equation = GMm_d_r2
        win.gravity_constant = 1

        m = 10000
        Celestial_Object(0,   0, 100 * m, 15, x_velocity = 0, y_velocity = -0.5, color = (255, 255, 0),   feather = False)
        Celestial_Object(400, 0, m,       10, x_velocity = 0 ,y_velocity=50    , color = (0,   0,   255), feather = True, trace_len = 100)
        Celestial_Object(425, 0, 100,      4, x_velocity = 0 ,y_velocity=68    , color = (0,   255, 0),   feather = True, trace_len = 100)
    
    elif example_n == 2: #polygon n-body problem        force=Any
        #force=G*M*m/R is recommended
        win.force_equation = GMm_d_r1
        win.gravity_constant = 100
        win.speed = 0.1

        m = 10000
        r = 400
        v = 500
        impacts = False
        n = 8
        for i in range(n):
            angle = 2 * pi * i / n
            Celestial_Object(cos(angle) * r, sin(angle) * r, m, 5, x_velocity = -sin(angle) * v, y_velocity = cos(angle) * v, color = rainbow_color(angle * 180 / pi), feather = False, trace_len = 1000, collision = impacts)
    
    elif example_n == 3: #Proto_solar_system-Black_hole force=G*M*m/R**2
        win.force_equation = GMm_d_r2
        win.gravity_constant = 10

        create_black_hole = False
        star_mass = 1000000
        proto_planet_mass = 100
        n = 21
        square_side = 6000
        velocity_factor = 80000
        Celestial_Object(0, 0, star_mass, 300, x_velocity = 0, y_velocity = 0, color = (255, 255, 0), feather = False)
        if create_black_hole == True:
            Celestial_Object(10000, 1000, 1000 * star_mass, 30,  x_velocity = 0, y_velocity = 0, color = (220, 20, 60), feather = False, color_mix = False, material_mix_type = 'density')
        for i in range(1, n):
            for j in range(1, n):
                x = i * square_side / n - square_side / 2
                y = j * square_side / n - square_side / 2
                distance = sqrt(x**2 + y**2)
                x_vel = -velocity_factor * y / distance**2
                y_vel =  velocity_factor * x / distance**2
                Celestial_Object(x, y, proto_planet_mass * randint(5, 15) / 10, 5, x_vel * randint(5, 15) / 10, y_vel * randint(5, 15) / 10, (randint(0,255), randint(0,255), randint(0,255)))

    elif example_n == 4: #Star-Planet                   force=G*M*m
        win.force_equation = GMm
        win.gravity_constant = 1

        Celestial_Object(0,   0, 2000, 30, x_velocity = 0 ,y_velocity = -1,  color = (255, 255, 0), feather = False)
        Celestial_Object(400, 0, 10,   10, x_velocity = 0 ,y_velocity = 200, color = (0, 0, 255),   feather = True, trace_len = 1000, trace_quality = 30)
    
    elif example_n == 5: #Star-Planet                   force=G*M*m/R
        win.force_equation = GMm_d_r1
        win.gravity_constant = 1

        Celestial_Object(0,   0, 1600, 30, x_velocity = 0 ,y_velocity = -0.05, color = (255, 255, 0), feather = False)
        Celestial_Object(200, 0, 1,    10, x_velocity = 0 ,y_velocity = 40, color = (0, 0, 255), feather = True, trace_len = 1000, trace_quality = 30)
        Celestial_Object(400, 0, 1,    10, x_velocity = 0 ,y_velocity = 40, color = (0, 0, 255), feather = True, trace_len = 1000, trace_quality = 30)
    
    elif example_n == 6: #Star-Planet                   force=G*M*m*R
        win.force_equation = GMmr1
        win.gravity_constant = 0.04

        Celestial_Object(0,   0, 1600, 30, x_velocity = 0 ,y_velocity = -3,   color = (255, 255, 0), feather = False)
        Celestial_Object(200, 0, 1,    10, x_velocity = 0 ,y_velocity = 1600, color = (0, 0, 255),   feather = True, trace_len = 1000, trace_quality = 10)
        Celestial_Object(400, 0, 1,    10, x_velocity = 0 ,y_velocity = 3200, color = (0, 0, 255),   feather = True, trace_len = 1000, trace_quality = 10)
    
    elif example_n == 7: #Star-Planet                   force=G*M*m*R
        #demonstation of local traces
        win.force_equation = GMmr1
        win.gravity_constant = 0.04

        Celestial_Object(0,   0, 1600, 30, x_velocity = 0 ,y_velocity = -3,   color = (255, 255, 0), feather = False)
        Celestial_Object(200, 0, 1,    10, x_velocity = 0 ,y_velocity = 3200, color = (0, 0, 255),   feather = True, trace_len = 1000, trace_quality = 10)
        Celestial_Object(400, 0, 1,    10, x_velocity = 0 ,y_velocity = 1600, color = (0, 0, 255),   feather = True, trace_len = 1000, trace_quality = 10)
    elif example_n == 8:
        #sample example
        win.force_equation = GMm_d_r2
        win.gravity_constant = 1

        pass
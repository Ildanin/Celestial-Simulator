from math import cos

def GMmrp(gravity_constant: float, main_mass: float, second_mass: float, distance:float, power: int = -2) -> float:
    return(gravity_constant * main_mass * second_mass / (distance ** power))

def GMm_d_r3(gravity_constant: float, main_mass: float, second_mass: float, distance:float) -> float:
    return(gravity_constant * main_mass * second_mass / (distance**3))

def GMm_d_r2(gravity_constant: float, main_mass: float, second_mass: float, distance:float) -> float:
    return(gravity_constant * main_mass * second_mass / (distance**2))

def GMm_d_r1(gravity_constant: float, main_mass: float, second_mass: float, distance:float) -> float:
    return(gravity_constant * main_mass * second_mass / (distance))

def GMm(gravity_constant: float, main_mass: float, second_mass: float, distance:float) -> float:
    return(gravity_constant * main_mass * second_mass)

def GMmr1(gravity_constant: float, main_mass: float, second_mass: float, distance:float) -> float:
    return(gravity_constant * main_mass * second_mass * (distance))

def GMmr2(gravity_constant: float, main_mass: float, second_mass: float, distance:float) -> float:
    return(gravity_constant * main_mass * second_mass * (distance**2))

def GMmr3(gravity_constant: float, main_mass: float, second_mass: float, distance:float) -> float:
    return(gravity_constant * main_mass * second_mass * (distance**3))

def string_like_gravity(gravity_constant: float, main_mass: float, second_mass: float, distance:float) -> float:
    string_len = 1000
    if distance > string_len:
        return(gravity_constant * (distance - string_len))
    else:
        return(0)

def WTF(gravity_constant: float, main_mass: float, second_mass: float, distance:float) -> float:
    return(gravity_constant * main_mass * second_mass * cos(distance / 315))



def rainbow_color(angle: float) -> tuple[int, int, int]:
    red = 0
    green = 0
    blue = 0
    if   0 <= angle <= 60:
        red = 255
        green = round(255 / 60 * angle)
        blue = 0
    elif 60 <= angle <= 120:
        red = round(255 - 255 / 60 * (angle - 60))
        green = 255
        blue = 0
    elif 120 <= angle <= 180:
        red = 0
        green = 255
        blue = round(255 / 60 * (angle - 120))
    elif 180 <= angle <= 240:
        red = 0
        green = round(255 - 255 / 60 * (angle - 180))
        blue = 255
    elif 240 <= angle <= 300:
        red = round(255 / 60 * (angle - 240))
        green = 0
        blue = 255
    elif 300 <= angle <= 360:
        red = 255
        green = 0
        blue = round(255 - 255 / 60 * (angle - 300))
    return((red, green, blue))
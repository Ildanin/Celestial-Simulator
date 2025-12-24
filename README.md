To run the code you need to download pygame library
https://www.pygame.org
command: pip install pygame

Keys:
- P to pause or unpause
- T to turn on/off traces (doesn't do anything to bodies that have feather = True)
- Y to change feather type (how trace is drawn with lines or dots)
- U to turn on/off local traces
- i  to cut traces max length by a factor or not
- J to change the simulation mode (preserve speed or delta time)
- L to draw connecting lines between bodies or not
- K to turn on/off mass center
- '<' to decrease speed or delta time (normal mode)
- '>' to increase speed or delta time (normal mode)
- Left mouse button to pin an object  (normal mode)
- Right mouse button to unpin         (normal mode)
- '/' to turn on/off creation mode
- '<' to decrease mass of generated object  (edit mode)
- '>' to increase mass of generated object  (edit mode)
- Left mouse button to set position -> set color and radius -> set speed and create an object  (edit mode)
- Right mouse button to undo (edit mode)
- Mouse wheel is used to zoom in or out
- Arrows are used to move around

How to create your own simulation:
All the simulations are created within presetExamples file. There is a sample on the botton that you can copy. 
First you need to define the gravity force equation and gravity constant. Force equation functions are defined in utiles file. You can create your own if you want.
command:
win.force_equation = GMm_d_r2 (here _d_ means divide and r2 means r to the power of two)
win.gravity_constant = 1

After that you create celestial body using Celestial_Object class:
Celestial_Object(x, y, mass, radius, x_velocity, y_velocity) 
Theese are main parametrs, but there are some additionals such as color, feather and collision.
In the end you need to change the EXAMPLE_NUMBER to the example_n you want to use.

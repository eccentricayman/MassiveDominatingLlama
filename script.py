import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    ident(tmp)
    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    tmp = []
    step = 0.1
    for command in commands:
        line = command[0]
        args = command[1:]
        top = stack[-1]

        if line == "push":
            stack.append([x[:] for x in top])

        elif line == "pop":
            stack.pop()

        elif line == "move":
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(top, t)
            top = [x[:] for x in t]

        elif line == "rotate":
            theta = float(args[1]) * (math.pi / 180)

            if args[0] == "x":
                t = make_rotX(theta)
            elif args[0] == "y":
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult(top, t)
            top = [x[:] for x in t]

        elif line == "scale":
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(top, t)
            top = [x[:] for x in t]

        elif line == "box":
            add_box(tmp,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult(top, tmp)
            draw_polygons(tmp, screen, color)
            tmp = []

        elif line == "sphere":
            add_sphere(tmp,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)
            matrix_mult(top, tmp)
            draw_polygons(tmp, screen, color)
            tmp = []

        elif line == "torus":
            add_torus(tmp,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step)
            matrix_mult(top, tmp)
            draw_polygons(tmp, screen, color)
            tmp = []
            
        elif line == "line":
            add_edge(tmp,
                     float(args[0]), float(args[1]), float(args[2]),
                     float(args[3]), float(args[4]), float(args[5]))
            matrix_mult(top, tmp)
            draw_lines(tmp, screen, color)
            tmp = []

        elif line == 'display' or line == 'save':
            if line == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])

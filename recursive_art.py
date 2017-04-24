""" TODO: Put your header comment here """

import random
import math
from PIL import Image

prod = lambda x, y, t: x*y*t
avg = lambda x, y, t: (x+y+t)/3
cos = lambda x, y, t: math.cos(math.pi*x)
sin = lambda x, y, t: math.sin(math.pi*x)
sqrt = lambda x, y, t: math.sqrt(abs(x))
cube = lambda x, y, t: x**3
x_x = lambda x, y, t: x
y_y = lambda x, y, t: y
t_t = lambda x, y, t: t
boi = [prod, avg, cos, sin, sqrt, cube, x_x, y_y, t_t]


def build_random_function(depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    if depth == 1:
        i = random.randint(6,7)
        return boi[i]
    else:
        i = random.randint(0,5)
        f1 = build_random_function(depth-1)
        f2 = build_random_function(depth-1)
        f3 = build_random_function(depth-1)
        return lambda x, y, t: boi[i](f1(x,y,t), f2(x,y,t), f3(x,y,t))

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """

    r = val - input_interval_start
    s = output_interval_end - output_interval_start
    m = input_interval_end - input_interval_start
    val_out = output_interval_start + s * (r/ m)
    return val_out


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def generate_art(filename, x_size=350, y_size=350, t_size=63):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(8)
    green_function = build_random_function(8)
    blue_function = build_random_function(8)

    # Create frames for the movie
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for k in range(t_size):
        t = remap_interval(k, 0, t_size, -1, 1)
        for i in range(x_size):
            for j in range(y_size):
                x = remap_interval(i, 0, x_size, -1, 1)
                y = remap_interval(j, 0, y_size, -1, 1)
                pixels[i, j] = (
                        color_map(red_function(x, y, t)),
                        color_map(green_function(x, y, t)),
                        color_map(blue_function(x, y, t)))
        im.save(filename + str(k) + ".png")


if __name__ == '__main__':
    #import doctest
    #doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myartmovie")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")

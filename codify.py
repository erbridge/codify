#!/usr/bin/env python

import math

import cairo

from bitarray import bitarray


class Painter:

    @staticmethod
    def draw_black(context, width, height):
        context.set_source_rgb(0, 0, 0)
        Painter._draw_rectangle(context, width, height)

    @staticmethod
    def draw_white(context, width, height):
        context.set_source_rgb(1, 1, 1)
        Painter._draw_rectangle(context, width, height)

    @staticmethod
    def _draw_rectangle(context, width, height):
        # Add 1 to ensure there's no visible gap between "1"s
        width += 1
        height += 1
        context.rel_line_to(width, 0)
        point = context.get_current_point()
        context.rel_line_to(0, height)
        context.rel_line_to(-width, 0)
        context.close_path()
        context.fill()
        context.move_to(point[0] - 1, point[1])


class SVGGenerator:

    @staticmethod
    def run(input_str, num_lines, width, height, output_filename):
        context = cairo.Context(
            cairo.SVGSurface(output_filename, width, height))

        line_height = height / num_lines

        bit_array = bitarray()
        bit_array.fromstring(input_str)
        bit_str = bit_array.to01()

        line_char_width = math.ceil(len(bit_str) * 1.0 / num_lines)
        lines = [bit_str[i:i + line_char_width]
                 for i in range(0, len(bit_str), line_char_width)]

        box_width = width / line_char_width

        current_y = -1
        for line in lines:
            # Start at -1 to cancel out the extra point added in `Painter`
            # to ensure there's no visible gap between "1"s
            context.move_to(-1, current_y)
            for bit in line:
                if int(bit):
                    Painter.draw_black(context, box_width, line_height)
                else:
                    Painter.draw_white(context, box_width, line_height)
            current_y += line_height

if __name__ == "__main__":
    import getopt
    import sys

    usage = "codify.py -i <input_str> [-o <output_filename> -n <num_lines> -W <width> -H <height>]"

    try:
        opts, _ = getopt.getopt(sys.argv[1:], "hi:o:n:W:H:", ["input_str=", "output_filename=", "num_lines=", "width=", "height="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(1)

    input_str = ""
    output_filename = "output.svg"
    num_lines = 3
    width = 600
    height = 200

    for opt, arg in opts:
        if opt == "-h":
            print(usage)
            sys.exit()
        elif opt in ("-i", "--input_str"):
            input_str = arg
        elif opt in ("-o", "--output_filename"):
            output_filename = arg
        elif opt in ("-n", "--num_lines"):
            num_lines = arg
        elif opt in ("-W", "--width"):
            width = arg
        elif opt in ("-H", "--height"):
            height = arg

    if not input_str:
        print(usage)
        sys.exit(1)

    SVGGenerator.run(input_str, num_lines, width, height, output_filename)

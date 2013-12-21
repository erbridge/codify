#!/usr/bin/env python

import math

import cairo

from bitarray import bitarray


class Painter:

    def _draw_rectangle(self, context, width, height):
        context.rel_line_to(width, 0)
        point = context.get_current_point()
        context.rel_line_to(0, height)
        context.rel_line_to(-width, 0)
        context.close_path()
        context.fill()
        context.move_to(point[0], point[1])


class NaivePainter(Painter):

    def draw_rectangle(self, bit, context, width, height):
        if bit:
            rgba = (0, 0, 0, 1)
        else:
            rgba = (1, 1, 1, 0)

        context.set_source_rgba(*rgba)
        self._draw_rectangle(context, width, height)


class SVGGenerator:

    @staticmethod
    def run(input_str, num_lines, width, height, output_filename, painter,
            export_filename):
        surface = cairo.SVGSurface(output_filename, width, height)
        context = cairo.Context(surface)

        line_height = int(height / num_lines)

        bit_array = bitarray()
        bit_array.fromstring(input_str)
        bit_str = bit_array.to01()

        line_char_width = math.ceil(len(bit_str) / num_lines)
        lines = [bit_str[i:i + line_char_width]
                 for i in range(0, len(bit_str), line_char_width)]

        box_width = int(width / line_char_width)

        current_y = 0
        for line in lines:
            context.move_to(0, current_y)
            for bit in line:
                painter.draw_rectangle(
                    int(bit), context, box_width, line_height)
            current_y += line_height

        if export_filename:
            surface.write_to_png(export_filename)


if __name__ == "__main__":
    import getopt
    import sys

    usage = "codify.py -i <input_str> [-o <output_filename> \n" + \
        "-n <num_lines> -W <width> -H <height> -p <painter> \n" + \
        "-e <export_filename]"

    try:
        opts, _ = getopt.getopt(
            sys.argv[1:],
            "hi:o:n:W:H:p:e:",
            ["input_str=", "output_filename=", "num_lines=", "width=",
             "height=", "painter=", "export="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(1)

    input_str = ""
    output_filename = "output.svg"
    num_lines = 1
    width = 600
    height = 200
    painter = NaivePainter()
    export_filename = ""

    for opt, arg in opts:
        if opt == "-h":
            print(usage)
            sys.exit()
        elif opt in ("-i", "--input_str"):
            input_str = arg
        elif opt in ("-o", "--output_filename"):
            output_filename = arg
        elif opt in ("-n", "--num_lines"):
            num_lines = int(arg)
        elif opt in ("-W", "--width"):
            width = int(arg)
        elif opt in ("-H", "--height"):
            height = int(arg)
        elif opt in ("-p", "--painter"):
            try:
                painter = globals()[arg]()
            except KeyError:
                print(usage)
                sys.exit(1)
        elif opt in ("-e", "--export"):
            export_filename = arg

    if not input_str:
        print(usage)
        sys.exit(1)

    SVGGenerator.run(input_str, num_lines, width, height, output_filename,
                     painter, export_filename)

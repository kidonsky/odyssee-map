#!/usr/bin/python

import argparse
import toml
import os
import sys
from graphviz import Digraph

# Graph is not pretty with durations < duration_offset
duration_offset = 15

line_expl = "\"Paris->20PA->Toulouse\""


def cf_color(place, colors_place, colorsheme):
    if place in colors_place.keys():
        return personnalized_color(colors_place[place], colorsheme)
    else:
        return personnalized_color(colors_place["default-color"], colorsheme)


def personnalized_color(value, colorscheme):
    if value in colorscheme.keys():
        return colorscheme[value]
    return value

def clean_line(line):
    for i, word in enumerate(line):
        line[i] = clean_name(word)
    return line


def clean_name(name):
    assert len(name) > 0, "Bad parameter"
    while name[0] == ' ':
        name = name[1:]
    while name[-1] == ' ':
        name = name[:-1]
    return name

def parse_parameters(args, defaults):

    # Output formats available with graphviz
    # Default is pdf, because is lighter and infinitely zoomable
    outformats_available = ("pdf", "png", "svg", "jpg", "dot")

    assert defaults["format"] in outformats_available, \
        bad_file("defaults", "Bad format. It must be one of : " + str(outformats_available), "of 'format'")
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--inputfile', required=True)
    parser.add_argument("-o", '--outputfile', default=defaults["outputfile"])
    parser.add_argument('-f', '--format', choices=outformats_available, default=defaults["format"])
    parser.add_argument('-cf', '--configurationfile', default=defaults["colorsfile"])
    parser.add_argument('-noview', '--noviewoutput', default=True, action="store_false")

    args = parser.parse_args(args)

    inputfile = args.inputfile
    outputformat = args.format
    outputfile = args.outputfile
    toml_file = args.configurationfile
    view = args.noviewoutput

    return (inputfile, outputformat, outputfile, toml_file, view)


def bad_file(file_type, msg_error, line_number):
    return "Problem in " + file_type + " file, line " + str(line_number) + " : " + msg_error


def extract_additional_infos(infos, line_number):
    # A non-duration text was inserted between places in input file
    if "PA" not in infos:
        # A note about path between two places in place of duration
        if '{' in infos:
            notes = infos.replace('{', ' {').replace('}', '} ')
        else:
            notes = ' {' + infos + '} '
        # true_duration will serve for the edge label
        true_duration = "0PA"
        # duration default
        duration = duration_offset
    else:
        notes = ''
        assert infos[:-2] == infos.replace('PA', ''), \
            bad_file("input", "Bad line format. Line should be like : " + line_expl, line_number)
        assert infos[:-2].isdigit(), bad_file("input", "Move cost must be a number", line_number)
        assert int(infos[:-2]) >= 0, bad_file("input", "Cost of move can not be negative", line_number)
        true_duration = infos
        # To keep a visible difference between durations,
        # we add here the offset and then we will make a division
        duration = int(infos[:-2]) + duration_offset

    return (notes, duration, true_duration)


def extract_info_fromline(line, line_number):
    line_splited = line.replace('\n', '').split("->")
    assert len(line_splited) == 2 or len(line_splited) == 3, bad_file("input", "It must have 1 or 2 '->'", line_number)
    # Check if there is a duration given on the line
    clean_line(line_splited)
    if len(line_splited) == 2:
        place_from, place_to = line_splited
        duration = duration_offset
        notes = ''
        true_duration = "0PA"
    else:
        place_from, infos, place_to = line_splited
        (notes, duration, true_duration) = extract_additional_infos(infos, line_number)

    return (place_from, place_to, duration, true_duration, notes)


def set_edge_color(duration, landings):
    # Set different colors in function of duration
    if duration < (duration_offset + landings[0]):
        difficulty = "black"
    elif duration < (duration_offset + landings[1]):
        difficulty = "grey"
    elif duration < (duration_offset + landings[2]):
        difficulty = "orange"
    elif duration < (duration_offset + landings[3]):
        difficulty = "red"
    else:
        duration = 30
        difficulty = "brown"

    return (duration, difficulty)


def create_graph_fromfile(input_file, graph, colors_place, colorsheme, defaults):
    placesfrom_list = ()

    assert len(defaults["duration_landings"]) == 4, \
        bad_file("defaults", "You must have 4 landings for duration.", "of 'duration_landings'")
    global duration_offset
    duration_offset = defaults["duration_offset"]

    for line_number, line in enumerate(input_file):
        # Escape comment lines from input file
        if line[0] == '#' or line[0] == ';' or len(line) < 2:
            continue

        (place_from, place_to, duration, true_duration, notes) = extract_info_fromline(line, line_number)

        (duration, difficulty) = set_edge_color(duration, defaults["duration_landings"])

        if place_from not in placesfrom_list:
            big_place = place_from.split(".")[0].split("_")[0].split(" ")[0]
            color = cf_color(big_place, colors_place, colorsheme)
            graph.node(place_from, shape="box", fillcolor=color, style='filled', color=color)

        graph.edge(
            place_from, place_to,
            label=(true_duration + notes),
            len=str(duration / 3),
            weigth=str(duration),
            color=difficulty
        )
    return graph


def main(cli_args):

    defaults_file = open("default_values.toml", "r")
    defaults_loaded = toml.loads(defaults_file.read())
    argparse_defaults = defaults_loaded["argparse_default_values"]
    edge_defaults = defaults_loaded["edge_default_values"]

    (inputfile, outputformat, outputfile, colors_filename, viewout) = parse_parameters(cli_args, argparse_defaults)

    print('Input file is :', inputfile)
    print('Output file is :', outputfile)

    colors_file = open(colors_filename, "r")
    colors_loaded = toml.loads(colors_file.read())
    colors_place = colors_loaded["places_color"]
    colorsheme = colors_loaded["color_sheme"]

    places_file = open(inputfile, "r")
    places_graph = Digraph(
        comment='My Odysse Map',
        engine='neato',
        format=outputformat
    )

    places_graph = create_graph_fromfile(places_file, places_graph, colors_place, colorsheme, edge_defaults)

    places_file.close()
    colors_file.close()

    places_graph.render(("output/" + outputfile), view=viewout)
    os.remove("output/" + outputfile)

    return 0


if __name__ == "__main__":
    main(sys.argv[1:])

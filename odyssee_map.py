#!/usr/bin/python

import argparse 
import toml
import os
import sys
from graphviz import Digraph

def personnalized_color(value, colorscheme):
    if value in colorscheme.keys():
        return colorscheme[value]

    return value

def parse_parameters(args):

    # Output formats available with graphviz
    # Default is pdf, because is lighter and infinitely zoomable
    outformats_available = ("pdf","png","svg","jpg", "dot")
    
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--inputfile', required = True)
    parser.add_argument("-o",'--outputfile', default = "odyssee-map")
    parser.add_argument('-f', '--format', choices = outformats_available, default = "pdf")
    parser.add_argument('-cf', '--configurationfile', default = "example/color_places.toml.example")
    parser.add_argument('-noview', '--noviewoutput', default=True, action="store_false")

    args = parser.parse_args(args)
    
    inputfile = args.inputfile
    outputformat = args.format
    outputfile = args.outputfile
    toml_file = args.configurationfile
    view = args.noviewoutput
 
    return (inputfile, outputformat, outputfile, toml_file, view)    

# Graph is not pretty with durations < duration_offset
duration_offset = 15

def extract_additional_infos(infos):
    # A non-duration text was inserted between places in input file
    if "PA" not in infos:
        # A note about path between two places in place of duration
        if '{' in infos :
            notes = infos.replace('{', ' {').replace('}', '} ')
        else :
            notes = ' {' + infos + '} '
        # true_duration will serve for the edge label
        true_duration = "0PA"
        # duration default
        duration = duration_offset
    else:
        notes = ''
        true_duration = infos
        # To keep a visible differences between durations, 
        # we add here the offset and then we will make a division
        duration = int(infos.replace("PA",''))+duration_offset

    return (notes, duration, true_duration)

def extract_info_fromline(line):
    line_splited = line.replace(' ', '').replace('\n', '').split("->")
    # Check if there is a duration given on the line ?
    if len(line_splited) == 2:
        place_from, place_to = line_splited
        duration = duration_offset
        notes = ''
        true_duration = "0PA"
    else:
        place_from, infos, place_to = line_splited
        (notes, duration, true_duration) = extract_additional_infos(infos)

    return (place_from, place_to, duration, true_duration, notes)

def set_edge_color(duration):
    # Set different colors in function of duration
    if duration < (duration_offset + 1) :
        difficulty = "black"
    elif duration < (duration_offset + 6) :
        difficulty = "grey"
    elif duration < (duration_offset + 11):
        difficulty = "orange"
    elif duration < (duration_offset + 21) :
        difficulty = "red"
    else :
        duration = 30
        difficulty = "brown"
    
    return (duration, difficulty)

def create_graph_fromfile(file, graph, colors_place, colorsheme):
    placesfrom_list = ()

    for line in file:
        # Escape comment lines from input file
        if line[0] == '#' or line[0] == ';' or len(line) < 2 :
            continue

        (place_from, place_to, duration, true_duration, notes) = extract_info_fromline(line)

        (duration, difficulty) = set_edge_color(duration)

        if place_from not in placesfrom_list:
            big_place = place_from.split(".")[0].split("_")[0] 
            if big_place in colors_place.keys():
                color = personnalized_color(colors_place[big_place], colorsheme)
            else:
                color = personnalized_color(colors_place["default-color"], colorsheme) 
            graph.node(place_from, shape="box", fillcolor=color, style='filled', color=color)
        
        graph.edge(place_from, place_to, 
                label = (true_duration + notes), 
                len = str(duration/3), 
                weigth = str(duration), 
                color = difficulty
                )
    return graph

def main(cli_args):
   
    (inputfile, outputformat, outputfile, toml_filename, viewout) = parse_parameters(cli_args) 
    
    print('Input file is :', inputfile)
    print('Output file is :', outputfile)

    toml_file = open(toml_filename,"r")
    toml_loaded = toml.loads(toml_file.read())
    colors_place = toml_loaded["places_color"]
    colorsheme = toml_loaded["color_sheme"]

    places_file = open(inputfile,"r")
    places_graph = Digraph(
            comment='My Odysse Map', 
            engine='neato', 
            format=outputformat
            )
    
    places_graph = create_graph_fromfile(places_file, places_graph, colors_place, colorsheme)
    
    places_file.close()
    toml_file.close() 
    
    places_graph.render(("output/"+outputfile), view=viewout) 
    os.remove("output/"+outputfile)

    return 0    

if __name__ == "__main__":
    main(sys.argv[1:])


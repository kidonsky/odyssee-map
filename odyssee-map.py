#!/usr/bin/python

import argparse 
from graphviz import Digraph

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-i', '--inputfile', required=True)
    parser.add_argument("-o",'--outputfile')
    parser.add_argument('-f', '--format')

    args = parser.parse_args()
    inputfile = args.inputfile
    
    # Check format given and store it
    if args.format not in ("pdf","png","svg","jpg", "dot"):
        if args.format is not None :
            print("Not good format.")
        print("Default format is pdf.")
        outputformat = "pdf"
    
    if args.outputfile is None :
        # Default output file
        outputfile = "output/odyssee-map"
    else:
        outputfile = args.outputfile

    print('Input file is :', inputfile)
    print('Output file is :', outputfile)
    
    file = open(inputfile,"r")
    placesfrom_list = ()
    places_graph = Digraph(
            comment='My Odysse Map', 
            engine='neato', 
            format=outputformat
            )
    
    for line in file:
        # Escape comment lines from input file
        if line[0] == '#' or line[0] == ';' or len(line) < 2 :
            continue

        line_splited = line.replace(' ', '').replace('\n', '').split("->")
        
        # Check if ther is a duration given on the line ?
        if len(line_splited) == 2:
            place_from, place_to = line_splited
            duration = '0PA'
        else:
            place_from, duration, place_to = line_splited

        # Graph is not pretty with durations < duration_offset
        duration_offset = 9

        # A non-duration text was inserted between places in input file
        if "PA" not in duration:
            # A note about path between two places in place of duration
            notes = duration
            # true_duration will serve for the edge label
            true_duration = "0PA"
            # duration default
            duration = str(duration_offset)
        else:
            notes = ''
            true_duration = duration
            # To keep a visible differences between durations, 
            # we add here the offset and then we will make a division
            duration = str(int(duration.replace("PA",''))+duration_offset)
            # Set different colors in function of duration
            if int(duration) < 10 :
                difficulty = "black"
            elif int(duration) < 15 :
                difficulty = "grey"
            elif int(duration) < 20 :
                difficulty = "orange"
            elif int(duration) < 30 :
                difficulty = "red"
            else :
                duration = "30"
                difficulty = "brown"

        if place_from not in placesfrom_list:
            places_graph.node(place_from, shape="box")
        
        places_graph.edge(place_from, place_to, 
                label = true_duration, 
                len = str(int(duration)/3), 
                weigth = duration, 
                color = difficulty
                )

    places_graph.render(("output/"+outputfile), view=True) 

if __name__ == "__main__":
    main()

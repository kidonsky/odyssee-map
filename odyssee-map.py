#!/usr/bin/python

import argparse 
from graphviz import Digraph

def main():
    inputfile = ''
    outputfile = ''

    parser = argparse.ArgumentParser()
    
    parser.add_argument('-i', '--inputfile', required=True)
    parser.add_argument("-o",'--outputfile')
    parser.add_argument('-f', '--format')

    args = parser.parse_args()
    inputfile = args.inputfile
    if args.format not in ("pdf","png","svg","jpg", "dot"):
        if args.format is not None :
            print("Not good format.")
        print("Default format is pdf.")
        outputformat = "pdf"
    if args.outputfile is None :
        outputfile = "output/odyssee-map"
    else:
        outputfile = args.outputfile

    print('Input file is :', inputfile)
    print('Output file is :', outputfile)
    
    file = open(inputfile,"r")
    places_dict = {}
    places_graph = Digraph(comment='My Odysse Map', engine='neato', format=outputformat)
    
    for line in file: 
        if line[0] == '#' or line[0] == ';' or len(line) < 2 :
            continue
        line_splited = line.replace(' ', '').replace('\n', '').split("->")
        if len(line_splited) == 2:
            place_from, place_to = line_splited
            duration = '0PA'
        else:
            place_from, duration, place_to = line_splited

        duration_offset = 9
        if "PA" not in duration:
            notes = duration
            true_duration = "0PA"
            duration = str(duration_offset)
        else:
            notes = ''
            true_duration = duration
            duration = str(int(duration.replace("PA",''))+duration_offset)
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

        if place_from in places_dict:
            places_dict[place_from][place_to] = duration
        else:
            places_dict[place_from] = {place_to: duration}
            places_graph.node(place_from, shape="box")
        
        places_graph.edge(place_from, place_to, label=true_duration, len=str(int(duration)/3), weigth=duration, color=difficulty)

    places_graph.render(("output/"+outputfile), view=True) 



if __name__ == "__main__":
    main()

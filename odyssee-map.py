#!/usr/bin/python

import sys, getopt
from graphviz import Digraph

def main():
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:o:f:",["help","ifile=","ofile=", "format="])
    except getopt.GetoptError as err:
        print('test.py -i <input file> -o <output file> -f <format>')
        sys.exit(2)
    if "i" not in opts and "--ifile" not in opts:
        print("You must give input file in parameter.")
        print('test.py -i <input file> [ <output file> -f <format>]')
        sys.exit(2)
    if "-o" not in opts and "--ofile" not in opts:
        outputfile = "odyssee_map"
    if "-f" not in opts and "--format" not in opts:
        outputformat = "pdf"

    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile> -f <format>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-f", "--format"):
            outputformat = arg

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

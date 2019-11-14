#!/usr/bin/python

import sys, getopt
from graphviz import Digraph

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    if outputfile == "":
       outputfile = "odysse_map.dot"

    print('Input file is :', inputfile)
    print('Output file is :', outputfile)
    
    file = open(inputfile,"r")
    places_dict = {}
    places_graph = Digraph(comment='My Odysse Map', engine='neato')
    
    for line in file: 
        if line[0] == '#' or line[0] == ';' or len(line) < 2 :
            continue
        line_splited = line.replace(' ', '').replace('\n', '').split("->")
        if len(line_splited) == 2:
            place_from, place_to = line_splited
            duration = '0PA'
        else:
            place_from, duration, place_to = line_splited

        if "PA" not in duration:
            notes = duration
            duration = "7"
        else:
            notes = ''
            duration = str(int(duration.replace("PA",''))+7)
            if int(duration) > 30:
                duration = "30"

        if place_from in places_dict:
            places_dict[place_from][place_to] = duration
        else:
            places_dict[place_from] = {place_to: duration}
            places_graph.node(place_from, shape="box")
        
        places_graph.edge(place_from, place_to, label=(duration+"PA"), len=duration, weigth=duration)


    places_graph.view()



if __name__ == "__main__":
    main(sys.argv[1:])

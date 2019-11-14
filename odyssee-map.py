#!/usr/bin/python

import sys, getopt

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
    for i, line in enumerate(file): 
        if line[0] == '#' or line[0] == ';' or len(line) < 2 :
            continue
        line_splited = line.replace(' ', '').replace('\n', '').split("->")
        if len(line_splited) == 2:
            place_from, place_to = line_splited
            duration = 0
        else:
            place_from, duration, place_to = line_splited
        print(line_splited)

        if i == 55:
            break
if __name__ == "__main__":
    main(sys.argv[1:])

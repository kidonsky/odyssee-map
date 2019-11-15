# Odyssee-map

Version 0.1

This is a project to generate a big intuitive map for the french online game [*Odyssée*](https://www.jdr-odyssee.net/odyssee/).
A simple input file is necessary. 
See `places_example.md` and [Input file](##Input-file 'Go to Input file section') to see the few requirements for the input file.

## Functionalities

### Present

- Draw quickly a map-like graph with colored edges from a simple text file
- All unvisited places are represented by an oval. All visited places are represented a box.

### Roadmap

- Color Nodes in function of big mother place with a personnal configuration file, 
by example all deserts places would be colored on yellow, even if the place name begin by *ds* and not *desert*.
- Enjoy and add functionnalities

## Usage

**/!\ Firstly to use this program, you will need a file with all places that you want to put in your map 
(see `places_example.md`).**

- Install `graphviz` package on your system. It is present on many Linux package manager. For Windows, see this [topic on StackOverflow](https://stackoverflow.com/questions/35064304/runtimeerror-make-sure-the-graphviz-executables-are-on-your-systems-path-aft)

- Then you must install requirements  (I recommend to use a Python virtual environment) :

  `pip install -r requirements.txt`

- Finally run the program :

  `python odyssee-map.py -i yourinputfile`

  For more details with options, run `python odyssee-map.py -h`

## Input file 

There are some exigences for the input file. See comments in  `places_example.md`.

### Paths 

- Paths must be represented by link between two places seperated by `->`.
- Action Points needed to walk this path can be inserted between the two places by adding a `->` symbol
By example :
`Paris->Toulouse` or `Paris->50PA->Toulouse`

### Places

All different representations of a place **must** be wrote exactly the same way. 
Indeed `Paris.road-north` is not the same place that `Paris.road_north` or `paris.road-north` etc, ...

### Comments

Comments can be add on the file by beginning a line by `#` or `;` symbols.

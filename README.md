# Odyssee-map

![GitHub r (latest by date)](https://img.shields.io/github/v/release/kidonsky/odyssee-map) 
![GitHub last commit](https://img.shields.io/github/last-commit/kidonsky/odyssee-map) 
![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/graphviz) 

![GitHub](https://img.shields.io/github/license/kidonsky/odyssee-map) 
![Open Source Love](https://github.com/kidonsky/open-source-badges/blob/master/badges/open-source-v3/open-source.svg)

![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/kidonsky/odyssee-map)

This is a project to generate a big intuitive map for the french online game [*Odyssée*](https://www.jdr-odyssee.net/odyssee/).
A simple input file is necessary. 
See `places_example.md` and [Input file](#Input-file 'Go to Input file section') to see the few requirements for the input file.

*French translation of this file can be found [here](#French-translation 'Go to French translation') at the end of English part.*

## Functionalities

### Present

- **Time efficiently** : draw quickly a map-like graph with colored edges from a simple text file
- **Quicly see un-visited places** : 
all unvisited places are represented by an oval and all visited places are represented a box
- **Estimate distances in a look** : edges are proportionnals to distance between places
- **Take notes on edges** : A river need to be crossed to go on an island ? Note it
in places file and see it quicly on map. (see [Input file](#Input-file 'Go to Input file section') for details)
- Color Nodes in function of big mother place with a personnal configuration file,
by example all deserts places would be colored on yellow, even if the place name begin by *ds* and not *desert*.
(see [Config file](#Config-file 'Go to Config file section') for details)

### Roadmap

- Add interface to get shorter road between two places
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

- Find your output file on the created `output/` folder

## Input file 

There are some exigences for the input file. See comments in `places_example.md`.

### Paths 

- Paths must be represented by link between two places seperated by `->`.
- Action Points needed to walk this path can be inserted between the two places by adding a `->` symbol
By example :
`Paris->Toulouse` or `Paris->50PA->Toulouse`

### Places

All different representations of a place **must** be wrote exactly the same way. 
Indeed `Paris.road-north` is not considerated the same place that `Paris.road_north` or `paris.road-north` etc, ...

### Notes

In your file, in place of cost of PA, you can add a note about the road between the 
two `->` symbols.
By example :
`Paris->Train->Toulouse`

### Comments

Comments can be add on the file by beginning a line by `#` or `;` symbols.

## Config file

The config file permits you to define colors for types of places. By example all forest related places 
could be drawn in green and all ocean related places in blue.

### Use your own config file

To use your own config file, create a new file named `new_name.toml` replacing *new_name* by what you want (you can
also only rename `color_places.toml.example` in `color_places.toml`) and give it in argument when you execute the 
program like that :
`python odyssee-map.py -i places-example.txt -cf new_name.toml`

### Associate colors to places

As in the example config file, you can associate them like that in the `places_color` section :
place_type = "color"

### Customize color

You can customize color by adding in `colorsheme` section a color with a new RGBA code.
Tip : So you can add transparency to your places.

---
# French translation

## Fonctionnalités

### Actuellement

- **Economisez du temps** : Le programme dessine rapidement une carte sous forme de graphe avec des liaisons colorées à partir d'un simple fichier texte très rapide à tenir à jour (environ une cinquantaine de lettres à taper par nouveau chemin)
- **Repérez rapidement les lieux non visités** : 
tous les lieux non visités (accessibles depuis un lieu visité) sont représentés par des ovales alors que tous les lieux visités sont rerésentés par des boîtes.
- **Estimez les distances en un coup d'oeil** : la taille des liaisons entre les lieux sont proportionnelles avec la distance entre les lieux.
- **Prenez des notes sur les chemins** : Une rivière doit être traversée pour 
atteindre un lieu ? Notez-le dans le fichier des lieux et retrouvez cette information
rapidement sur la carte. (voir [Fichier d'entrée](#Fichier-d'entrée "Aller à la section fichier d'entrée") pour des  détails)
- Colorer les lieux en fonction du grand lieu "mère" auquel il appartient, par exemple,
tous les lieux de désert seraient colorés en jaune même si son nom commence par *des* et non par *désert*.
(voir [Fichier de configuration](#Fichier-de-configuration "Aller à la section fichier de configuration") pour des détails)

### En projet

- Implémenter une interface pour calculer les plus court chemin entre deux lieux 
(le calcul c'est facile avec la librairie utilisée).
- Utiliser le programme et avec le temps, imaginer et implémenter de nouvelles fonctionnalités.

## Utilisation

**/!\ Tout d'abord, pour utiliser ce programme, vous aurez besoin d'un fichier texte d'entrée 
avec tous les lieux et chemins que vous voulez afficher dans la carte (généralement tous) 
(voir `places_example.md` qui vous ai donné).**

- Installer le paquet `graphviz` sur votre système. Il est présent sur plusieurs gestionnaire de paquets Linux (au moins Debian/Ubuntu et Fedora). Pour Windows, voir cette [question sur StackOverflow qui en parle](https://stackoverflow.com/questions/35064304/runtimeerror-make-sure-the-graphviz-executables-are-on-your-systems-path-aft)

- Puis installer les dépendances Python (je recommande de le faire dans un environnement virtuel de développement Python) :

  `pip install -r requirements.txt`

- Finallement lancer the programme depuis un terminal :

  `python odyssee-map.py -i votrefichierdentreee`

  Pour plus de détails avec les options, lancer `python odyssee-map.py -h`

- Trouver votre fichier de sortie dans le dossier crée `output/`

## Fichier d'entrée

Il y a certaines exigences par rapport au fichier d'entrée. Voir en plus les commentaires dans le fichier `places_example.md`

### Chemins

- Chemins doivent être représentés par des liaisons entre deux lieux séparés par `->`.
- Les Points d'Action (PA) nécessaires pour marcher entre deux lieux peut être inséré entre les deux lieux en ajoutant un symbole `->`
Par exemple :
`Paris->Toulouse` ou `Paris->50PA->Toulouse`

### Lieux

Toutes les occurences d'un certain lieu doivent absolument être écries de la même manière. 
En effet, `Paris.route-nord` n'est pas considérer comme le même lieu que `Paris.route_nord` ou `paris.route-nord` etc, ...

### Commentaires

Des commentaires peuvent être ajoutés dans le fichier en commençant une ligne par `#` ou `;`.

## Fichier de configuration

Le fichier de configuration vous permet de définir les couleurs de différents types de lieux. Par exemple, tous
les lieux de la forêt pevent colorier en vert et tout ceux de l'océan en bleu.

### Utiliser votre propre fichier de configuration

Pour utiliser votre propre fichier de configuration, créer un nouveau fichier de configuration `nouveau_nom.toml` 
(en remplaçant *nouveau_nom* par ce que vous voulez) (ou vous pouvez juste renommez color_places.toml.example) 
et passez le argument de l'appel du programme comme ceci :
`python odyssee-map.py -i places-example.txt -cf nouveau_nom.toml`

### Associer les couleurs aux lieux

Comme dans le fichier de configuration exemple, vous pour les associer dans la section `places_color` comme ceci :
place_type = "color"

### Personnaliser les couleurs

Vous pouvez personnaliser des couleurs en les ajoutant dans la partie `colorsheme` avec un nouveau code RGBA.
Conseil : Vous pouvez ainsi utiliser de la transparence pour vos lieux.

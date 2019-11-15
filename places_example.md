# Carte des lieux connus de Odyssée

;Carte des lieux connus de Odyssée:

foret->boisdore
foret->5PA->Brumevent

boisdore->1PA->Arbre
# Le trajet boisdore vers foret coute plus cher que l'inverse. 
# On sait que c'est dur de partir d'un village hobbit
boisdore->1PA->foret 

Brumevent->50PA->Fournaise
Brumevent->20PA->Baie

Baie->{Bateau}->Ocean
Baie->Fournaise

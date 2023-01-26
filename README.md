# Rush Hour

Hier staat een korte beschrijving van het probleem evt. met plaatje.

## TODO

- In main.py run_algorithms and display_results to Rushhour class if better
- Experiments
- Make sure README and requirements correct

## Aan de slag (Getting Started)

### Vereisten (Prerequisites)

Deze codebase is volledig geschreven in [Python3.9.13](https://www.python.org/downloads/). In requirements.txt staan alle benodigde packages om de code succesvol te draaien. Deze zijn gemakkelijk te installeren via pip dmv. de volgende instructie:

```
pip install -r requirements.txt
```

### Structuur (Structure)

* Alle Python scripts, op main.py na, staan in de folder rushhourcode.
	- De gebruikte algoritmes staan in de folder algorithms.
	- De classes voor auto, bord en rushhour staan in de folder classes.
	- De visualitie staat in de folder visualization. 

* Alle startborden staan in csv formaat in de map gameboards.
* Het python script om het programma te runnen, main.py, staat in de root directory.

### Test (Testing)

Om de code te runnen gebruik de instructie:

```
python main.py [filename (0-7)] [algorithm number (random=0, bfs=1)]
```

Dus wil je file 4 runnen met breadth first search gebruik de instructie:

```
python main.py 4 1
```

### Visualisatie 

De visualisatie is gedaan met behulp van de pygame module. Om de visualisatie te runnen 
moet het volgende worden gedaan. Eerst wordt het programma gerund, zoals hierboven
staat vermeld. Hierin worden twee output files gecreëerd: path output en board output. De 
laatste output file wordt gebruikt door visualize.py (in de visualization folder) te runnen.

![Voorbeeld visualisatie](visualization_demo.png)

## Auteurs (Authors)

* Anoeya Sivanathan
* Bauke Nieuwenhuis
* Wouter Bant

## Dankwoord (Acknowledgments)

* Minor Programmeren van de UvA
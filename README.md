
# Rush Hour

In dit project zijn verschillende algoritme en heurisitieken geïmplementeerd om rushhour puzzles op te lossen.

Met behulp van visualisaties, resultaten van de algoritmen en random borden is geprobeerd te achterhalen welke algoritmen en heuristieken goed werken en wat een rushhour puzzel moeilijk maakt.

![Solve Rush Hour](media/SolveRushHour.gif)

## TODO

- In main.py run_algorithms and display_results to Rushhour class if better

- Experiments

- Make sure README and requirements correct

## Aan de slag

### Vereisten

Deze codebase is volledig geschreven in [Python3.9.13](https://www.python.org/downloads/). In requirements.txt staan alle benodigde packages om de code succesvol te draaien. Deze zijn gemakkelijk te installeren via pip dmv. de volgende instructie:

```

pip install -r requirements.txt

```
  
### Structuur
  
* Alle Python scripts, op main.py na, staan in de folder [rushhourcode](rushhourcode).

* De gebruikte algoritmes staan in de folder [algorithms](rushhourcode/algorithms).

* De classes voor [auto](rushhourcode/classes/car.py), [bord](rushhourcode/classes/board.py) en [rushhour](rushhourcode/classes/rushhour.py) staan in de folder [classes](rushhourcode/classes).

* De visualitie staat in de folder [visualization](rushhourcode/visualization).

* De random bord generator staat in de folder [board_generator](rushhourcode/board_generator).

* Alle startborden staan in csv formaat in de folder [gameboards](gameboards).

* De output van de laatste run wordt opgeslagen in de folder [output](output) en de beste ouputs in de subdirectory [best_outputs](output/best_outputs)

* Het python script om het programma te runnen, [main.py](main.py) en de file die het mogelijk maakt om de laatste oplossing te visualiseren, [visualize.py](visualize.py) staan in de root directory.

### Test

Om de code te runnen op 1 van de 7 gegeven borden gebruik de instructie:

```

python main.py algorithm_number board_number [-v] [-d]

```

De volgende opties zijn er voor algoritmen, een uitleg kan [hier](rushhourcode/algorithms/README.md) gevonden worden:
| 0 	| 1 	| 2 	| 3 	| 4 	| 5 	| 6 	| 7 	|
|:---:	|:---:	|:---:	|:---:	|:---:	|:---:	|:---:	|:---:	|
| Random 	| Shortened Path Random 	| Iterative Deepening 	| Breadth First Search 	| Beam Search 	| AStar 1 	| AStar 2 	| Moves Freed Heuristic 	|

Met de optie -v zul je een visualisatie van de oplossing zien wanneer die gevonden is en met de optie -d kun je tussendoor zien wat de diepte is die het algoritme nu doorzoekt.

  Om de code te runnen op een random gegenereerd bord gebruik de instructie:
```

python main.py algorithm_number -r [-v] [-d]

```

Dus wil je Breadth First Search runnen op bord 2 en na het runnen een visualisatie zien van de oplossing:

```

python main.py 1 2 -v

```

Heb je niet de optie -v gegeven maar wil je wel graag een visualisatie zien, run de instructie:

```

python visualize.py

```

## Auteurs


* Anoeya Sivanathan

* Bauke Nieuwenhuis

* Wouter Bant


## Dankwoord

* Minor Programmeren van de UvA
# Resultaten

[results.csv](results.csv): bevatd de resultaten van **Breadth First Search**, **Beam Search** en **AStar** met de verschillende heurisitieken op de borden 1 tot en met 6. Voor **Beam Search** staat aangegeven wat de waarde van ***k***, het aantal volgende staten dat bekeken gaat worden van het huidige bord, is. Het geheugen en tijd dat genoteerd is zal verschillen per run iets verschillen. Dit komt bij **Breadth First Search** doordat de volgende borden in een willeurige volgorde bekeken wordt. Bij de andere genoemde algoritme komt dit doordat verschillende borden dezelfde score kunnen krijgen van de heuristiek. Dit laatste zorgt er bij **Beam Search** en **AStar3** (of **Freed Moves Heuristic**) voor dat het aantal stappen ook verschilt per run. Om deze reden zijn deze 2 algoritme 3 keer gerunt op alle borden en de resultaten van de waarneming in het midden (gebaseerd op het aantal stappen) is genoteerd. Over het algemeen zijn de resultaten vergelijkbaar met 1 uitzondering: **Beam Search** op bord 6. Daar werd 2 keer een oplossing binnen 5 minuten gevonden, maar 1 keer kwam er helemaal geen oplossing. Dit komt waarschijnlijk dat er meerdere borden dezelfde score krijgen en maar een aantal van deze naar een oplossing leiden. ***k*** is zo gekozen dat deze wel een oplossing geeft maar 1 lager niet. Verder valt op dat we **Iterative Deepening** niet hebben meegenomen, dit komt doordat dit algoritme erg traag is. We hebben er voor gekozen hem toch te laten staan in het project want het is het enige algoritme dat zonder dat het geheugen vol gaat zitten de beste oplossing kan vinden.

[/random_vs_compressed](random_vs_compressed): bevat resultaten die het effect van path compression op een gevonden random oplossen aangeven. [/distribution_random](distribution_random) bevat de verdelingen van deze random runs zonder path compression.

[/best_results](best_results): bevat de beste oplossing voor elk bord. [/moves](best_results/moves): bevat de zetten die naar de korst gevonden oplossing leiden en [/visualizations](best_results/visualizations): bevat visualisaties hiervan. Bord 1 tot en met 6 zijn gevonden in het minimum aantal stappen. De korste oplossing van bord 7 is gevonden door shortened path random met 5 batches van grootte 100. De visualisatie voor bord 7 kan gemaakt worden door [boards_output7.csv](best_results/visualizations/boards_output7.csv) in de [ouput](output) folder te stoppen, te hernoemen naar boars_output.csv en python visualize.py te gebruiken.

De resulaten zijn allemaal gevonden op dezelfde laptop met de volgende specificaties: 

* Processor: 11th Gen Intel(R) Core(TM) i7-1165G7 @ 2.80GHz

* Installed RAM: 32.0 GB (31.8 GB usable)

* System type: 64-bit operating system, x64-based processor

* OS: Windows 11 Pro

Tijdens de runs was altijd alleen VSCode, een terminal en taakbeheer geopend. Er werden ook geen updates of dergelijke uitgevoerd.

[reproduce.py](reproduce.py): bevat code en uitleg om de csv bestanden en plots te reproduceren.
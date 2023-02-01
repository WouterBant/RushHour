# Visualisatie

## Werking

Als met behulp van een algoritme een oplossing gevonden is, worden de borden in deze oplossing opgeslagen in de [output](../../output/) folder als [boards_output](../../output/boards_output.csv). Dit bestand wordt gebruikt voor de visualisatie. Welk plaatje wordt toegekent aan een auto gebeurt random, op de rode auto na want die wordt rood. Dit wordt dan in een dictionary opgeslagen zodat in de volgende stappen dezelfde auto's dezelfde plaatjes krijgen. De visualisatie is te zien als bij het aanroepen van de instructie om een algoritme te runnen de optie -v meegegeven wordt. Of na het runnen the visualize.py wordt aangeroepen.

Bijvoorbeeld:

```

python main.py 1 2 -v

```

Of:

```

python main.py 1 2

```

Gevolgd door:

```

python visualize.py

```
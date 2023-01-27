
# Algoritmen and Heuristieken

  

## Kort Overzicht

Om de rushhour puzzles op te lossen zijn de volgende algoritmen gebruikt:

- **Random**
- **Shortened Path Random** ***(aantal batches, batch grootte)***
- **Iterative Deepening**
- **Breadth First Search**
- **Beam Search** ***(k)***
- **AStar**

En de volgende heuristieken zijn gebruikt voor **Beam Search** en **AStar** en kunnen worden gevonden in [Board Class](../classes/board.py):
- Met een heurisitiek dat het aantal blokkerende auto's telt, admissible.
- Met de vorige heurisitiek + een lowerbound voor het aantal zetten dat nodig is om deze blokkerende auto's te verplaatsen, admissible. De lowerbound is als volgt bepaald: er worden 3 plekken naar beneden en boven gescanned op blokkers. Dan als de auto al uit de weg kan wordt er niks geteld. Als het bord grootte 6 heeft en de blokkerende auto lengte 3, moet deze naar beneden dus tellen we alle blokkerende auto's beneden die we nog niet eerder gezien hebben hierbij op. De auto's die boven blokkeren en nog niet eerder gezien waren, markeren we weer als ongezien. Als het bord groter is dan 6 en de lengte van de auto is 3, wordt er min(blokkerend boven ongezien, blokkerend onder ongezien) opgeteld alle auto's worden wel als gezien gemarkeerd omdat niet zeker kan zijn in welke richting echt bewogen zal worden. Verder als de auto lengte 2 en deze kan niet al vrij bewegen wordt er niks bij opgeteld. De reden hiervoor is omdat er dan met posities van de blokkers gewerkt moet worden en dit maakt de code nog moeilijker te begrijpen. Ook zorgde dit algorime niet voor veel snellere oplossingen.
- Een niet admissible heuristiek dat ook gebruikt maakt van het aantal gecreëerde zetten ten opzichte van het vorige bord. Dit kan eigenlijk niet **AStar** genoemd worden omdat het niet gegarandeerd de korste oplossing geeft, maar omdat het alleen een andere cost functie heeft wordt hij toch in de **AStar** geïmplementeerd. Deze heuristiek maakt ook gebruik van de afstand tot de uitgang zodat als het pad naar de uitgang vrij is deze sneller genomen wordt.

  

## Toelichting Algoritmen

### Random

Bij het **Random** algoritme wordt gekeken naar alle zetten die mogelijk zijn in de huidige configuratie van het bord en wordt er random 1 uitgevoerd. Dit wordt gedaan totdat een oplossing is gevonden. Dit levert vaak snel een oplossing op, maar deze is vaak erg lang.

### Shortened Path Random

Om toch de snelheid van **Random** te benutten en de informatie die de verschillende oplossing geven is er ook een algoritme geïmplementeerd dat meerdere malen het random algoritme runt en dan **path compression** toepast op de gevonden oplossingen. **Path compression** wordt gedaan door middel van breadt first search op een adjacacency list die all parent borden naar zijn children mapt. Dit algoritme is geïmplementeerd zodat de gebruiker het ***aantal batches*** en de ***batch grootte*** kan aangeven. Hoe meer runs er worden gedaan, des te groter de kans dat er een kortere oplossing gevonden wordt. Het aantal stappen dat uiteindelijk gereturned wordt is nooit meer dan het minimaal aantal stappen gevonden. Batches zijn gebruikt omdat als je veel runs wilt doen het geheugen snel vol gaat zitten, dus op de hele grote adjacency list wordt al vroegtijdig **path compression** toegepast en alleen dit path wordt onthouden voor de volgende batches. Uiteindelijk wordt op deze gecompressede paths nog eenmaal path compression toegepast en die oplossing wordt gereturned. Deze aanpak zorgt ervoor dat auto's nooit heen en weer bewogen worden. Ook zorgt het ervoord dat als een bepaalde configuratie in slechts een aantal stappen in 1 oplossing gevonden wordt en in een andere oplossing dicht bij het opgeloste bord, dat er direct van het bord voor deze configuratie in de eerste situatie naar het bord in de laatste situatie gegaan kan worden. Dit zal leiden tot een afname van het aantal benodigde stappen.

### Iterative Deepening
**Iterative Deepening** is geïmplementeerd met behulp van **Depth First Search**. De maximale diepte begin op 1 en wordt verhoogd zolang er na het afzoeken van deze maximale diepte geen oplossing gevonden is. Deze methode garandeerd de oplossing te vinden in het minimaal aantal stappen. Omdat deze methode vaak dezelfde paden bekijkt, alleen dan iets verder elke iteratie, is het erg traag. Om geheugen te besparen is hier gekozen om geen visit set te gebruiken. Het is afgeraden dit algoritme op grote borden te runnen, om te zien of het werkt kan er op bord 0 gerunt worden.

### Breadth First Search
Net zoals **Iterative Deepening** zal **Breadth First Search** gegarandeerd de korste oplossing vinden. Voor een gegeven configuratie van een bord zal het kijken naar alle mogelijke zetten en deze uitvoeren als het resulterende bord niet eerder gezien is. Dit wordt voor een gehele diepte gedaan voordat naar de volgende gegaan wordt. Wanneer dit algoritme gerunt wordt totdat de queue leeg is kan de werkelijke statespace bepaald worden. Dit algoritme is een stuk sneller dan **Iterative Deepening**, maar gebruikt ook vlink meer geheugen, waardoor dit algoritme op een computer met een werkgeheugen van 32GB niet een oplossing kan vinden voordat het geheugen vol zit.

### Beam Search
**Beam Search** maakt gebruikt de eerde genoemde heurisitieken en zal alleen kijken naar de ***k*** meest belovende zetten. ***k*** is een parameter die door de gebruiker gegeven kan worden. In het algemeen zal een lage ***k*** sneller een oplossing vinden, maar als ***k*** te laag is zal helemaal geen oplossing gevonden worden. Dit algoritme is vaak sneller en meer geheugen efficiënt dan **Breadth First Search**.

### AStar
**AStar** maakt gebuiken van heurisitieken om te bepalen wanneer te kijken naar welk bord. De eerste twee heuristieken geven aan hoeveel stappen er minimaal nodig zijn om tot een oplossing te komen, deze zijn admissible. Deze informatie kan gebuikt worden om eerst te kijken naar borden waar de som van het minimaal aantal nog nodige stappen + aantal al gezette stappen het laagst is. Dit is precies wat **AStar** doet met behulp van een priority queue.  
 - **AStar 1** maakt gebruik van het eerste heuristiek
 - **AStar 2** maakt gebruik van het tweede heuristiek
 - **Moves Freed Heuristic** is het derde heuristiek in combinatie met de tweede toegepast op het algoritme wat ook door **AStar** gebruikt wordt. Alleen kan het niet **AStar** genoemd worden, omdat niet gegarandeerd is dat het minimaal aantal stappen gevonden wordt. Om deze reden is gekozen om het gewoon **Moves Freed Heuristic** te noemen.
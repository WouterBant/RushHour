# Random bord generator

## Werking

Gebaseerd op de waarde die de gebuiker opgeeft voor de grootte van het bord, wordt er een bord gegenereerd met een aantal geplaatste auto's en random shuffles. Om het bord moeilijker te maken wordt met de de heuristiek die het aantal blokkerende auto's met daarbij een lowerbound om deze weg te halen in combinatie met een hill climber het bord moeilijk gemaakt. Om ervoor te zorgen dat het bord oplosbaar is wordt bij het plaatsen van de auto's ervoor gezorgd dat de rode auto een vrij pad heeft naar de uitgang. Na de shuffle en de hill climber is het waarschijnlijk dat je een moeilijkere puzzel hebt gekregen en deze is dus oplosbaar, omdat je altijd met geldige zetten terugkan naar de beginconfiguratie van het bord. Het random bord kan gegenereerd en opgelost worden als in plaats van een bord nummer de -r flag gegeven wordt.

Voorbeeld om een random gegenereerd bord met **AStar 2** op te lossen:

```

python main.py 6 -r

```
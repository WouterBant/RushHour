# Random bord generator

## Werking

Gebaseerd op waarden die de gebuiker opgeeft voor de grootte van het bord, het aantal auto's dat geprobeerd moet worden op het bord te plaatsen en het aantal random shuffles wordt een bord gegenereerd. Om het bord moeilijker te maken wordt met behulp van de de heuristiek die het aantal blokkerende auto's met daarbij een lowerbound om deze weg te halen gebruikt in combinatie met een hill climber. Om ervoor te zorgen dat het bord oplosbaar is wordt bij het plaatsen van de auto's ervoor gezorgd dat de rode auto een vrij pad heeft naar de uitgang. Na de shuffle en de hill climber is het waarschijnlijk dat je een moeilijker puzzel hebt gekregen en deze is dus oplosbaar.
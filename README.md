TD5 CARIOU CHOUCHANE

Il existe 4 micro-services:
- Evitement d'obstacles
- Line Following Left
- Line Following Right
- Voting

Pour lancer tous les micro-services: docker-compose up --build -d

Evitement d'obstacles récupérer les données des deux capteurs à l'avant du robot et retourne "stop","turnright","turnleft","forward".

Line Following Left et Right retourne des vitesses moteurs, une vitesse moteur gauche du robot et une vitesse moteur droit du robot (exemple: "60 60").

Voting récupére les valeurs des trois micro-services à partir de MQTT(de nouveaux topics ont été créés). Si l'évitement d'obstacles lui indique stop, le rabot s'arrête.
S'il lui indique forward alors, on combine les valeurs reçues de Line Following Left et Right. On fait la moyenne pour le moteur gauche, moyenne pour le moteur droit. Ces valeurs sont ensuite envoyées par MQTT au robot pour contrôler les moteurs.

Le robot ne tente pas de contourner l'obstacle s'il en trouve un. Il s'arrête.

N'ayant plus de batterie pour les tests vidéos, nous avons dû utiliser l'alimentation filaire.
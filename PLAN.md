# TODO

# Tests unitaires - 60 tests :

**Cas 1** : Trois points → un seul triangle
**Pourquoi ?** Vérifier que la triangulation de trois points génère exactement un triangle valide.
**Comment ?** Appeler la fonction avec trois points distincts et vérifier qu'elle retourne un seul triangle composé exactement de ces trois points.

**Cas 2** : Plusieurs points → plusieurs triangles
**Pourquoi ?** Pour vérifier que l'algorithme crée bien plusieurs triangles quand on lui donne plus de trois points.
**Comment ?** Appeler la fonction avec par exemple 5 points bien répartis, puis vérifier que le résultat contient plusieurs triangles.

**Cas 3**: Un carré → deux triangles
**Pourquoi ?** S'assurer que quatre points formant un carré sont triangulés en deux triangles.
**Comment ?** Appeler la fonction avec quatre points formant un carré et vérifier qu'il y a exactement deux triangles, que les triangles sont différents, que chaque triangle utilise exclusivement des points du carré.

**Cas 4** : Moins de trois points → erreur (3 variantes paramétrées)
**Pourquoi ?** Une triangulation est impossible avec moins de trois points.
**Comment ?** Appeler la fonction avec 0, 1 ou 2 points et vérifier qu'une exception est levée.

**Cas 5** : Trois points colinéaires → lève une exception
**Pourquoi ?** Trois points alignés ne forment aucun triangle valide.
**Comment ?** Tester avec (0,0), (0,1), (0,2) et vérifier qu'on lève une exception.

**Cas 6** : Points dupliqués → lève une exception
**Pourquoi ?** Les points dupliqués ne doivent pas être acceptés car ils peuvent provoquer des incohérences ou des erreurs dans l'algorithme.
**Comment ?** Appeler la fonction avec une liste contenant au moins un doublon, par exemple: (0,0), (1,1), (2,0), (1,1) et vérifier que l'algorithme lève l'exception prévue.

**Cas 7** : Polygone concave → triangulation correcte
**Pourquoi ?** Vérifier que l'algorithme gère les polygones non convexes.
**Comment ?** Créer un polygone concave (ex: forme en L) et vérifier que tous les triangles retournés utilisent uniquement les points du polygone.

**Cas 8** : Points avec coordonnées négatives
**Pourquoi ?** S'assurer que l'algorithme fonctionne avec toutes les coordonnées, pas seulement positives.
**Comment ?** Tester avec des points ayant des coordonnées négatives et vérifier le résultat.

**Cas 9** : Points très proches (précision numérique)
**Pourquoi ?** Tester la robustesse face aux erreurs d'arrondi.
**Comment ?** Créer des points avec des coordonnées très proches (différence < 0.001) et vérifier le comportement.

**Cas 10** : Grand nombre de points
**Pourquoi ?** Vérifier que l'algorithme fonctionne avec des ensembles de points plus grands.
**Comment ?** Trianguler 50 points en cercle et vérifier que le nombre de triangles est cohérent.

**Cas 11** : Triangle rectangle
**Pourquoi ?** Vérifier le bon fonctionnement avec une forme géométrique simple.
**Comment ?** Trianguler un triangle rectangle et vérifier le résultat.

**Cas 12** : Pentagone régulier
**Pourquoi ?** Tester avec un polygone régulier à 5 côtés.
**Comment ?** Créer 5 points en cercle et vérifier qu'on obtient 3 triangles.

**Cas 13** : Points alignés horizontalement → erreur
**Pourquoi ?** Les points sur une ligne horizontale ne peuvent pas être triangulés.
**Comment ?** Tester avec des points de même ordonnée et vérifier l'exception.

**Cas 14** : Points alignés sur diagonale → erreur
**Pourquoi ?** Les points colinéaires sur une diagonale doivent être rejetés.
**Comment ?** Tester avec (0,0), (1,1), (2,2), (3,3) et vérifier l'exception.

**Cas 15** : Coordonnées à zéro
**Pourquoi ?** Vérifier que l'origine (0,0) est gérée correctement.
**Comment ?** Trianguler avec des points incluant (0,0).

**Cas 16** : Triangle très plat mais valide
**Pourquoi ?** Tester la robustesse avec des triangles de faible hauteur.
**Comment ?** Créer un triangle avec une hauteur très petite et vérifier qu'il est accepté.

**Cas 17** : Forme en étoile (polygone non convexe)
**Pourquoi ?** Vérifier le traitement des formes complexes non convexes.
**Comment ?** Créer une étoile à 5 branches (10 points) et vérifier la triangulation.

**Cas 18** : Rectangle
**Pourquoi ?** Tester avec un quadrilatère simple.
**Comment ?** Trianguler un rectangle et vérifier qu'on obtient 2 triangles.

**Cas 19** : Triangles avec aire positive
**Pourquoi ?** Vérifier qu'aucun triangle dégénéré n'est créé.
**Comment ?** Calculer l'aire de chaque triangle et vérifier qu'elle est > 0.

**Cas 20** : Somme des aires = aire du polygone
**Pourquoi ?** Vérifier la conservation de la surface totale.
**Comment ?** Calculer la somme des aires des triangles et comparer avec l'aire du polygone initial.

**Cas 21** : Pas de triangles qui se chevauchent
**Pourquoi ?** Vérifier que les triangles ne se superposent pas incorrectement.
**Comment ?** Tester que les centres des triangles ne sont pas dans d'autres triangles.

**Cas 22** : Nombre de triangles selon formule d'Euler
**Pourquoi ?** Vérifier que n points donnent n-2 triangles pour un polygone simple.
**Comment ?** Tester avec 3, 4, 5 et 6 points et vérifier la formule.

**Cas 23** : Triangulation déterministe
**Pourquoi ?** Vérifier que la même entrée donne toujours le même résultat.
**Comment ?** Exécuter 5 fois la triangulation sur les mêmes points et comparer.

**Cas 24** : Points sur grille entière
**Pourquoi ?** Tester avec des coordonnées entières.
**Comment ?** Créer des points sur une grille et vérifier la triangulation.

**Cas 25** : Polygone avec trou visuel (forme en U)
**Pourquoi ?** Tester une forme concave complexe.
**Comment ?** Créer 8 points en forme de U et vérifier qu'on obtient 6 triangles.

**Cas 26** : Triangle isocèle
**Pourquoi ?** Vérifier les propriétés géométriques spécifiques.
**Comment ?** Trianguler un triangle isocèle et vérifier que deux côtés sont égaux.

**Cas 27** : Points presque colinéaires
**Pourquoi ?** Tester la limite entre points colinéaires et non-colinéaires.
**Comment ?** Créer des points avec une très petite déviation de la colinéarité.

**Cas 28** : Ordre des points différent
**Pourquoi ?** Vérifier que l'ordre d'entrée n'affecte pas le nombre de triangles.
**Comment ?** Mélanger aléatoirement les points et vérifier qu'on obtient le même nombre de triangles.

**Cas 29** : Décodage d'un flux binaire valide
**Pourquoi ?** Vérifier que le flux binaire reçu est bien traduit en liste de points correcte.
**Comment ?** Utiliser un petit flux binaire connu et le comparer avec les points attendus.

**Cas 30** : Encodage d'une liste de points
**Pourquoi ?** S'assurer que l'encodage en binaire est conforme au format prévu.
**Comment ?** Fournir une liste de points simples et vérifier que le flux peut être relu sans erreur.

**Cas 31** : Flux binaires invalides (3 variantes paramétrées)
**Pourquoi ?** Vérifier que la fonction gère correctement les flux corrompus ou incomplets.
**Comment ?** Fournir un flux invalide (vide, incomplet, tronqué) et vérifier qu'une exception est levée.

**Cas 32** : Encodage → Décodage (cohérence)
**Pourquoi ?** Vérifier que les deux fonctions sont cohérentes entre elles.
**Comment ?** Encoder puis décoder la même liste de points et vérifier qu'on obtient le même résultat.

**Cas 33** : Encodage de points avec coordonnées négatives
**Pourquoi ?** S'assurer que l'encodage fonctionne avec toutes les coordonnées.
**Comment ?** Encoder et décoder des points avec coordonnées négatives, vérifier la cohérence avec tolérance float32.

**Cas 34** : Encodage de triangles
**Pourquoi ?** Valider le format binaire complet des triangles (vertices + indices).
**Comment ?** Encoder des triangles et vérifier la structure du flux (taille, contenu, nombre de vertices et triangles).

**Cas 35** : Grand PointSet (encodage/décodage)
**Pourquoi ?** Tester la robustesse avec beaucoup de données.
**Comment ?** Encoder/décoder 1000 points et vérifier la cohérence.

**Cas 36** : PointSet vide
**Pourquoi ?** Vérifier le traitement du cas limite sans points.
**Comment ?** Encoder/décoder une liste vide et vérifier que le flux fait 4 bytes.

**Cas 37** : Très grands nombres
**Pourquoi ?** Tester les limites de float32.
**Comment ?** Encoder/décoder des nombres de l'ordre de 1e10 et vérifier avec tolérance.

**Cas 38** : Un seul point
**Pourquoi ?** Tester le cas minimum avec un point.
**Comment ?** Encoder/décoder un seul point et vérifier l'exactitude.

**Cas 39** : Points avec coordonnées identiques
**Pourquoi ?** Vérifier que plusieurs points aux mêmes coordonnées sont gérés.
**Comment ?** Encoder/décoder des points dupliqués.

**Cas 40** : Flux avec padding supplémentaire
**Pourquoi ?** Tester que le décodeur ignore les bytes en trop à la fin.
**Comment ?** Ajouter du padding après un flux valide et vérifier le décodage.

**Cas 41** : Encoder triangles multiples avec vertices partagés
**Pourquoi ?** Vérifier l'optimisation des vertices uniques.
**Comment ?** Encoder 3 triangles partageant des sommets et vérifier le nombre de vertices uniques.

**Cas 42** : Coordonnées extrêmes de float32
**Pourquoi ?** Tester les valeurs limites de float32.
**Comment ?** Utiliser des valeurs proches de 3.4e38 et vérifier avec tolérance.

**Cas 43** : Décodage nombre de points = 0
**Pourquoi ?** Vérifier le cas où le flux indique explicitement 0 points.
**Comment ?** Décoder un flux avec count=0 et vérifier qu'on obtient une liste vide.

**Cas 44** : Multiples cycles encodage/décodage
**Pourquoi ?** Vérifier la stabilité sur plusieurs itérations.
**Comment ?** Encoder/décoder 3 fois de suite et vérifier que les points restent identiques.

**Cas 45** : Décodage flux tronqué
**Pourquoi ?** Tester la détection de flux incomplets.
**Comment ?** Couper un flux au milieu et vérifier qu'une exception est levée.

**Cas 46** : Décodage nombre de points négatif
**Pourquoi ?** Vérifier le rejet de données invalides.
**Comment ?** Créer un flux avec un nombre négatif signé et vérifier l'exception.

**Cas 47** : Décodage nombre de points énorme
**Pourquoi ?** Tester la détection de valeurs irréalistes.
**Comment ?** Créer un flux indiquant 4 milliards de points sans données et vérifier l'exception.

**Cas 48** : Ordre des bytes big-endian
**Pourquoi ?** Vérifier que le format est bien big-endian.
**Comment ?** Vérifier que les 4 premiers bytes sont bien en big-endian.

**Cas 49** : Encoder triangles - un seul
**Pourquoi ?** Tester le cas minimal d'encodage de triangles.
**Comment ?** Encoder 1 triangle et vérifier la structure (3 vertices, 1 triangle).

**Cas 50** : Encoder triangles sans vertices partagés
**Pourquoi ?** Vérifier le cas où aucun sommet n'est partagé.
**Comment ?** Encoder 2 triangles complètement distincts et vérifier 6 vertices.

**Cas 51** : PointSet avec tailles puissance de 2
**Pourquoi ?** Tester des tailles spécifiques (alignement mémoire).
**Comment ?** Tester avec 2, 4, 8, 16, 32, 64, 128, 256 points.

**Cas 52** : Coordonnées infinies
**Pourquoi ?** Vérifier que float32 peut représenter l'infini.
**Comment ?** Encoder/décoder math.inf et vérifier le résultat.

**Cas 53** : Coordonnées NaN
**Pourquoi ?** Tester le traitement de Not-a-Number.
**Comment ?** Encoder/décoder math.nan et vérifier avec math.isnan().

**Cas 54** : Formule taille flux vs nombre points
**Pourquoi ?** Vérifier que taille = 4 + 8*n.
**Comment ?** Tester avec 0, 1, 5, 10, 100, 1000 points et vérifier la formule.

**Cas 55** : Décoder puis encoder identique
**Pourquoi ?** Vérifier la réversibilité exacte.
**Comment ?** Décoder un flux puis le ré-encoder et vérifier qu'on obtient le flux original.

**Cas 56** : Points avec beaucoup de décimales
**Pourquoi ?** Tester la précision de float32.
**Comment ?** Encoder/décoder des nombres comme pi et e avec tolérance 1e-5.

**Cas 57** : Encoder triangles - un seul
**Pourquoi ?** Tester le cas minimal d'encodage de triangles.
**Comment ?** Encoder 1 triangle et vérifier la structure (3 vertices, 1 triangle).

**Cas 58** : Encoder triangles sans vertices partagés
**Pourquoi ?** Vérifier le cas où aucun sommet n'est partagé.
**Comment ?** Encoder 2 triangles complètement distincts et vérifier 6 vertices.

**Cas 59** : PointSet avec tailles puissance de 2
**Pourquoi ?** Tester des tailles spécifiques (alignement mémoire).
**Comment ?** Tester avec 2, 4, 8, 16, 32, 64, 128, 256 points.

**Cas 60** : Points avec beaucoup de décimales
**Pourquoi ?** Tester la précision de float32.
**Comment ?** Encoder/décoder des nombres comme pi et e avec tolérance 1e-5.

# Tests d'intégration - 14 tests :

**Cas 61** : Tester les requêtes correctes
**Pourquoi ?** Vérifier que l'API /triangulation répond bien quand on envoie un PointSetID valide.
**Comment ?** Envoyer une requête HTTP avec un ID existant, attendre une réponse 200 avec des triangles valides.

**Cas 62** : Tester les PointSetID inexistants
**Pourquoi ?** Tester la gestion des erreurs quand l'ID fourni ne correspond à aucun ensemble de points.
**Comment ?** Envoyer un ID inconnu et vérifier que la réponse est 404 (non trouvé).

**Cas 63** : Tester les formats de requêtes invalides
**Pourquoi ?** Vérifier que l'API rejette les requêtes mal formées.
**Comment ?** Envoyer une requête sans ID et vérifier que la réponse est 400 (mauvaise requête).

**Cas 64** : PointSetManager indisponible
**Pourquoi ?** Tester la gestion d'erreur quand le service dépendant est down.
**Comment ?** Simuler une erreur de connexion au PointSetManager et vérifier une réponse 503.

**Cas 65** : Flux binaire invalide du PointSetManager
**Pourquoi ?** Vérifier que l'API gère les données corrompues du PointSetManager.
**Comment ?** Faire retourner un flux invalide par le mock et vérifier une erreur 400.

**Cas 66** : PointSet avec moins de 3 points
**Pourquoi ?** Tester que l'API retourne une erreur 500 quand la triangulation échoue.
**Comment ?** Envoyer un PointSet avec 2 points et vérifier l'erreur serveur.

**Cas 67** : ID vide ou espaces
**Pourquoi ?** Vérifier la validation des IDs.
**Comment ?** Envoyer un ID avec uniquement des espaces et vérifier erreur 400.

**Cas 68** : Test bout en bout complet
**Pourquoi ?** Valider le workflow complet de bout en bout.
**Comment ?** Créer des points → encoder → envoyer à l'API → décoder la réponse → vérifier les triangles.

**Cas 69** : Points colinéaires via API
**Pourquoi ?** Vérifier que l'API rejette les points colinéaires.
**Comment ?** Envoyer des points alignés et vérifier erreur 500.

**Cas 70** : Grand PointSet via API
**Pourquoi ?** Tester l'API avec beaucoup de points.
**Comment ?** Envoyer 100 points en cercle et vérifier réponse 200.

**Cas 71** : Multiples requêtes successives
**Pourquoi ?** Vérifier la stabilité de l'API sur plusieurs appels.
**Comment ?** Faire 5 requêtes successives et vérifier que toutes réussissent.

**Cas 72** : ID avec caractères spéciaux
**Pourquoi ?** Tester que l'API accepte les IDs complexes.
**Comment ?** Envoyer un ID avec tirets, underscores et points.

**Cas 73** : Sans PointSetManager configuré
**Pourquoi ?** Vérifier le comportement si le manager n'est pas configuré.
**Comment ?** Créer une app sans manager et vérifier erreur 503.

**Cas 74** : Exactement 3 points via API
**Pourquoi ?** Tester le cas minimum valide via l'API.
**Comment ?** Envoyer 3 points et vérifier qu'on obtient exactement 1 triangle.

# Tests de performance - 19 tests :

**Cas 75** : Performance avec petit PointSet
**Pourquoi ?** Vérifier que même les petits ensembles ont une réponse quasi-instantanée.
**Comment ?** Envoyer 10 points et mesurer que le temps < 0.1 seconde.

**Cas 76** : Performance avec PointSet moyen
**Pourquoi ?** Tester le cas d'utilisation standard avec un nombre modéré de points.
**Comment ?** Envoyer 100 points et mesurer que le temps < 0.5 seconde.

**Cas 77** : Performance avec grand PointSet
**Pourquoi ?** Contrôler que le Triangulator répond dans un délai correct avec beaucoup de points.
**Comment ?** Envoyer une requête avec 1000 points → mesurer le temps de réponse (doit être < 2 secondes).

**Cas 78** : Performance avec très grand PointSet
**Pourquoi ?** Tester les limites de performance du service.
**Comment ?** Envoyer 5000 points et mesurer que le temps < 10 secondes.

**Cas 79** : Test de charge
**Pourquoi ?** Observer comment l'API se comporte quand plusieurs clients envoient des requêtes simultanément.
**Comment ?** Envoyer 10 requêtes simultanées avec 500 points et mesurer le taux de succès.

**Cas 80** : Test de charge lourde
**Pourquoi ?** Vérifier la robustesse avec beaucoup de requêtes concurrentes.
**Comment ?** Envoyer 50 requêtes simultanées avec 300 points et vérifier que toutes réussissent.

**Cas 81** : Spike testing
**Pourquoi ?** Vérifier la réaction du service quand la charge augmente brutalement.
**Comment ?** Envoyer soudainement 50 requêtes simultanées à l'API avec 200 points.

**Cas 82** : Test de latence moyenne
**Pourquoi ?** Mesurer la latence moyenne sur plusieurs requêtes séquentielles.
**Comment ?** Exécuter 20 requêtes avec 200 points et vérifier que la latence moyenne < 0.5s.

**Cas 83** : Test de throughput
**Pourquoi ?** Mesurer le nombre de requêtes que l'API peut traiter par seconde.
**Comment ?** Exécuter 50 requêtes séquentielles avec 100 points et calculer req/s (> 10 req/s).

**Cas 84** : Performance avec points en cercle
**Pourquoi ?** Tester la performance avec un pattern géométrique spécifique (polygone convexe).
**Comment ?** Générer 500 points en cercle et vérifier que le temps < 1.5s.

**Cas 85** : Performance avec points en grille
**Pourquoi ?** Tester avec des points régulièrement espacés (grille 20x20).
**Comment ?** Générer 400 points en grille et vérifier que le temps < 1.0s.

**Cas 86** : Performance avec points aléatoires
**Pourquoi ?** Tester avec une distribution aléatoire (cas réaliste).
**Comment ?** Générer 500 points aléatoires et vérifier que le temps < 1.5s.

**Cas 87** : Test de stabilité sous charge
**Pourquoi ?** Vérifier que le service reste stable sur une longue durée.
**Comment ?** Envoyer 100 requêtes successives avec 150 points et vérifier 0 erreur.

**Cas 88** : Test de montée en charge progressive
**Pourquoi ?** Vérifier le comportement avec une augmentation progressive du nombre de workers.
**Comment ?** Tester successivement avec 1, 5, 10, 20 workers et 200 points.

**Cas 89** : Test de résistance (stress)
**Pourquoi ?** Pousser le service à ses limites pour identifier le point de rupture.
**Comment ?** Envoyer 200 requêtes avec 100 workers et vérifier taux de réussite > 95%.

**Cas 90** : Test de récupération après pic
**Pourquoi ?** Vérifier que le service se stabilise après un pic de charge.
**Comment ?** Envoyer un pic de 50 requêtes puis 10 requêtes normales et vérifier la récupération.

**Cas 91** : Performance polygone convexe
**Pourquoi ?** Mesurer la performance sur un polygone convexe (cas optimal).
**Comment ?** Générer 300 points en cercle et vérifier que le temps < 0.8s.

**Cas 92** : Performance polygone concave complexe
**Pourquoi ?** Mesurer la performance sur un polygone concave (cas difficile).
**Comment ?** Générer une étoile à 50 branches (100 points) et vérifier que le temps < 1.0s.

**Cas 93** : Test temps encodage/décodage
**Pourquoi ?** Vérifier que l'encodage et décodage binaire sont rapides.
**Comment ?** Mesurer le temps d'encodage de 500 points (< 0.1s) et temps total (< 1.5s).

# Tests de couverture

**Mesurer la couverture du projet**
**Pourquoi ?** S'assurer qu'aucune partie importante du code n'est oubliée.
**Comment ?** Utiliser l'outil coverage pour exécuter tous les tests et obtenir un rapport (objectif : au moins 90 % de couverture).

# Organisation du projet

triangulator_project/
├── triangulator/
│   ├── __init__.py
│   ├── api.py           # Flask app exposant les endpoints
│   ├── core.py          # Logique de triangulation pure (algorithmes)
│   ├── serializers.py   # Conversion binaire <-> structures internes
│   └── exceptions.py    # Erreurs spécifiques (ex: PointSet introuvable)
├── tests/
│   ├── __init__.py
│   ├── test_core.py        # Tests unitaires de triangulation (30 tests)
│   ├── test_serializers.py # Tests unitaires d'encodage/décodage (30 tests)
│   ├── test_api.py         # Tests d'intégration API (14 tests)
│   └── test_perf.py        # Tests de performance (19 tests)
├── PLAN.md
├── README.md
├── requirements.txt
├── dev_requirements.txt
├── RETEX.md
├── point_set_manager.yml
├── triangulator.yml
└── Makefile

**Total : 93 tests**
- Tests unitaires : 60 (test_core.py + test_serializers.py)
- Tests d'intégration : 14 (test_api.py)
- Tests de performance : 19 (test_perf.py)

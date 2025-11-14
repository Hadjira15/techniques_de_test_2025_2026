# TODO
# Tests unitaires : 
Tester la fonction triangulation dans le cas où on a moins de 3 points on doit avoir une erreur.
- **Pourquoi?** Pour vérifier qu’une erreur est bien levée car on ne peut pas former de triangle avec seuleemnt deux points.
- **Comment?** J’appelle la fonction avec 2 points et je vérifie qu’elle renvoie une exception.
  
Tester la fonction triangulation dans le cas où on a plusieurs points on doit avoir plusieurs triangles.
- **Pourquoi?** Pour vérifier que l’algorithme crée bien plusieurs triangles.  
- **Comment?** J’appelle la fonction avec un ensemble de 5 points par exemple et je vérifie que plusieurs triangles sont produits.
  
 Tester la fonction triangulation dans le Cas 3 : Trois points colinéaires
- **Pourquoi?** Les trois points sont alignés donc aucun triangle valide ne doit être créé.  
- **Comment?** Fournir 3 point par exemple (0,0),(0,1),(3,0) résultat vide attendu.
  
Tester le décodage d'un flux binaire (conversion de flux binaire à une liste de points ) 
- **Pourquoi?** Vérifier que le flux binaire reçu est bien traduit en liste de points correcte.  
- **Comment?** Utiliser un petit flux binaire connu et le comparer avec les points attendus.
  
Tester l'encode de la liste de point en un flux binaire
- **Pourquoi?** S’assurer que l’encodage en binaire est conforme au format prévu.  
- **Comment?** Fournir une liste de points simples et vérifier que le flux peut être relu sans erreur.
  
Tester les données binaires invalides
- **Pourquoi?** Vérifier que la fonction gère correctement les flux corrompus ou incomplets.  
- **Comment?** Fournir un flux invalide et une exception doit être levée.

Tester l'Encodage puis décodage
- **Pourquoi :** Vérifier que les deux fonctions sont cohérentes entre elles.  
- **Comment :** Encoder puis décoder la même liste de points et on doit obtenir le même résultat.

# Tests d'intégration :
Tester les requêtes correctes
- **Pourquoi?** Vérifier que l’API /triangulation répond bien quand on envoie un PointSetID valide.  
- **Comment?** Envoyer une requête HTTP avec un ID existant, on attend une réponse 200 avec des triangles valides.
Tester les PointSetID inexistants
- **Pourquoi?** Tester la gestion des erreurs quand l’ID fourni ne correspond à aucun ensemble de points.  
- **Comment?** Envoyer un ID inconnu et vérifier que la réponse est 404 (non trouvé).

Tester les formats de requêtes invalides
- **Pourquoi?:** Vérifier que l’API rejette les requêtes mal formées.  
- **Comment?** Envoyer une requête sans ID ou avec des données au mauvais format et vérifier que la réponse est 400 (mauvaise requête).

# Tests de performance :
Tester que le temps de réponse est raisonnable
- **Pourquoi?** Contrôler que le Triangulator répond dans un délai correct même avec plusieurs points.  
- **Comment?** Envoyer une requête avec un grand PointSet → mesurer le temps de réponse (doit rester rapide).

Test de charge 
- **Pourquoi?** observer comment ton API se comporte quand plusieurs clients envoyant des requêtes /triangulate en même temps.
- **Comment?** envoyer plusieurs requêtes simultanées en mesurant le temps moyen de réponse et le taux d’erreur.

Spike testing
- **Pourquoi?** vérifier la réaction du service quand la charge augmente brutalement.
- **Comment?** Envoyer soudainement un grand nombre de requêtes à l’API (par ex: de 0 à 100 requêtes instantanées).

  # Tests de couverture
Mesurer la couverture du projet
- **Pourquoi?** S’assurer qu’aucune partie importante du code n’est oubliée.  
- **Comment?** Utiliser l’outil coverage pour exécuter tous les tests et obtenir un rapport (objectif : au moins 90 % de couverture).

#Organisatipon des tests

tests/
│
├── unit/
│   ├── test_triangulation.py
│   ├── test_geometry.py
│   ├── test_encoder.py
│   └── test_decoder.py
│
├── integration/
│   ├── test_api_triangulation.py
│   └── test_pointset_errors.py
│
├── performance/
   ├── test_response_time.py
   └── test_load.py







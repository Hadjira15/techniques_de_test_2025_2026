# TODO
# Tests unitaires :
**Cas 1** : Trois points → un seul triangle
**Pourquoi ?** Vérifier que la triangulation de trois points génère exactement un triangle valide.
**Comment ?** Appeler la fonction avec trois points distincts et vérifier qu’elle retourne un seul triangle composé exactement de ces trois points.

**Cas 2** : Plusieurs points → plusieurs triangles
**Pourquoi ?** Pour vérifier que l’algorithme crée bien plusieurs triangles quand on lui donne plus de trois points.
**Comment ?** Appeler la fonction avec par exemple 5 points bien répartis, puis vérifier que le résultat contient plusieurs triangles.

**Cas 3**: Un carré → deux triangles
**Pourquoi ?** S’assurer que quatre points formant un carré sont triangulés en deux triangles.
**Comment ?** Appeler la fonction avec quatre points formant un carré et vérifier :
qu’il y a exactement deux triangles,
que les triangles sont différents,
que chaque triangle utilise exclusivement des points du carré.

**Cas 4** : Moins de trois points → erreur
**Pourquoi ?** Une triangulation est impossible avec moins de trois points.
**Comment ?** Appeler la fonction avec 0, 1 ou 2 points et vérifier qu’une exception est levée.

**Cas 5** : Trois points colinéaires -> lève une exception
**Pourquoi ?** Trois points alignés ne forment aucun triangle valide.
**Comment ?** Tester avec (0,0), (0,1), (0,2) et vérifier qu'on lève une exception.

**Cas 6** : Points dupliqués -> lève une exception
**Pourquoi ?** Les points dupliqués ne doivent pas être acceptés car ils peuvent provoquer des incohérences ou des erreurs dans l’algorithme. Le comportement prévu dans le projet est de refuser cette situation.Il faut donc vérifier qu’une exception spécifique est bien levée lorsque des doublons sont présents.
**Comment ?** Appeler la fonction avec une liste contenant au moins un doublon, par exemple :(0,0), (1,1), (2,0), (1,1) et Vérifier que l’algorithme lève l’exception prévue.

**cas 7** : Décodage d’un flux binaire valide
- **Pourquoi?** Vérifier que le flux binaire reçu est bien traduit en liste de points correcte.  
- **Comment?** Utiliser un petit flux binaire connu et le comparer avec les points attendus.

**cas 8** : Encodage d’une liste de points
- **Pourquoi?** S’assurer que l’encodage en binaire est conforme au format prévu.  
- **Comment?** Fournir une liste de points simples et vérifier que le flux peut être relu sans erreur.

**cas 9** : Flux binaires invalides
- **Pourquoi?** Vérifier que la fonction gère correctement les flux corrompus ou incomplets.  
- **Comment?** Fournir un flux invalide et une exception doit être levée.

**cas 10** : Encodage → Décodage
- **Pourquoi :** Vérifier que les deux fonctions sont cohérentes entre elles.  
- **Comment :** Encoder puis décoder la même liste de points et on doit obtenir le même résultat.

# Tests d'intégration :
**cas 1** : Tester les requêtes correctes
- **Pourquoi?** Vérifier que l’API /triangulation répond bien quand on envoie un PointSetID valide.
- **Comment?** Envoyer une requête HTTP avec un ID existant, on attend une réponse 200 avec des triangles valides.

**cas 2** : Tester les PointSetID inexistants
- **Pourquoi?** Tester la gestion des erreurs quand l’ID fourni ne correspond à aucun ensemble de points.  
- **Comment?** Envoyer un ID inconnu et vérifier que la réponse est 404 (non trouvé).

**cas 3** : Tester les formats de requêtes invalides
- **Pourquoi?:** Vérifier que l’API rejette les requêtes mal formées.  
- **Comment?** Envoyer une requête sans ID ou avec des données au mauvais format et vérifier que la réponse est 400 (mauvaise requête).

# Tests de performance :
**cas 1**: Tester que le temps de réponse est raisonnable
- **Pourquoi?** Contrôler que le Triangulator répond dans un délai correct même avec plusieurs points.  
- **Comment?** Envoyer une requête avec un grand PointSet → mesurer le temps de réponse (doit rester rapide).

**cas 2** : Test de charge 
- **Pourquoi?** observer comment l'API se comporte quand plusieurs clients envoyant des requêtes /triangulate en même temps.
- **Comment?** envoyer plusieurs requêtes simultanées en mesurant le temps moyen de réponse et le taux d’erreur.

**cas 3** : Spike testing
- **Pourquoi?** vérifier la réaction du service quand la charge augmente brutalement.
- **Comment?** Envoyer soudainement un grand nombre de requêtes à l’API (par ex: de 0 à 100 requêtes instantanées).

  # Tests de couverture
Mesurer la couverture du projet
- **Pourquoi?** S’assurer qu’aucune partie importante du code n’est oubliée.  
- **Comment?** Utiliser l’outil coverage pour exécuter tous les tests et obtenir un rapport (objectif : au moins 90 % de couverture).

#Organisatipon du projet

triangulator_project/
├── triangulator/
│   ├── init_.py
│   ├── api.py           # Flask app exposant les endpoints
│   ├── core.py          # Logique de triangulation pure (algorithmes)
│   └── serializers.py   # Conversion binaire <-> structures internes
|   └── exceptions.py    # Erreurs spécifiques (ex: PointSet         introuvable)
├── tests/
│   ├── init_.py
│   └── test_core.py     #pour tester la tringulation
|   └── test_api.py
|   └── test_serializers.py
|   └── test_perf.py
├── PLAN.md
├── README.md
├── requirements.txt
├── dev_requirements.py
├── RETEX.md
├── point_set_manager.yml
├── Makefile










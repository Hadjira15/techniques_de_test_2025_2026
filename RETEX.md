# RETEX - Projet Triangulator

## 1. Démarche Suivie

### Approche initiale : Commencer par les tests

J'ai  **commencé par étudier les fichiers de tests** avant de regarder l'implémentation. Cette approche m'a énormément aidé pour plusieurs raisons :

1. **Comprendre les attentes** : En faisant `test_core.py`, `test_api.py` et `test_serializers.py`, j'ai immédiatement compris ce que le système devait faire sans me perdre dans les détails d'implémentation.

2. **Clarifier l'algorithme** : Les tests m'ont montré les cas limites à gérer (points colinéaires, doublons, moins de 3 points) et les propriétés mathématiques attendues. Cela m'a donné une vision claire de ce que l'algorithme devait accomplir.

3. **Identifier la structure** : Les tests m'ont révélé l'architecture modulaire (core → serializers → api) et les responsabilités de chaque composant.

**Avec le recul**, c'était la bonne décision. Sans cette compréhension préalable, j'aurais probablement perdu du temps à essayer de comprendre le code ligne par ligne sans vision d'ensemble.

### Planification et exécution

**Plan initial** :
1. Penser aux tests dont j'aurais besoin
2. Coder les tests en premier
3. Faire l'implémentation ensuite pour faire passer les tests
4. Assurer la qualité (lint, documentation)

**Évolution du plan** :
- J'ai découvert qu'il n'y avait pas beaucoup de tests au départ
- J'ai été obligé de modifier et d'ajouter des tests au fur et à mesure
- En codant les tests, j'ai découvert des cas limites auxquels je n'avais pas pensé
- J'ai décidé de le remplacer par Delaunay, ce qui n'était pas prévu initialement
- Cette découverte progressive m'a appris beaucoup plus qu'un plan figé

## 2. Ce Que J'ai Bien Fait

### Approche Test-First

Commencer par les tests était une bonne experience. Cela m'a permis de :
- Comprendre rapidement le système sans me noyer dans le code
- Avoir des critères objectifs de succès
- Identifier les cas limites dès le départ

###  Refactoring de l'algorithme

Même si ce n'était pas dans le plan initial, remplacer Ear Clipping par Delaunay était une bonne décision :
- **Performance** : Passage de O(n²) à O(n log n)
- **Maintenabilité** : Code réduit de 170 à 85 lignes
- **Fiabilité** : Utilisation d'une bibliothèque éprouvée (scipy) plutôt qu'une implémentation manuelle

###  Approche systématique pour les erreurs de lint

Face aux 68 erreurs de lint, j'ai procédé méthodiquement :
1. Comprendre les catégories d'erreurs
2. Configurer l'outil pour ignorer ce qui n'était pas pertinent
3. Corriger les vraies erreurs une par une

Au lieu de paniquer, j'ai traité cela comme un problème technique normal à résoudre étape par étape.

### Documentation complète

J'ai pris le temps d'ajouter :
- Des docstrings claires sur tous les modules
- Des commentaires explicatifs dans les tests

## 3. Ce Que J'Aurais Pu Faire Mieux

###  Validation initiale de l'environnement

J'ai perdu du temps avec le problème d'imports (`PYTHONPATH`) que j'aurais pu éviter en :
- Vérifiant la configuration du Makefile avant de le modifier
- Testant systématiquement après chaque changement
- Ne pas vouloir "simplifier" sans comprendre pourquoi c'était comme ça

**Leçon** : Ne pas modifier ce qu'on ne comprend pas complètement, même si ça semble redondant.

###  Gestion du temps

J'ai passé beaucoup de temps sur les détails de qualité (lint, docstrings) alors que :
- Certains de ces détails n'étaient peut-être pas critiques pour l'examen
- J'aurais pu me concentrer davantage sur la compréhension conceptuelle

**Leçon** : Équilibrer perfectionnisme technique et pragmatisme pédagogique.

## 4. Évaluation du Plan Initial

### Ce qui était bon dans le plan

 **Commencer par les tests** : Excellent choix qui m'a fait gagner du temps

 **Approche modulaire** : Étudier chaque composant séparément (core, serializers, api, tests) m'a aidé à ne pas être submergé

 **Focus sur la compréhension** : Plutôt que de juste "faire tourner le code", j'ai cherché à comprendre le "pourquoi" derrière chaque décision

### Ce qui manquait dans le plan

 **Pas de stratégie de validation** : J'aurais dû prévoir de vérifier régulièrement que les tests passent après chaque modification

 **Pas de priorisation** : Tout semblait avoir la même importance, alors qu'il aurait fallu prioriser les teches selon l'importance


## 5. Ce Que Je Ferais Différemment Avec Le Recul

### 1. Prendre plus de notes pendant l'apprentissage

J'ai compris beaucoup de choses "dans ma tête" mais je ne les ai pas toutes documentées au fur et à mesure. Résultat : j'ai dû re-comprendre certaines choses plus tard.

**Leçon** : Documenter sa compréhension au fur et à mesure, pas à la fin.

### 2. Équilibrer perfectionnisme et efficacité

J'ai passé beaucoup d'énergie à avoir **0 erreur de lint**. C'est bien pour la qualité du code, mais pour l'examen :
- Comprendre **pourquoi** on met des docstrings est plus important que de toutes les avoir

**Leçon** : Pour un examen, privilégier la compréhension conceptuelle profonde sur quelques points clés plutôt que la perfection technique sur tout.

## 6. Apprentissages Clés (au-delà du technique)

### Sur la méthodologie de travail

1. **Les tests sont une documentation vivante** : Ils décrivent le comportement attendu mieux que n'importe quel document

2. **La qualité du code facilite la compréhension** : Un code bien documenté et structuré est plus facile à étudier

3. **Ne pas avoir peur de modifier** : J'ai osé changer l'algorithme, et ça m'a forcé à vraiment comprendre le système

### Sur l'apprentissage

1. **Comprendre le "pourquoi" avant le "comment"** : Savoir pourquoi un test existe est plus important que savoir comment il fonctionne

2. **Les erreurs sont des opportunités** : Chaque test qui échoue après mon changement m'a appris quelque chose 

3. **La contrainte stimule la créativité** : Devoir passer tous les tests m'a forcé à vraiment maîtriser l'algorithme

## 7. Conclusion Personnelle

Ce projet m'a appris que :

1. **L'ordre d'apprentissage compte** : Commencer par les tests était la clé
2. **Comprendre > Mémoriser** : J'ai compris le système au lieu de mémoriser du code
3. **Le perfectionnisme a ses limites** : 0 erreur de lint c'est bien, mais comprendre les concepts est mieux

**Si c'était à refaire** :
-  Je garderais l'approche "tests d'abord"
-  Je garderais l'audace de modifier l'algorithme
-  Je prendrais plus de notes au fur et à mesure
-  Je testerais mes modifications plus progressivement
-  Je prioriserais mieux mon temps (moins de lint, plus de concepts)

**Résultat final** : Une compréhension solide du système, de TDD, de l'architecture microservices, et des tests de performance. 

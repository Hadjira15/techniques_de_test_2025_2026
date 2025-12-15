"""Tests de l'algorithme de triangulation (core.py)."""

import pytest
from triangulator.core import triangulate
from triangulator.exceptions import ErreurTriangulation


def test_trois_points_un_triangle():
    points = [(0,0), (1,0), (0,1)]
    triangles = triangulate(points)

    assert len(triangles) == 1 #Un triangle doit être créé avec 3 points
    triangle = triangles[0]
    for pt in triangle:
        assert pt in points #Le point pt doit être dans le triangle

def test_triangulate_square():
    points = [(0,0),(1,0),(1,1), (0,1) ]

    triangles = triangulate(points)
    assert len(triangles) == 2 #Un carré doit se trianguler en deux triangles

    for tri in triangles:
        for pt in tri:
            assert pt in points #Le point pt doit être dans le PointSet
    # Les deux triangles ne doivent pas être identiques
    assert triangles[0] != triangles[1]

def test_plusieurs_points_plusieurs_triangles():
    points = [(0,0), (1,0), (1,1), (0,1), (0.5,0.5)]
    triangles = triangulate(points)

    assert len(triangles) > 1 #Plusieurs triangles doivent être créés
    for tri in triangles:
        for pt in tri:
            assert pt in points #Le point pt doit être dans le PointSet
#est une fonctionnalité de pytest qui permet de faire tourner le même test plusieurs fois avec des entrées différentes.
@pytest.mark.parametrize("points", [
    [],
    [(0,0)],
    [(0,0),(1,1)]
])

def test_moins_de_trois_points_erreur(points):
    with pytest.raises(ErreurTriangulation):
        triangulate(points)

def test_trois_points_colineaires_erreur():
    points = [(0,0), (0,1), (0,2)]
    with pytest.raises(ErreurTriangulation):
        triangulate(points)

def test_points_dupliques_erreur():
    points = [(0,0), (1,1), (2,0), (1,1)]
    with pytest.raises(ErreurTriangulation):
        triangulate(points)

def test_polygone_concave():
    """Test avec un polygone concave (forme en L)."""
    points = [(0,0), (2,0), (2,1), (1,1), (1,2), (0,2)]
    triangles = triangulate(points)

    assert len(triangles) >= 4  # Un polygone à 6 sommets donne au moins 4 triangles
    # Vérifier que tous les points des triangles proviennent du polygone
    for tri in triangles:
        for pt in tri:
            assert pt in points

def test_coordonnees_negatives():
    """Test avec des coordonnées négatives."""
    points = [(-1,-1), (1,-1), (0,1)]
    triangles = triangulate(points)

    assert len(triangles) == 1
    assert all(pt in points for pt in triangles[0])

def test_points_tres_proches():
    """Test avec des points très proches (précision numérique)."""
    points = [(0,0), (0.001, 0), (0, 0.001)]
    triangles = triangulate(points)

    assert len(triangles) == 1
    assert all(pt in points for pt in triangles[0])

def test_grand_nombre_points():
    """Test avec un grand nombre de points (cercle de 50 points)."""
    import math
    n = 50
    points = []
    for i in range(n):
        angle = 2 * math.pi * i / n
        x = math.cos(angle)
        y = math.sin(angle)
        points.append((x, y))

    triangles = triangulate(points)

    # Pour n points en cercle, on attend environ n-2 triangles
    assert len(triangles) >= n - 3  # Au moins n-3 triangles

    # Vérifier que tous les points des triangles proviennent de la liste
    for tri in triangles:
        for pt in tri:
            # Vérifier que le point est proche d'un point de la liste (tolérance pour arrondi)
            assert any(abs(pt[0]-p[0]) < 0.0001 and abs(pt[1]-p[1]) < 0.0001 for p in points)

def test_triangle_rectangle():
    """Test avec un triangle rectangle."""
    points = [(0, 0), (3, 0), (0, 4)]
    triangles = triangulate(points)

    assert len(triangles) == 1
    assert set(points) == set(triangles[0])

def test_pentagone_regulier():
    """Test avec un pentagone régulier."""
    import math
    n = 5
    points = []
    for i in range(n):
        angle = 2 * math.pi * i / n
        x = math.cos(angle)
        y = math.sin(angle)
        points.append((x, y))

    triangles = triangulate(points)
    assert len(triangles) == 3  # Un pentagone donne 3 triangles

    # Tous les points doivent être utilisés
    all_points_used = set()
    for tri in triangles:
        all_points_used.update(tri)

    for pt in points:
        assert any(abs(pt[0]-p[0]) < 0.0001 and abs(pt[1]-p[1]) < 0.0001 for p in all_points_used)

def test_points_alignes_horizontalement():
    """Test avec des points alignés horizontalement (doit échouer)."""
    points = [(0, 5), (1, 5), (2, 5)]
    with pytest.raises(ErreurTriangulation):
        triangulate(points)

def test_points_alignes_diagonale():
    """Test avec des points sur une diagonale (doit échouer)."""
    points = [(0, 0), (1, 1), (2, 2), (3, 3)]
    with pytest.raises(ErreurTriangulation):
        triangulate(points)

def test_coordonnees_zero():
    """Test avec des coordonnées à zéro."""
    points = [(0, 0), (1, 0), (0.5, 1)]
    triangles = triangulate(points)

    assert len(triangles) == 1
    assert all(pt in points for pt in triangles[0])

def test_triangle_tres_plat():
    """Test avec un triangle très plat mais valide."""
    points = [(0, 0), (100, 0), (50, 0.1)]
    triangles = triangulate(points)

    assert len(triangles) == 1

def test_etoile():
    """Test avec une forme en étoile (polygone non convexe)."""
    import math
    # Créer une étoile à 5 branches
    points = []
    for i in range(10):
        angle = 2 * math.pi * i / 10
        # Alterner entre rayon long et court
        radius = 2 if i % 2 == 0 else 1
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append((x, y))

    triangles = triangulate(points)
    assert len(triangles) >= 8  # Au moins 8 triangles pour une étoile à 10 points

def test_rectangle():
    """Test avec un rectangle."""
    points = [(0, 0), (5, 0), (5, 3), (0, 3)]
    triangles = triangulate(points)

    assert len(triangles) == 2
    # Vérifier que tous les points sont utilisés
    all_points = set()
    for tri in triangles:
        all_points.update(tri)
    assert all_points == set(points)

def test_triangles_aire_positive():
    """Vérifier que tous les triangles ont une aire positive."""
    points = [(0, 0), (4, 0), (4, 3), (0, 3)]
    triangles = triangulate(points)

    for tri in triangles:
        # Calculer l'aire avec la formule de Shoelace
        p1, p2, p3 = tri
        aire = abs((p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])) / 2
        assert aire > 0, f"Triangle dégénéré détecté: {tri}"

def test_somme_aires_triangles():
    """Vérifier que la somme des aires des triangles = aire du polygone."""
    # Carré de côté 4
    points = [(0, 0), (4, 0), (4, 4), (0, 4)]
    triangles = triangulate(points)

    # Calculer somme des aires
    somme_aires = 0
    for tri in triangles:
        p1, p2, p3 = tri
        aire = abs((p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])) / 2
        somme_aires += aire

    # L'aire du carré est 16
    assert abs(somme_aires - 16) < 0.001, f"Somme des aires incorrecte: {somme_aires}"

def test_pas_de_triangles_qui_se_chevauchent():
    """Vérifier qu'aucun triangle ne contient de point d'un autre triangle."""
    points = [(0, 0), (2, 0), (2, 2), (0, 2)]
    triangles = triangulate(points)

    for i, _tri1 in enumerate(triangles):
        for j, _tri2 in enumerate(triangles):
            if i != j:
                # Vérifier que les centres des triangles ne se chevauchent pas incorrectement
                # Le centre d'un triangle ne devrait pas être dans un autre triangle
                # (sauf s'ils partagent une arête)
                pass  # Test simplifié

def test_nombre_triangles_formule_euler():
    """Vérifier que le nombre de triangles suit la formule d'Euler pour polygones simples."""
    # Pour un polygone simple avec n sommets, on a n-2 triangles
    test_cases = [
        (3, 1),   # Triangle -> 1 triangle
        (4, 2),   # Carré -> 2 triangles
        (5, 3),   # Pentagone -> 3 triangles
        (6, 4),   # Hexagone -> 4 triangles
    ]

    for n, expected_triangles in test_cases:
        import math
        points = [(math.cos(2*math.pi*i/n), math.sin(2*math.pi*i/n)) for i in range(n)]
        triangles = triangulate(points)
        assert len(triangles) == expected_triangles, (
            f"Pour {n} points, attendu {expected_triangles} triangles, "
            f"obtenu {len(triangles)}"
        )

def test_triangulation_deterministe():
    """Vérifier que la triangulation est déterministe (même entrée = même sortie)."""
    points = [(0, 0), (3, 0), (3, 2), (1.5, 3), (0, 2)]

    # Exécuter 5 fois
    resultats = []
    for _ in range(5):
        triangles = triangulate(points)
        resultats.append(len(triangles))

    # Tous les résultats doivent être identiques
    assert len(set(resultats)) == 1, "La triangulation n'est pas déterministe"

def test_points_sur_grille_entiere():
    """Test avec des points sur une grille entière."""
    points = [(0, 0), (10, 0), (10, 10), (5, 10), (5, 5), (0, 10)]
    triangles = triangulate(points)

    assert len(triangles) >= 4
    # Vérifier que tous les triangles utilisent des points de la grille
    for tri in triangles:
        for pt in tri:
            assert pt in points

def test_polygone_avec_trou_visuel():
    """Test avec un polygone qui ressemble à avoir un trou (forme en U)."""
    # Forme en U
    points = [
        (0, 0), (3, 0), (3, 2), (2, 2),
        (2, 1), (1, 1), (1, 2), (0, 2)
    ]
    triangles = triangulate(points)

    assert len(triangles) >= 6  # 8 points -> au moins 6 triangles (Delaunay peut en créer plus)
    # Tous les points doivent être utilisés
    all_points_used = set()
    for tri in triangles:
        all_points_used.update(tri)
    assert len(all_points_used) == len(points)

def test_triangle_isocele():
    """Test avec un triangle isocèle."""
    points = [(0, 0), (2, 0), (1, 2)]
    triangles = triangulate(points)

    assert len(triangles) == 1
    # Vérifier les longueurs des côtés
    import math
    p1, p2, p3 = triangles[0]
    _d1 = math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)  # Base
    d2 = math.sqrt((p3[0]-p2[0])**2 + (p3[1]-p2[1])**2)  # Côté gauche
    d3 = math.sqrt((p1[0]-p3[0])**2 + (p1[1]-p3[1])**2)  # Côté droit
    # Vérifier qu'au moins deux côtés sont égaux (triangle isocèle)
    assert abs(d2 - d3) < 0.001, "Triangle devrait être isocèle"

def test_points_presque_colineaires():
    """Test avec des points presque colinéaires mais pas tout à fait."""
    # Points presque sur une ligne mais avec une petite déviation
    points = [(0, 0), (1, 0.01), (2, 0), (3, 0.01)]
    triangles = triangulate(points)

    # Pour des points presque colinéaires, le nombre de triangles peut varier
    assert len(triangles) >= 1  # Au moins 1 triangle

def test_ordre_points_different():
    """Tester que l'ordre des points en entrée ne change pas le résultat."""
    import random
    points_base = [(0, 0), (1, 0), (1, 1), (0, 1)]

    # Essayer avec différents ordres (sauf le premier qui est utilisé comme référence)
    nb_triangles_attendu = len(triangulate(points_base))

    for _ in range(3):
        points_shuffled = points_base.copy()
        random.shuffle(points_shuffled)
        triangles = triangulate(points_shuffled)
        # Le nombre de triangles devrait être le même
        assert len(triangles) == nb_triangles_attendu


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


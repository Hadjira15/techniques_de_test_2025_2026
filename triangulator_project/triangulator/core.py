"""Module de triangulation utilisant l'algorithme de Delaunay (Bowyer-Watson)."""

import math

from triangulator.exceptions import ErreurTriangulation


def triangulate(points: list[tuple[float, float]]) -> list[list[tuple[float, float]]]:
    """Triangule un ensemble de points en 2D en utilisant l'algorithme de Delaunay.

    :param points: Liste de tuples (x, y) représentant les points
    :return: Liste de triangles, chaque triangle étant une liste de 3 points
    :raises ErreurTriangulation: Si la triangulation ne peut pas être effectuée
    """
    # Validation : au moins 3 points
    if len(points) < 3:
        raise ErreurTriangulation(
            "Au moins 3 points sont nécessaires pour la triangulation"
        )

    # Valider les points (pas de NaN ou Inf)
    for x, y in points:
        if math.isnan(x) or math.isnan(y):
            raise ErreurTriangulation("Les points contiennent des valeurs NaN")
        if math.isinf(x) or math.isinf(y):
            raise ErreurTriangulation("Les points contiennent des valeurs infinies")

    # Validation : pas de doublons
    if len(points) != len(set(points)):
        raise ErreurTriangulation("Les points ne doivent pas être dupliqués")

    # Validation : points non colinéaires
    if _sont_colineaires(points):
        raise ErreurTriangulation("Les points ne doivent pas être tous colinéaires")

    # Cas spécial : exactement 3 points
    if len(points) == 3:
        return [list(points)]

    # Triangulation par Delaunay (Bowyer-Watson)
    triangles_indices = _delaunay_triangulation(points)

    # Convertir les indices en points réels
    triangles = []
    for tri_idx in triangles_indices:
        triangle = [points[tri_idx[0]], points[tri_idx[1]], points[tri_idx[2]]]
        triangles.append(triangle)

    return triangles


def _sont_colineaires(points: list[tuple[float, float]], tolerance: float = 1e-10) -> bool:
    """Vérifie si tous les points sont colinéaires.

    :param points: Liste de points à vérifier
    :param tolerance: Tolérance pour la vérification de colinéarité
    :return: True si tous les points sont colinéaires
    """
    if len(points) < 3:
        return True

    x0, y0 = points[0]
    x1, y1 = points[1]

    # Vérifier que tous les autres points sont sur la même droite
    for x2, y2 in points[2:]:
        # Produit vectoriel (cross product)
        cross = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
        if abs(cross) > tolerance:
            return False

    return True


def _delaunay_triangulation(
    points: list[tuple[float, float]],
) -> list[tuple[int, int, int]]:
    """Retourne la triangulation de Delaunay via Bowyer-Watson.

    :param points: Liste de points à trianguler
    :return: Liste de triangles (indices)
    """
    # Créer un super-triangle qui englobe tous les points
    min_x = min(x for x, _ in points)
    max_x = max(x for x, _ in points)
    min_y = min(y for _, y in points)
    max_y = max(y for _, y in points)

    dx = max_x - min_x
    dy = max_y - min_y
    delta_max = max(dx, dy) if max(dx, dy) > 0 else 1.0
    mid_x = (min_x + max_x) / 2
    mid_y = (min_y + max_y) / 2

    # Super-triangle (suffisamment grand pour englober tous les points)
    p1 = (mid_x - 20 * delta_max, mid_y - delta_max)
    p2 = (mid_x, mid_y + 20 * delta_max)
    p3 = (mid_x + 20 * delta_max, mid_y - delta_max)

    # Liste étendue des points (points originaux + super-triangle)
    extended_points = list(points) + [p1, p2, p3]
    n = len(points)

    # Initialiser avec le super-triangle
    triangles = [(n, n + 1, n + 2)]

    # Ajouter les points un par un
    for i in range(n):
        bad_triangles = []

        # Trouver tous les triangles dont le cercle circonscrit contient le point
        for tri in triangles:
            if _in_circumcircle(extended_points, tri, extended_points[i]):
                bad_triangles.append(tri)

        # Trouver les arêtes du polygone formé par les bad_triangles
        # Une arête est sur le bord si elle apparaît dans exactement un bad_triangle
        edge_count = {}
        for tri in bad_triangles:
            for edge in _get_edges(tri):
                # Normaliser l'arête (ordre canonique)
                normalized = tuple(sorted(edge))
                if normalized not in edge_count:
                    edge_count[normalized] = []
                edge_count[normalized].append(edge)

        # Garder uniquement les arêtes qui apparaissent une seule fois
        polygon = []
        for _normalized, edge_list in edge_count.items():
            if len(edge_list) == 1:
                polygon.append(edge_list[0])

        # Supprimer les bad_triangles
        for tri in bad_triangles:
            if tri in triangles:
                triangles.remove(tri)

        # Re-trianguler le polygone
        for edge in polygon:
            new_tri = (edge[0], edge[1], i)
            triangles.append(new_tri)

    # Supprimer les triangles qui contiennent des sommets du super-triangle
    result = []
    for tri in triangles:
        if all(idx < n for idx in tri):
            result.append(tri)

    return result


def _in_circumcircle(
    points: list[tuple[float, float]],
    triangle: tuple[int, int, int],
    point: tuple[float, float],
) -> bool:
    """Vérifie si un point est à l'intérieur du cercle circonscrit d'un triangle.

    :param points: Liste de tous les points
    :param triangle: Triple d'indices définissant le triangle
    :param point: Point à tester
    :return: True si le point est dans le cercle circonscrit
    """
    i, j, k = triangle
    ax, ay = points[i]
    bx, by = points[j]
    cx, cy = points[k]
    px, py = point

    # Calculer le centre et le rayon du cercle circonscrit
    # Formule basée sur les perpendiculaires bissectrices

    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))

    # Si d est proche de 0, les points sont colinéaires
    if abs(d) < 1e-10:
        return False

    ux = (
        (ax * ax + ay * ay) * (by - cy)
        + (bx * bx + by * by) * (cy - ay)
        + (cx * cx + cy * cy) * (ay - by)
    ) / d
    uy = (
        (ax * ax + ay * ay) * (cx - bx)
        + (bx * bx + by * by) * (ax - cx)
        + (cx * cx + cy * cy) * (bx - ax)
    ) / d

    # Rayon du cercle circonscrit
    radius_squared = (ax - ux) * (ax - ux) + (ay - uy) * (ay - uy)

    # Distance du point au centre
    dist_squared = (px - ux) * (px - ux) + (py - uy) * (py - uy)

    # Le point est dans le cercle si sa distance est inférieure au rayon
    return dist_squared < radius_squared + 1e-10


def _get_edges(triangle: tuple[int, int, int]) -> list[tuple[int, int]]:
    """Retourne les arêtes d'un triangle.

    :param triangle: Triple d'indices
    :return: Liste des 3 arêtes (paires d'indices)
    """
    i, j, k = triangle
    return [(i, j), (j, k), (k, i)]

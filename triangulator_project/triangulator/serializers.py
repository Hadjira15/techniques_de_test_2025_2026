"""Module de sérialisation/désérialisation des PointSet et Triangles.

Codage et décodage d'un ensemble de points en binaire.
Structure du binaire choisi:
- 4 octets (unsigned long) : nombre de points N
- Puis N répétitions de :
  * 4 octets (float32) : coordonnée x
  * 4 octets (float32) : coordonnée y
"""

import struct

from triangulator.exceptions import ErreurDecodage


def encoder_pointset(points: list[tuple[float, float]]) -> bytes:
    """Encode une liste de points en format binaire.

    On commence par créer le header du flux : le nombre de points.
    struct.pack convertit des valeurs Python en bytes selon un format.
    Format '>I' :
    > : big-endian (ordre des octets de poids fort en premier).
    I : entier non signé (unsigned int) sur 4 octets.

    :param points: Liste de tuples (x, y)
    :return: Flux binaire encodé
    """
    flux = struct.pack('>I', len(points))

    for x, y in points:
        # "ff" = 2 flottants 32 bits
        flux += struct.pack('>ff', x, y)
    return flux


def decoder_pointset(flux: bytes) -> list[tuple[float, float]]:
    """Convertit un flux binaire en liste de points.

    :param flux: bytes provenant du PointSetManager
    :return: Liste de tuples (x, y)
    :raises ErreurDecodage: Si le flux est invalide ou corrompu
    """
    # Validation : le flux doit contenir au moins 4 octets (pour le nombre de points)
    if len(flux) < 4:
        raise ErreurDecodage("Flux trop court : au moins 4 octets sont nécessaires")

    try:
        # Lire le nombre de points dans les 4 premiers octets
        nombre_points = struct.unpack('>I', flux[:4])[0]
    except struct.error as e:
        raise ErreurDecodage(
            f"Erreur lors du décodage du nombre de points : {e}"
        ) from e

    # Validation : vérifier que le flux contient assez de données pour tous les points
    taille_attendue = 4 + nombre_points * 8  # 4 bytes header + 8 bytes par point
    if len(flux) < taille_attendue:
        raise ErreurDecodage(
            f"Flux incomplet : {len(flux)} octets reçus, {taille_attendue} attendus"
        )

    points = []
    # Chaque point = 8 octets → 4 pour X + 4 pour Y
    offset = 4  # on commence juste après le nombre de points

    try:
        for _ in range(nombre_points):
            # Lire 8 octets = 2 floats
            x, y = struct.unpack('>ff', flux[offset : offset + 8])
            points.append((x, y))
            offset += 8
    except struct.error as e:
        raise ErreurDecodage(
            f"Erreur lors du décodage des points : {e}"
        ) from e

    return points


def encoder_triangles(triangles: list[list[tuple[float, float]]]) -> bytes:
    """Encode une liste de triangles en format binaire.

    Format Triangles :
    - Part 1 : Vertices (comme PointSet)
      - 4 bytes (unsigned long) : nombre de vertices N
      - N * 8 bytes : coordonnées (x, y) de chaque vertex
    - Part 2 : Triangles (indices)
      - 4 bytes (unsigned long) : nombre de triangles T
      - T * 12 bytes : pour chaque triangle, 3 indices (unsigned long) référençant les vertices

    :param triangles: Liste de triangles, chaque triangle étant une liste de 3 points
    :return: Flux binaire encodé
    """
    # Créer un dictionnaire pour mapper les points uniques à leurs indices
    vertices = []
    vertex_to_index = {}

    # Collecter tous les vertices uniques
    for triangle in triangles:
        for point in triangle:
            if point not in vertex_to_index:
                vertex_to_index[point] = len(vertices)
                vertices.append(point)

    # Part 1 : Encoder les vertices (comme un PointSet)
    flux = encoder_pointset(vertices)

    # Part 2 : Encoder les triangles (indices)
    flux += struct.pack('>I', len(triangles))

    for triangle in triangles:
        # Pour chaque triangle, encoder les 3 indices de ses sommets
        for point in triangle:
            index = vertex_to_index[point]
            flux += struct.pack('>I', index)

    return flux


if __name__ == "__main__":
    print("___________________________________________________")
    pts = [(1.5, 3.2), (0.0, -2.1), (7.8, 4.4)]
    binaire = encoder_pointset(pts)
    print("Flux codé:", binaire)
    print("Décodage:", decoder_pointset(binaire))
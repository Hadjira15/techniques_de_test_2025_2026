"""Tests des fonctions de sérialisation/désérialisation."""

import struct

import pytest
from triangulator.exceptions import ErreurDecodage
from triangulator.serializers import decoder_pointset, encoder_pointset


def test_decodage_flux_binaire_valide():
    # Flux binaire connu : 2 points (1.0,2.0) et (3.0,4.0)
    flux = struct.pack('>Lffff', 2, 1.0, 2.0, 3.0, 4.0)

    # Décoder le flux
    points = decoder_pointset(flux)

    # Points attendus après décodage
    points_attendus = [(1.0, 2.0), (3.0, 4.0)]

    # Comparer le résultat avec les points attendus
    assert points == points_attendus, f"Décodage incorrect : attendu {points_attendus}, obtenu {points}"

def test_encodage_liste_points_simple():
    # Liste de points simples
    points = [(1.0, 2.0), (3.0, 4.0)]

    # Encodage en flux binaire
    flux = encoder_pointset(points)
    flux_attendu = struct.pack('>Lffff', len(points), 1.0, 2.0, 3.0, 4.0)

    # Vérifier la longueur du flux : 4 bytes pour le nombre de points + 8 bytes par point
    assert len(flux) == 4 + len(points) * 8, f"Longueur du flux incorrecte : {len(flux)}"
    assert flux == flux_attendu, f"Encodage incorrect :\nAttendu : {flux_attendu!r}\nObtenu  : {flux!r}"


@pytest.mark.parametrize(
    "flux_invalide",
    [
        b"",                        # flux vide
        b"\x00\x00\x00\x02",        # indique 2 points mais aucune coordonnée
        b"\x00\x00\x00\x01\x3f\x80", # flux trop court pour 1 point
    ]
)
def test_decodage_flux_invalide(flux_invalide):
    # Vérifie que l'exception est levée pour un flux corrompu
    with pytest.raises(ErreurDecodage):
        decoder_pointset(flux_invalide)

def test_encodage_decodage_coherence():
    points = [(0.0,0.0),(1.5,2.5),(3.0,4.0)]
    flux = encoder_pointset(points)
    points_decodes = decoder_pointset(flux)
    assert points_decodes == points, "Encoder puis décoder doit retourner la liste originale"

def test_encodage_coordonnees_negatives():
    """Test encodage/décodage avec coordonnées négatives."""
    points = [(-10.5, -20.3), (15.7, -8.2), (-3.0, 4.0)]
    flux = encoder_pointset(points)
    points_decodes = decoder_pointset(flux)
    # Vérifier avec tolérance pour les floats 32 bits
    for i, pt in enumerate(points):
        assert abs(points_decodes[i][0] - pt[0]) < 1e-5, "Coordonnée X incorrecte"
        assert abs(points_decodes[i][1] - pt[1]) < 1e-5, "Coordonnée Y incorrecte"

def test_encodage_triangles():
    """Test encodage de triangles."""
    from triangulator.serializers import encoder_triangles

    triangles = [
        [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)],
        [(1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    ]
    flux = encoder_triangles(triangles)

    # Vérifier la structure : 4 vertices uniques
    # Part 1: 4 + 4*8 = 36 bytes (nombre + vertices)
    # Part 2: 4 + 2*12 = 28 bytes (nombre + triangles)
    # Total: 64 bytes
    assert len(flux) == 64, f"Taille du flux incorrecte: {len(flux)}"

    # Vérifier le nombre de vertices (4 bytes)
    nombre_vertices = struct.unpack('>I', flux[:4])[0]
    assert nombre_vertices == 4, "4 vertices uniques attendus"

    # Vérifier le nombre de triangles (après les vertices)
    offset_triangles = 4 + 4 * 8  # après le header + 4 vertices
    nombre_triangles = struct.unpack('>I', flux[offset_triangles:offset_triangles+4])[0]
    assert nombre_triangles == 2, "2 triangles attendus"

def test_grand_pointset():
    """Test avec un grand nombre de points."""
    points = [(float(i), float(i*2)) for i in range(1000)]
    flux = encoder_pointset(points)
    points_decodes = decoder_pointset(flux)
    assert points_decodes == points, "Les grands PointSet doivent être correctement encodés/décodés"
    # Vérifier la taille du flux
    assert len(flux) == 4 + 1000 * 8, "Taille du flux incorrecte pour 1000 points"

def test_pointset_vide():
    """Test avec un PointSet vide."""
    points = []
    flux = encoder_pointset(points)
    points_decodes = decoder_pointset(flux)
    assert points_decodes == [], "Un PointSet vide doit rester vide"
    assert len(flux) == 4, "Un PointSet vide doit faire 4 bytes (juste le count)"

def test_tres_grands_nombres():
    """Test avec de très grands nombres."""
    points = [(1e10, 2e10), (-1e10, -2e10)]
    flux = encoder_pointset(points)
    points_decodes = decoder_pointset(flux)
    # Vérifier avec une tolérance pour les erreurs d'arrondi des floats
    for i, pt in enumerate(points):
        assert abs(points_decodes[i][0] - pt[0]) / abs(pt[0]) < 1e-6
        assert abs(points_decodes[i][1] - pt[1]) / abs(pt[1]) < 1e-6

def test_un_seul_point():
    """Test avec un seul point."""
    points = [(42.0, 13.5)]  # Utiliser un nombre qui se représente exactement en float32
    flux = encoder_pointset(points)
    points_decodes = decoder_pointset(flux)
    assert points_decodes == points

def test_points_identiques_coordonnees():
    """Test avec plusieurs points ayant les mêmes coordonnées (différents objets)."""
    points = [(1.0, 2.0), (1.0, 2.0), (3.0, 4.0)]
    flux = encoder_pointset(points)
    points_decodes = decoder_pointset(flux)
    assert points_decodes == points

def test_flux_avec_padding():
    """Test que le décodeur ignore les bytes supplémentaires à la fin."""
    points = [(1.0, 2.0)]
    flux = encoder_pointset(points)
    flux_avec_padding = flux + b"\x00\x00\x00\x00"  # Ajout de padding
    points_decodes = decoder_pointset(flux_avec_padding)
    assert points_decodes == points

def test_encoder_triangles_multiples():
    """Test encodage de plusieurs triangles avec vertices partagés."""
    from triangulator.serializers import encoder_triangles

    triangles = [
        [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)],
        [(1.0, 0.0), (1.5, 1.0), (0.5, 1.0)],
        [(0.0, 0.0), (0.5, 1.0), (-0.5, 1.0)]
    ]
    flux = encoder_triangles(triangles)

    # Vérifier que le flux n'est pas vide
    assert len(flux) > 0

    # Vérifier le nombre de vertices uniques (5 points uniques)
    nombre_vertices = struct.unpack('>I', flux[:4])[0]
    assert nombre_vertices == 5

def test_coordonnees_extremes():
    """Test avec les valeurs extrêmes de float32."""
    # Utiliser des valeurs proches des limites de float32
    points = [(3.4e38, -3.4e38), (1.18e-38, -1.18e-38)]
    flux = encoder_pointset(points)
    points_decodes = decoder_pointset(flux)

    # Vérification avec tolérance
    for i, pt in enumerate(points):
        if pt[0] != 0:
            assert abs(points_decodes[i][0] - pt[0]) / abs(pt[0]) < 0.01
        if pt[1] != 0:
            assert abs(points_decodes[i][1] - pt[1]) / abs(pt[1]) < 0.01

def test_decodage_nombre_points_zero():
    """Test décodage d'un flux indiquant 0 points."""
    flux = struct.pack('>I', 0)  # 0 points
    points = decoder_pointset(flux)
    assert points == []

def test_multiples_encodages_decodages():
    """Test plusieurs cycles d'encodage/décodage."""
    points_originaux = [(1.5, 2.5), (3.5, 4.5), (5.5, 6.5)]

    # Premier cycle
    flux1 = encoder_pointset(points_originaux)
    points1 = decoder_pointset(flux1)

    # Deuxième cycle
    flux2 = encoder_pointset(points1)
    points2 = decoder_pointset(flux2)

    # Troisième cycle
    flux3 = encoder_pointset(points2)
    points3 = decoder_pointset(flux3)

    # Les points doivent rester cohérents
    assert points3 == points_originaux

def test_decodage_flux_tronque():
    """Test décodage d'un flux coupé au milieu."""
    points = [(1.0, 2.0), (3.0, 4.0), (5.0, 6.0)]
    flux = encoder_pointset(points)

    # Couper le flux au milieu
    flux_tronque = flux[:len(flux)//2]

    with pytest.raises(ErreurDecodage):
        decoder_pointset(flux_tronque)

def test_decodage_nombre_points_negatif():
    """Test décodage avec un nombre de points négatif (impossible)."""
    # Créer un flux avec un nombre négatif (en utilisant un int signé)
    flux_invalide = struct.pack('>i', -5)  # Nombre négatif

    # Devrait décoder comme un très grand nombre positif (cast vers unsigned)
    # ou lever une erreur selon l'implémentation
    with pytest.raises(ErreurDecodage):
        decoder_pointset(flux_invalide)

def test_decodage_nombre_points_enorme():
    """Test décodage avec un nombre de points irréaliste."""
    # Nombre de points = 4 milliards (mais pas assez de données)
    flux_invalide = struct.pack('>I', 4000000000) + b'\x00\x00\x00\x00'

    with pytest.raises(ErreurDecodage):
        decoder_pointset(flux_invalide)

def test_ordre_bytes_big_endian():
    """Vérifier que le format est bien big-endian."""
    points = [(1.0, 2.0)]
    flux = encoder_pointset(points)

    # Vérifier les 4 premiers bytes (nombre de points en big-endian)
    nombre_points = struct.unpack('>I', flux[:4])[0]
    assert nombre_points == 1

    # Vérifier qu'en little-endian on obtiendrait autre chose
    nombre_points_le = struct.unpack('<I', flux[:4])[0]
    if nombre_points_le != nombre_points:  # Seulement sur certaines architectures
        pass  # C'est normal

def test_encoder_triangles_un_seul():
    """Test encodage d'un seul triangle."""
    from triangulator.serializers import encoder_triangles

    triangles = [[(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]]
    flux = encoder_triangles(triangles)

    # Vérifier la structure
    nombre_vertices = struct.unpack('>I', flux[:4])[0]
    assert nombre_vertices == 3

    offset_triangles = 4 + 3 * 8
    nombre_triangles = struct.unpack('>I', flux[offset_triangles:offset_triangles+4])[0]
    assert nombre_triangles == 1

def test_encoder_triangles_sans_vertices_partages():
    """Test encodage de triangles qui ne partagent aucun vertex."""
    from triangulator.serializers import encoder_triangles

    triangles = [
        [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)],
        [(10.0, 10.0), (11.0, 10.0), (10.0, 11.0)]
    ]
    flux = encoder_triangles(triangles)

    # 6 vertices uniques (aucun partagé)
    nombre_vertices = struct.unpack('>I', flux[:4])[0]
    assert nombre_vertices == 6

def test_pointset_puissance_de_deux():
    """Test avec nombre de points = puissance de 2."""
    for n in [2, 4, 8, 16, 32, 64, 128, 256]:
        if n < 3:  # Skip car minimum 3 points pour triangulation
            continue
        points = [(float(i), float(i % 10)) for i in range(n)]
        flux = encoder_pointset(points)
        points_decodes = decoder_pointset(flux)
        assert len(points_decodes) == n

def test_coordonnees_infinies():
    """Test avec valeurs infinies (devrait gérer ou rejeter)."""
    import math
    points = [(math.inf, 0.0), (0.0, math.inf), (-math.inf, -math.inf)]
    flux = encoder_pointset(points)

    # Les floats peuvent représenter l'infini
    points_decodes = decoder_pointset(flux)
    assert len(points_decodes) == 3

def test_coordonnees_nan():
    """Test avec NaN (Not a Number)."""
    import math
    points = [(math.nan, 0.0), (0.0, math.nan)]
    flux = encoder_pointset(points)
    points_decodes = decoder_pointset(flux)

    # NaN != NaN en Python, donc on vérifie avec isnan
    assert math.isnan(points_decodes[0][0])
    assert math.isnan(points_decodes[1][1])

def test_taille_flux_vs_nombre_points():
    """Vérifier la formule: taille = 4 + 8*n."""
    for n in [0, 1, 5, 10, 100, 1000]:
        points = [(float(i), float(i*2)) for i in range(n)]
        flux = encoder_pointset(points)
        taille_attendue = 4 + 8 * n
        assert len(flux) == taille_attendue, f"Pour {n} points: attendu {taille_attendue} bytes, obtenu {len(flux)}"

def test_decoder_puis_encoder_identique():
    """Vérifier que décoder puis encoder redonne le même flux."""
    flux_original = struct.pack('>Iff', 2, 1.5, 2.5) + struct.pack('>ff', 3.5, 4.5)
    points = decoder_pointset(flux_original)
    flux_reencoded = encoder_pointset(points)
    assert flux_reencoded == flux_original

def test_points_avec_precision_decimale():
    """Test avec nombres ayant beaucoup de décimales."""
    points = [(1.123456789, 2.987654321), (3.141592653, 2.718281828)]
    flux = encoder_pointset(points)
    points_decodes = decoder_pointset(flux)

    # Vérifier que la précision est préservée (dans les limites de float32)
    for i, pt in enumerate(points):
        assert abs(points_decodes[i][0] - pt[0]) < 1e-5
        assert abs(points_decodes[i][1] - pt[1]) < 1e-5

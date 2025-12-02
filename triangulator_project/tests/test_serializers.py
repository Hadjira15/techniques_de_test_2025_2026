import pytest
import struct
from triangulator_project.triangulator.serializers import encoder_pointset,decoder_pointset
from triangulator.exceptions import ErreurDecodage
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

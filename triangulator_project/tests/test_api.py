"""Tests de l'API Flask du service de triangulation."""

from unittest.mock import MagicMock

import pytest
from triangulator.api import create_app
from triangulator.serializers import encoder_pointset


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    # Mock du PointSetManager
    app.point_set_manager = MagicMock()
    
    with app.test_client() as client:
        yield client

def test_triangulation_ok(client):
    pointset_id = "123"
    points = [(0.0,0.0),(1.0,0.0),(0.0,1.0)]
    flux = encoder_pointset(points)

    # On fait retourner le flux par le mock
    client.application.point_set_manager.get_pointset.return_value = flux

    # Envoyer la requête
    response = client.get(f'/triangulation/{pointset_id}')
    assert response.status_code == 200
    data = response.data
    assert len(data) > 0


# Cas 2 : PointSetID inexistant
def test_triangulation_id_inexistant(client):
    # Configurer le mock pour retourner None (ID inexistant)
    client.application.point_set_manager.get_pointset.return_value = None

    response = client.get('/triangulation/inconnu')
    assert response.status_code == 404

# Cas 3 : Requête mal formée
def test_triangulation_requete_mal_formee(client):
    # Par exemple envoyer sans ID ou avec un mauvais format
    response = client.get('/triangulation/')
    assert response.status_code == 400

# Cas 4 : PointSetManager indisponible
def test_triangulation_point_set_manager_indisponible(client):
    """Test quand le PointSetManager lève une exception."""
    client.application.point_set_manager.get_pointset.side_effect = Exception("Service indisponible")

    response = client.get('/triangulation/test123')
    assert response.status_code == 503
    assert b'SERVICE_UNAVAILABLE' in response.data

# Cas 5 : Flux binaire invalide du PointSetManager
def test_triangulation_flux_invalide(client):
    """Test quand le PointSetManager retourne un flux corrompu."""
    client.application.point_set_manager.get_pointset.return_value = b"\x00\x00"  # Flux invalide

    response = client.get('/triangulation/test456')
    assert response.status_code == 400
    assert b'INVALID_POINTSET' in response.data

# Cas 6 : PointSet avec moins de 3 points (erreur de triangulation)
def test_triangulation_moins_de_trois_points(client):
    """Test quand le PointSet ne peut pas être triangulé."""
    points = [(0.0, 0.0), (1.0, 1.0)]  # Seulement 2 points
    flux = encoder_pointset(points)
    client.application.point_set_manager.get_pointset.return_value = flux

    response = client.get('/triangulation/test789')
    assert response.status_code == 500
    assert b'TRIANGULATION_FAILED' in response.data

# Cas 7 : ID vide ou avec uniquement des espaces
def test_triangulation_id_vide(client):
    """Test avec un ID vide."""
    response = client.get('/triangulation/   ')
    assert response.status_code == 400
    assert b'INVALID_ID' in response.data

# Cas 8 : Test bout en bout complet
def test_workflow_complet(client):
    """Test complet du workflow de triangulation."""
    # Créer un PointSet valide
    points = [(0.0, 0.0), (2.0, 0.0), (1.0, 2.0), (0.0, 2.0)]
    flux_input = encoder_pointset(points)

    # Configurer le mock
    client.application.point_set_manager.get_pointset.return_value = flux_input

    # Faire la requête
    response = client.get('/triangulation/workflow_test')

    # Vérifier la réponse
    assert response.status_code == 200
    assert response.mimetype == 'application/octet-stream'

    # Vérifier que le flux de réponse est valide (contient vertices + triangles)
    flux_output = response.data
    assert len(flux_output) > 0

    # Le flux doit contenir au moins le header des vertices et le header des triangles
    import struct
    nombre_vertices = struct.unpack('>I', flux_output[:4])[0]
    assert nombre_vertices == 4, "4 vertices uniques attendus"

# Cas 9 : Test avec points colinéaires (erreur de triangulation)
def test_triangulation_points_colineaires(client):
    """Test avec des points colinéaires qui ne peuvent pas être triangulés."""
    points = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]
    flux = encoder_pointset(points)
    client.application.point_set_manager.get_pointset.return_value = flux

    response = client.get('/triangulation/colinear_test')
    assert response.status_code == 500
    assert b'TRIANGULATION_FAILED' in response.data

# Cas 10 : Test avec grand PointSet
def test_triangulation_grand_pointset(client):
    """Test avec un grand nombre de points."""
    import math
    n = 100
    points = [(math.cos(2*math.pi*i/n), math.sin(2*math.pi*i/n)) for i in range(n)]
    flux = encoder_pointset(points)
    client.application.point_set_manager.get_pointset.return_value = flux

    response = client.get('/triangulation/large_set')
    assert response.status_code == 200
    assert len(response.data) > 0

# Cas 11 : Test avec plusieurs requêtes successives
def test_multiples_requetes_successives(client):
    """Test avec plusieurs requêtes successives pour vérifier la stabilité."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
    flux = encoder_pointset(points)

    for i in range(5):
        client.application.point_set_manager.get_pointset.return_value = flux
        response = client.get(f'/triangulation/test_{i}')
        assert response.status_code == 200

# Cas 12 : Test avec caractères spéciaux dans l'ID
def test_triangulation_id_caracteres_speciaux(client):
    """Test avec un ID contenant des caractères spéciaux."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    flux = encoder_pointset(points)
    client.application.point_set_manager.get_pointset.return_value = flux

    # ID avec caractères spéciaux (URL encodés)
    response = client.get('/triangulation/test-id_123.456')
    assert response.status_code == 200

# Cas 13 : Test sans PointSetManager configuré
def test_triangulation_sans_manager():
    """Test quand aucun PointSetManager n'est configuré."""
    app = create_app()  # Pas de manager
    app.config['TESTING'] = True

    with app.test_client() as test_client:
        response = test_client.get('/triangulation/test123')
        assert response.status_code == 503

# Cas 14 : Test avec PointSet à 3 points exacts
def test_triangulation_trois_points_exact(client):
    """Test avec exactement 3 points (cas minimum valide)."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    flux = encoder_pointset(points)
    client.application.point_set_manager.get_pointset.return_value = flux

    response = client.get('/triangulation/three_points')
    assert response.status_code == 200

    # Vérifier qu'il y a exactement 1 triangle
    import struct
    flux_output = response.data
    nombre_vertices = struct.unpack('>I', flux_output[:4])[0]
    offset_triangles = 4 + nombre_vertices * 8
    nombre_triangles = struct.unpack('>I', flux_output[offset_triangles:offset_triangles+4])[0]
    assert nombre_triangles == 1

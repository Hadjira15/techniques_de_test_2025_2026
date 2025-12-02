import pytest
from unittest.mock import MagicMock
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
    response = client.get('/triangulation/inconnu')
    assert response.status_code == 404

# Cas 3 : Requête mal formée
def test_triangulation_requete_mal_formee(client):
    # Par exemple envoyer sans ID ou avec un mauvais format
    response = client.get('/triangulation/')
    assert response.status_code == 400

import time
import pytest
from unittest.mock import MagicMock
from concurrent.futures import ThreadPoolExecutor
from triangulator.serializers import encoder_pointset
from triangulator.api import create_app

@pytest.mark.performance
def test_performance_grand_pointset():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    # Générer un grand PointSet (par ex: 1000 points)
    points = [(float(x), float(x*x % 100)) for x in range(1000)]
    flux = encoder_pointset(points)

    # Ajouter le PointSet dans l'app (simulation)
    pointset_id = "perf_test"
    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux

    # Mesurer le temps de réponse
    start = time.time()
    response = client.get(f'/triangulation/{pointset_id}')
    duration = time.time() - start

    assert response.status_code == 200
    assert duration < 1.0, f"Temps de réponse trop long : {duration:.2f}s"

def test_performance_charge():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    points = [(float(x), float(x)) for x in range(500)]
    flux = encoder_pointset(points)
    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux
    pointset_id = "charge_test"

    def requete():
        resp = client.get(f'/triangulation/{pointset_id}')
        return resp.status_code

    # Lancer 10 requêtes simultanées
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(requete, range(10)))

    # Vérifier que toutes les requêtes ont réussi
    assert all(r == 200 for r in results)

def test_performance_spike():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    points = [(float(x), float(x)) for x in range(200)]
    flux = encoder_pointset(points)
    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux
    pointset_id = "spike_test"

    def requete():
        return client.get(f'/triangulation/{pointset_id}').status_code

    # Envoi soudain de 50 requêtes simultanées
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(requete, range(50)))

    # Vérifier que toutes les réponses sont 200
    assert all(r == 200 for r in results)

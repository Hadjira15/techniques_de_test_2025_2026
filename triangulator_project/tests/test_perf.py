"""Tests de performance du service de triangulation."""

import time
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import MagicMock

import pytest
from triangulator.api import create_app
from triangulator.serializers import encoder_pointset


@pytest.mark.performance
def test_performance_petit_pointset():
    """Test avec un petit PointSet (10 points)."""
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    points = [(float(x), float(x*x % 10)) for x in range(10)]
    flux = encoder_pointset(points)

    pointset_id = "perf_petit"
    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux

    start = time.time()
    response = client.get(f'/triangulation/{pointset_id}')
    duration = time.time() - start

    assert response.status_code == 200
    assert duration < 0.1, f"Temps de réponse trop long pour 10 points : {duration:.3f}s"


@pytest.mark.performance
def test_performance_moyen_pointset():
    """Test avec un PointSet moyen (100 points)."""
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    points = [(float(x), float(x*x % 100)) for x in range(100)]
    flux = encoder_pointset(points)

    pointset_id = "perf_moyen"
    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux

    start = time.time()
    response = client.get(f'/triangulation/{pointset_id}')
    duration = time.time() - start

    assert response.status_code == 200
    assert duration < 0.5, f"Temps de réponse trop long pour 100 points : {duration:.3f}s"


@pytest.mark.performance
def test_performance_grand_pointset():
    """Test avec un grand PointSet (1000 points)."""
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    points = [(float(x), float(x*x % 100)) for x in range(1000)]
    flux = encoder_pointset(points)

    pointset_id = "perf_test"
    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux

    start = time.time()
    response = client.get(f'/triangulation/{pointset_id}')
    duration = time.time() - start

    assert response.status_code == 200
    assert duration < 2.0, f"Temps de réponse trop long pour 1000 points : {duration:.3f}s"


@pytest.mark.performance
def test_performance_tres_grand_pointset():
    """Test avec un très grand PointSet (5000 points)."""
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    points = [(float(x), float(x*x % 200)) for x in range(5000)]
    flux = encoder_pointset(points)

    pointset_id = "perf_tres_grand"
    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux

    start = time.time()
    response = client.get(f'/triangulation/{pointset_id}')
    duration = time.time() - start

    assert response.status_code == 200
    assert duration < 30.0, f"Temps de réponse trop long pour 5000 points : {duration:.3f}s"


@pytest.mark.performance
def test_performance_charge():
    """Test de charge avec 10 requêtes simultanées."""
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    points = [(float(x), float(x % 100)) for x in range(500)]
    flux = encoder_pointset(points)
    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux
    pointset_id = "charge_test"

    def requete(_):
        resp = client.get(f'/triangulation/{pointset_id}')
        return resp.status_code

    # Lancer 10 requêtes simultanées
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(requete, range(10)))

    # Vérifier que toutes les requêtes ont réussi
    assert all(r == 200 for r in results)


@pytest.mark.performance
def test_performance_charge_lourde():
    """Test de charge lourde avec 50 requêtes simultanées."""
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    points = [(float(x), float(x % 100)) for x in range(300)]
    flux = encoder_pointset(points)
    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux
    pointset_id = "charge_lourde"

    def requete(_):
        resp = client.get(f'/triangulation/{pointset_id}')
        return resp.status_code

    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(requete, range(50)))

    assert all(r == 200 for r in results)


@pytest.mark.performance
def test_performance_spike():
    """Test spike: montée brutale de 0 à 50 requêtes."""
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    points = [(float(x), float((x*x) % 100)) for x in range(200)]
    flux = encoder_pointset(points)
    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux
    pointset_id = "spike_test"

    def requete(_):
        return client.get(f'/triangulation/{pointset_id}').status_code

    # Envoi soudain de 50 requêtes simultanées
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(requete, range(50)))

    assert all(r == 200 for r in results)


@pytest.mark.performance
def test_performance_latence_moyenne():
    """Test de latence moyenne sur 20 requêtes séquentielles."""
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    points = [(float(x), float(x % 50)) for x in range(200)]
    flux = encoder_pointset(points)
    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux

    durations = []
    for i in range(20):
        start = time.time()
        response = client.get(f'/triangulation/latence_{i}')
        duration = time.time() - start
        durations.append(duration)
        assert response.status_code == 200

    latence_moyenne = sum(durations) / len(durations)
    assert latence_moyenne < 0.5, f"Latence moyenne trop élevée : {latence_moyenne:.3f}s"


@pytest.mark.performance
def test_performance_throughput():
    """Test de throughput: nombre de requêtes par seconde."""
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    points = [(float(x), float(x % 50)) for x in range(100)]
    flux = encoder_pointset(points)
    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux

    start = time.time()
    nb_requetes = 50
    for i in range(nb_requetes):
        response = client.get(f'/triangulation/throughput_{i}')
        assert response.status_code == 200

    duration = time.time() - start
    throughput = nb_requetes / duration

    assert throughput > 10, f"Throughput trop faible : {throughput:.2f} req/s"


@pytest.mark.performance
def test_performance_points_en_cercle():
    """Test de performance avec points disposés en cercle."""
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    import math
    n = 500
    points = [(math.cos(2*math.pi*i/n), math.sin(2*math.pi*i/n)) for i in range(n)]
    flux = encoder_pointset(points)

    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux

    start = time.time()
    response = client.get('/triangulation/cercle')
    duration = time.time() - start

    assert response.status_code == 200
    assert duration < 1.5, f"Triangulation du cercle trop lente : {duration:.3f}s"


@pytest.mark.performance
def test_performance_points_en_grille():
    """Test de performance avec points sur une grille."""
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    # Grille 20x20 = 400 points
    points = [(float(x), float(y)) for x in range(20) for y in range(20)]
    flux = encoder_pointset(points)

    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux

    start = time.time()
    response = client.get('/triangulation/grille')
    duration = time.time() - start

    assert response.status_code == 200
    assert duration < 1.0, f"Triangulation de la grille trop lente : {duration:.3f}s"


@pytest.mark.performance
def test_performance_points_aleatoires():
    """Test de performance avec points aléatoires."""
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    import random
    random.seed(42)
    points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(500)]
    flux = encoder_pointset(points)

    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux

    start = time.time()
    response = client.get('/triangulation/aleatoire')
    duration = time.time() - start

    assert response.status_code == 200
    assert duration < 1.5, f"Triangulation aléatoire trop lente : {duration:.3f}s"


@pytest.mark.performance
def test_performance_stabilite_sous_charge():
    """Test de stabilité: 100 requêtes successives."""
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    points = [(float(x), float(x % 50)) for x in range(150)]
    flux = encoder_pointset(points)
    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux

    erreurs = 0
    for i in range(100):
        response = client.get(f'/triangulation/stabilite_{i}')
        if response.status_code != 200:
            erreurs += 1

    assert erreurs == 0, f"{erreurs} erreurs sur 100 requêtes"


@pytest.mark.performance
def test_performance_montee_en_charge_progressive():
    """Test de montée en charge progressive (1, 5, 10, 20 workers)."""
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    points = [(float(x), float(x % 50)) for x in range(200)]
    flux = encoder_pointset(points)
    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux

    def requete(_):
        return client.get('/triangulation/montee').status_code

    for nb_workers in [1, 5, 10, 20]:
        with ThreadPoolExecutor(max_workers=nb_workers) as executor:
            results = list(executor.map(requete, range(nb_workers)))
        assert all(r == 200 for r in results), f"Erreur avec {nb_workers} workers"


@pytest.mark.performance
def test_performance_resistance_stress():
    """Test de résistance: 200 requêtes avec 100 workers."""
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    points = [(float(x), float(x % 50)) for x in range(100)]
    flux = encoder_pointset(points)
    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux

    def requete(_):
        return client.get('/triangulation/stress').status_code

    start = time.time()
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(requete, range(200)))
    duration = time.time() - start

    taux_reussite = sum(1 for r in results if r == 200) / len(results)
    assert taux_reussite > 0.95, f"Taux de réussite trop faible : {taux_reussite*100:.1f}%"
    assert duration < 10.0, f"Test de stress trop long : {duration:.2f}s"


@pytest.mark.performance
def test_performance_recuperation_apres_pic():
    """Test de récupération après un pic de charge."""
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    points = [(float(x), float(x % 50)) for x in range(150)]
    flux = encoder_pointset(points)
    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux

    def requete(_):
        return client.get('/triangulation/recuperation').status_code

    # Pic de charge
    with ThreadPoolExecutor(max_workers=50) as executor:
        _results_pic = list(executor.map(requete, range(50)))

    # Requêtes normales après le pic
    time.sleep(0.1)
    results_apres = []
    for i in range(10):
        response = client.get(f'/triangulation/apres_pic_{i}')
        results_apres.append(response.status_code)

    assert all(r == 200 for r in results_apres), "Service non récupéré après le pic"


@pytest.mark.performance
def test_performance_polygone_convexe():
    """Test de performance avec un polygone convexe (cercle)."""
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    import math
    n = 300
    points = [(math.cos(2*math.pi*i/n)*10, math.sin(2*math.pi*i/n)*10) for i in range(n)]
    flux = encoder_pointset(points)

    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux

    start = time.time()
    response = client.get('/triangulation/convexe')
    duration = time.time() - start

    assert response.status_code == 200
    assert duration < 0.8, f"Polygone convexe trop lent : {duration:.3f}s"


@pytest.mark.performance
def test_performance_polygone_concave_complexe():
    """Test de performance avec un polygone concave complexe (étoile)."""
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    import math
    # Étoile à 50 branches
    points = []
    for i in range(100):
        angle = 2 * math.pi * i / 100
        radius = 10 if i % 2 == 0 else 5
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append((x, y))

    flux = encoder_pointset(points)
    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux

    start = time.time()
    response = client.get('/triangulation/etoile_complexe')
    duration = time.time() - start

    assert response.status_code == 200
    assert duration < 1.0, f"Étoile complexe trop lente : {duration:.3f}s"


@pytest.mark.performance
def test_performance_temps_encodage_decodage():
    """Test du temps d'encodage et décodage des résultats."""
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    points = [(float(x), float(x % 50)) for x in range(500)]

    start_encode = time.time()
    flux = encoder_pointset(points)
    temps_encodage = time.time() - start_encode

    client.application.point_set_manager = MagicMock()
    client.application.point_set_manager.get_pointset.return_value = flux

    start_total = time.time()
    response = client.get('/triangulation/encodage_test')
    temps_total = time.time() - start_total

    assert response.status_code == 200
    assert temps_encodage < 0.1, f"Encodage trop lent : {temps_encodage:.3f}s"
    assert temps_total < 1.5, f"Traitement total trop lent : {temps_total:.3f}s"

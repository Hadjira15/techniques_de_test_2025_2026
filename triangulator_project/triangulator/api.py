"""Module API Flask pour le service de triangulation."""

from flask import Flask, Response, jsonify

from triangulator.core import triangulate
from triangulator.exceptions import ErreurDecodage, ErreurTriangulation
from triangulator.serializers import decoder_pointset, encoder_triangles


def create_app(point_set_manager=None):
    """Crée et configure l'application Flask.

    :param point_set_manager: Instance du client PointSetManager
        (optionnel pour les tests)
    :return: Application Flask configurée
    """
    app = Flask(__name__)

    # Stocker le PointSetManager dans l'app pour le rendre accessible
    if point_set_manager is not None:
        app.point_set_manager = point_set_manager

    @app.route('/triangulation/<pointset_id>', methods=['GET'])
    def get_triangulation(pointset_id):
        """Endpoint pour calculer la triangulation d'un PointSet.

        :param pointset_id: L'ID du PointSet à trianguler
        :return: Flux binaire contenant les triangles ou erreur JSON
        """
        # Validation : vérifier que l'ID n'est pas vide
        if not pointset_id or pointset_id.strip() == '':
            return jsonify({
                'code': 'INVALID_ID',
                'message': 'PointSetID invalide ou vide'
            }), 400

        try:
            # Récupérer le PointSet depuis le PointSetManager
            if not hasattr(app, 'point_set_manager') or app.point_set_manager is None:
                return jsonify({
                    'code': 'SERVICE_UNAVAILABLE',
                    'message': 'PointSetManager non disponible'
                }), 503

            # Appeler le PointSetManager pour récupérer le flux binaire
            flux_binaire = app.point_set_manager.get_pointset(pointset_id)

            if flux_binaire is None:
                return jsonify({
                    'code': 'NOT_FOUND',
                    'message': f'PointSet avec ID {pointset_id} non trouvé'
                }), 404

        except Exception as e:
            return jsonify({
                'code': 'SERVICE_UNAVAILABLE',
                'message': (
                    f'Erreur lors de la communication avec PointSetManager: {str(e)}'
                )
            }), 503

        try:
            # Décoder le flux binaire en liste de points
            points = decoder_pointset(flux_binaire)
        except ErreurDecodage as e:
            return jsonify({
                'code': 'INVALID_POINTSET',
                'message': f'Erreur lors du décodage du PointSet: {str(e)}'
            }), 400

        try:
            # Calculer la triangulation
            triangles = triangulate(points)
        except ErreurTriangulation as e:
            return jsonify({
                'code': 'TRIANGULATION_FAILED',
                'message': f'Erreur lors de la triangulation: {str(e)}'
            }), 500

        try:
            # Encoder le résultat en format binaire Triangles
            flux_resultat = encoder_triangles(triangles)
        except Exception as e:
            return jsonify({
                'code': 'ENCODING_FAILED',
                'message': f'Erreur lors de l\'encodage du résultat: {str(e)}'
            }), 500

        # Retourner le flux binaire
        return Response(flux_resultat, mimetype='application/octet-stream'), 200

    @app.route('/triangulation/', methods=['GET'])
    def get_triangulation_sans_id():
        """Endpoint pour gérer les requêtes mal formées (sans ID).

        :return: Erreur JSON
        """
        return jsonify({
            'code': 'BAD_REQUEST',
            'message': 'PointSetID requis dans l\'URL'
        }), 400

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)

"""Module contenant les exceptions personnalisées du triangulator."""


class ErreurTriangulation(Exception):
    """Exception levée lorsque la triangulation ne peut pas être effectuée."""

    pass


class ErreurDecodage(Exception):
    """Exception levée lorsque le décodage d'un flux binaire échoue."""

    pass

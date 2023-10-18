from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


class SchemaView(SpectacularAPIView):
    """Получение текущей схемы OPEN API"""

    throttle_classes = []
    pass


class SwaggerView(SpectacularSwaggerView):
    """Документация на основе схемы OPEN API"""

    throttle_classes = []
    pass

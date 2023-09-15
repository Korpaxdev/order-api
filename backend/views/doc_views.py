from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


class SchemaView(SpectacularAPIView):
    """Класс представления для схемы OPEN API"""

    throttle_classes = []
    pass


class SwaggerView(SpectacularSwaggerView):
    """Класс представления документации на основе схемы OPEN API"""

    throttle_classes = []
    pass

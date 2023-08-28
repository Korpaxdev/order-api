from backend.models import ProductModel


def get_cats_names(instance: ProductModel) -> list[str]:
    """Возвращает список из имен категорий модели ProductModel"""
    return [cat.name for cat in instance.categories.all()]

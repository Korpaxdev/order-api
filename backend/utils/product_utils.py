from backend.models import ProductModel


def get_cats_names(instance: ProductModel):
    return [cat.name for cat in instance.categories.all()]

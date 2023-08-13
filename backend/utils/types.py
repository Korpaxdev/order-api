from typing import Optional, TypedDict


class FixturesPathsType(TypedDict):
    product: str
    product_param: str


class ProductType(TypedDict):
    name: str
    categories: list[str]
    description: Optional[str]
    quantity: int
    price: int
    price_rrc: int
    params: Optional[list[dict]]


class ProductFieldType(TypedDict):
    name: str
    validation: list[str]

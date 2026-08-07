"""Product data-access operations."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Product


def list_products(db: Session, skip: int, limit: int) -> list[Product]:
    return list(db.scalars(select(Product).order_by(Product.id).offset(skip).limit(limit)))


def get_product(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)

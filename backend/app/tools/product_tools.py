"""Read-only product tools for accurate feature and version answers."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Product
from app.services.product_service import get_product
from app.tools.errors import ToolNotFoundError
from app.tools.schemas import ProductListInput, ProductLookupInput, ProductToolOutput


def _product_output(product: Product) -> ProductToolOutput:
    return ProductToolOutput(product_id=product.id, name=product.name, description=product.description,
                             version=product.version, is_active=product.is_active)


def get_product_tool(db: Session, tool_input: ProductLookupInput) -> ProductToolOutput:
    """Retrieve one product's supported version and feature description."""
    product = get_product(db, tool_input.product_id)
    if product is None:
        raise ToolNotFoundError(f"Product {tool_input.product_id} was not found.")
    return _product_output(product)


def list_products_tool(db: Session, tool_input: ProductListInput) -> list[ProductToolOutput]:
    """List the products available to support, optionally including retired products."""
    statement = select(Product).order_by(Product.name).limit(tool_input.limit)
    if tool_input.active_only:
        statement = statement.where(Product.is_active.is_(True))
    return [_product_output(product) for product in db.scalars(statement)]

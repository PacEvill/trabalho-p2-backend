from sqlalchemy.orm import Session
from app import models, schemas

def get_product(db: Session, product_id: int):
    """
    Busca um produto pelo seu ID.
    """
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    """
    Busca uma lista de produtos com paginação.
    """
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    """
    Cria e persiste um novo produto no banco.
    """
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    """
    Atualiza um produto existente. Retorna o produto atualizado ou None se não encontrado.
    """
    db_product = get_product(db, product_id)
    if db_product is None:
        return None
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.stock = product.stock
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int) -> bool:
    """
    Deleta um produto pelo ID. Retorna True se deletado ou False se não existia.
    """
    db_product = get_product(db, product_id)
    if db_product is None:
        return False
    db.delete(db_product)
    db.commit()
    return True

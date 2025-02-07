from dao.productDAO import ProductDAO
from models.Product import Product
import sqlite3

class ProductService:
    def __init__(self):
        self.productDAO = ProductDAO()

    def create_product(self, product):
        return self.productDAO.create_product(product)

    def delete_product(self, productID):
        self.productDAO.delete_product(productID)

    def get_all_products(self):
        return self.productDAO.get_all_products()

    def get_product_by_id(self, productID):
        return self.productDAO.get_product_by_id(productID)

    def get_product_by_type(self, type):
        return self.productDAO.get_products_by_type(type)

    def update_product(self, product):
        return self.productDAO.update_product(product)
"""
productName, price, type, gender=None, movable=None, isMirror=None, character=None,
hasColour=None, dimensions=None, material=None, scale=None, isLimited=None, description=None,
image_blob=None):
        # Create a Product object with the provided attributes
        product = Product(
            productID=None,
            productName=productName,
            price=price,
            type=type,
            gender=gender,
            movable=movable,
            isMirror=isMirror,
            character=character,
            hasColour=hasColour,
            dimensions=dimensions,
            material=material,
            scale=scale,
            isLimited=isLimited,
            description=description,
            image_blob=image_blob)
        self.productDAO.create_product(product)
"""


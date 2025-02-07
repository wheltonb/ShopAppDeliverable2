from dao.productDAO import ProductDAO
from models.Product import Product
import sqlite3

class ProductService:
    def __init__(self):
        self.productDAO = ProductDAO()

    def create_product(self, productName, price, type, gender=None, movable=None, isMirror=None, character=None,
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


    def delete_product(self, productID):
        self.productDAO.delete_product(productID)


    def get_all_products(self):
        products = []
        cursor = self.productDAO.conn.execute("SELECT * FROM products")
        for row in cursor.fetchall():
            product = Product(*row)  # Convert each row into a Product object
            products.append(product)
        return products


    def get_product_by_id(self, productID):
        return self.productDAO.get_product_by_id(productID)



    def get_product_by_type(self, productType):
        sql = '''SELECT * FROM products WHERE type = ?'''
        cursor = self.productDAO.conn.execute(sql, (productType,))
        products = []
        for row in cursor.fetchall():
            product = Product(*row)  # Convert each row into a Product object
            products.append(product)
        return products


    def update_product(self, productID, productName=None, price=None, type=None, gender=None, movable=None,
                       isMirror=None, character=None, hasColour=None, dimensions=None, material=None, scale=None,
                       isLimited=None, description=None, image_blob=None):
        existing_product = self.productDAO.get_product_by_id(productID)
        if not existing_product:
            return None  # Product does not exist

        # Update only the fields that are provided (non-None values)
        updated_product = Product(
            productID=productID,  # Keep the same product ID
            productName=productName if productName is not None else existing_product.productName,
            price=price if price is not None else existing_product.price,
            type=type if type is not None else existing_product.type,
            gender=gender if gender is not None else existing_product.gender,
            movable=movable if movable is not None else existing_product.movable,
            isMirror=isMirror if isMirror is not None else existing_product.isMirror,
            character=character if character is not None else existing_product.character,
            hasColour=hasColour if hasColour is not None else existing_product.hasColour,
            dimensions=dimensions if dimensions is not None else existing_product.dimensions,
            material=material if material is not None else existing_product.material,
            scale=scale if scale is not None else existing_product.scale,
            isLimited=isLimited if isLimited is not None else existing_product.isLimited,
            description=description if description is not None else existing_product.description,
            image_blob=image_blob if image_blob is not None else existing_product.image_blob
        )
        self.productDAO.update_product(updated_product)
        return updated_product
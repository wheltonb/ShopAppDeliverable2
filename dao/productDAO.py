from models.Product import Product
import sqlite3
class ProductDAO:
    def __init__(self):
        db_file = 'shop.db'
        self.conn = sqlite3.connect(db_file)

    def create_product(self, product):
        sql = '''INSERT INTO products (productName, price, type, gender, movable, isMirror, character, hasColour, dimensions, material, scale, isLimited, description, image_blob)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        self.conn.execute(sql, (
            product.productName, product.price, product.type, product.gender, product.movable,
            product.isMirror, product.character, product.hasColour, product.dimensions, product.material,
            product.scale, product.isLimited, product.description, product.image_blob
        ))
        self.conn.commit()
        self.conn.close()


    def get_all_products(self):
        sql = '''SELECT * FROM products '''
        cursor = self.conn.execute(sql)
        row = cursor.fetchall()
        products = []
        if row:
            for row in row:
                product = Product(*row)  # Assuming the Product constructor takes the values in the row
                products.append(product)
        return products

    def get_product_by_id(self, productID):
        sql = '''SELECT * FROM products WHERE productID = ?'''
        cursor = self.conn.execute(sql, (productID,))
        row = cursor.fetchone()
        if row:
            return Product(*row)
        self.conn.close()
        return None

    def update_product(self, product):
        sql = '''UPDATE products
                 SET productName = ?, price = ?, type = ?, gender = ?, movable = ?, isMirror = ?, character = ?, hasColour = ?, dimensions = ?, material = ?, scale = ?, isLimited = ?, description = ?, image_blob = ?
                 WHERE productID = ?'''
        self.conn.execute(sql, (
            product.productName, product.price, product.type, product.gender, product.movable,
            product.isMirror, product.character, product.hasColour, product.dimensions, product.material,
            product.scale, product.isLimited, product.description, product.image_blob, product.productID
        ))
        self.conn.commit()
        self.conn.close()

    def delete_product(self, productID):
        sql = '''DELETE FROM products WHERE productID = ?'''
        self.conn.execute(sql, (productID,))
        self.conn.commit()
        self.conn.close()

    def get_products_by_type(self, type):
        sql = '''SELECT * FROM products WHERE type = ?'''
        cursor = self.conn.execute(sql, (type,))
        row = cursor.fetchall()
        products = []
        if row:
            for row in row:
                product = Product(*row)  # Assuming the Product constructor takes the values in the row
                products.append(product)
        return products
        self.conn.commit()
        self.conn.close()



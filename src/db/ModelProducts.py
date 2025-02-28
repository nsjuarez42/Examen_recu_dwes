from entities.Product import Product
class ModelProducts():

    @classmethod 
    def get_all(cls,db):

        cursor = db.cursor()

        cursor.execute("SELECT * FROM products")
        
        products = cursor.fetchall()
        print(products)
        product_obj =[]

        if len(products) == 0:
            return products

        for product in products:
            product_obj.append(Product(product[0],product[1],product[2],product[3]))
        print(product_obj)
        return product_obj

        
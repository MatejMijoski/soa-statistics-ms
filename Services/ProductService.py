from Repository.ProductRepository import ProductRepository


class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()

    def update_product(self, invoice_body):
        return self.product_repository.update_product_counter(invoice_body['product_id'],
                                                              invoice_body['quantity'])

    def get_top_monthly_products(self, limit):
        return self.product_repository.get_top_monthly_products(limit)

    def get_end_monthly_products(self, limit):
        return self.product_repository.get_end_monthly_products(limit)

    def get_top_yearly_products(self, limit):
        return self.product_repository.get_top_yearly_products(limit)

    def get_end_yearly_products(self, limit):
        return self.product_repository.get_end_yearly_products(limit)

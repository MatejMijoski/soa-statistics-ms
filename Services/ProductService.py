from Repository.ProductRepository import ProductRepository


class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()

    def update_product(self, invoice_body):
        return self.product_repository.update_product_counter(invoice_body['product_id'],
                                                              invoice_body['quantity'])

    def get_monthly_score(self, limit):
        return self.product_repository.get_monthly_score(limit)

    def get_yearly_score(self, limit):
        return self.product_repository.get_yearly_score(limit)
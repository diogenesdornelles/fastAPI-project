from services import ClientsService, ProductsService


class RemoveController:
    def __init__(self):
        self.service_clients: ClientsService = ClientsService()
        self.service_products: ProductsService = ProductsService()

    def remove_photo_client(self, client_id: str, photo_url: str):
        self.service_clients.get_one_by_id(client_id)
        self.service_clients.remove_photo_from_client(photo_url)
        return self.service_clients.delete_photo_result

    def remove_photo_product(self, product_id: str, photo_url: str):
        self.service_products.get_one_by_id(product_id)
        self.service_products.remove_photo_from_product(photo_url)
        return self.service_products.delete_photo_result

from services import ClientsService, ProductsService


class UploadsController:
    def __init__(self):
        self.service_clients: ClientsService = ClientsService()
        self.service_products: ProductsService = ProductsService()

    def upload_photo_client(self, client_id: str, photo_url: str):
        self.service_clients.get_one_by_id(client_id)
        self.service_clients.insert_photo(photo_url)
        return self.service_clients.insert_new_photo_result

    def upload_photo_product(self, product_id: str, photo_url: str):
        self.service_products.get_one_by_id(product_id)
        self.service_products.insert_photo(photo_url)
        return self.service_products.insert_new_photo_result

    def remove_photo_client(self, client_id: str, photo_url: str):
        self.service_clients.get_one_by_id(client_id)
        self.service_clients.remove_photo(photo_url)
        return self.service_clients.insert_new_photo_result

    def remove_photo_product(self, product_id: str, photo_url: str):
        self.service_products.get_one_by_id(product_id)
        self.service_products.remove_photo(photo_url)
        return self.service_products.insert_new_photo_result

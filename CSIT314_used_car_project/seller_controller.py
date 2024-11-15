from seller import Seller

class SellerController:
    def __init__(self):
        # Initialize the Seller entity
        self.seller_entity = Seller()

    def manage_seller_listings(self, seller_id):

        # Retrieve the seller's car listings
        return self.seller_entity.get_seller_listings(seller_id)

class TrackViewsController:
    def __init__(self):
        # Initialize the Seller entity
        self.seller_entity = Seller()
    def get_view_count(self, car_id):
        return self.seller_entity.get_view_count(car_id)
class TrackShortlistsController:
    def __init__(self):
        # Initialize the Seller entity
        self.seller_entity = Seller()
    def get_shortlist_count(self, car_id):
        return self.seller_entity.get_shortlist_count(car_id)


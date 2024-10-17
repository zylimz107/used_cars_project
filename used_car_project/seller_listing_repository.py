# repositories/seller_listing_repository.py
from base_repository import BaseRepository

class SellerListingRepository(BaseRepository):
    def get_seller_listings(self, seller_id):
        query = '''
            SELECT uc.*, 
                   (SELECT COUNT(*) FROM shortlist WHERE car_id = uc.car_id) AS short_count
            FROM used_cars uc
            WHERE seller_id = ?
        '''
        return self.fetch_all(query, (seller_id,))

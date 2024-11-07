from base_repository import BaseRepository


class Seller(BaseRepository):
    def get_seller_listings(self, seller_id):
        query = '''
            SELECT *
            FROM used_cars
            WHERE seller_id = ?
        '''
        return self.fetch_all(query, (seller_id,))
    
    def get_view_count(self, car_id):
        query = 'SELECT view_count FROM used_cars WHERE car_id = ?'
        result = self.fetch_one(query, (car_id,))
        return result['view_count'] if result else 0
    
    def get_shortlist_count(self, car_id):
        query = '''
            SELECT COUNT(*) AS short_count
            FROM shortlist
            WHERE car_id = ?
        '''
        result = self.fetch_one(query, (car_id,))
        return result['short_count'] if result else 0
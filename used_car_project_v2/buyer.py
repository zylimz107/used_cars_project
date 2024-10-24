from base_repository import BaseRepository
from used_car import UsedCar

class Buyer(BaseRepository):
    def search_listings(self, search_term=None):
        if search_term:
            query = '''
                SELECT * FROM used_cars 
                WHERE make LIKE ? OR model LIKE ? OR year LIKE ? OR agent_id LIKE ?
            '''
            like_term = f'%{search_term}%'
            return self.fetch_all(query, (like_term, like_term, like_term, like_term))
        else:
            query = 'SELECT * FROM used_cars'
            return self.fetch_all(query)

    def get_car_by_id(self, car_id):
        return UsedCar().get_car_by_id(car_id)

    def increment_view_count(self, car_id):
        query = 'UPDATE used_cars SET view_count = view_count + 1 WHERE car_id = ?'
        self.execute_query(query, (car_id,))

    def add_to_shortlist(self, buyer_id, car_id):
        query = '''INSERT INTO shortlist (buyer_id, car_id) VALUES (?, ?)'''
        self.execute_query(query, (buyer_id, car_id))

    def get_shortlist(self, buyer_id):
        query = '''
            SELECT uc.* FROM used_cars uc 
            JOIN shortlist s ON uc.car_id = s.car_id 
            WHERE s.buyer_id = ?
        '''
        return self.fetch_all(query, (buyer_id,))

    def search_shortlist(self, buyer_id, search_term):
        query = '''
            SELECT uc.* FROM used_cars uc 
            JOIN shortlist s ON uc.car_id = s.car_id 
            WHERE s.buyer_id = ? AND (uc.make LIKE ? OR uc.model LIKE ?)
        '''
        like_term = f'%{search_term}%'
        return self.fetch_all(query, (buyer_id, like_term, like_term))
    
    def get_all_cars(self):
        return UsedCar().get_all_cars

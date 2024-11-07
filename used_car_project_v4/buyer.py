from base_repository import BaseRepository

class Buyer(BaseRepository):
    def view_listing(self, car_id):
        increment_query = 'UPDATE used_cars SET view_count = view_count + 1 WHERE car_id = ?'
        self.execute_query(increment_query, (car_id,))
        query = 'SELECT * FROM used_cars WHERE car_id = ?'
        return self.fetch_one(query, (car_id,))

    def add_to_shortlist(self, buyer_id, car_id):
        check_query = 'SELECT * FROM shortlist WHERE car_id = ?'
        current_car = self.fetch_one(check_query, (car_id,))
        if current_car:
            return False
        query = '''INSERT INTO shortlist (buyer_id, car_id) VALUES (?, ?)'''
        self.execute_query(query, (buyer_id, car_id))
        return True

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
    
    def loan_calculator(self, car_id):
        query = 'SELECT * FROM used_cars WHERE car_id = ?'
        return self.fetch_one(query, (car_id,))

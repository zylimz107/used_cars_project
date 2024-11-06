from base_repository import BaseRepository

class Buyer(BaseRepository):
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

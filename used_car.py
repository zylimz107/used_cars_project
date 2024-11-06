from base_repository import BaseRepository

class UsedCar(BaseRepository):
    def get_all_cars(self):
        query = 'SELECT * FROM used_cars'
        return self.fetch_all(query)

    def get_car_by_id(self, car_id):
        query = 'SELECT * FROM used_cars WHERE car_id = ?'
        return self.fetch_one(query, (car_id,))

    def create_car(self, make, model, year, price, description, agent_id, seller_id):
        query = '''
            INSERT INTO used_cars (make, model, year, price, description, agent_id, seller_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        self.execute_query(query, (make, model, year, price, description, agent_id, seller_id))

    def update_car(self, car_id, make, model, year, price, description, seller_id):
        query = '''
            UPDATE used_cars 
            SET make = ?, model = ?, year = ?, price = ?, description = ?, seller_id = ? 
            WHERE car_id = ?
        '''
        self.execute_query(query, (make, model, year, price, description, seller_id, car_id))


    def delete_car(self, car_id):
        query = 'DELETE FROM used_cars WHERE car_id = ?'
        self.execute_query(query, (car_id,))

    def search_cars(self, search_term=None):
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
    
    def get_active_sellers(self):
        query = '''
            SELECT ua.id, ua.name 
            FROM user_accounts ua
            INNER JOIN user_profiles up ON ua.profile_id = up.profile_id
            WHERE up.role = 'seller' AND ua.status = 'active'
        '''
        return self.fetch_all(query)
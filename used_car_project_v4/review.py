from base_repository import BaseRepository

class Review(BaseRepository):
    def get_reviews_by_agent(self, agent_id):
        query = '''
            SELECT r.rating, r.review, u.name AS reviewer
            FROM reviews r
            JOIN user_accounts u ON r.user_id = u.id
            WHERE r.agent_id = ?
        '''
        return self.fetch_all(query, (agent_id,))

    def submit_review(self, agent_id, user_id, rating, review):
        query = '''
            INSERT INTO reviews (agent_id, user_id, rating, review) 
            VALUES (?, ?, ?, ?)
        '''
        self.execute_query(query, (agent_id, user_id, rating, review))

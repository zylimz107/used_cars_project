from base_repository import BaseRepository

class UserProfile(BaseRepository):
    def get_all_profiles(self):
        query = 'SELECT * FROM user_profiles'
        return self.fetch_all(query)

    def get_profile_by_id(self, profile_id):
        query = 'SELECT * FROM user_profiles WHERE profile_id = ?'
        return self.fetch_one(query, (profile_id,))
    
    def get_profile_by_role(self, role):
        query = 'SELECT * FROM user_profiles WHERE role = ?'
        return self.fetch_one(query, (role,))

    def create_profile(self, role, status):
        query = 'INSERT INTO user_profiles (role, status) VALUES (?, ?)'
        self.execute_query(query, (role, status))

    def update_profile(self, profile_id, role, status):
        query = 'UPDATE user_profiles SET role = ?, status = ? WHERE profile_id = ?'
        self.execute_query(query, (role, status, profile_id))

    def suspend_profile(self, profile_id):
        query = 'UPDATE user_profiles SET status = "suspended" WHERE profile_id = ?'
        self.execute_query(query, (profile_id,))

    def search_profiles(self, role):
        query = 'SELECT * FROM user_profiles WHERE role LIKE ?'
        return self.fetch_all(query, (f'%{role}%',))
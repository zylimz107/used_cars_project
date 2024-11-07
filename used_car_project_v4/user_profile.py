from base_repository import BaseRepository

class UserProfile(BaseRepository):
    def get_all_profiles(self):
        query = 'SELECT * FROM user_profiles'
        return self.fetch_all(query)

    def create_profile(self, role, status, description):
        # Check if a profile with the same role already exists
        check_query = 'SELECT * FROM user_profiles WHERE role = ?'
        existing_profile = self.fetch_one(check_query, (role,))
        if existing_profile:
            return False  # Role already exists

        # Proceed with profile creation
        query = 'INSERT INTO user_profiles (role, status, description) VALUES (?, ?,?)'
        self.execute_query(query, (role, status, description))
        return True

    def update_profile(self, profile_id, role, status, description):
        # Check if a profile with the updated role already exists
        check_query = 'SELECT * FROM user_profiles WHERE role = ?'
        existing_profile = self.fetch_one(check_query, (role,))
        if existing_profile and existing_profile['profile_id'] != profile_id:
            return False  # Role already exists for a different profile

        # Update profile if no conflicts
        query = 'UPDATE user_profiles SET role = ?, status = ?, description = ? WHERE profile_id = ?'
        self.execute_query(query, (role, status, description, profile_id))
        return True


    def suspend_profile(self, profile_id):

            # Check if the account is already suspended
        check_query = 'SELECT status FROM user_profiles WHERE profile_id = ?'
        current_status = self.fetch_one(check_query, (profile_id,))

        if current_status and current_status["status"] == "suspended":
            return False  # Account is already suspended

        query = 'UPDATE user_profiles SET status = "suspended" WHERE profile_id = ?'
        self.execute_query(query, (profile_id,))
        return True

    def search_profiles(self, search_term):
        query = 'SELECT * FROM user_profiles WHERE role LIKE ?'
        return self.fetch_all(query, (f'%{search_term}%',))
    
    def get_active_profiles(self):
        query = 'SELECT * FROM user_profiles WHERE status = "active"'
        return self.fetch_all(query)
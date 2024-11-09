from base_repository import BaseRepository

class UserAccount(BaseRepository):
    def view_accounts(self):
        query = '''
            SELECT ua.*, up.role 
            FROM user_accounts ua 
            LEFT JOIN user_profiles up ON ua.profile_id = up.profile_id
        '''
        return self.fetch_all(query)
    
    def create_account(self, id, name, password, email, profile_id, status):
        # Check if the user already exists in the Entity itself
        check_query = '''
            SELECT * FROM user_accounts 
            WHERE id = ? OR email = ?
        '''
        existing_user = self.fetch_one(check_query, (id, email))
        if existing_user:
            return False  # User exists, account creation fails

        # Insert the new account
        query = '''
        INSERT INTO user_accounts (id, name, password, email, profile_id, status) 
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.execute_query(query, (id, name, password, email, profile_id, status))
        return True  # Account created successfully


    def update_account(self, id, name, password, email, profile_id, status, old_id):
        check_query = '''
            SELECT * FROM user_accounts 
            WHERE id = ? OR email = ?
        '''
        existing_user = self.fetch_one(check_query, (id, email))
        current_query = '''
            SELECT * FROM user_accounts 
            WHERE id = ?
        '''
        current_user = self.fetch_one(current_query, (old_id,))
        if existing_user and existing_user!=current_user: #if user exists and is not the current user then return false
            return False 
        query = '''
        UPDATE user_accounts 
        SET id = ?, name = ?, password = ?, email = ?, profile_id = ?, status = ? 
        WHERE id = ?
        '''
        self.execute_query(query, (id, name, password, email, profile_id, status, old_id))
    
        return True  


    def suspend_account(self, user_id):
        # Check if the account is already suspended
        check_query = 'SELECT status FROM user_accounts WHERE id = ?'
        current_status = self.fetch_one(check_query, (user_id,))

        if current_status and current_status["status"] == "suspended":
            return False  # Account is already suspended

        # Suspend the account
        query = 'UPDATE user_accounts SET status = "suspended" WHERE id = ?'
        self.execute_query(query, (user_id,))
        return True  # Account suspended successfully


    def search_accounts(self, search_term):
        query = '''
            SELECT ua.*, up.role 
            FROM user_accounts ua
            LEFT JOIN user_profiles up ON ua.profile_id = up.profile_id
            WHERE ua.id LIKE ?
        '''
        return self.fetch_all(query, (f'%{search_term}%',))

    def login_user(self, user_id, password):
        query = '''
            SELECT ua.*, up.role 
            FROM user_accounts ua 
            LEFT JOIN user_profiles up ON ua.profile_id = up.profile_id
            WHERE ua.id = ? AND ua.password = ? AND ua.status = "active" AND up.status = "active"
        '''
        return self.fetch_one(query, (user_id, password))
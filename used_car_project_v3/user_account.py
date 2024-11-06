from base_repository import BaseRepository

class UserAccount(BaseRepository):
    def get_all_accounts(self):
        query = '''
            SELECT ua.*, up.role 
            FROM user_accounts ua 
            LEFT JOIN user_profiles up ON ua.profile_id = up.profile_id
        '''
        return self.fetch_all(query)

    def get_account_by_id(self, user_id):
        query = 'SELECT * FROM user_accounts WHERE id = ?'
        return self.fetch_one(query, (user_id,))
    
    def get_account_by_id_or_email(self, user_id, email):
        query = '''
            SELECT * FROM user_accounts 
            WHERE id = ? OR email = ?
        '''
        return self.fetch_one(query, (user_id, email))
    
    def get_account_by_email(self, email):
        query = 'SELECT * FROM user_accounts WHERE email = ?'
        return self.fetch_one(query, (email,))
    
    def create_account(self, id, name, password, email, profile_id, status):
        query = '''
            INSERT INTO user_accounts (id, name, password, email, profile_id, status) 
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.execute_query(query, (id, name, password, email, profile_id, status))

    def update_account(self, id, name, password, email, profile_id, status, old_id):
        query = '''
            UPDATE user_accounts 
            SET id = ?, name = ?, password = ?, email = ?, profile_id = ?, status = ?
            WHERE id = ?
        '''
        self.execute_query(query, (id, name, password, email, profile_id, status, old_id))


    def suspend_account(self, user_id):
        query = 'UPDATE user_accounts SET status = "suspended" WHERE id = ?'
        self.execute_query(query, (user_id,))

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

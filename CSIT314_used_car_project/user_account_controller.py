from user_account import UserAccount

class ViewAccountController:
    def __init__(self):
        # Initialize the entities
        self.user_account_entity = UserAccount()

    def view_accounts(self):
        # Fetch and display all user accounts
       return self.user_account_entity.view_accounts()

class CreateAccountController:
    def __init__(self):
        # Initialize the entities
        self.user_account_entity = UserAccount()
    def create_account(self, account_data):

        return self.user_account_entity.create_account(
            id=account_data['id'],
            name=account_data['name'],
            password=account_data['password'],
            email=account_data['email'],
            profile_id=account_data['profile_id'],
            status=account_data['status'],
        )
class UpdateAccountController:
    def __init__(self):
        # Initialize the entities
        self.user_account_entity = UserAccount()
    def update_account(self, id, account_data):
        # Update account information using the provided data dictionary
        return self.user_account_entity.update_account(
            id=account_data['id'],
            name=account_data['name'],
            password=account_data['password'],
            email=account_data['email'],
            profile_id=account_data['profile_id'],
            status=account_data['status'],
            old_id=id
        )
        
class SuspendAccountController:
    def __init__(self):
        # Initialize the entities
        self.user_account_entity = UserAccount()
    def suspend_account(self, id):
        # Suspend the selected account
        return self.user_account_entity.suspend_account(id)

class SearchAccountController:
    def __init__(self):
        # Initialize the entities
        self.user_account_entity = UserAccount()
    def search_accounts(self, search_term):
        return self.user_account_entity.search_accounts(search_term)

class LoginController:
    def __init__(self):
        # Initialize the entities
        self.user_account_entity = UserAccount()
    def login(self, user_id, password):
        # Attempt to log in with the provided credentials
        return self.user_account_entity.login_user(
            user_id=user_id,
            password=password
        )    

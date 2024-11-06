from flask import request, session, flash, redirect, url_for, render_template
from user_account import UserAccount
from user_profile import UserProfile

class UserAccountController:
    def __init__(self):
        # Initialize the entities
        self.user_account_entity = UserAccount()
        self.user_profile_entity = UserProfile()

    def view_accounts(self):
        # Fetch and display all user accounts
        accounts = self.user_account_entity.get_all_accounts()
        return render_template('accounts.html', accounts=accounts)

    def create_account(self, request):
        profiles = self.user_profile_entity.get_all_profiles()
        if request.method == 'POST':
            try:
                # Check if user ID or email already exists before creating account
                existing_user = self.user_account_entity.get_account_by_id_or_email(
                    user_id=request.form['id'], 
                    email=request.form['email']
                )
                if existing_user:
                    flash('User ID or email already exists.', 'error')
                    return render_template('create_account.html', profiles=profiles)

                # Create the new account
                self.user_account_entity.create_account(
                    id=request.form['id'],
                    name=request.form['name'],
                    password=request.form['password'],
                    email=request.form['email'],
                    profile_id=request.form['profile_id'],
                    status=request.form['status']
                )
                return redirect(url_for('view_accounts'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'error')
        return render_template('create_account.html', profiles=profiles)

    def update_account(self, id, request):
        # Fetch the account and profiles for the form
        account = self.user_account_entity.get_account_by_id(id)
        profiles = self.user_profile_entity.get_active_profiles()
        if request.method == 'POST':
            try:
                # Update account information
                self.user_account_entity.update_account(
                    id=request.form['id'],
                    name=request.form['name'],
                    password=request.form['password'],
                    email=request.form['email'],
                    profile_id=request.form['profile_id'],
                    status=request.form['status'],
                    old_id=id
                )
                flash('User account updated successfully!')
                return redirect(url_for('view_accounts'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'error')
        return render_template('edit_account.html', account=account, profiles=profiles)

    def suspend_account(self, id):
        # Suspend the selected account
        self.user_account_entity.suspend_account(id)
        flash('User account suspended successfully!')
        return redirect(url_for('view_accounts'))

    def search_accounts(self):
        if request.method == 'POST':
            search_term = request.form['search_term']
            accounts = self.user_account_entity.search_accounts(search_term)
            return render_template('accounts.html', accounts=accounts)
        return render_template('search_accounts.html')

    def login(self, request):
        if request.method == 'POST':
            # Attempt to log in with the provided credentials
            user = self.user_account_entity.login_user(
                user_id=request.form['id'],
                password=request.form['password']
            )      
            if user:
                # Set session variables for the logged-in user
                session['user'] = {
                    'id': user['id'],
                    'name': user['name'],
                    'profile_id': user['profile_id'],
                    'role': user['role']
                }
                flash(f'Welcome {user["name"]}!')
                # Redirect based on user role
                if user['role'] == 'admin':
                    return redirect(url_for('view_accounts'))
                elif user['role'] == 'buyer':
                    return redirect(url_for('search_listings'))
                elif user['role'] == 'seller':
                    return redirect(url_for('manage_seller_listings'))
                elif user['role'] == 'agent':
                    return redirect(url_for('view_cars'))
                else:
                    return redirect(url_for('welcome'))
            else:
                # Invalid credentials or suspended account
                flash('Invalid credentials or account suspended')
        return render_template('login.html')

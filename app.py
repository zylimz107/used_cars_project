from functools import wraps
from flask import Flask, render_template, request, redirect, session, url_for, flash
from buyer_controller import BuyerController
from review_controller import ReviewController
from seller_controller import SellerController
from used_car_controller import UsedCarController
from user_account_controller import UserAccountController
from user_profile_controller import UserProfileController


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management and flashing messages

# Create instances of controller classes for managing different functionalities
user_account_controller = UserAccountController()
profile_controller = UserProfileController()
car_controller = UsedCarController()
buyer_controller = BuyerController()
seller_controller = SellerController()
review_controller = ReviewController()

# Decorator to check if user is an admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user']['role'] != 'admin':
            flash('You do not have permission to access this page.')
            return redirect(url_for('login'))  # Redirect to login if not admin
        return f(*args, **kwargs)
    return decorated_function

# Decorators for other user roles (buyer, seller, agent)
def buyer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user']['role'] != 'buyer':
            flash('You do not have permission to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def seller_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user']['role'] != 'seller':
            flash('You do not have permission to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def agent_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user']['role'] != 'agent':
            flash('You do not have permission to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# -- USER ACCOUNTS CRUDS --

@app.route('/accounts')
@admin_required
def view_accounts():
    return user_account_controller.view_accounts()  # View all user accounts

@app.route('/accounts/new', methods=('GET', 'POST'))
@admin_required
def create_account():
    return user_account_controller.create_account(request)  # Create a new user account

@app.route('/accounts/<string:id>/edit', methods=('GET', 'POST'))
@admin_required
def update_account(id):
    return user_account_controller.update_account(id, request)  # Update user account details

@app.route('/accounts/<string:id>/suspend')
@admin_required
def suspend_account(id):
    return user_account_controller.suspend_account(id)  # Suspend a user account

@app.route('/accounts/search', methods=('GET', 'POST'))
@admin_required
def search_accounts():
    return user_account_controller.search_accounts()  # Search for user accounts

# -- LOGIN & LOGOUT --

@app.route('/', methods=('GET', 'POST'))
def login():
    return user_account_controller.login(request)  # User login

@app.route('/logout')
def logout():
    session.clear()  # Clear session on logout
    flash('You have been logged out.')
    return redirect(url_for('login'))  # Redirect to login page

# -- USER PROFILE CRUDS --

@app.route('/profiles')
@admin_required
def view_profiles():
    return profile_controller.view_profiles()  # View all user profiles

@app.route('/profiles/new', methods=('GET', 'POST'))
@admin_required
def create_profile():
    return profile_controller.create_profile()  # Create a new user profile

@app.route('/profiles/<int:profile_id>/edit', methods=('GET', 'POST'))
@admin_required
def update_profile(profile_id):
    return profile_controller.update_profile(profile_id)  # Update user profile

@app.route('/profiles/<int:profile_id>/suspend')
@admin_required
def suspend_profile(profile_id):
    return profile_controller.suspend_profile(profile_id)  # Suspend a user profile

@app.route('/profiles/search', methods=('GET', 'POST'))
@admin_required
def search_profiles():
    return profile_controller.search_profiles()  # Search for user profiles

# -- used car listings CRUDS --

@app.route('/cars')
@agent_required
def view_cars():
    return car_controller.view_cars()  # View all car listings

@app.route('/cars/new', methods=['GET', 'POST'])
@agent_required
def create_car():
    return car_controller.create_car()  # Create a new car listing

@app.route('/cars/<int:car_id>/edit', methods=['GET', 'POST'])
@agent_required
def update_car(car_id):
    return car_controller.update_car(car_id)  # Edit a specific car listing

@app.route('/cars/<int:car_id>/delete', methods=['POST'])
@agent_required
def delete_car(car_id):
    return car_controller.delete_car(car_id)  # Delete a specific car listing

@app.route('/cars/search', methods=['GET', 'POST'])
@agent_required
def search_cars():
    return car_controller.search_cars()  # Search for car listings

# -- BUYER used car listings and shortlist --

@app.route('/buyer/search', methods=('GET', 'POST'))
@buyer_required
def search_listings():
    return buyer_controller.search_listings()  # Search for used car listings

@app.route('/buyer/cars/<int:car_id>')
@buyer_required
def view_listing(car_id):
    return buyer_controller.view_listing(car_id)  # View details of a specific car

@app.route('/buyer/shortlist/add/<int:car_id>')
@buyer_required
def save_listing(car_id):
    return buyer_controller.save_listing(car_id)  # Add car to the shortlist

@app.route('/buyer/shortlist')
@buyer_required
def view_shortlist():
    return buyer_controller.view_shortlist()  # View the shortlist of cars

@app.route('/buyer/shortlist/search', methods=('GET', 'POST'))
@buyer_required
def search_shortlist():
    return buyer_controller.search_shortlist()  # Search within the shortlist

# -- SELLER -- 

@app.route('/seller/listings')
@seller_required
def manage_seller_listings():
    return seller_controller.manage_seller_listings()  # Manage seller's car listings

# -- BUYER loan calculator --

@app.route('/loan_calculator', methods=('GET', 'POST'))
@buyer_required
def loan_calculator():
    return buyer_controller.loan_calculator()  # Loan calculator for buyers

# -- RATINGS & REVIEWS --

@app.route('/agents')
def view_agents():
    return review_controller.view_agents()  # View all agents available for reviews

@app.route('/agents/<string:agent_id>/reviews')
def view_reviews(agent_id):
    return review_controller.view_reviews(agent_id)  # View reviews for a specific agent

@app.route('/agents/<string:agent_id>/review', methods=('GET', 'POST'))
def submit_review(agent_id):
    return review_controller.submit_review(agent_id)  # Submit a review for an agent

# Placeholder for undefined roles
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # Welcome page for users

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode

from functools import wraps
from math import pow
from sqlite3 import IntegrityError
import sqlite3
from flask import Flask, render_template, request, redirect, session, url_for, flash
from buyer_listing_repository import BuyerListingRepository
from review_repository import ReviewRepository
from seller_listing_repository import SellerListingRepository
from used_car_repository import UsedCarRepository
from user_account_repository import UserAccountRepository
from user_profile_repository import UserProfileRepository


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages
user_repo = UserAccountRepository()
profile_repo = UserProfileRepository()
car_repo = UsedCarRepository()
buyer_repo = BuyerListingRepository()
seller_repo = SellerListingRepository()
review_repo = ReviewRepository()

# Decorator to check if user is an admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user']['role'] != 'admin':
            flash('You do not have permission to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

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

# View all accounts
@app.route('/accounts')
@admin_required
def view_accounts():
    accounts = user_repo.get_all_accounts()
    return render_template('accounts.html', accounts=accounts)

# Create a new user account
@app.route('/accounts/new', methods=('GET', 'POST'))
@admin_required
def create_account():
    profiles = user_repo.fetch_all('SELECT * FROM user_profiles WHERE status = "active"')

    if request.method == 'POST':
        try:
            # Check if user ID or email already exists
            existing_user = user_repo.get_account_by_id_or_email(
                user_id=request.form['id'], 
                email=request.form['email']
            )

            if existing_user:
                flash('User ID or email already exists. Please use a different one.', 'error')
                return render_template('create_account.html', profiles=profiles)

            # Create the new user account
            user_repo.create_account(
                id=request.form['id'],
                name=request.form['name'],
                password=request.form['password'],
                email=request.form['email'],
                profile_id=request.form['profile_id'],
                status=request.form['status']
            )
            return redirect(url_for('view_accounts'))

        except IntegrityError:
            flash('An unexpected error occurred. Please try again.', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    return render_template('create_account.html', profiles=profiles)

# Update a user account
@app.route('/accounts/<string:id>/edit', methods=('GET', 'POST'))
@admin_required
def update_account(id):
    account = user_repo.get_account_by_id(id)  # Fetch existing account
    profiles = user_repo.fetch_all('SELECT * FROM user_profiles WHERE status = "active"')

    if request.method == 'POST':
        try:
            # Get the new ID and email from the form
            new_id = request.form['id']
            new_email = request.form['email']

            # Check if the new ID is taken by another user (not the current one)
            if new_id != id:
                existing_user_with_id = user_repo.get_account_by_id(new_id)
                if existing_user_with_id:
                    flash('Username already exists for another user. Please choose a different one.', 'error')
                    return render_template('edit_account.html', account=account, profiles=profiles)

            # Check if the email belongs to another user (not the current one)
            existing_user_with_email = user_repo.get_account_by_email(new_email)
            if existing_user_with_email and existing_user_with_email['id'] != id:
                flash('Email already exists for another user. Please use a different one.', 'error')
                return render_template('edit_account.html', account=account, profiles=profiles)

            # Perform the update
            user_repo.update_account(
                id=new_id,
                name=request.form['name'],
                password=request.form['password'],
                email=new_email,
                profile_id=request.form['profile_id'],
                status=request.form['status'],
                old_id=id  # Pass the old ID for WHERE clause
            )
            flash('User account updated successfully!', 'success')
            return redirect(url_for('view_accounts'))

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    return render_template('edit_account.html', account=account, profiles=profiles)




# Suspend a user account
@app.route('/accounts/<string:id>/suspend')
@admin_required
def suspend_account(id):
    user_repo.suspend_account(id)
    flash('User account suspended successfully!')
    return redirect(url_for('view_accounts'))

# Search user accounts by username
@app.route('/accounts/search', methods=('GET', 'POST'))
@admin_required
def search_accounts():
    if request.method == 'POST':
        search_term = request.form['search_term']
        accounts = user_repo.search_accounts(search_term)
        return render_template('accounts.html', accounts=accounts)

    return render_template('search_accounts.html')

# -- USER PROFILE CRUDS --

# View all user profiles
@app.route('/profiles')
@admin_required
def view_profiles():
    profiles = profile_repo.get_all_profiles()
    return render_template('profiles.html', profiles=profiles)

@app.route('/profiles/new', methods=('GET', 'POST'))
@admin_required
def create_profile():
    if request.method == 'POST':
        role = request.form['role'].strip()
        status = request.form['status']

        try:
            # Check if the role already exists
            existing_profile = profile_repo.get_profile_by_role(role)
            if existing_profile:
                flash('Role already exists. Please choose a different role.', 'error')
                return render_template('create_profile.html')

            # Create the new profile
            profile_repo.create_profile(role, status)
            flash('Profile created successfully!', 'success')
            return redirect(url_for('view_profiles'))

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    return render_template('create_profile.html')


@app.route('/profiles/<int:profile_id>/edit', methods=('GET', 'POST'))
@admin_required
def update_profile(profile_id):
    profile = profile_repo.get_profile_by_id(profile_id)

    if request.method == 'POST':
        role = request.form['role'].strip()
        status = request.form['status']

        try:
            # Check if the new role already exists
            existing_profile = profile_repo.get_profile_by_role(role)
            if existing_profile and existing_profile['profile_id'] != profile_id:
                flash('Role already exists. Please choose a different role.', 'error')
                return render_template('edit_profile.html', profile=profile)

            # Update the profile
            profile_repo.update_profile(profile_id, role, status)
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('view_profiles'))

        except Exception as e:
            flash(f'Error updating profile: {str(e)}', 'error')

    return render_template('edit_profile.html', profile=profile)


# Suspend a user profile
@app.route('/profiles/<int:profile_id>/suspend')
@admin_required
def suspend_profile(profile_id):
    profile_repo.suspend_profile(profile_id)
    flash('Profile suspended successfully!')
    return redirect(url_for('view_profiles'))

# Search user profiles
@app.route('/profiles/search', methods=('GET', 'POST'))
@admin_required
def search_profiles():
    if request.method == 'POST':
        role = request.form['role']
        profiles = profile_repo.search_profiles(role)
        return render_template('profiles.html', profiles=profiles)

    return render_template('search_profiles.html')

# -- AGENT used car listings CRUDS --

# View all used car listings
@app.route('/cars')
@agent_required
def view_cars():
    cars = car_repo.get_all_cars()
    return render_template('cars.html', cars=cars)

# Create a new used car listing
@app.route('/cars/new', methods=('GET', 'POST'))
@agent_required
def create_car():
    sellers = user_repo.get_active_sellers()
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']
        description = request.form['description']
        agent_id = request.form['agent_id']
        seller_id = request.form['seller_id']

        try:
            car_repo.create_car(make, model, year, price, description, agent_id, seller_id)
            flash('Car listing created successfully!', 'success')
            return redirect(url_for('view_cars'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

        car_repo.create_car(make, model, year, price, description, agent_id, seller_id)
        flash('Car listing created successfully!')
        return redirect(url_for('view_cars'))

    return render_template('create_car.html', sellers=sellers)

@app.route('/cars/<int:car_id>/edit', methods=('GET', 'POST'))
@agent_required
def update_car(car_id):
    car = car_repo.get_car_by_id(car_id)
    sellers = user_repo.get_active_sellers()  # Fetch sellers

    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']
        description = request.form['description']
        seller_id = request.form['seller_id']

        try:
            car_repo.update_car(car_id, make, model, year, price, description, seller_id)
            flash('Car listing updated successfully!', 'success')
            return redirect(url_for('view_cars'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    return render_template('edit_car.html', car=car, sellers=sellers)


# Delete a used car listing
@app.route('/cars/<int:car_id>/delete', methods=('POST',))
@agent_required
def delete_car(car_id):
    car_repo.delete_car(car_id)
    flash('Car listing deleted successfully!')
    return redirect(url_for('view_cars'))

# Search used car listings
@app.route('/cars/search', methods=('GET', 'POST'))
@agent_required
def search_cars():
    if request.method == 'POST':
        search_term = request.form['search_term']
        cars = car_repo.search_cars(search_term)
        return render_template('cars.html', cars=cars)

    return render_template('search_cars.html')

# -- BUYER used car listings and shortlist --

# Search used car listings
@app.route('/buyer/search', methods=('GET', 'POST'))
@buyer_required
def search_listings():
    if request.method == 'POST':
        search_term = request.form['search_term']
        cars = buyer_repo.search_listings(search_term)
    else:
        cars = buyer_repo.search_listings()

    return render_template('buyer_listings.html', cars=cars)

# View a car listing
@app.route('/buyer/cars/<int:car_id>')
@buyer_required
def view_listing(car_id):
    buyer_repo.increment_view_count(car_id)
    car = buyer_repo.get_car_by_id(car_id)

    return render_template('view_car.html', car=car)

# Save a car listing to the shortlist
@app.route('/buyer/shortlist/add/<int:car_id>')
@buyer_required
def save_listing(car_id):
    buyer_id = session['user']['id']

    try:
        # Attempt to add the car to the shortlist
        buyer_repo.add_to_shortlist(buyer_id, car_id)
        flash('Car added to your shortlist!')
    except sqlite3.IntegrityError:
        # Handle the case where the car is already in the shortlist
        flash('This car is already in your shortlist.')

    return redirect(url_for('view_shortlist'))

# View the buyer's shortlist
@app.route('/buyer/shortlist')
@buyer_required
def view_shortlist():
    buyer_id = session['user']['id']
    shortlist = buyer_repo.get_shortlist(buyer_id)

    return render_template('shortlist.html', cars=shortlist)

# Search the buyer's shortlist
@app.route('/buyer/shortlist/search', methods=('GET', 'POST'))
@buyer_required
def search_shortlist():
    buyer_id = session['user']['id']

    if request.method == 'POST':
        search_term = request.form['search_term']
        shortlist = buyer_repo.search_shortlist(buyer_id, search_term)
    else:
        shortlist = buyer_repo.get_shortlist(buyer_id)

    return render_template('shortlist.html', cars=shortlist)

# -- SELLER -- 

# Seller listings
@app.route('/seller/listings')
@seller_required
def manage_seller_listings():
    seller_id = session['user']['id']
    cars = seller_repo.get_seller_listings(seller_id)
    
    return render_template('seller_listings.html', cars=cars)

# -- BUYER loan calculator --

@app.route('/loan_calculator', methods=('GET', 'POST'))
@buyer_required
def loan_calculator():
    cars = car_repo.get_all_cars()  # Fetch all cars from the repository
    monthly_payment = None

    if request.method == 'POST':
        car_id = int(request.form['car_id'])
        selected_car = car_repo.get_car_by_id(car_id)  # Fetch selected car by ID
        price = selected_car['price']

        # Get loan details from the form
        interest_rate = float(request.form['interest_rate']) / 100 / 12  # Monthly rate
        loan_term = int(request.form['loan_term']) * 12  # Total months

        # Calculate monthly payment using loan formula
        monthly_payment = (price * interest_rate * pow(1 + interest_rate, loan_term)) / (
            pow(1 + interest_rate, loan_term) - 1
        )

        # flash(f'Estimated Monthly Payment: ${monthly_payment:.2f}')

    return render_template(
        'loan_calculator.html', 
        cars=cars, 
        monthly_payment=monthly_payment
    )

# -- RATINGS & REVIEWS --

# View all agents for reviews
@app.route('/agents')
def view_agents():
    agents = user_repo.get_active_agents()
    return render_template('agents.html', agents=agents)

# View reviews for a specific agent
@app.route('/agents/<string:agent_id>/reviews')
def view_reviews(agent_id):
    reviews = review_repo.get_reviews_by_agent(agent_id)
    return render_template('agent_reviews.html', reviews=reviews, agent_id=agent_id)

# Submit a review for an agent
@app.route('/agents/<string:agent_id>/review', methods=('GET', 'POST'))
def submit_review(agent_id):
    if request.method == 'POST':
        rating = int(request.form['rating'])
        review = request.form['review']
        user_id = session['user']['id']

        review_repo.submit_review(agent_id, user_id, rating, review)
        flash('Thank you for your feedback!')
        return redirect(url_for('view_reviews', agent_id=agent_id))

    return render_template('submit_review.html', agent_id=agent_id)

# -- LOGIN & LOGOUT

# User login
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user = user_repo.login_user(
            user_id=request.form['id'],
            password=request.form['password']
        )

        if user:
            session['user'] = {
                'id': user['id'],
                'name': user['name'],
                'profile_id': user['profile_id'],
                'role': user['role']
            }
            flash(f'Welcome {user["name"]}!')
            if user['role'] == 'admin':
              return redirect(url_for('view_accounts'))
            elif user['role'] == 'buyer':
              return redirect(url_for('search_listings'))
            elif user['role'] == 'seller':
              return redirect(url_for('manage_seller_listings'))
            elif user['role'] == 'agent':
              return redirect(url_for('view_cars'))
            else: return redirect(url_for('welcome'))
        else:
            flash('Invalid credentials or account suspended')

    return render_template('login.html')

# User logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/')
def home():
    return redirect(url_for('login'))  # Redirect to the login page

#placeholder for undefined roles
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(debug=True)


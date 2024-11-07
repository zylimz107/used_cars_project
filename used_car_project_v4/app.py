from functools import wraps
from flask import Flask, jsonify, render_template, request, redirect, session, url_for, flash
from buyer_controller import LoanCalculatorController, SaveListingController, SearchListingController, SearchShortlistController, ViewListingController, ViewShortlistController
from review_controller import AgentReviewController, BuyerReviewController, SellerReviewController
from seller_controller import SellerController, TrackShortlistsController, TrackViewsController
from used_car_controller import CreateCarController, DeleteCarController, SearchCarController, UpdateCarController, ViewCarController
from user_account_controller import CreateAccountController, LoginController, SearchAccountController, SuspendAccountController, UpdateAccountController, ViewAccountController
from user_profile_controller import CreateProfileController, SearchProfileController, SuspendProfileController, UpdateProfileController, ViewProfileController


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management and flashing messages

# Create instances of controller classes for managing different functionalities
#user account controllers
view_account_controller = ViewAccountController()
create_account_controller = CreateAccountController()
update_account_controller = UpdateAccountController()
suspend_account_controller = SuspendAccountController()
search_account_controller = SearchAccountController()
login_controller = LoginController()
#user profile controllers
view_profile_controller = ViewProfileController()
create_profile_controller = CreateProfileController()
update_profile_controller = UpdateProfileController()
suspend_profile_controller = SuspendProfileController()
search_profile_controller = SearchProfileController()
#used_car controllers
view_car_controller = ViewCarController()
create_car_controller = CreateCarController()
update_car_controller = UpdateCarController()
delete_car_controller = DeleteCarController()
search_car_controller = SearchCarController()
#buyer controllers
search_listing_controller = SearchListingController()
view_listing_controller = ViewListingController()
save_listing_controller = SaveListingController()
view_shortlist_controller = ViewShortlistController()
search_shortlist_controller = SearchShortlistController()
loan_calculator_controller = LoanCalculatorController()
#seller controllers
seller_controller = SellerController()
track_views_controller = TrackViewsController()
track_shortlists_controller = TrackShortlistsController()
#review controllers
buyer_review_controller = BuyerReviewController()
seller_review_controller = SellerReviewController()
agent_review_controller = AgentReviewController()

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
    accounts = view_account_controller.view_accounts()
    return render_template('accounts.html', accounts=accounts)  # View all user accounts

@app.route('/accounts/new', methods=('GET', 'POST'))
@admin_required
def create_account():

    profiles = view_profile_controller.view_profiles()
    if request.method == 'POST':
        # Call the controller to update the account, passing in form data
        account_data = {
            'id': request.form['id'],
            'name': request.form['name'],
            'password': request.form['password'],
            'email': request.form['email'],
            'profile_id': request.form['profile_id'],
            'status': request.form['status']
        }
        
    
        account = create_account_controller.create_account(account_data)
        if not account:
            flash('User ID or email already exists.')
        else:
            flash('Account created')
        
        return render_template('create_account.html', profiles=profiles)
    return render_template('create_account.html', profiles=profiles)
@app.route('/accounts/<string:id>/edit', methods=('GET', 'POST'))
@admin_required
def update_account(id):
    profiles = view_profile_controller.view_profiles()  # Fetch profiles for the form

    if request.method == 'POST':
        # Call the controller to update the account, passing in form data
        account_data = {
            'id': request.form['id'],
            'name': request.form['name'],
            'password': request.form['password'],
            'email': request.form['email'],
            'profile_id': request.form['profile_id'],
            'status': request.form['status']
        }
        
        # Pass data to the controller for updating the account
        up_account = update_account_controller.update_account(id, account_data)
        
        if not up_account:
            flash('User ID or email already exists.')
        else:
            flash('Account Updated')
        
        return render_template('edit_account.html', profiles=profiles)

    return render_template('edit_account.html', profiles=profiles)

@app.route('/accounts/<string:id>/suspend')
@admin_required
def suspend_account(id):
    suspend = suspend_account_controller.suspend_account(id)  # Attempt to suspend the account

    # Check the result and flash the appropriate message
    if suspend is False:
        flash('User account is already suspended!', 'warning')
    elif suspend is True:
        flash('User account suspended successfully!', 'success')
    
    return redirect(url_for('view_accounts'))

@app.route('/accounts/search', methods=('GET', 'POST'))
@admin_required
def search_accounts():
    if request.method == 'POST':
        search_term = request.form['search_term']
        accounts = search_account_controller.search_accounts(search_term) # Search for user accounts
        return render_template('accounts.html', accounts=accounts) 

# -- LOGIN & LOGOUT --

@app.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user_id = request.form['id']
        password = request.form['password']
        user = login_controller.login(user_id,password)
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
    
    # Render login form for both GET requests and failed POST requests
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()  # Clear session on logout
    flash('You have been logged out.')
    return redirect(url_for('login'))  # Redirect to login page

# -- USER PROFILE CRUDS --

@app.route('/profiles')
@admin_required
def view_profiles():
    profiles = view_profile_controller.view_profiles()
    return render_template('profiles.html', profiles=profiles)  # View all user profiles

@app.route('/profiles/new', methods=('GET', 'POST'))
@admin_required
def create_profile():
    if request.method == 'POST':
        # Collect form data
        profile_data = {
            'role': request.form['role'].strip(),
            'status': request.form['status'],
            'description': request.form['description'].strip()
        }


        # Call the controller to create the profile
        success = create_profile_controller.create_profile(profile_data)

        # Flash message based on the outcome
        if not success:
            flash('Role already exists. Please choose a different role.', 'error')
            return render_template('create_profile.html')
        
        flash('Profile created successfully!', 'success')
        return redirect(url_for('view_profiles'))

    # For GET requests, render the form
    return render_template('create_profile.html')

@app.route('/profiles/<int:profile_id>/edit', methods=('GET', 'POST'))
@admin_required
def update_profile(profile_id):

    if request.method == 'POST':
        # Collect form data
        profile_data = {
            'role': request.form['role'].strip(),
            'status': request.form['status'],
            'description': request.form['description'].strip()
        }

        # Call the controller to update the profile
        success = update_profile_controller.update_profile(profile_id, profile_data)

        # Handle success or failure messages
        if not success:
            flash('Role already exists. Please choose a different role.', 'error')
            return render_template('edit_profile.html')
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('view_profiles'))

    # For GET requests, render the form with current profile data
    return render_template('edit_profile.html')
 # Update user profile

@app.route('/profiles/<int:profile_id>/suspend')
@admin_required
def suspend_profile(profile_id):

    suspend = suspend_profile_controller.suspend_profile(profile_id)  # Suspend a user profile

    # Check the result and flash the appropriate message
    if suspend is False:
        flash('User account is already suspended!', 'warning')
    elif suspend is True:
        flash('User account suspended successfully!', 'success')
    return redirect(url_for('view_profiles'))

@app.route('/profiles/search', methods=('GET', 'POST'))
@admin_required
def search_profiles():
    if request.method == 'POST':
        search_term = request.form['search_term']
        profiles = search_profile_controller.search_profiles(search_term) # Search for user profiles
        return render_template('profiles.html', profiles=profiles)

# -- used car listings CRUDS --

@app.route('/cars')
@agent_required
def view_cars():
    cars = view_car_controller.view_cars()
    return render_template('cars.html', cars=cars)  # View all car listings

# Boundary
@app.route('/cars/new', methods=['GET', 'POST'])
@agent_required
def create_car():
    if request.method == 'POST':
        # Get form data
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']
        description = request.form['description']
        agent_id = request.form['agent_id']
        seller_id = request.form['seller_id']

        # Call controller to create the car
        success = create_car_controller.create_car(make, model, year, price, description, agent_id, seller_id)

        if success:
            flash('Car listing created successfully!', 'success')
            return redirect(url_for('view_cars'))
        else:
            flash('Error creating car listing.', 'error')

    return render_template('create_car.html')


@app.route('/cars/<int:car_id>/edit', methods=['GET', 'POST'])
@agent_required
def update_car(car_id):
    if request.method == 'POST':
        # Get form data
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']
        description = request.form['description']
        seller_id = request.form['seller_id']

        # Call controller to update the car
        success = update_car_controller.update_car(car_id,make, model, year, price, description, seller_id)

        if success:
            flash('Car listing updated successfully!', 'success')
            return redirect(url_for('view_cars'))
        else:
            flash('Error updating car listing.', 'error')

    return render_template('edit_car.html')

@app.route('/cars/<int:car_id>/delete', methods=['POST'])
@agent_required
def delete_car(car_id):
    delete_car_controller.delete_car(car_id)
    flash('Car listing deleted successfully!')
    return redirect(url_for('view_cars'))# Delete a specific car listing

@app.route('/cars/search', methods=['GET', 'POST'])
@agent_required
def search_cars():
    if request.method == 'POST':
            # Search for cars based on the search term
        search_term = request.form['search_term']
        cars = search_car_controller.search_cars(search_term)# Search for car listings
        return render_template('cars.html', cars=cars) 
# -- BUYER used car listings and shortlist --

@app.route('/buyer/search', methods=('GET', 'POST'))
@buyer_required
def search_listings():
    if request.method == 'POST':
        search_term = request.form['search_term']
        cars = search_listing_controller.search_listings(search_term)# Search for used car listings
    else:
        # If no search term, retrieve all listings
        cars = search_listing_controller.search_listings(search_term='')
    return render_template('buyer_listings.html', cars=cars)
@app.route('/buyer/cars/<int:car_id>')
@buyer_required
def view_listing(car_id):
    car = view_listing_controller.view_listing(car_id)# View details of a specific car
    return render_template('view_car.html', car=car)
@app.route('/buyer/shortlist/add/<int:car_id>')
@buyer_required
def save_listing(car_id):
    buyer_id = session['user']['id']

    success = save_listing_controller.save_listing(buyer_id, car_id ) # Add car to the shortlist
    if success:
        flash('Car added to your shortlist!','success')
    else:
        flash('This car is already in your shortlist.','error')

    return redirect(url_for('view_shortlist'))

@app.route('/buyer/shortlist')
@buyer_required
def view_shortlist():
    buyer_id = session['user']['id']
    shortlist = view_shortlist_controller.view_shortlist(buyer_id)# View the shortlist of cars
    return render_template('shortlist.html', cars=shortlist)

@app.route('/buyer/shortlist/search', methods=('GET', 'POST'))
@buyer_required
def search_shortlist():
    buyer_id = session['user']['id']

    if request.method == 'POST':
        search_term = request.form['search_term']
        shortlist = search_shortlist_controller.search_shortlist(buyer_id,search_term)

    return render_template('shortlist.html', cars=shortlist)


# -- SELLER -- 

@app.route('/seller/listings')
@seller_required
def manage_seller_listings():
    # Get the seller's ID from the session
    seller_id = session['user']['id']
    cars = seller_controller.manage_seller_listings(seller_id)
    return render_template('seller_listings.html', cars=cars)

@app.route('/car/<int:car_id>/view_count', methods=['GET'])
def get_view_count(car_id):
    view_count = track_views_controller.get_view_count(car_id)
    return jsonify({'view_count': view_count})

@app.route('/car/<int:car_id>/shortlist_count', methods=['GET'])
def get_shortlist_count(car_id):
    shortlist_count = track_shortlists_controller.get_shortlist_count(car_id)
    return jsonify({'shortlist_count': shortlist_count})


# -- BUYER loan calculator --

@app.route('/loan_calculator', methods=('GET', 'POST'))
@buyer_required
def loan_calculator():
    cars = view_car_controller.view_cars()
    monthly_payment = None

    if request.method == 'POST':
        # Extract loan details from the form
        car_id = int(request.form['car_id'])
        selected_car = loan_calculator_controller.loan_calculator(car_id)
        price = selected_car['price']

        interest_rate = float(request.form['interest_rate']) / 100 / 12  # Monthly rate
        loan_term = int(request.form['loan_term']) * 12  # Total months

        # Calculate monthly payment using the loan formula
        if interest_rate > 0:
            monthly_payment = (price * interest_rate * pow(1 + interest_rate, loan_term)) / (
                pow(1 + interest_rate, loan_term) - 1
                )
        else:
            monthly_payment = price / loan_term  # Simple division for zero interest

        flash(f'Estimated Monthly Payment: ${monthly_payment:.2f}')

    return render_template(
        'loan_calculator.html',
        cars=cars,
        monthly_payment=monthly_payment
    )

# -- RATINGS & REVIEWS --
@app.route('/agents/review/buyer', methods=('GET', 'POST'))
def submit_buyer_review():
    if request.method == 'POST':
        agent_id = request.form['agent_id']
        rating = int(request.form['rating'])
        review = request.form['review']
        user_id = session['user']['id']

        # Submit the review as a buyer
        buyer_review_controller.submit_review(agent_id, user_id, rating, review)
        flash('Thank you for your feedback as a buyer!')
        return redirect(url_for('search_listings'))

    return render_template('submit_review.html', user_type='buyer')

@app.route('/agents/review/seller', methods=('GET', 'POST'))
def submit_seller_review():
    if request.method == 'POST':
        agent_id = request.form['agent_id']
        rating = int(request.form['rating'])
        review = request.form['review']
        user_id = session['user']['id']

        # Submit the review as a seller
        seller_review_controller.submit_review(agent_id, user_id, rating, review)
        flash('Thank you for your feedback as a seller!')
        return redirect(url_for('manage_seller_listings',))

    return render_template('submit_review.html', user_type='seller')

@app.route('/reviews')
def view_reviews():
    # Get reviews associated with a specific agent
    agent_id = session['user']['id']
    reviews = agent_review_controller.view_reviews(agent_id)
    return render_template('agent_reviews.html', reviews=reviews, agent_id=agent_id)

# Placeholder for undefined roles
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # Welcome page for users

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode

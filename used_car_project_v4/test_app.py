import pytest
from flask import Flask, session
from boundary import app, view_reviews
import sqlite3

# Connect to the database
connection = sqlite3.connect('used_car.db')
cursor = connection.cursor()


# Fixture for setting up the app for testing
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'testsecret'  # Set a test secret key for sessions
    client = app.test_client()
    yield client  # This will be available as "client" in the tests
    # After the test, you can clean up any resources if necessary

def reset_auto_increment():
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='used_cars';")
    connection.commit()  # Commit changes to the database

# Test viewing accounts
def test_view_accounts(client):
    # Assuming you have an admin user for authentication
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'admin1', 'role': 'admin'}

    response = client.get('/accounts')
    assert response.status_code == 200
    assert b'Accounts' in response.data  # Check if the page contains "Accounts" text

# Test account creation
def test_create_account(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'admin1', 'role': 'admin'}

    response = client.post('/accounts/new', data={
        'id': 'newuser',
        'name': 'New User',
        'password': 'password123',
        'email': 'newuser@example.com',
        'profile_id': '2',  # Adjust according to your profile IDs
        'status': 'active'
    })

    assert response.status_code == 200
    assert b'Account created' in response.data

# Test updating an account
def test_update_account(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'admin1', 'role': 'admin'}

    # First create a test account
    client.post('/accounts/new', data={
        'id': 'user123',
        'name': 'User 123',
        'password': 'password123',
        'email': 'user123@example.com',
        'profile_id': '2',
        'status': 'active'
    })

    # Now update that account
    response = client.post('/accounts/user123/edit', data={
        'id': 'user123',
        'name': 'Updated User',
        'password': 'newpassword',
        'email': 'updateduser@example.com',
        'profile_id': '3',
        'status': 'suspended'
    })

    assert response.status_code == 200
    assert b'Account Updated' in response.data

# Test suspending an account
def test_suspend_account(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'admin1', 'role': 'admin'}

    # Create a test account to suspend
    client.post('/accounts/new', data={
        'id': 'user_to_suspend',
        'name': 'User to Suspend',
        'password': 'password123',
        'email': 'suspenduser@example.com',
        'profile_id': '2',
        'status': 'active'
    })

    response = client.get('/accounts/user_to_suspend/suspend')

    # Check for redirection
    assert response.status_code == 302  # Redirect after suspension

    # Check if flash message is in session (not in the body)
    with client.session_transaction() as sess:
        flash_message = sess.get('_flashes', [])
        assert any('User account suspended successfully!' in msg[1] for msg in flash_message)

# Test searching for accounts
def test_search_accounts(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'admin1', 'role': 'admin'}

    # Create a test account
    client.post('/accounts/new', data={
        'id': 'user_to_search',
        'name': 'User to Search',
        'password': 'password123',
        'email': 'searchuser@example.com',
        'profile_id': '2',
        'status': 'active'
    })

    response = client.post('/accounts/search', data={'search_term': 'User to Search'})
    assert response.status_code == 200
    assert b'User to Search' in response.data

# Test login functionality
def test_login(client):
    response = client.post('/', data={
        'id': 'admin1',
        'password': 'admin123'
    })

    assert response.status_code == 302  # Should redirect to /accounts

    # Check if the flash message is in the session after login
    with client.session_transaction() as sess:
        flash_message = sess.get('_flashes', [])
        assert any('Welcome' in msg[1] for msg in flash_message)


# Test login with invalid credentials
def test_invalid_login(client):
    response = client.post('/', data={
        'id': 'wronguser',
        'password': 'wrongpassword'
    })

    assert response.status_code == 200
    assert b'Invalid credentials or account suspended' in response.data

# -- Test View Profiles --
def test_view_profiles(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'admin1', 'role': 'admin'}

    # Create a profile to check if the view displays correctly
    client.post('/profiles/new', data={
        'role': 'super',
        'status': 'active',
        'description': 'super profile'
    })

    # Test that the profiles are viewable
    response = client.get('/profiles')
    assert response.status_code == 200
    assert b'super' in response.data


# -- Test Create Profile --
def test_create_profile(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'admin1', 'role': 'admin'}

    # Test profile creation
    response = client.post('/profiles/new', data={
        'role': 'special',
        'status': 'active',
        'description': 'special profile'
    })
    assert response.status_code == 302  # Should redirect after creation
    assert response.location == '/profiles'  # Check if it redirects to /profiles

    # Check for the success message in the session or on the next page
    with client.get('/profiles') as resp:
        assert b'Profile created successfully!' in resp.data


    # Test creating a profile with an existing role
    response = client.post('/profiles/new', data={
        'role': 'agent',  # Same role as before
        'status': 'active',
        'description': 'Another Agent profile'
    })
    assert b'Role already exists. Please choose a different role.' in response.data


# -- Test Update Profile --
def test_update_profile(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'admin1', 'role': 'admin'}

    # Create a profile to update
    client.post('/profiles/new', data={
        'role': 'godlike',
        'status': 'active',
        'description': 'godlike profile'
    })

    # Test updating the profile
    response = client.post('/profiles/5/edit', data={
        'role': 'godlike2',
        'status': 'active',
        'description': 'Updated godlike profile'
    })
    assert response.status_code == 302  # Should redirect after update
    assert response.location == '/profiles'  # Check if it redirects to /profiles

    # Check the success message in the redirected page
    with client.get('/profiles') as resp:
        assert b'Profile updated successfully!' in resp.data

    # Test updating to a duplicate role
    response = client.post('/profiles/5/edit', data={
        'role': 'admin',  # Existing role, should fail
        'status': 'active',
        'description': 'Profile with duplicate role'
    })
    assert b'Role already exists. Please choose a different role.' in response.data


# -- Test Suspend Profile --
def test_suspend_profile(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'admin1', 'role': 'admin'}

    # Create a profile to suspend
    client.post('/profiles/new', data={
        'role': 'suspender',
        'status': 'active',
        'description': 'suspender profile'
    })

    # Suspend the profile
    response = client.get('/profiles/5/suspend')
    assert response.status_code == 302  # Should redirect after suspension
    assert response.location == '/profiles' # Check if it redirects to /profiles

    # Check the success message in the redirected page
    with client.get('/profiles') as resp:
        assert b'User account suspended successfully!' in resp.data



# -- Test Search Profiles --
def test_search_profiles(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'admin1', 'role': 'admin'}

    # Create some profiles to search
    client.post('/profiles/new', data={
        'role': 'cow',
        'status': 'active',
        'description': 'cow profile'
    })
    client.post('/profiles/new', data={
        'role': 'cat',
        'status': 'active',
        'description': 'cat profile'
    })

    # Test searching profiles
    response = client.post('/profiles/search', data={'search_term': 'cat'})
    assert response.status_code == 200

    # Check that 'cat profile' is in the search results
    assert b'cat' in response.data
    # Check that 'cow profile' is not in the search results
    assert b'cow' not in response.data

def test_view_cars(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}

    # Make a GET request to the /cars page
    response = client.get('/cars')
    assert response.status_code == 200
    assert b'Car Listings' in response.data  # Ensure the page contains the title or keyword

def test_create_car(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}

    # Test the POST method to create a car
    response = client.post('/cars/new', data={
        'make': 'Toyota',
        'model': 'Corolla',
        'year': '2020',
        'price': '20000',
        'description': 'A reliable car',
        'agent_id': '1',
        'seller_id': '2'
    })
    
    assert response.status_code == 302  # Should redirect after creation
    assert response.location == '/cars'  # Should redirect to the car listing page

    # Check for success flash message
    with client.get('/cars') as resp:
        assert b'Car listing created successfully!' in resp.data
    client.post('/cars/1/delete')
    reset_auto_increment()
def test_update_car(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}

    # Create a car to update
    client.post('/cars/new', data={
        'make': 'Toyota',
        'model': 'Corolla',
        'year': '2020',
        'price': '20000',
        'description': 'A reliable car',
        'agent_id': '1',
        'seller_id': '2'
    })
    
    # Test the GET method to retrieve the car and update it
    response = client.get('/cars/1/edit')
    assert response.status_code == 200
    assert b'Edit Car' in response.data  # Ensure the page is for editing

    # Test the POST method to update the car
    response = client.post('/cars/1/edit', data={
        'make': 'Toyota',
        'model': 'Camry',
        'year': '2021',
        'price': '25000',
        'description': 'An upgraded reliable car',
        'seller_id': '2'
    })
    
    assert response.status_code == 302  # Should redirect after update
    assert response.location == '/cars'  # Should redirect to the car listing page

    # Check for success flash message
    with client.get('/cars') as resp:
        assert b'Car listing updated successfully!' in resp.data
    client.post('/cars/1/delete')
    reset_auto_increment()


def test_delete_car(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}

    # Create a car to delete
    client.post('/cars/new', data={
        'make': 'Toyota',
        'model': 'Corolla',
        'year': '2020',
        'price': '20000',
        'description': 'A reliable car',
        'agent_id': '1',
        'seller_id': '2'
    })
    
    # Test the POST method to delete the car
    response = client.post('/cars/1/delete')
    assert response.status_code == 302  # Should redirect after deletion
    assert response.location == '/cars'  # Should redirect to the car listing page

    # Check for success flash message
    with client.get('/cars') as resp:
        assert b'Car listing deleted successfully!' in resp.data
    reset_auto_increment()
def test_search_cars(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}

    # Create a few car listings to search
    client.post('/cars/new', data={
        'make': 'Toyota',
        'model': 'Corolla',
        'year': '2020',
        'price': '20000',
        'description': 'A reliable car',
        'agent_id': '1',
        'seller_id': '2'
    })
    client.post('/cars/new', data={
        'make': 'Honda',
        'model': 'Civic',
        'year': '2021',
        'price': '22000',
        'description': 'A sporty car',
        'agent_id': '1',
        'seller_id': '3'
    })

    # Test the POST method to search for a car
    response = client.post('/cars/search', data={'search_term': 'Corolla'})
    assert response.status_code == 200

    # Check if the search term is found in the response
    assert b'Corolla' in response.data
    # Ensure the other car is not included in the results
    assert b'Civic' not in response.data

    client.post('/cars/1/delete')
    client.post('/cars/2/delete')
    reset_auto_increment()

def test_search_listings(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}

    # Create some car listings
    client.post('/cars/new', data={
        'make': 'Toyota',
        'model': 'Corolla',
        'year': '2020',
        'price': '20000',
        'description': 'A reliable car',
        'agent_id': '1',
        'seller_id': '2'
    })
    client.post('/cars/new', data={
        'make': 'Honda',
        'model': 'Civic',
        'year': '2021',
        'price': '22000',
        'description': 'A sporty car',
        'agent_id': '1',
        'seller_id': '3'
    })
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'buyer', 'role': 'buyer'}

    # Test the POST method to search for a car
    response = client.post('/buyer/search', data={'search_term': 'Corolla'})
    assert response.status_code == 200

    # Check if the search term is found in the response
    assert b'Corolla' in response.data
    # Ensure the other car is not included in the results
    assert b'Civic' not in response.data
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}
    client.post('/cars/1/delete')
    client.post('/cars/2/delete')
    reset_auto_increment()

def test_view_listing(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}

    # Create a car listing
    client.post('/cars/new', data={
        'make': 'Toyota',
        'model': 'Corolla',
        'year': '2020',
        'price': '20000',
        'description': 'A reliable car',
        'agent_id': '1',
        'seller_id': '2'
    })
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'buyer', 'role': 'buyer'}

    # Test the GET method to view the car's details
    response = client.get('/buyer/cars/1')
    assert response.status_code == 200
    assert b'Corolla' in response.data  # Check if the car's make and model appear
    assert b'A reliable car' in response.data  # Check if the description appears
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}
    client.post('/cars/1/delete')
    reset_auto_increment()
def test_save_listing(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}


    # Create a car listing
    client.post('/cars/new', data={
        'make': 'Toyota',
        'model': 'Corolla',
        'year': '2020',
        'price': '20000',
        'description': 'A reliable car',
        'agent_id': '1',
        'seller_id': '2'
    })
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'buyer', 'role': 'buyer'}

    # Test adding the car to the shortlist
    response = client.get('/buyer/shortlist/add/1')
    assert response.status_code == 302  # Should redirect after adding to the shortlist
    assert response.location == '/buyer/shortlist'  # Should redirect to the shortlist page
    
    # Check for success flash message
    with client.get('/buyer/shortlist') as resp:
        assert b'Car added to your shortlist!' in resp.data

    # Test adding the same car again (should show an error message)
    response = client.get('/buyer/shortlist/add/1')
    assert response.status_code == 302  # Should redirect again
    assert response.location == '/buyer/shortlist'  # Should redirect to the shortlist page

    with client.get('/buyer/shortlist') as resp:
        assert b'This car is already in your shortlist.' in resp.data  # Error message should appear
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}
    client.post('/cars/1/delete')
    reset_auto_increment()

def test_view_shortlist(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}

    # Create a car listing and add it to the shortlist
    client.post('/cars/new', data={
        'make': 'Toyota',
        'model': 'Corolla',
        'year': '2020',
        'price': '20000',
        'description': 'A reliable car',
        'agent_id': '1',
        'seller_id': '2'
    })
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'buyer', 'role': 'buyer'}
    client.get('/buyer/shortlist/add/1')

    # Test viewing the shortlist
    response = client.get('/buyer/shortlist')
    # Perform assertions
    assert response.status_code == 200
    assert b'Corolla' in response.data  # Ensure the car is in the shortlist
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}
    # Simulate deleting the car
    client.post('/cars/1/delete')

    # Reset auto increment (if applicable)
    reset_auto_increment()


def test_search_shortlist(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}
    # Create car listings and add them to the shortlist
    client.post('/cars/new', data={
        'make': 'Toyota',
        'model': 'Corolla',
        'year': '2020',
        'price': '20000',
        'description': 'A reliable car',
        'agent_id': '1',
        'seller_id': '2'
    })
    client.post('/cars/new', data={
        'make': 'Honda',
        'model': 'Civic',
        'year': '2021',
        'price': '22000',
        'description': 'A sporty car',
        'agent_id': '1',
        'seller_id': '3'
    })
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'buyer', 'role': 'buyer'}

    client.get('/buyer/shortlist/add/1')
    client.get('/buyer/shortlist/add/2')

    # Test searching within the shortlist
    response = client.post('/buyer/shortlist/search', data={'search_term': 'Corolla'})
    assert response.status_code == 200
    assert b'Corolla' in response.data  # Should be in the shortlist results
    assert b'Civic' not in response.data  # Should not be in the results
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}
    client.post('/cars/1/delete')
    client.post('/cars/2/delete')
    reset_auto_increment()

def test_manage_seller_listings(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}
    # Create some car listings for the seller
    client.post('/cars/new', data={
        'make': 'Toyota',
        'model': 'Corolla',
        'year': '2020',
        'price': '20000',
        'description': 'A reliable car',
        'agent_id': '1',
        'seller_id': 'seller'
    })
    client.post('/cars/new', data={
        'make': 'Honda',
        'model': 'Civic',
        'year': '2021',
        'price': '22000',
        'description': 'A sporty car',
        'agent_id': '1',
        'seller_id': 'seller'
    })
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'seller', 'role': 'seller'}
    # Test viewing the seller's own listings
    response = client.get('/seller/listings')
    assert response.status_code == 200
    assert b'Corolla' in response.data  # The car should be visible in the seller's listings
    assert b'Civic' in response.data  # The other car should also be visible
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}
    client.post('/cars/1/delete')
    client.post('/cars/2/delete')
    reset_auto_increment()

def test_get_view_count(client):
    # Simulate the request to get the view count of a car
    response = client.get('/car/1/view_count')
    assert response.status_code == 200

    # Check the response JSON for the view count
    json_data = response.get_json()
    assert 'view_count' in json_data  # Ensure view_count is present
    assert isinstance(json_data['view_count'], int)  # View count should be an integer

def test_get_shortlist_count(client):
    # Simulate the request to get the shortlist count of a car
    response = client.get('/car/1/shortlist_count')
    assert response.status_code == 200

    # Check the response JSON for the shortlist count
    json_data = response.get_json()
    assert 'shortlist_count' in json_data  # Ensure shortlist_count is present
    assert isinstance(json_data['shortlist_count'], int)  # Shortlist count should be an integer

def test_loan_calculator(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}

    # Create some cars for the buyer to choose from
    client.post('/cars/new', data={
        'make': 'Toyota',
        'model': 'Corolla',
        'year': '2020',
        'price': '20000',
        'description': 'A reliable car',
        'agent_id': '1',
        'seller_id': 'seller'
    })
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'buyer', 'role': 'buyer'}
    # Test the GET request to load the loan calculator form
    response = client.get('/loan_calculator')
    assert response.status_code == 200
    assert b'Corolla' in response.data  # Ensure that the car options are listed

    # Test the POST request with loan details
    response = client.post('/loan_calculator', data={
        'car_id': '1',
        'interest_rate': '5',
        'loan_term': '5'
    })
    assert response.status_code == 200
    assert b'Estimated Monthly Payment: $' in response.data
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}
    client.post('/cars/1/delete')
    reset_auto_increment()

def test_submit_buyer_review(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'buyer', 'role': 'buyer'}

    # Simulate submitting a review for an agent as a buyer
    response = client.post('/agents/review/buyer', data={
        'agent_id': 'agent',
        'rating': '5',
        'review': 'Excellent service!'
    })
    assert response.status_code == 302  # Redirect to the listings page
    response = client.get('/buyer/search')
    assert b'Thank you for your feedback as a buyer!' in response.data  # Flash message confirmation

def test_submit_seller_review(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'seller', 'role': 'seller'}

    # Simulate submitting a review for an agent as a seller
    response = client.post('/agents/review/seller', data={
        'agent_id': 'agent',
        'rating': '4',
        'review': 'Good experience, but could improve communication.'
    })
    assert response.status_code == 302  # Redirect to the seller's listings page
    response = client.get('/seller/listings')
    assert b'Thank you for your feedback as a seller!' in response.data  # Flash message confirmation

def test_view_reviews(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id': 'agent', 'role': 'agent'}

    # Simulate getting reviews for the agent
    response = client.get('/reviews')
    assert response.status_code == 200
    assert b'Excellent service!' in response.data  # The review submitted by the buyer should be visible
    assert b'Good experience, but could improve communication.' in response.data  # The review from the seller should also be visible

    # Additional checks can be made to verify that the correct agent's reviews are shown

import sqlite3
from flask import render_template, redirect, url_for, request, flash, session
from buyer import Buyer
from used_car import UsedCar

class BuyerController:
    def __init__(self):
        # Initialize the entities
        self.buyer_entity = Buyer()
        self.car_entity = UsedCar()

    def search_listings(self):
        # Search for car listings based on user input
        if request.method == 'POST':
            search_term = request.form['search_term']
            cars = self.car_entity.search_cars(search_term)
        else:
            # If no search term, retrieve all listings
            cars = self.car_entity.search_cars()

        return render_template('buyer_listings.html', cars=cars)

    def view_listing(self, car_id):
        # Increment the view count for the specified car and display its details
        self.buyer_entity.increment_view_count(car_id)
        car = self.car_entity.get_car_by_id(car_id)
        return render_template('view_car.html', car=car)

    def save_listing(self, car_id):
        # Add the selected car to the buyer's shortlist
        buyer_id = session['user']['id']
        
        try:
            self.buyer_entity.add_to_shortlist(buyer_id, car_id)
            flash('Car added to your shortlist!')
        except sqlite3.IntegrityError:
            flash('This car is already in your shortlist.')

        return redirect(url_for('view_shortlist'))

    def view_shortlist(self):
        # Display the buyer's shortlist of cars
        buyer_id = session['user']['id']
        shortlist = self.buyer_entity.get_shortlist(buyer_id)
        return render_template('shortlist.html', cars=shortlist)

    def search_shortlist(self):
        # Search for cars in the buyer's shortlist
        buyer_id = session['user']['id']

        if request.method == 'POST':
            search_term = request.form['search_term']
            shortlist = self.buyer_entity.search_shortlist(buyer_id, search_term)
        else:
            # If no search term, retrieve the entire shortlist
            shortlist = self.buyer_entity.get_shortlist(buyer_id)

        return render_template('shortlist.html', cars=shortlist)
    
    def loan_calculator(self):
        # Retrieve all cars for loan calculation purposes
        cars = self.car_entity.get_all_cars()
        monthly_payment = None

        if request.method == 'POST':
            # Extract loan details from the form
            car_id = int(request.form['car_id'])
            selected_car = self.car_entity.get_car_by_id(car_id)
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

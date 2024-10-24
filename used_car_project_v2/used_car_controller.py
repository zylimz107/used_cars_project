from flask import render_template, redirect, url_for, request, flash
from used_car import UsedCar

class UsedCarController:
    def __init__(self):
        # Initialize the UsedCar entity
        self.used_car_entity = UsedCar()

    def view_cars(self):
        # Retrieve and display all used cars
        cars = self.used_car_entity.get_all_cars()
        return render_template('cars.html', cars=cars)

    def create_car(self):
        if request.method == 'POST':
            # Get car details from the form
            make = request.form['make']
            model = request.form['model']
            year = request.form['year']
            price = request.form['price']
            description = request.form['description']
            agent_id = request.form['agent_id']
            seller_id = request.form['seller_id']

            try:
                # Create a new car listing
                self.used_car_entity.create_car(make, model, year, price, description, agent_id, seller_id)
                flash('Car listing created successfully!', 'success')
                return redirect(url_for('view_cars'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'error')

        # Fetch active sellers for the form
        sellers = self.used_car_entity.get_active_sellers()
        return render_template('create_car.html', sellers=sellers)

    def update_car(self, car_id):
        # Retrieve the specific car for editing
        car = self.used_car_entity.get_car_by_id(car_id)
        sellers = self.used_car_entity.get_active_sellers()

        if request.method == 'POST':
            # Get updated car details from the form
            make = request.form['make']
            model = request.form['model']
            year = request.form['year']
            price = request.form['price']
            description = request.form['description']
            seller_id = request.form['seller_id']

            try:
                # Update the car listing
                self.used_car_entity.update_car(car_id, make, model, year, price, description, seller_id)
                flash('Car listing updated successfully!', 'success')
                return redirect(url_for('view_cars'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'error')

        return render_template('edit_car.html', car=car, sellers=sellers)

    def delete_car(self, car_id):
        # Delete the specified car listing
        self.used_car_entity.delete_car(car_id)
        flash('Car listing deleted successfully!')
        return redirect(url_for('view_cars'))

    def search_cars(self):
        if request.method == 'POST':
            # Search for cars based on the search term
            search_term = request.form['search_term']
            cars = self.used_car_entity.search_cars(search_term)
            return render_template('cars.html', cars=cars)

        return render_template('search_cars.html')

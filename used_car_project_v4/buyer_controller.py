from flask import render_template, redirect, url_for, request, flash, session
from buyer import Buyer
from used_car import UsedCar

class SearchListingController:
    def __init__(self):
        # Initialize the entities
        self.used_car_entity = UsedCar()

    def search_listings(self,search_term):
        # Search for car listings based on user input
        return self.used_car_entity.search_cars(search_term)

class ViewListingController:
    def __init__(self):
        # Initialize the entities
        self.buyer_entity = Buyer()
    def view_listing(self, car_id):
        return self.buyer_entity.view_listing(car_id)#view car and increment view count

class SaveListingController:
    def __init__(self):
        # Initialize the entities
        self.buyer_entity = Buyer()
    def save_listing(self, buyer_id, car_id):
        # Add the selected car to the buyer's shortlist
        return self.buyer_entity.add_to_shortlist(buyer_id, car_id)

class ViewShortlistController:
    def __init__(self):
        # Initialize the entities
        self.buyer_entity = Buyer()
    def view_shortlist(self, buyer_id):
        # Display the buyer's shortlist of cars
        return self.buyer_entity.get_shortlist(buyer_id)

class SearchShortlistController:
    def __init__(self):
        # Initialize the entities
        self.buyer_entity = Buyer()
    def search_shortlist(self, buyer_id,search_term):
        # Search for cars in the buyer's shortlist
        return self.buyer_entity.search_shortlist(buyer_id,search_term)
    
class LoanCalculatorController:
    def __init__(self):
        # Initialize the entities
        self.buyer_entity = Buyer()
    def loan_calculator(self,car_id):
        return self.buyer_entity.loan_calculator(car_id)


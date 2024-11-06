from flask import render_template, session
from seller import Seller

class SellerController:
    def __init__(self):
        # Initialize the Seller entity
        self.seller_entity = Seller()

    def manage_seller_listings(self):
        # Get the seller's ID from the session
        seller_id = session['user']['id']
        # Retrieve the seller's car listings
        cars = self.seller_entity.get_seller_listings(seller_id)
        return render_template('seller_listings.html', cars=cars)

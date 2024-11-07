from used_car import UsedCar

class ViewCarController:
    def __init__(self):
        # Initialize the UsedCar entity
        self.used_car_entity = UsedCar()

    def view_cars(self):
        # Retrieve and display all used cars
        return self.used_car_entity.get_all_cars()

class CreateCarController:
    def __init__(self):
        self.used_car_entity = UsedCar()

    def create_car(self, make, model, year, price, description, agent_id, seller_id):
        # Create a new car listing
        return self.used_car_entity.create_car(make, model, year, price, description, agent_id, seller_id)

class UpdateCarController:
    def __init__(self):
        self.used_car_entity = UsedCar()
    def update_car(self, car_id, make, model, year, price, description, seller_id):
        return self.used_car_entity.update_car(car_id, make, model, year, price, description, seller_id)


class DeleteCarController:
    def __init__(self):
        self.used_car_entity = UsedCar()
    def delete_car(self, car_id):
        # Delete the specified car listing
        return self.used_car_entity.delete_car(car_id)

class SearchCarController:
    def __init__(self):
        self.used_car_entity = UsedCar()
    def search_cars(self, search_term):
        return self.used_car_entity.search_cars(search_term)


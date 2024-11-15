from user_profile import UserProfile

class ViewProfileController:
    def __init__(self):
        # Initialize the UserProfile entity, which interacts with the database
        self.user_profile_entity = UserProfile()

    def view_profiles(self):
        # Retrieve all user profiles from the entity and display them in the 'profiles.html' template
        return self.user_profile_entity.view_profiles()
    
class CreateProfileController:
    def __init__(self):
        self.user_profile_entity = UserProfile()

    def create_profile(self, profile_data):
        # Call entity to create the profile with provided data
        return self.user_profile_entity.create_profile(
            role=profile_data['role'],
            status=profile_data['status'],
            description=profile_data['description']
        )


class UpdateProfileController:
    def __init__(self):
        self.user_profile_entity = UserProfile()

    def update_profile(self, profile_id, profile_data):
        # Call entity to update the profile with provided data
        return self.user_profile_entity.update_profile(
            profile_id=profile_id,
            role=profile_data['role'],
            status=profile_data['status'],
            description=profile_data['description']
        )


class SuspendProfileController:
    def __init__(self):
        # Initialize the UserProfile entity, which interacts with the database
        self.user_profile_entity = UserProfile()

    def suspend_profile(self, profile_id):
        # Suspend a user profile by its ID
        return self.user_profile_entity.suspend_profile(profile_id)

    
class SearchProfileController:
    def __init__(self):
        # Initialize the UserProfile entity, which interacts with the database
        self.user_profile_entity = UserProfile()

    def search_profiles(self, search_term):
        return self.user_profile_entity.search_profiles(search_term)  # Retrieve matching profiles

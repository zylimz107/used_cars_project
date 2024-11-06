from flask import render_template, redirect, url_for, request, flash
from user_profile import UserProfile

class UserProfileController:
    def __init__(self):
        # Initialize the UserProfile entity, which interacts with the database
        self.user_profile_entity = UserProfile()

    def view_profiles(self):
        # Retrieve all user profiles from the entity and display them in the 'profiles.html' template
        profiles = self.user_profile_entity.get_all_profiles()
        return render_template('profiles.html', profiles=profiles)

    def create_profile(self):
        # Handles the creation of a new user profile
        if request.method == 'POST':
            role = request.form['role'].strip()  # Get and clean the role from the form
            status = request.form['status']      # Get the status from the form
            description = request.form['description'].strip()  # Get the description from the form

            try:
                # Check if a profile with the same role already exists
                existing_profile = self.user_profile_entity.get_profile_by_role(role)
                if existing_profile:
                    # If the role already exists, display an error message
                    flash('Role already exists. Please choose a different role.', 'error')
                    return render_template('create_profile.html')

                # Create the new profile if no conflicts
                self.user_profile_entity.create_profile(role, status, description)
                flash('Profile created successfully!', 'success')
                return redirect(url_for('view_profiles'))

            except Exception as e:
                # Handle any errors that may occur during profile creation
                flash(f'Error: {str(e)}', 'error')

        return render_template('create_profile.html')

    def update_profile(self, profile_id):
        # Handles updating an existing user profile
        profile = self.user_profile_entity.get_profile_by_id(profile_id)  # Get the profile by its ID

        if request.method == 'POST':
            role = request.form['role'].strip()  # Get the updated role from the form
            status = request.form['status']      # Get the updated status
            description = request.form['description'].strip()  # Get the updated description

            try:
                # Check if a profile with the updated role already exists
                existing_profile = self.user_profile_entity.get_profile_by_role(role)
                if existing_profile and existing_profile['profile_id'] != profile_id:
                    # If the role exists and it’s not the current profile being updated, show an error
                    flash('Role already exists. Please choose a different role.', 'error')
                    return render_template('edit_profile.html', profile=profile)

                # Update the profile with new details
                self.user_profile_entity.update_profile(profile_id, role, status, description)
                flash('Profile updated successfully!', 'success')
                return redirect(url_for('view_profiles'))

            except Exception as e:
                # Handle any errors that occur during profile update
                flash(f'Error updating profile: {str(e)}', 'error')

        return render_template('edit_profile.html', profile=profile)

    def suspend_profile(self, profile_id):
        # Suspend a user profile by its ID
        self.user_profile_entity.suspend_profile(profile_id)
        flash('Profile suspended successfully!')
        return redirect(url_for('view_profiles'))

    def search_profiles(self):
        # Search profiles based on role
        if request.method == 'POST':
            role = request.form['role']  # Get the role to search for
            profiles = self.user_profile_entity.search_profiles(role)  # Retrieve matching profiles
            return render_template('profiles.html', profiles=profiles)

        return render_template('search_profiles.html')

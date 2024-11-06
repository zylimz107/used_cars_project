from flask import render_template, redirect, url_for, request, flash, session
from review import Review

class ReviewController:
    def __init__(self):
        # Initialize the Review entity
        self.review_entity = Review()

    def view_agents(self):
        # Retrieve a list of active agents
        agents = self.review_entity.get_active_agents()
        return render_template('agents.html', agents=agents)

    def view_reviews(self, agent_id):
        # Get reviews associated with a specific agent
        reviews = self.review_entity.get_reviews_by_agent(agent_id)
        return render_template('agent_reviews.html', reviews=reviews, agent_id=agent_id)

    def submit_review(self, agent_id):
        if request.method == 'POST':
            # Extract review details from the form
            rating = int(request.form['rating'])
            review = request.form['review']
            user_id = session['user']['id']

            # Submit the review to the database
            self.review_entity.submit_review(agent_id, user_id, rating, review)
            flash('Thank you for your feedback!')
            return redirect(url_for('view_reviews', agent_id=agent_id))

        # Render the review submission form for the agent
        return render_template('submit_review.html', agent_id=agent_id)

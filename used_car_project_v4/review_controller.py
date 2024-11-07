from review import Review

class BuyerReviewController:
    def __init__(self):
        self.review_entity = Review()

    def submit_review(self, agent_id, user_id, rating, review):
        self.review_entity.submit_review(agent_id, user_id, rating, review)

class SellerReviewController:
    def __init__(self):
        self.review_entity = Review()

    def submit_review(self, agent_id, user_id, rating, review):
        self.review_entity.submit_review(agent_id, user_id, rating, review)

class AgentReviewController:
    def __init__(self):
        self.review_entity = Review()

    def view_reviews(self, agent_id):
        return self.review_entity.get_reviews_by_agent(agent_id)
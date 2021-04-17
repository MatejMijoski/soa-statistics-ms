from Repository.AchievementRepository import AchievementRepository
from Repository.AchievementCounterRepository import AchievementCounterRepository


class AchievementService:
    def __init__(self):
        self.achievement_repo = AchievementRepository()
        self.achievement_counter_repo = AchievementCounterRepository()

    def get_achievement(self, user_id):
        return self.achievement_repo.get_achievement_user(user_id)

    def update_achievement(self, invoice_body):
        return self.achievement_counter_repo.update_counter(invoice_body['user_id'],
                                                            invoice_body['type_of_product'],
                                                            invoice_body['quantity'])

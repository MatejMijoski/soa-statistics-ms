from Repository.AchievementRepository import AchievementRepository


class AchievementService:
    def __init__(self):
        self.achievement_repo = AchievementRepository()

    def get_achievement(self, id):
        return self.achievement_repo.get_achievement_by_id(id)

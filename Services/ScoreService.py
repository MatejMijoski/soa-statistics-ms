from Repository.ScoreRepository import ScoreRepository


class ScoreService:
    def __init__(self):
        self.score_repository = ScoreRepository()

    def get_monthly_score(self, limit):
        return self.score_repository.get_monthly_score(limit)

    def get_yearly_score(self, limit):
        return self.score_repository.get_yearly_score(limit)

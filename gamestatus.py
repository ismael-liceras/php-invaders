class GameStatus():
    def __init__(self):
        self.initial_time = 20
        self.bonus_invictus = 100
        self.bonus_prisoners = 200
        self.lives = None
        self.time = None
        self.stage = None
        self.score = None
        self.stage_score = None
        self.stage_invictus = None
        self.reset()

    def reset(self):
        self.lives = 3
        self.time = 0
        self.stage = 0
        self.score = 0
        self.stage_score = 0
        self.stage_invictus = True

    def set_stage(self, stage):
        self.stage = stage

    def get_stage(self):
        return self.stage

    def set_lives(self, lives):
        self.lives = lives

    def get_lives(self):
        return self.lives

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score

    def set_time(self, time):
        self.time = time

    def get_time(self):
        return self.time

    def add_bonus_time(self):
        self.score += self.time
        return self.time

    def add_bonus_invictus(self):
        self.score += self.bonus_invictus
        return self.bonus_invictus

    def add_bonus_prisoners(self, nprisoners):
        total_bonus_prisoners = (nprisoners * self.bonus_prisoners)
        self.score += total_bonus_prisoners
        return total_bonus_prisoners

    def add_score(self, score):
        self.score += score
        self.stage_score += score

    def run_1_sec(self):
        self.time -= 1
        return self.time

    def reset_time(self):
        self.time = self.initial_time

    def remove_life(self):
        self.lives -= 1
        return self.lives

    def get_stage_score(self):
        return self.stage_score

    def reset_stage_score(self):
        self.stage_score = 0

    def get_stage_invictus(self):
        return self.stage_invictus

    def set_stage_invictus(self, value):
        self.stage_invictus = value

    def reset_to_next_stage(self, stage):
        self.set_stage(stage)
        self.reset_time()
        self.set_stage_invictus(True)
        self.reset_stage_score()
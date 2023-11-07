class Warrior:
    def __init__(self):
        self.experience = 100
        self.achievements = []
        self.level = 1
        self.rank = "Pushover"

    def add_experience(self, points):
        cap = 10000
        if self.experience + points >= cap:
            self.experience = cap
        else:
            self.experience += points
        ranks = ["Pushover", "Novice", "Fighter", "Warrior", "Veteran", "Sage",
                 "Elite", "Conqueror", "Champion", "Master", "Greatest"]
        self.level = self.experience // 100
        self.rank = ranks[self.level // 10]

    # ach[0] = name, ach[1] = exp points, ach[2] = required lvl
    def training(self, ach):
        if not 1 <= ach[2] <= 100:
            return "Invalid level"
        elif self.level >= ach[2]:
            self.add_experience(ach[1])
            self.achievements.append(ach[0])
            return ach[0]
        else:
            return "Not strong enough"

    def battle(self, enemy_level):
        if not 1 <= enemy_level <= 100:
            return "Invalid level"
        elif enemy_level - self.level >= 5 and enemy_level // 10 > self.level // 10:
            return "You've been defeated"
        else:
            diff = enemy_level - self.level
            if enemy_level > self.level:
                self.add_experience(20 * diff * diff)
                return "An intense fight"
            elif diff >= -1:
                self.add_experience(10 + 5 * diff)
                return "A good fight"
            elif diff < -1:
                return "Easy fight"



class Agent:
    def __init__(self, role, hand):
        self.role = role
        self.hand = hand
        self.broken_tools = False
        self._known_goals = {"gold": None, "goals": []}

    def update_known_goals(self, coord, gold = False):
        if gold:
            self._known_goals["gold"] = coord
        else:
            self._known_goals["goal"] = coord
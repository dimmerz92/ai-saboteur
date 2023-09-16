import constants as C
from assets import IMG_PATH

class Card:
    def __init__(self, name, card_type, directions, gold = False):
        self.name = name
        self.type = card_type
        self.directions = directions
        self._img = self._set_img(name, gold)
        self._gold = gold

    def _set_img(self, name, gold):
        return IMG_PATH[name] + ("_GOLD" if gold else "")
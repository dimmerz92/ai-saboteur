import constants as C
from assets import IMG_PATH

class Card:
    def __init__(self, name, card_type, directions):
        self.name = name
        self.type = card_type
        self.directions = directions
        self.img = self._set_img(name)

    def _set_img(self, name):
        return IMG_PATH[name]
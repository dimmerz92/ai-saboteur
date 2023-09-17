from assets import IMG_PATH
import constants as C

class Card:
    def __init__(self, name: str, card_type: str, directions: list,
                 gold: bool = False):
        self.name = name
        self.type = card_type
        self.directions = directions
        self.img = self._set_img(name)
        self._gold = gold

    def _set_img(self, name: str) -> dict:
        """
        Returns a dictionary containing the path and rotation of the card image

            Parameters:
                name (str): a string

            Returns:
                img (Surface): a pygame image
        """
        return {"path": IMG_PATH[name], "angle": 0}
    
    def flip(self) -> None:
        """
        Flips a card from hidden position to visible
        """
        if self.name == "GOAL":
            if self._gold:
                self.name = "CROSS_ROAD_GOLD"
                self.img["path"] = IMG_PATH["CROSS_ROAD_GOLD"]
            else:
                self.name = "CROSS_ROAD"
                self.img["path"] = IMG_PATH["CROSS_ROAD"]

    def transpose(self, angle: int) -> None:
        """
        Transposes a card in 90 degree increments

            Parameters:
                angle (int): integer options 90, 180, 270
        """
        assert self.type == "PATH", \
            "Only PATH cards are transposable"
        
        assert angle in [90, 180, 270], \
            "Transpositions can only occur at 90, 180, or 270 degree increments"

        transpositions = angle // 90
        self.img["angle"] = angle
        for _ in range(transpositions):
            for i, dir in enumerate(self.directions):
                self.directions[i] = C.TRANSPOSE[dir]

    def is_gold(self) -> bool:
        """
        Checks whethere a card is gold

            Returns:
                (bool)
        """
        return self._gold
    
if __name__ == "__main__":
    card = Card("GOAL", "PATH", C.PATH_CARDS["CROSS_ROAD"]["PATH"])
    gold = Card("GOAL", "PATH", C.PATH_CARDS["CROSS_ROAD"]["PATH"], True)
    print(card.name, card.type, card.directions, card.img, card._gold)
    print(gold.name, gold.type, gold.directions, gold.img, gold._gold)
    card.flip()
    gold.flip()
    print(card.name, card.type, card.directions, card.img, card._gold)
    print(gold.name, gold.type, gold.directions, gold.img, gold._gold)

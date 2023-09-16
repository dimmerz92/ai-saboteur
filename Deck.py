from Card import Card
import constants as C
import random

class Deck:
    def __init__(self):
        self._deck = self._init_deck()

    def _init_deck(self):
        deck = []
        for key, value in C.ACTION_CARDS.items():
            for _ in range(value):
                deck.append(Card(key, "ACTION", None))

        for key, value in {**C.PATH_CARDS, **C.DEAD_END_CARDS}.items():
            for _ in range(value["QTY"]):
                deck.append(Card(key, "PATH", value["PATH"]))

        random.shuffle(deck)
        return deck
    
    def deal_hand(self, quantity):
        return [self._deck.pop() for _ in range(quantity)]
    
    @staticmethod
    def get_special_cards():
        cards = {
            "start": Card("CROSS_ROAD", "PATH", C.SPECIAL_CARDS["START"]["PATH"]),
            "goal": [],
            "hidden": []
        }

        gold = random.randint(0, len(C.GOAL_COORDS))

        for i in range(C.SPECIAL_CARDS["GOAL"]["QTY"]):
            cards["goal"].append(Card("CROSS_ROAD", "PATH", C.SPECIAL_CARDS["GOAL"]["PATH"], gold == i))
            cards["hidden"].append(Card("GOAL", "PATH", C.SPECIAL_CARDS["GOAL"]["PATH"], gold == i))
            
        return cards
    
if __name__ == "__main__":
    deck = Deck()
    print(deck.get_special_cards())
    print(deck.deal_hand(4))
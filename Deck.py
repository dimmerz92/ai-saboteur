from Card import Card
import constants as C
import random

class Deck:
    def __init__(self):
        self.deck = self._init_deck()
        self.goal_cards = Deck._get_special_cards()

    def _init_deck(self) -> list:
        """
        Initialises a deck of agent playable cards

            Returns:
                deck (list): a list of Card instances
        """
        deck = []
        for key, value in C.ACTION_CARDS.items():
            for _ in range(value):
                deck.append(Card(key, "ACTION", None))

        for key, value in {**C.PATH_CARDS, **C.DEAD_END_CARDS}.items():
            for _ in range(value["QTY"]):
                deck.append(Card(key, "PATH", value["PATH"]))

        random.shuffle(deck)
        return deck
    
    def _get_special_cards() -> dict:
        """
        Initialises the special cards (Start, gold, and goals)

            Returns:
                cards (dict): a dictionary
        """
        cards = {
            "start": Card(
                "CROSS_ROAD", "PATH", C.SPECIAL_CARDS["START"]["PATH"]),
            "goal": []
        }

        gold = random.randint(0, len(C.GOAL_COORDS))

        for i in range(C.SPECIAL_CARDS["GOAL"]["QTY"]):
            cards["goal"].append(Card(
                "GOAL","PATH",C.SPECIAL_CARDS["GOAL"]["PATH"], gold == i
                ))
            
        return cards
    
    def deal_hand(self, quantity: int) -> list:
        """
        Deals a starting hand

            Parameters:
                quantity (int): a positive nonzero integer
            
            Returns:
                cards (list): a list of Card instances
        """
        assert quantity > 0, \
            "Initial hand must be greater than zero"
        
        return [self.deck.pop() for _ in range(quantity)]
    
    def draw_card(self) -> Card:
        """
        Draws an agent playable card from the deck

        Returns:
            card (Card): an instance of Card
        """
        return self.deck.pop() if len(self.deck) > 0 else None
    
if __name__ == "__main__":
    deck = Deck()
    print(Deck._get_special_cards())
    print(deck.deal_hand(4))
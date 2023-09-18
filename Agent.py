from Card import Card

from typing import Callable
import heapq
import random

class Agent:
    def __init__(self, role: str, hand: list,
                 logic: Callable[[dict, list], dict]):
        self._role = role
        self._hand = hand
        self._logic = logic
        self.broken_tools = False
        self._known_goals = {"gold": None, "goals": []}

    def update_known_goals(self, coord: tuple, gold: bool = False) -> None:
        """
        Updates known goals if agent plays MAP card or goal is flipped

            Parameters:
                coord (tuple): a tuple of x, y ints
                gold (bool)
        """
        if gold:
            self._known_goals["gold"] = coord
        else:
            self._known_goals["goal"] = coord

    def remove_used_card(self, next_card):
        for i, card in enumerate(self._hand):
            if card.name == next_card.name:
                self._hand.pop(i)
                return

    def sense_think_act(self, game_state: dict, card: Card) -> dict|None:
        """
        Supplies the game_state percepts to the agent's think logic and returns
        the action

            Parameters:
                game_state (dict): a dictionary

            Returns:
                action (dict|None): a dictionary or None
        """
        # append drawn card to hand
        self._hand.append(card)

        # think
        if self.broken_tools:
            for card in self._hand:
                if card.name == "MEND":
                    return {"card": card, "target": self}
                
            if self._hand:
                self._hand.pop(random.randint(0, len(self._hand) - 1))

            return None

        internal_state = {
            "game_state": game_state,
            "hand": self._hand,
            "goals": self._known_goals
        }

        (min_heap, max_heap) = self._logic(internal_state)
        
        action = None
        if self._role == "SABOTAGE" and min_heap:
            result = heapq.heappop(min_heap)
            action = {"card": result[2][0], "target": result[2][1]}
            self.remove_used_card(action["card"])
        elif max_heap:
            result = heapq.heappop(max_heap)
            action = {"card": result[2][0], "target": result[2][1]}
            self.remove_used_card(action["card"])

        # act
        if not action:
            return None
        
        return action


    
if __name__ == "__main__":
    x = Agent("s",[], lambda x: x)
    x.print_self()
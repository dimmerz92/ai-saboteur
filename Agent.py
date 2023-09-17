from typing import Callable

class Agent:
    def __init__(self, role: str, hand: list, logic: Callable[[dict], dict]):
        self._role = role
        self._hand = hand
        self._logic = logic
        self.broken_tools = False
        self._known_goals = {"gold": None, "goals": []}

    def update_known_goals(self, coord: tuple, gold: bool = False) -> None:
        """
        Updates known goals if agent plays MAP card

            Parameters:
                coord (tuple): a tuple of x, y ints
                gold (bool)
        """
        if gold:
            self._known_goals["gold"] = coord
        else:
            self._known_goals["goal"] = coord

    def sense_think_act(self, game_state: dict) -> dict|None:
        """
        Supplies the game_state percepts to the agent's think logic and returns
        the action

            Parameters:
                game_state (dict): a dictionary

            Returns:
                action (dict|None): a dictionary or None
        """
        # think
        action = self._logic(game_state)

        # act
        if not action:
            return None
        
        return action
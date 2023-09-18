from Agent import Agent
from Card import Card
from Deck import Deck
from agent_logic import random_behaviour

from typing import Callable
from copy import deepcopy
import constants as C
import numpy as np
import random

ROLES = random.sample(C.ROLES, C.PLAYERS)

class Game:
    def __init__(self):
        self.deck = Deck()
        self.gameboard = self._init_gameboard(C.ROWS, C.COLS)
        self.agents = self._init_agents()
        self.turn = random.choice(list(self.agents.keys()))
        self.winner = None
        self.skipped = 0

    def _init_gameboard(self, rows: int, cols: int) -> np.ndarray:
        """
        Initialises an n x m 2D gameboard populated with None
        
            Parameters:
                rows (int): positive nonzero int
                cols (int): positive nonzero int

            Returns:
                gameboard (ndarray): a 2D numpy array of size (rows, cols)
        """
        gameboard = np.full((rows, cols), None)
        gameboard[C.START] = self.deck.goal_cards["start"]

        for i, coord in enumerate(C.GOAL_COORDS):
            gameboard[coord] = self.deck.goal_cards["goal"][i]

        return gameboard
    
    def _init_agents(self) -> dict:
        """
        Initialises dictionary of Agent objects based on length of ROLES

            Returns:
                agents (dict): a nested dictionary of Agents and their history
        """
        agents = {}
        for i, role in enumerate(ROLES):
            agents[f"agent-{i}"] = {
                "agent": Agent(role, self.deck.deal_hand(C.DEAL), random_behaviour),
                "history": []
            }
        
        return agents
    
    def whos_turn(self) -> Agent:
        return self.agents[self.turn]["agent"]
    
    @staticmethod
    def _valid_tunnel(game_state: np.ndarray, start_coords: tuple) -> bool:
        """
        Checks if a given coordinate corresponds to a valid tunnel back to the
        start
        
            Parameters:
                game_state (dict): a dictionary
                coords (tuple): a tuple containing 2 positive zero inclusive
                integers

            Returns:
                (bool)
        """
        gameboard = game_state["gameboard"]
        visited = []
        nodes = [start_coords]

        while nodes:
            node = nodes.pop()
            visited.append(node)

            for offset in C.DIRECTIONS.values():
                next_node = tuple(map(sum, zip(offset, node)))

                if next_node == C.START:
                    return True

                if (next_node < (0, 0) or next_node[0] > C.ROWS - 1 or
                    next_node[1] > C.COLS - 1):
                    continue

                next_cell = gameboard[next_node]
                if not next_cell:
                    continue
                elif "DE" in next_cell.name:
                    continue
                elif next_node not in visited:
                    nodes.append(next_node)

            if C.START in nodes:
                return True
            
        return False
    
    @staticmethod
    def get_valid_cells(game_state: dict) -> list:
        """
        Gets all valid, playable cells on the gameboard

            Parameters:
                game_state (dict): a dictionary

            Returns:
                neighbours (list): a list of x, y coordinate tuples
        """
        gameboard = game_state["gameboard"]
        neighbours = []

        for row in range(C.ROWS - 1):
            for col in range(C.COLS - 1):

                if not gameboard[(row, col)]:
                    continue

                card = gameboard[(row, col)]
                for dir in card.directions:
                    offset = C.DIRECTIONS[dir]
                    next_coord = tuple(map(sum, zip((row, col), offset)))

                    if (next_coord < (0, 0) or next_coord[0] > C.ROWS - 1 or
                        next_coord[1] > C.COLS - 1):
                        continue

                    next_cell = gameboard[next_coord]
                    if ((next_cell and "DE" in next_cell.name) or
                        not Game._valid_tunnel(game_state, next_coord)):
                        continue

                    neighbours.append(next_coord)

        return neighbours
    
    @staticmethod
    def is_valid_play(game_state: dict, card: Card,
                      target: tuple|Agent=None) -> bool:
        """
        Checks if a move is valid

            Parameters:
                game_state (dict): a dictionary
                card (Card): a Card object
                target (tuple|Agent): a tuple or Agent object, defaults to None

            Returns:
                (bool)
        """
        if card.name in ["SABOTAGE", "MEND"]:
            assert "agent" in target, \
                "The target for this card should be an agent identifier -> "\
                "'agent-\{i\}'"
            
            if card.name == "SABOTAGE":
                return not game_state["agents"][target]["agent"].broken_tools
            else:
                return game_state["agents"][target]["agent"].broken_tools
        
        gameboard = game_state["gameboard"]
        cell = gameboard[target]
        if card.name == "MAP":
            if cell:
                return cell.name == "GOAL"
            else:
                return False
        elif card.name == "DYNAMITE":
            if cell:
                return cell.name not in C.SPECIAL_CARDS.keys()
            else:
                return False
        
        if gameboard[target]:
            return False
            
        checks = []
        for dir, offset in C.DIRECTIONS.items():
            next_coord = tuple(map(sum, zip(target, offset)))

            if (next_coord < (0, 0) or next_coord[0] > C.ROWS - 1 or
                next_coord[1] > C.COLS - 1):
                continue

            next_cell = gameboard[next_coord]
            if not next_cell:
                checks.append(None)
            elif next_cell.name in ["START", "GOAL"] and "DE" in card.name:
                return False
            elif ((dir in card.directions and
                   C.COMPLEMENT[dir] not in next_cell.directions) or
                  (dir not in card.directions and 
                   C.COMPLEMENT[dir] in next_cell.directions)):
                return False
            else:
                checks.append(True)
            
        return True in checks
    
    @staticmethod
    def _next_turn(game_state: dict) -> str:
        """
        Returns the string identifier of the next Agent object's turn

            Parameters:
                game_state (dict): a dictionary

            Returns:
                agent (str): a string
        """
        current_agent = game_state["turn"]
        current_index = list(game_state["agents"].keys()).index(current_agent)
        next = current_index + 1 if current_index + 1 < len(ROLES) else 0

        return list(game_state["agents"].keys())[next]
    
    @staticmethod
    def _is_terminal(game_state: dict, coord: tuple) -> bool:
        """
        Checks if the game is in a terminal/finished state

            Parameters:
                game_state (dict): a dictionary
                coord (tuple): a tuple containing 2 positive zero inclusive
                integers

            Returns:
                (bool)
        """
        if game_state["skipped"] == len(ROLES):
            return True
        
        if not game_state["gameboard"][coord]:
            return False
        
        card = game_state["gameboard"][coord]
        for dir in card.directions:
            offset = C.DIRECTIONS[dir]
            next_coord = tuple(map(sum, zip(coord, offset)))

            if (next_coord < (0, 0) or next_coord[0] > C.ROWS - 1 or
                next_coord[1] > C.COLS - 1):
                continue

            if not game_state["gameboard"][next_coord]:
                continue

            next_cell = game_state["gameboard"][next_coord]
            if next_cell.name == "GOAL":
                next_cell.flip()

                if next_cell.is_gold():
                    return True
                
        return False
    
    def get_percepts(self) -> dict:
        """
        Returns a copy of the current game_state

            Returns:
                game_state (dict): a dictionary
        """
        return {
            "gameboard": self.gameboard.copy(),
            "agents": deepcopy(self.agents),
            "turn": self.turn,
            "winner": self.winner,
            "skipped": self.skipped
        }
    
    def draw(self) -> Card:
        """
        Draws a card from the deck and checks if the deck is empty

            Returns:
                card (Card): an instance of Card class
        """
        card = self.deck.draw_card()
        if not card:
            self.winner = "SABOTAGE"

        return card

    
    @staticmethod
    def transition_result(game_state: dict, action: dict) -> dict:
        """
        Returns a new game state after an agent move

            Parameters:
                game_state (dict): a dictionary
                action (dict): a dictionary {card: Card, target: str|tuple}

            Returns:
                new_game_state (dict): a dictionary
        """
        new_game_state = deepcopy(game_state)
        if not action:
            new_game_state["skipped"] += 1
            return new_game_state
        
        card = action["card"]
        target = action["target"]

        assert Game.is_valid_play(new_game_state, card, target), \
            f"This is not a valid play\n{action}"
        
        if card.name in ["SABOTAGE", "MEND"]:
            assert isinstance(target, str) and "agent" in target, \
                "The target for this card should be an agent identifier -> "\
                "'agent-\{i\}'"
            
            if card.name == "SABOTAGE":
                new_game_state["agents"][target]["agent"].broken_tools = True
            else:
                new_game_state["agents"][target]["agent"].broken_tools = False
            
            new_game_state["turn"] = Game._next_turn(new_game_state)

            return new_game_state

        assert (isinstance(target, tuple) and len(target) == 2 and
                   all(isinstance(v, int) for v in target) and
                   target >= (0, 0) and target[0] <= C.ROWS - 1 and
                   target[1] <= C.COLS - 1), \
            f"The target must be a tuple of len 2 with integers in the "\
                "gameboard bounds: (0, 0) and ({C.ROWS - 1}, {C.COLS - 1})"
        
        agent = new_game_state["agents"][new_game_state["turn"]]
        if card.name == "MAP":
            gold = new_game_state["gameboard"][target].is_gold()
            agent["agent"].update_known_goals(target, gold)
        else:
            assert target in Game.get_valid_cells(new_game_state), \
                f"Target coords are not in the list of valid cells"
            if card.name == "DYNAMITE":
                new_game_state["gameboard"][target] = None
            else:
                new_game_state["gameboard"][target] = card
        
        if Game._is_terminal(new_game_state, target):
            new_game_state["winner"] = agent["agent"].role
        else:
            new_game_state["agents"][new_game_state["turn"]]["history"].append(
                card.name)
            new_game_state["turn"] = Game._next_turn(new_game_state)

        return new_game_state
    
    def state_transition(self, action: dict,
                         _callback: Callable[[tuple],None]) -> None:
        """
        Transitions the state of the Game object

            Parameters:
                action (dict): a dictionary {card: Card, target: str|tuple}
        """
        if not action:
            self.skipped += 1
            return
        
        card = action["card"]
        target = action["target"]
        game_state = self.get_percepts()
      
        if card.name in ["SABOTAGE", "MEND"]:
            _callback((target, card))
            pass
        elif card.name in ["MAP", "DYNAMITE"]:
            _callback((target, card))
            pass

        new_game_state = Game.transition_result(game_state, action)
        self.gameboard = new_game_state["gameboard"]
        self.turn = new_game_state["turn"]
        self.winner = new_game_state["winner"]
        
if __name__ == "__main__":
    game = Game()
    state = game.get_percepts()
    #print(game.turn)
    # print(game.agents)
    #crrd = Card("CROSS_ROAD", "PATH", C.PATH_CARDS["CROSS_ROAD"]["PATH"])
    lnr = Card("LINEAR", "PATH", C.PATH_CARDS["LINEAR"]["PATH"])
    lnr.transpose(90)
    # game.gameboard[(6,11)] = crrd
    # # print(game.gameboard)
    # print(Game.get_valid_cells(game.get_percepts()["gameboard"]))
    #print(crrd.name, crrd.type, crrd.directions)
    # print(Game._valid_tunnel(game.get_percepts()["gameboard"], (6,11)))
    # print(Game.is_valid_play(game.get_percepts()["gameboard"], crrd, (6,12)))
    # print(game.get_percepts())
    # print(Game._next_turn(game.get_percepts()))
    #print(Game.transition_result(state, {"card": lnr, "target": (6,11)}))
    print(game.turn)
    game.state_transition({"card": lnr, "target": (6,11)})
    print(game.gameboard)
    print(game.turn)

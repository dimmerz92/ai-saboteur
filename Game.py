# AGENT
from Deck import Deck
from Card import Card
import constants as C
import numpy as np
import random

ROLES = random.sample(C.ROLES, C.PLAYERS)

class Game:
    def __init__(self):
        self.deck = Deck()
        self.gameboard = self._init_gameboard(C.ROWS, C.COLS)
        #self.agents = self._init_agents()
        #self.turn = random.choice(self.agents)

    def _init_gameboard(self, rows, cols):
        gameboard = np.full((rows, cols), None)
        gameboard[C.START] = self.deck._goal_cards["start"]

        for i, coord in enumerate(C.GOAL_COORDS):
            gameboard[coord] = self.deck._goal_cards["hidden"][i]

        return gameboard
    
    def _init_agents(self):
        pass

    def get_percepts(self):
        return {
            "gameboard": self.gameboard.copy(),
            #"turn": self.turn
        }
    
    def _valid_tunnel(game_state, coords):
        visited = []
        nodes = [coords]

        while nodes:
            node = nodes.pop()
            visited.append(node)

            for offset in C.DIRECTIONS.values():
                next_node = tuple(map(sum, zip(offset, node)))

                if next_node < (0, 0) or next_node > (C.ROWS - 1, C.COLS - 1):
                    continue

                next_cell = game_state[next_node]
                if next_cell and not node == coords:
                    if not Game.is_valid_play(game_state, next_cell, next_node):
                        continue
                
                if (next_cell and next_node not in visited):
                    nodes.append(next_node)

            if C.START in nodes:
                return True
            
        return False

    def get_valid_cells(game_state):
        neighbours = []

        for row in range(C.ROWS - 1):
            for col in range(C.COLS - 1):

                if not game_state[(row, col)]:
                    continue

                card = game_state[(row, col)]
                for dir in card.directions:
                    offset = C.DIRECTIONS[dir]
                    next_coord = tuple(map(sum, zip((row, col), offset)))

                    if (next_coord < (0, 0) or
                        next_coord > (C.ROWS - 1, C.COLS - 1)):
                        continue

                    next_cell = game_state[next_coord]
                    if (next_cell or
                        not Game._valid_tunnel(game_state, next_coord)):
                        continue
                    neighbours.append(next_coord)

        return neighbours
    
    def is_valid_play(game_state, card, coords=None):
        if card.name in ["SABOTAGE", "MEND"]:
            # add later
            return False
        
        target = game_state[coords]
        if card.name == "MAP":
            if target:
                return target.name == "GOAL"
            else:
                return False
        elif card.name == "DYNAMITE":
            if target:
                return target.name not in C.SPECIAL_CARDS.keys()
            else:
                return False
        
        checks = []
        for dir in card.directions:
            offset = C.DIRECTIONS[dir]
            next_coord = tuple(map(sum, zip(coords, offset)))

            if next_coord < (0, 0) or next_coord > (C.ROWS - 1, C.COLS - 1):
                continue

            next_cell = game_state[next_coord]
            if not next_cell:
                checks.append(None)
            elif C.COMPLEMENT[dir] not in next_cell.directions:
                return False
            else:
                checks.append(True)
            
        return True in checks



    
if __name__ == "__main__":
    game = Game()
    crrd = Card("CROSS_ROAD", "PATH", C.PATH_CARDS["CROSS_ROAD"]["PATH"])
    game.gameboard[(6,11)] = crrd
    # print(game.gameboard)
    print(Game.get_valid_cells(game.get_percepts()["gameboard"]))
    print(crrd.name, crrd.type, crrd.directions)
    print(Game._valid_tunnel(game.get_percepts()["gameboard"], (6,11)))
    print(Game.is_valid_play(game.get_percepts()["gameboard"], crrd, (6,13)))
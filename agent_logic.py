from Game import Game

import constants as C
from copy import deepcopy
import random
import heapq

def manhattan_distance(coord: tuple, goal: tuple) -> int:
    return abs(coord[0] - goal[0]) + abs(coord[1] - goal[1])

def score_agents(agents):
    agent_scores = {}
    score = 0

    for key, value in agents.items():
        if not value["history"]:
            continue
        for card in value["history"]:
            score += C.ALL_PLAYABLE_CARDS[card]["SCORE"]
            
        agent_scores[key] = score / len(value["history"])
        score = 0
    
    return agent_scores

# I don't really plan on developing this feature, it's just a test to ensure
# that all the classes are interacting properly. Use of this logic over a
# longer period of time will likely end in something breaking or an infinite
# while loop
def random_behaviour(internal_state: dict) -> dict:
    game_state = internal_state["game_state"]
    hand = internal_state["hand"]
    valid_cells = Game.get_valid_cells(game_state)
    agents = list(game_state["agents"].keys())
    action = None

    while not action:
        card = random.choice(hand)
        if card.name in ["SABOTAGE", "MEND"]:
            agent = random.choice(agents)
            if Game.is_valid_play(game_state, card, agent):
                return {"card": card, "target": agent}
            else:
                continue

        for cell in valid_cells:
            if Game.is_valid_play(game_state, card, cell):
                return {"card": card, "target": cell}
            
def intelligent_behaviour(internal_state: dict) -> dict:
    game_state = internal_state["game_state"]
    hand = internal_state["hand"]
    goals = internal_state["goals"]
    valid_cells = Game.get_valid_cells(game_state)
    agents = game_state["agents"]
    goal = float("Inf")
    agent_scores = score_agents(agents)

    max_heap = []
    min_heap = []

    mend_checked = False
    sabotage_checked = False

    # determine best goal for manhattan distance
    if goals["gold"]:
        goal = goals["gold"]
    else:
        goal = random.choice(list(set(C.GOAL_COORDS) - set(goals["goals"])))

    for card in hand:
        if card.name == "MEND" and not mend_checked and agent_scores:
            for key, value in agents.items():
                if (value["agent"].broken_tools and key in agent_scores and
                    Game.is_valid_play(game_state, card, key)):
                    heapq.heappush(min_heap, (agent_scores[key],
                                              id((key, value)),
                                              (card, key)))
                    heapq.heappush(max_heap, (-agent_scores[key],
                                              id((key, value)),
                                              (card, key)))

        if card.name == "SABOTAGE" and not sabotage_checked and agent_scores:
            for key, value in agents.items():
                if (key in agent_scores and
                    Game.is_valid_play(game_state, card, key)):
                    heapq.heappush(min_heap, (agent_scores[key],
                                              id((key, value)),
                                              (card, key)))
                    heapq.heappush(max_heap, (-agent_scores[key],
                                              id((key, value)),
                                              (card, key)))
        
        else:
            for coord in valid_cells:
                dist = manhattan_distance(coord, goal)
                heuristic = C.DIST_MAX / dist * 0.25
                if (card.name in ["MAP", "DYNAMITE"] and
                    Game.is_valid_play(game_state, card, coord)):
                    score = C.ACTION_CARDS[card.name]["SCORE"] / heuristic
                    heapq.heappush(min_heap, (score, id((coord, card)),
                                              (card, coord)))
                    heapq.heappush(max_heap,(-score, id((coord, card)),
                                             (card, coord)))
                    
                elif card.name in {**C.PATH_CARDS, **C.DEAD_END_CARDS}.keys():
                    new_card = deepcopy(card)
                    for rot in [0, 90, 180, 270]:
                        if rot > 0:
                            new_card.transpose(rot)
                        if not Game.is_valid_play(game_state, card, coord):
                            continue
                        heapq.heappush(min_heap,(heuristic,
                                                 id((card, coord, rot)),
                                                 (card, coord)))
                        heapq.heappush(max_heap,(-heuristic,
                                                 id((card, coord, rot)),
                                                 (card, coord)))
                    
    return (min_heap, max_heap)

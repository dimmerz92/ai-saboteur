import random

def random_behaviour(game_state: dict, hand: list) -> dict:
    from Game import Game
    valid_cells = Game.get_valid_cells(game_state)
    print(valid_cells)
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
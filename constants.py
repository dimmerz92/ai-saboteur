ROWS = 20
COLS = 20
GOALS = 3
DEAL = 4

START = (6, 10)
GOAL_COORDS = [(14, 8), (14, 10), (14, 12)]

ROLES = ["DIG"] * 6 + ["SAB"] * 3
PLAYERS = 8

DIRECTIONS = {
    "NORTH": (-1, 0),
    "SOUTH": (1, 0),
    "EAST": (0, 1),
    "WEST": (0, -1)
}

COMPLEMENT = {
    "NORTH": "SOUTH",
    "SOUTH": "NORTH",
    "EAST": "WEST",
    "WEST": "EAST"
}

TRANSPOSE = {
    "NORTH": "WEST",
    "SOUTH": "EAST",
    "EAST": "NORTH",
    "WEST": "SOUTH"
}

ACTION_CARDS = {
    "MAP": {"QTY": 6, "SCORE": 4},
    "DYNAMITE": {"QTY": 3, "SCORE": 2},
    "SABOTAGE": {"QTY": 9, "SCORE": -4},
    "MEND": {"QTY": 9, "SCORE": 4}
}

PATH_CARDS = {
    "CORNER": {"PATH": ["SOUTH", "EAST"], "QTY": 9, "SCORE": 2},
    "CROSS_ROAD": {"PATH": ["NORTH", "SOUTH", "EAST", "WEST"], "QTY": 1,
                   "SCORE": 4},
    "JUNCTION": {"PATH": ["WEST", "SOUTH", "EAST"], "QTY": 10, "SCORE": 3},
    "LINEAR": {"PATH": ["NORTH", "SOUTH"], "QTY": 7, "SCORE": 2}
}

SPECIAL_CARDS = {
    "GOAL": {"PATH": ["NORTH", "SOUTH", "EAST", "WEST"], "QTY": 3},
    "START": {"PATH": ["NORTH", "SOUTH", "EAST", "WEST"], "QTY": 1}
}

DEAD_END_CARDS = {
    "CORNER_DE": {"PATH": ["SOUTH", "EAST"], "QTY": 1, "SCORE": -10},
    "CROSS_ROAD_DE": {"PATH": ["NORTH", "SOUTH", "EAST", "WEST"], "QTY": 1,
                      "SCORE": -10},
    "SINGLE_DE": {"PATH": ["SOUTH"], "QTY": 1, "SCORE": -10},
    "JUNCTION_DE": {"PATH": ["WEST", "SOUTH", "EAST"], "QTY": 1, "SCORE": -10},
    "LINEAR_DE": {"PATH": ["NORTH", "SOUTH"], "QTY": 1, "SCORE": -10}
}

ALL_PLAYABLE_CARDS = {**ACTION_CARDS, **PATH_CARDS, **DEAD_END_CARDS}
ACTION_MIN = min([v["SCORE"] for v in ACTION_CARDS.values()])
ACTION_MAX = max([v["SCORE"] for v in ACTION_CARDS.values()])
PATH_MIN = min([v["SCORE"] for v in {**PATH_CARDS, **DEAD_END_CARDS}.values()])
PATH_MAX = max([v["SCORE"] for v in {**PATH_CARDS, **DEAD_END_CARDS}.values()])
DIST_MAX = ROWS + COLS
DIST_MIN = 1

CELL_SIZE = 50
INFO_SIZE = 35
HAND_SIZE = 50
WINDOW_SIZE = (COLS * CELL_SIZE, ROWS * CELL_SIZE + INFO_SIZE + HAND_SIZE)
FPS = 30
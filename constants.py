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
    "MAP": 6,
    "DYNAMITE": 3,
    "SABOTAGE": 9,
    "MEND": 9
}

PATH_CARDS = {
    "CORNER": {"PATH": ["SOUTH", "EAST"], "QTY": 9},
    "CROSS_ROAD": {"PATH": ["NORTH", "SOUTH", "EAST", "WEST"], "QTY": 1},
    "JUNCTION": {"PATH": ["WEST", "SOUTH", "EAST"], "QTY": 10},
    "LINEAR": {"PATH": ["NORTH", "SOUTH"], "QTY": 7}
}

SPECIAL_CARDS = {
    "GOAL": {"PATH": ["NORTH", "SOUTH", "EAST", "WEST"], "QTY": 3},
    "START": {"PATH": ["NORTH", "SOUTH", "EAST", "WEST"], "QTY": 1}
}

DEAD_END_CARDS = {
    "CORNER_DE": {"PATH": ["SOUTH", "EAST"], "QTY": 1},
    "CROSS_ROAD_DE": {"PATH": ["NORTH", "SOUTH", "EAST", "WEST"], "QTY": 1},
    "SINGLE_DE": {"PATH": ["SOUTH"], "QTY": 1},
    "JUNCTION_DE": {"PATH": ["WEST", "SOUTH", "EAST"], "QTY": 1},
    "LINEAR_DE": {"PATH": ["NORTH", "SOUTH"], "QTY": 1}
}

CELL_SIZE = 50
INFO_SIZE = 35
HAND_SIZE = 50
WINDOW_SIZE = (COLS * CELL_SIZE, ROWS * CELL_SIZE + INFO_SIZE + HAND_SIZE)
FPS = 30
import enum


class SquareStates(enum.Enum):
    EMPTY = 1
    X = 2
    O = 3


class GameStates(enum.Enum):
    XWIN = 1
    OWIN = 2
    DRAW = 3
    INVALID_SCREEN = 4
    GOING_ON = 5

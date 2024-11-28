from enum import Enum


class PlayerID(Enum):
    O = 1  # For O player
    X = 2  # For x player
    N = 3  # If nobody still has played this
    F = 4  # If a big grid is full

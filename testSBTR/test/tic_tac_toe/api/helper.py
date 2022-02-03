class Enumerate:
    values = {}

    @classmethod
    def choices(cls):
        return cls.values.items()


class GameEnum(Enumerate):
    RUNNING = "RUNNING"
    X_WON = "X_WON"
    O_WON = "O_WON"
    DRAW = "DRAW"

    values = {
        RUNNING: "The game is running!",
        X_WON: "Player X won the game!",
        O_WON: "Player O won the game!",
        DRAW: "The game is not active.",
    }


class PlayerEnum(Enumerate):
    X = "X"
    O = "O"
    NOBODY = "NOBODY"

    values = {X: "Player is X", O: "Player is O", NOBODY: "Player is Nobody"}

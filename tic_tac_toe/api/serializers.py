from collections import Counter

from rest_framework import serializers

from api.core import make_move, choose_side, get_move, is_winner, is_board_full
from api.helper import PlayerEnum, GameEnum
from api.models import Game


class GameSerializer(serializers.ModelSerializer):
    game_id = serializers.UUIDField(
        format="hex_verbose", required=False, read_only=True
    )
    board = serializers.CharField(required=False)
    status = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = Game
        fields = (
            "game_id",
            "board",
            "status",
        )

    def check_order(self, board):
        for idx in range(9):
            if (
                str(idx) != board[idx]
                and board[idx] != PlayerEnum.X
                and board[idx] != PlayerEnum.O
            ):
                raise serializers.ValidationError("Order is wrong!")

    def validate(self, data):
        data = super().validate(data)
        required_board_cells = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
        if data.get("board"):
            board = data["board"].upper()
            self.check_order(list(board))
            cells_counter = Counter(board)
            self.validate_basics(board, cells_counter, required_board_cells)
        return data

    def validate_basics(self, *args):
        raise NotImplemented


class StartGameSerializer(GameSerializer):
    def validate_basics(self, board, cells_counter, required_board_cells):
        msg = "Invalid cell`s number"
        if any(elem for elem in cells_counter if cells_counter[elem] > 1):
            raise serializers.ValidationError(msg)
        if cells_counter[PlayerEnum.X] and cells_counter[PlayerEnum.O]:
            raise serializers.ValidationError(msg)
        if not any(cell in required_board_cells for cell in board):
            raise serializers.ValidationError(msg)
        if not any(cell in [PlayerEnum.X, PlayerEnum.O] for cell in board):
            raise serializers.ValidationError("No X or O on the board")
        if len(board) != 9:
            raise serializers.ValidationError("Not enough cells on the board")

    def create(self, validated_data):
        self.start_game(validated_data)
        return super().create(validated_data)

    def start_game(self, validated_data):
        board = validated_data.get("board")
        if board:
            board = list(board.upper())
            ai = PlayerEnum.O if PlayerEnum.X in board else PlayerEnum.X
        else:
            ai = choose_side()
            board = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
        move = get_move(board, ai)
        make_move(board, ai, move)
        validated_data["board"] = "".join(board)
        validated_data["player"] = PlayerEnum.X if ai == PlayerEnum.O else PlayerEnum.O
        validated_data["status"] = GameEnum.RUNNING


class PlayGameSerializer(GameSerializer):
    def validate_basics(self, *args):
        if self.instance.status != GameEnum.RUNNING:
            raise serializers.ValidationError("Game over!")

    def update(self, instance, validated_data):
        new_board = list(validated_data["board"].upper())
        if is_winner(new_board, instance.player):
            status = (
                GameEnum.O_WON if instance.player == PlayerEnum.O else GameEnum.X_WON
            )
            validated_data["board"] = "".join(new_board)
            validated_data["status"] = status
        if is_board_full(new_board):
            validated_data["board"] = "".join(new_board)
            validated_data["status"] = GameEnum.DRAW
        else:
            board = list(instance.board)
            ai = PlayerEnum.X if instance.player == PlayerEnum.O else PlayerEnum.O
            self.validate_players_move(new_board, board, ai)
            move = get_move(new_board, ai)
            make_move(new_board, ai, move)
            validated_data["board"] = "".join(new_board)
            if is_winner(new_board, ai):
                validated_data["status"] = (
                    GameEnum.O_WON if ai == PlayerEnum.O else GameEnum.X_WON
                )
            if is_board_full(new_board):
                validated_data["status"] = GameEnum.DRAW
        return super().update(instance, validated_data)

    def validate_players_move(self, new_board, board, ai):
        msg = "Your move is wrong!"
        steps = list(self.get_player_steps(new_board, board))
        if len(steps) > 1 or len(steps) == 0:
            raise serializers.ValidationError(msg)
        board_dict = {str(idx): val for idx, val in enumerate(list(new_board))}
        if board_dict[steps[0]] == ai:
            raise serializers.ValidationError(msg)

    def get_player_steps(self, new_board, board):
        new_board = set(new_board)
        board = set(board)
        steps = board - new_board
        return steps

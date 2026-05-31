"""
Phase 2 - Automatic Threes solver using a fixed movement cycle.

The strategy repeatedly tries moves in this order:
Left -> Down -> Right -> Up

It keeps applying each direction while the board changes, stops when it uses all
placements, or stops earlier if the game is over.
"""

from threes_core import (
    apply_move,
    copy_board,
    insert_tile_after_move,
    is_game_over,
    print_board,
    print_score_status,
    read_board,
    read_placements,
)

MOVE_CYCLE = ("L", "D", "R", "U")


def main() -> None:
    board = read_board()
    placement_count = int(input())
    placements = read_placements(placement_count)

    move_sequence = ""
    placement_index = 0

    while len(move_sequence) < placement_count and not is_game_over(board):
        for direction in MOVE_CYCLE:
            previous_board = None

            while (
                previous_board != board
                and len(move_sequence) < placement_count
                and not is_game_over(board)
            ):
                previous_board = copy_board(board)
                apply_move(board, direction)

                if board != previous_board:
                    insert_tile_after_move(board, direction, placements[placement_index])
                    placement_index += 1
                    move_sequence += direction

    print(move_sequence)
    print_board(board)
    print_score_status(board)


if __name__ == "__main__":
    main()

"""
Phase 1 - Replay a given sequence of Threes moves.

Input format:
1. Board size n
2. n lines of board values
3. A string of moves, for example: LDRU
4. One placement line for each successful move in the move string

The script applies the given moves, inserts new tiles only when a move changes
something, prints the final board, and prints the partial/final score.
"""

from threes_core import (
    apply_move,
    copy_board,
    insert_tile_after_move,
    print_board,
    print_score_status,
    read_board,
    read_placements,
)


def main() -> None:
    board = read_board()
    move_sequence = input().strip()
    placements = read_placements(len(move_sequence))

    placement_index = 0

    for direction in move_sequence:
        previous_board = copy_board(board)
        apply_move(board, direction)

        # A new tile is inserted only if the board actually changed.
        if board != previous_board:
            insert_tile_after_move(board, direction, placements[placement_index])
            placement_index += 1

    print_board(board)
    print_score_status(board)


if __name__ == "__main__":
    main()

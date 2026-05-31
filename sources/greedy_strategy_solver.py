"""
Phase 3 - Automatic Threes solver using a greedy strategy.

For each turn, the script tests Left, Down, Right, and Up. It chooses the move
that creates the largest merged tile. If multiple directions are tied, it keeps
the original priority order: Left, Down, Right, Up.
"""

from threes_core import (
    apply_move,
    best_greedy_direction,
    copy_board,
    insert_tile_after_move,
    is_game_over,
    print_board,
    print_score_status,
    read_board,
    read_placements,
)


def main() -> None:
    board = read_board()
    placement_count = int(input())
    placements = read_placements(placement_count)

    move_sequence = ""
    placement_index = 0

    while len(move_sequence) < placement_count and not is_game_over(board):
        direction = best_greedy_direction(board)
        previous_board = copy_board(board)
        apply_move(board, direction)

        if board != previous_board:
            insert_tile_after_move(board, direction, placements[placement_index])
            placement_index += 1
            move_sequence += direction
        else:
            # Safety stop: if the selected move cannot change the board, avoid
            # an infinite loop. This should happen only in unusual edge cases.
            break

    print(move_sequence)
    print_board(board)
    print_score_status(board)


if __name__ == "__main__":
    main()

"""
Core helper functions for the Threes puzzle project.

The original project had the same board movement, tile insertion, scoring,
and game-over logic repeated in several phase files. This module keeps the
shared logic in one place so the phase scripts are easier to read.
"""

from copy import deepcopy
from typing import List, Tuple

Board = List[List[int]]
Placement = Tuple[int, int]  # (index_seed, tile_value)

DIRECTIONS = ("L", "D", "R", "U")


def copy_board(board: Board) -> Board:
    # Return a separate copy of the board so moves can be tested safely.
    return deepcopy(board)


def can_merge(left_tile: int, right_tile: int) -> bool:
    # Return True when two adjacent tiles can merge in Threes.

    # Rules used by the original code:
    # - 1 and 2 merge into 3.
    # - Tiles 3 and above merge only with the same value.
    
    if left_tile == 0 or right_tile == 0:
        return False
    if left_tile + right_tile == 3:
        return True
    return left_tile > 2 and left_tile == right_tile


def merged_value(left_tile: int, right_tile: int) -> int:
    # Return the resulting tile after merging two valid Threes tiles.
    if left_tile + right_tile == 3:
        return 3
    return left_tile + right_tile


def slide_cell(board: Board, target_row: int, target_col: int, source_row: int, source_col: int) -> int:
    # Move or merge one source cell into one target cell.

    # Returns the value created by a merge. A normal slide into an empty cell
    # returns 0 because it does not create a new merged tile.
    
    target = board[target_row][target_col]
    source = board[source_row][source_col]

    if source == 0:
        return 0

    if target == 0:
        board[target_row][target_col] = source
        board[source_row][source_col] = 0
        return 0

    if can_merge(target, source):
        new_value = merged_value(target, source)
        board[target_row][target_col] = new_value
        board[source_row][source_col] = 0
        return new_value

    return 0


def move_left(board: Board) -> Board:
    # Apply one left move to the board, modifying and returning it.
    size = len(board)
    for row in range(size):
        for col in range(size - 1):
            slide_cell(board, row, col, row, col + 1)
    return board


def move_right(board: Board) -> Board:
    # Apply one right move to the board, modifying and returning it.
    size = len(board)
    for row in range(size):
        for col in range(size - 1, 0, -1):
            slide_cell(board, row, col, row, col - 1)
    return board


def move_up(board: Board) -> Board:
    # Apply one upward move to the board, modifying and returning it.
    size = len(board)
    for row in range(size - 1):
        for col in range(size):
            slide_cell(board, row, col, row + 1, col)
    return board


def move_down(board: Board) -> Board:
    # Apply one downward move to the board, modifying and returning it.
    size = len(board)
    for row in range(size - 1, 0, -1):
        for col in range(size):
            slide_cell(board, row, col, row - 1, col)
    return board


def apply_move(board: Board, direction: str) -> Board:
    # Apply one move in the requested direction.
    if direction == "L":
        return move_left(board)
    if direction == "R":
        return move_right(board)
    if direction == "U":
        return move_up(board)
    if direction == "D":
        return move_down(board)
    raise ValueError(f"Unknown direction: {direction!r}")


def insert_tile_after_move(board: Board, direction: str, placement: Placement) -> Board:
    # Insert the next tile on the edge opposite to the move direction.

    # The input placement contains an index seed and a tile value. The seed is
    # converted with modulo over the available empty edge cells, matching the
    # behavior of the original project.

    index_seed, tile_value = placement
    size = len(board)

    if direction == "U":
        empty_columns = [col for col in range(size) if board[size - 1][col] == 0]
        if empty_columns:
            board[size - 1][empty_columns[index_seed % len(empty_columns)]] = tile_value

    elif direction == "D":
        empty_columns = [col for col in range(size) if board[0][col] == 0]
        if empty_columns:
            board[0][empty_columns[index_seed % len(empty_columns)]] = tile_value

    elif direction == "R":
        empty_rows = [row for row in range(size) if board[row][0] == 0]
        if empty_rows:
            board[empty_rows[index_seed % len(empty_rows)]][0] = tile_value

    elif direction == "L":
        empty_rows = [row for row in range(size) if board[row][size - 1] == 0]
        if empty_rows:
            board[empty_rows[index_seed % len(empty_rows)]][size - 1] = tile_value

    return board


def is_game_over(board: Board) -> bool:
    # Return True when no empty cell and no legal merge remain.
    size = len(board)

    for row in board:
        if 0 in row:
            return False

    for row in range(size):
        for col in range(size):
            current = board[row][col]
            if row + 1 < size and can_merge(current, board[row + 1][col]):
                return False
            if col + 1 < size and can_merge(current, board[row][col + 1]):
                return False

    return True


def calculate_tile_score(tile: int) -> int:
    # Calculate the score contribution of one tile.

    # Tiles 1 and 2 do not contribute to the score. For 3 and above, the score
    # follows the original formula: 3 -> 3, 6 -> 9, 12 -> 27, etc.

    if tile in (0, 1, 2):
        return 0

    power = 0
    value = tile // 3
    while value != 1:
        value //= 2
        power += 1

    return 3 ** (power + 1)


def calculate_board_score(board: Board) -> int:
    # Return the total score of all scoring tiles on the board.
    return sum(calculate_tile_score(tile) for row in board for tile in row)


def move_creates_change(board: Board, direction: str) -> bool:
    # Return True if applying this move changes the board.
    before = copy_board(board)
    after = copy_board(board)
    apply_move(after, direction)
    return after != before


def best_greedy_direction(board: Board) -> str:
    # Choose the direction that creates the largest merge value.

    # Ties follow the original order: Left, Down, Right, Up.
    
    best_direction = "L"
    best_merge_value = -1

    for direction in DIRECTIONS:
        trial_board = copy_board(board)
        largest_merge = simulate_largest_merge(trial_board, direction)
        if largest_merge > best_merge_value:
            best_merge_value = largest_merge
            best_direction = direction

    return best_direction


def simulate_largest_merge(board: Board, direction: str) -> int:
    # Apply a move on a copy-like board and return the largest created tile.
    size = len(board)
    largest_merge = 0

    if direction == "L":
        for row in range(size):
            for col in range(size - 1):
                largest_merge = max(largest_merge, slide_cell(board, row, col, row, col + 1))
    elif direction == "D":
        for row in range(size - 1, 0, -1):
            for col in range(size):
                largest_merge = max(largest_merge, slide_cell(board, row, col, row - 1, col))
    elif direction == "R":
        for row in range(size):
            for col in range(size - 1, 0, -1):
                largest_merge = max(largest_merge, slide_cell(board, row, col, row, col - 1))
    elif direction == "U":
        for row in range(size - 1):
            for col in range(size):
                largest_merge = max(largest_merge, slide_cell(board, row, col, row + 1, col))
    else:
        raise ValueError(f"Unknown direction: {direction!r}")

    return largest_merge


def read_board() -> Board:
    # Read board size and board values from standard input.
    size = int(input())
    board = []
    for _ in range(size):
        board.append([int(value) for value in input().split()])
    return board


def read_placements(count: int) -> List[Placement]:
    # Read tile placements from standard input.
    placements = []
    for _ in range(count):
        index_seed, tile_value = map(int, input().split())
        placements.append((index_seed, tile_value))
    return placements


def print_board(board: Board) -> None:
    # Print the board using tabs, matching the original output style.
    for row in board:
        print("\t".join(str(tile) for tile in row))


def print_score_status(board: Board) -> None:
    # Print whether the current board has a partial or final score.
    score = calculate_board_score(board)
    status = "final" if is_game_over(board) else "partial"
    print(f"The {status} score is {score}.")

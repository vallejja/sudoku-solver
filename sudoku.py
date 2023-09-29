from utils import *


def display_sudoku(sudoku_str):
    # Check if the input string is of the correct length (81 characters)
    if len(sudoku_str) != 81:
        raise ValueError("Invalid Sudoku string length")

    # Initialize the board string with the top horizontal line
    board = HORIZONTAL_LINE + "\n"

    for i in range(9):
        # Add a vertical line at the beginning of each row
        row = "|"
        for j in range(9):
            # Get the digit or dot for the cell
            cell_value = sudoku_str[i * 9 + j]
            # Add the cell value with space padding
            # cell_value = cell_value.ljust(9, ' ')
            cell_value = cell_value.center(9)
            row += f" {cell_value} "
            # Add a vertical line to separate the regions
            if j == 2 or j == 5:
                row += "|"
        # Add a vertical line at the end of each row
        row += "|"
        # Add the row to the board
        board += row + "\n"
        # Add horizontal lines to separate regions
        if i == 2 or i == 5:
            board += HORIZONTAL_LINE + "\n"

    # Add the bottom horizontal line
    board += HORIZONTAL_LINE

    return board


def display_sudoku_dict(sudoku_dict):
    # print("-" * 23)
    print(HORIZONTAL_LINE)
    for row_char in ROWS:  # 'ABCDEFGHI':
        for col_char in COLS:  # '123456789':
            cell = row_char + col_char
            value = sudoku_dict[cell]
            # if col_char in '36':
            if value == COLS:
                displayValue = '.'
            else:
                displayValue = value

            # displayValue = displayValue.ljust(9, ' ')
            displayValue = displayValue.center(9)
            if int(col_char) % 3 == 0:
                print(f"{displayValue} | ", end="")
            else:
                print(displayValue + " ", end="")
        print()
        if row_char in 'CFI':
            # print("-" * 23)
            print(HORIZONTAL_LINE)


def cross(a, b):
    return [s + t for s in a for t in b]


def grid_values(grid_string) -> dict:
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.
    Args:
        grid_string: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """
    assert len(grid_string) == 81  # Input grid must be a string of length 81 (9x9)"
    #return dict(zip(boxes, grid_string))
    i = 0
    grid_dict = {}
    for val in grid_string:
        try:
            if val == '.':
                grid_dict[boxes[i]] = COLS
            else:
                grid_dict[boxes[i]] = val
            i += 1
        except:
            break
    return grid_dict


def get_box_peers() -> dict:
    box_peers = {}
    for box in boxes:
        peer_unit_list = []
        for unit in unit_list:
            if box in unit:
                unit.remove(box)
                peer_unit_list.append(unit)
        box_peers[box] = peer_unit_list
    return box_peers


def get_unit_dict() -> dict:
    i = 0
    colnr = sqrnr = rownr = i
    unit_dict = {}
    for unit in unit_list:
        i += 1
        if i > 18:
            sqrnr += 1
            unit_dict['S' + str(sqrnr)] = unit
        elif i > 9:
            colnr += 1
            unit_dict['C' + str(colnr)] = unit
        else:
            rownr += 1
            unit_dict['R' + str(rownr)] = unit
    return unit_dict


def get_box_peers_dict() -> dict:
    i = 0
    box_peers_dict = {}
    for box in boxes:
        peer_unit_list = []
        for unit in unit_list:
            if box in unit:
                unit_copy = unit.copy()
                unit_copy.remove(box)
                peer_unit_list.append(unit_copy)
        box_peers_dict[box] = peer_unit_list
    return box_peers_dict


# Ucomment and run the code below to view your result.
# Make sure to **comment** the code below before submitting your code.
# from copy import deepcopy


def eliminate(values) -> dict:
    """
    Eliminate values from peers of each box with a single value.
    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.
    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        # identify the peer units
        for box_peers_key in box_peers_dict:
            if box_peers_key == box:
                box_peers_list = box_peers_dict[box_peers_key]
                for peers in box_peers_list:
                    digit = values[box]
                    for peer in peers:
                        if digit in values[peer]:
                            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values) -> dict:
    for unit in unit_list:
        for digit in COLS:
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values) -> dict:
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values) -> dict:
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        # m,k = max((len(attempt[k]), k) for k in boxes if len(attempt[k]) > 1)
        # if all(len(attempt[box]) == 1 for box in boxes):
        # if m == 1:
        if attempt:
            return attempt


# =================================================
# def main():
# =================================================
if __name__ == "__main__":
    HORIZONTAL_LINE = "------------------------------|-------------------------------|-------------------------------|"

    # ===============
    # Sudoku Input
    # ===============
    # L1. Simple
    sudoku_board_string = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    # L2. Hard
    # sudoku_board_string = '......6....7...91..1.58..2...9......53.2..7.416....5.8.2.8......45.62..1.914.72..'
    # L3. Harder
    sudoku_board_string = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

    ROWS = 'ABCDEFGHI'
    COLS = '123456789'

    boxes = cross(ROWS, COLS)

    row_units = [cross(r, COLS) for r in ROWS]
    # Element example:
    # row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
    # This is the top most row.

    column_units = [cross(ROWS, c) for c in COLS]
    # Element example:
    # column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
    # This is the left most column.

    square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
    # Element example:
    # square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
    # This is the top left square.

    unit_list = row_units + column_units + square_units
    print('unit_list:', unit_list)

    unit_dict = get_unit_dict()
    print('unit_dict:', unit_dict)

    box_peers_dict = get_box_peers_dict()
    print('box_peers:', box_peers_dict)

    print(HORIZONTAL_LINE)
    sudoku_board_dict = grid_values(sudoku_board_string)
    # To validate Exercise
    # sudoku_board_dict = {'I6': '123456789', 'H9': '123456789', 'I2': '123456789', 'E8': '123456789', 'H3': '123456789', 'H7': '123456789', 'I7': '123456789', 'I4': '123456789', 'H5': '123456789', 'F9': '123456789', 'G7': '123456789', 'G6': '3', 'G5': '123456789', 'E1': '123456789', 'G3': '123456789', 'G2': '123456789', 'G1': '123456789', 'I1': '1', 'C8': '123456789', 'I3': '4', 'E5': '8', 'I5': '123456789', 'C9': '123456789', 'G9': '123456789', 'G8': '7', 'A1': '4', 'A3': '123456789', 'A2': '123456789', 'A5': '123456789', 'A4': '123456789', 'A7': '8', 'A6': '123456789', 'C3': '123456789', 'C2': '123456789', 'C1': '123456789', 'E6': '123456789', 'C7': '123456789', 'C6': '123456789', 'C5': '123456789', 'C4': '7', 'I9': '123456789', 'D8': '6', 'I8': '123456789', 'E4': '123456789', 'D9': '123456789', 'H8': '123456789', 'F6': '123456789', 'A9': '5', 'G4': '6', 'A8': '123456789', 'E7': '4', 'E3': '123456789', 'F1': '123456789', 'F2': '123456789', 'F3': '123456789', 'F4': '123456789', 'F5': '1', 'E2': '123456789', 'F7': '123456789', 'F8': '123456789', 'D2': '2', 'H1': '5', 'H6': '123456789', 'H2': '123456789', 'H4': '2', 'D3': '123456789', 'B4': '123456789', 'B5': '123456789', 'B6': '123456789', 'B7': '123456789', 'E9': '123456789', 'B1': '123456789', 'B2': '3', 'B3': '123456789', 'D6': '123456789', 'D7': '123456789', 'D4': '123456789', 'D5': '123456789', 'B8': '123456789', 'B9': '123456789', 'D1': '123456789'}
    display_sudoku_dict(sudoku_board_dict)
    print(HORIZONTAL_LINE)

    # sudoku_board_dict = eliminate(sudoku_board_dict)
    # display_sudoku_dict(sudoku_board_dict)
    #
    # sudoku_board_dict = only_choice(sudoku_board_dict)
    # display_sudoku_dict(sudoku_board_dict)

    # reduce_puzzle(sudoku_board_dict)
    sudoku_board_dict = search(sudoku_board_dict)
    display_sudoku_dict(sudoku_board_dict)
    print(HORIZONTAL_LINE)

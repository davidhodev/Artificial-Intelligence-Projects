# Artificial Intelligence Sudoku
# David Ho
import sys
from copy import copy, deepcopy
from itertools import product

def solve_sudoku(filename):
    sudoku = []
    #Reads in the file and puts the values in a usable 2D Array
    with open(filename) as file:
        for line in file:
            row = []
            line = line.replace(' ', "")
            line = line.replace('\n', "")
            for character in line:
                row.append(int(character))
            sudoku.append(row)
    print_sudoku(sudoku)

    domain = find_initial_domain(sudoku)

    print("COUNT OF DOMAIN BEFORE: ", countTotalDomainLength(domain))
    print(domain)
    if (forward_check(sudoku, domain) != 0):
        solve(sudoku, domain)
    print("COUNT OF DOMAIN AFTER: ", countTotalDomainLength(domain))
    print(domain)
    print("DONE SUDOKU")
    outputNumber = filename[12]
    output_filename = filename[0:-10]
    output_filename += "OUTPUT"
    output_filename += outputNumber
    output_filename += ".txt"
    output_file = open(output_filename, "w")
    for row in sudoku:
        for val in row:
            value = str(val) + ' '
            output_file.write(value)
        output_file.write('\n')
    print(sudoku)

# Solves the Sudoku Puzzle using Backtracking and Forward-Checking
def solve(sudoku, domain):
    # Get all the Empty Squares
    # empty_squares = get_empty_squares( puzzle )

    # Check if the puzzle is solved, then break
    if check_done(sudoku):
        print("DONE")
        print_sudoku(sudoku)
        return 1

    # Heuristic
    tile = select_unassigned_variable(sudoku, domain)
    row_to_test = tile[0]
    col_to_test = tile[1]

    for i in domain[row_to_test][col_to_test]:
        if (check_location(sudoku, row_to_test, col_to_test, i)):
            sudoku[row_to_test][col_to_test] = i
            if solve(sudoku,domain):
                return 1
            sudoku[row_to_test][col_to_test] = 0
    return 0


# Forward-checking algorithm that updates the possible numbers in each square (3D Matrix)
def forward_check(sudoku, domain):
    # All Values that are not 0
    known_values = [(row,col) for row in range(len(sudoku)) for col in range(len(sudoku[0])) if sudoku[row][col] != 0]

    for known_val in known_values:
        # All Values that the known value affects
        for compare_values in get_row_col_blocks_vals(known_val[0], known_val[1]):
            row = compare_values[0]
            col = compare_values[1]

            if domain[known_val[0]][known_val[1]][0] in domain[row][col]:

                domain[row][col].remove(domain[known_val[0]][known_val[1]][0])
                if len(domain[row][col]) == 0:
                    print("TEST", row, col)
                    return 0
                if len(domain[row][col]) == 1:
                    known_values.append((row,col))
    return 1

# Gets all of the positions in the row, column, and block
def get_row_col_blocks_vals(given_row, given_col):
    all_positions = []
    # All positions in that row
    for col in range(9):
        # if col != given_col:
        all_positions.append((given_row, col))
    # All positions in that column
    for row in range(9):
        # if row != given_row:
        all_positions.append((row, given_col))
    # All positions in that block
    block_row_position = given_row//3
    block_col_position = given_col//3
    for row in range(3):
        for col in range(3):
            all_positions.append((row+(block_row_position*3), col+(block_col_position*3)))
    #We have the given row and col three extra times.
    all_positions.remove((given_row, given_col))
    all_positions.remove((given_row, given_col))
    all_positions.remove((given_row, given_col))
    return all_positions

#Check the Row
def check_row(sudoku, given_row, val):
    # print("ROW TEST:", sudoku[given_row])
    if val in sudoku[given_row]:
        return True
    return False

# Check the Column
def check_col(sudoku, given_col, val):
    for i in range(9):
        if sudoku[i][given_col] == val:
            return True
    return False

# Check the Block
def check_block(sudoku, given_row, given_col, val):
    block_row_position = given_row//3
    block_col_position = given_col//3
    for i in range(3):
        for k in range(3):
            if(sudoku[i+(block_row_position*3)][k+(block_col_position*3)] == val):
                return True
    return False

def check_location(sudoku, given_row, given_col, val):
    return not check_row(sudoku,given_row,val) and not check_col(sudoku,given_col,val) and not check_block(sudoku,given_row,given_col,val)

# Initializes the domain 3D Array
def find_initial_domain(sudoku):
    domain = deepcopy(sudoku)
    for row in range(len(domain)):
        for col in range(len(domain[0])):
            if domain[row][col] == 0:
                domain[row][col] = [1,2,3,4,5,6,7,8,9]
            else:
                domain[row][col] = [domain[row][col]]
    return domain


# Goes through the sudoku and makes sure there are no 0 values.
def check_done(sudoku):
    for row in range(len(sudoku)):
        for col in range(len(sudoku[0])):
            if sudoku[row][col] == 0:
                return False
    return True

def countTotalDomainLength(domain):
    counter = 0
    for row in range(len(domain)):
        for col in range(len(domain[0])):
            for k in domain[row][col]:
                counter +=1
    return counter

def select_unassigned_variable(sudoku, domain):
    min_domain_length = 9
    for row in range(9):
        for col in range(9):
            if sudoku[row][col] == 0:
                min_domain_length = min(len(domain[row][col]), min_domain_length)

    # Find all rows and cols with the min domain length
    all_rowcol_with_min_domain_length = []
    for row in range(9):
        for col in range(9):
            if (sudoku[row][col] == 0 and len(domain[row][col]) == min_domain_length):
                all_rowcol_with_min_domain_length.append((row,col))
    # If only one tile has the min domain length, return that tile
    if len(all_rowcol_with_min_domain_length) == 1:
        return all_rowcol_with_min_domain_length[0]

    # Otherwise, check the degree Heuristic
    largest_degree = 0
    tile_with_largest_degree = all_rowcol_with_min_domain_length[0]
    for tile in all_rowcol_with_min_domain_length:
        temp_largest_degree = get_degree(sudoku, tile)
        if largest_degree < temp_largest_degree:
            largest_degree = temp_largest_degree
            tile_with_largest_degree = tile

    return tile_with_largest_degree


def get_degree(sudoku, tile):
    given_row = tile[0]
    given_col = tile[1]
    degree = 0
    neighbors = []
    for c in product(*(range(n-1, n+2) for n in tile)):
        if c != tile and all(0 <= n < 3 for n in c):
            neighbors.append(c)
    for test_tile in neighbors:
        if sudoku[test_tile[0]][test_tile[1]] == 0:
            degree += 1
    return degree

# Print the Sudoku Puzzle
def print_sudoku(sudoku):
    for row in sudoku:
        print(row)

if __name__=="__main__":
    solve_sudoku('SUDUKO_Input3.txt')

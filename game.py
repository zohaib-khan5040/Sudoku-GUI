# Instantiate the Sudoku board as a nested 9x9 list
board = [
    [0,0,0,0,2,7,0,0,0],
    [0,0,0,5,9,4,0,2,7],
    [0,0,0,0,0,0,6,0,0],
    [8,0,0,1,0,5,4,0,0],
    [0,0,0,0,0,8,0,5,3],
    [0,0,4,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,6,0],
    [0,9,0,0,3,0,1,0,0],
    [5,1,0,0,0,2,0,0,0]
]

def find_empty(board):
    """ Finds some empty position on the board and returns it """
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i,j)
    # If no empty was found, return None
    return None

def is_complete(board):
    """ Returns True if board assignment is complete """
    if find_empty(board) is None:
        return True
    return False


def validate(board, pos, k):
    """ Validating whether some k can take a certain pos, following the rules of sudoku """
    row = pos[0]
    col = pos[1]

    # Check if k already exists in the same row 
    for j in range(9):
        if board[row][j] == k and (j != col):
            return False
    
    # Check if k already exists in the same column
    for i in range(9):
        if board[i][col] == k and (i != row):
            return False

    # Checking the box is a bit trickier
    # We find the locations to start indexing each box using floor division of the coordinates 
    # The second box would give (row//3 = 0) and (col//3 = 1)
    box_i = row // 3
    box_j = col // 3

    for i in range(box_i*3, box_i*3+3):
        for j in range(box_j*3,box_j*3+3):
            if board[i][j] == k and (i != row) and (j != col):
                return False
    
    return True

def print_board(board):
    """ Print the board, formatted with newline chars """
    for i in range(9):
        print(board[i])

def solve(board):
    """ Backtracking algorithm to solve the puzzle modelled as a CSP """
    # Check if the board is complete, in which case print it out
    if is_complete(board):
        # The Base Case for the recursive function
        return True
    
    # Find some unassigned variable/position on the board
    pos = find_empty(board)

    # Loop through all values in the domain (1-9) and validate
    # This is also the recursive part
    for k in range(1,10):
        if validate(board, pos, k):
            # Fill in the board with this valid value
            board[pos[0]][pos[1]] = k

            if solve(board):
                return True
            
            # Backtrack 
            board[pos[0]][pos[1]] = 0

    return False

if __name__ == '__main__':
    solve(board)
    print_board(board)
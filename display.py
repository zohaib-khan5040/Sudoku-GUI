from game import validate,find_empty,is_complete,solve
import sys
import copy
import pygame 
import time
import random

pygame.init()

BLACK = (0,0,0)
WHITE = (255,255,255)

def generate():
    """ Generates a random solvable Sudoku board """
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        # Make an empty board to start
        board = [[0 for i in range(9)] for j in range(9)]

        # Put a random number in a random spot
        for i in range(9):
            for j in range(9):
                # Ghetto probability: very unlikely for the board to be mostly complete
                if random.randint(1,9) >= 5:
                    board[i][j] = random.randint(1,9)
                    if validate(board,(i,j),board[i][j]):
                        continue
                    else:
                        board[i][j] = 0
        
        # Store a deep copy since solve modifies the board inplace
        partial_board = copy.deepcopy(board)
        if solve(board):
            return partial_board


class Cell:
    """ Representing each of the 81 cells on the Sudoku Grid """
    def __init__(self,value,window,x1,y1):
        self.value = value
        self.window = window
        # Pygame Rect for the actual representation
        self.rect = pygame.Rect(x1,y1,60,60)
        self.selected = False
        self.correct = False
        self.incorrect = False

    def draw(self,color,thickness):
        """ Draw the Rect on the screen """
        pygame.draw.rect(self.window,color,self.rect,thickness)

    def is_clicked(self,mouse_cor):
        """ Checks if the mouse clicks on a cell """
        if self.rect.collidepoint(mouse_cor):
            self.selected = True
        return self.selected

    def display(self, value, position, color):
        """ Display number on the cell """
        font = pygame.font.SysFont('Bahnschrift', 42)
        text = font.render(str(value),True,color)
        self.window.blit(text,position)

class Board():
    """ The board is a 9x9 grid of Cells """
    def __init__(self,window):
        self.board = generate()
        self.solution = copy.deepcopy(self.board)
        self.window = window
        solve(self.solution)
        self.cells = [[Cell(self.board[i][j], window, i*60, j*60) for j in range(9)] for i in range(9)]

    def draw_board(self):
        """ Fills board with cells and renders the fonts """
        for i in range(9):
            for j in range(9):
                # Draw black lines to demarkate the 'boxes'
                if j%3 == 0 and j != 0:
                    pygame.draw.line(self.window, BLACK, ((j//3)*180, 0), ((j//3)*180, 540), 4)
                if i%3 == 0 and i != 0:
                    pygame.draw.line(self.window, BLACK, (0, (i//3)*180), (540, (i//3)*180), 4)
                
                # Draw the cells 
                self.cells[i][j].draw(BLACK, 1)

                # Don't draw the placeholder 0s on the grid
                if self.cells[i][j].value != 0:
                    self.cells[i][j].display(self.cells[i][j].value, (21+(j*60), (16+(i*60))), (0, 0, 0))
                
                # Bottom most line
                pygame.draw.line(self.window, (0, 0, 0), (0, ((i+1) // 3) * 180), (540, ((i+1) // 3) * 180), 4)

    def deselect_all(self, selected_cell):
            """ Deselect all tiles except the one currently clicked on """
            for i in range(9):
                for j in range(9):
                    if self.cells[i][j] != selected_cell:
                        self.cells[i][j].selected = False
    
    def redraw(self, keys, wrong, time):
        """ Redraw the board with highlighted tiles """
        self.window.fill(WHITE)
        self.draw_board()
        for i in range(9):
            for j in range(9):
                # Draw a border on selected tiles
                if self.cells[i][j].selected:  
                    self.cells[i][j].draw((50, 205, 50), 4)
                # Different border for correct tiles
                elif self.cells[i][j].correct:
                    self.cells[j][i].draw((34, 139, 34), 4)
                # Another border for incorrect
                elif self.cells[i][j].incorrect:
                    self.cells[j][i].draw((255, 0, 0), 4)

        # Allows user to place values on each cell which are not the final responses
        if len(keys) != 0: 
            for value in keys:
                self.cells[value[0]][value[1]].display(keys[value], (21+(value[0]*60), (16+(value[1]*60))), (128, 128, 128))
        
        if wrong > 0:
            # Draw a Red X near the bottom-left of the window
            font = pygame.font.SysFont('Bauhaus 93', 35) 
            text = font.render('X', True, (255, 0, 0))
            self.window.blit(text, (10, 554))

            font = pygame.font.SysFont('Bahnschrift', 40) 
            text = font.render(str(wrong), True, BLACK)
            self.window.blit(text, (32, 540))

        font = pygame.font.SysFont('Bahnschrift', 40) #Time Display
        text = font.render(str(time), True, BLACK)
        self.window.blit(text, (388, 542))
        pygame.display.flip()

    def visualSolve(self,wrong,time):
        """ Showcasing the Backtracking Algorithm """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        pos = find_empty(self.board)
        
        if not pos:
            return True
        
        i,j = pos[0],pos[1]

        for n in range(1,10):
            if validate(self.board, pos, n):
                self.board[i][j] = n
                self.cells[i][j].value = n
                self.cells[i][j].correct = True

                # Slow down the visuals
                # pygame.time.delay(20)
                self.redraw({},wrong,time)

                if self.visualSolve(wrong,time):
                    return True

                # Failed
                self.board[i][j] = 0
                self.cells[i][j].value = 0
                self.cells[i][j].incorrect = True
                self.cells[i][j].correct = False
                # pygame.time.delay(20)
                self.redraw({}, wrong, time)

def main():
    '''Runs the main Sudoku GUI/Game'''
    screen = pygame.display.set_mode((540, 590))
    screen.fill(WHITE)
    pygame.display.set_caption("Sudoku")

    # Loading screen when generating grid
    font = pygame.font.SysFont('Bahnschrift', 40)
    text = font.render("Generating", True,  BLACK)
    screen.blit(text, (175, 245))

    font = pygame.font.SysFont('Bahnschrift', 40)
    text = font.render("Grid", True, BLACK)
    screen.blit(text, (230, 290))
    pygame.display.flip()

    # Initiliaze values and variables
    wrong = 0
    board = Board(screen)
    selected = -1,-1 #NoneType error when selected = None, easier to just format as a tuple whose value will never be used
    keyDict = {}
    running = True
    startTime = time.time()
    while running:
        elapsed = time.time() - startTime
        passedTime = time.strftime("%H:%M:%S", time.gmtime(elapsed))

        if board.board == board.solution: #user has solved the board
            for i in range(9):
                for j in range(9):
                    board.cells[i][j].selected = False
                    running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit() 

            elif event.type == pygame.MOUSEBUTTONUP: # Allow clicks only while the board hasn't been solved
                mousePos = pygame.mouse.get_pos()
                for i in range(9):
                    for j in range(9):
                        if board.cells[i][j].is_clicked(mousePos):
                            selected = i,j
                            board.deselect_all(board.cells[i][j]) # Deselects every Cell except the one currently clicked

            elif event.type == pygame.KEYDOWN:
                if board.board[selected[1]][selected[0]] == 0 and selected != (-1,-1):
                    if event.key == pygame.K_1:
                        keyDict[selected] = 1

                    if event.key == pygame.K_2:
                        keyDict[selected] = 2

                    if event.key == pygame.K_3:
                        keyDict[selected] = 3

                    if event.key == pygame.K_4:
                        keyDict[selected] = 4

                    if event.key == pygame.K_5:
                        keyDict[selected] = 5

                    if event.key == pygame.K_6:
                        keyDict[selected] = 6

                    if event.key == pygame.K_7:
                        keyDict[selected] = 7

                    if event.key == pygame.K_8:
                        keyDict[selected] = 8

                    if event.key == pygame.K_9:
                        keyDict[selected] = 9

                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:  # clears tile out
                        if selected in keyDict:
                            board.cells[selected[1]][selected[0]].value = 0
                            del keyDict[selected]

                    elif event.key == pygame.K_RETURN:
                        if selected in keyDict:
                            if keyDict[selected] != board.solution[selected[1]][selected[0]]: #clear tile when incorrect value is inputted
                                wrong += 1
                                board.cells[selected[1]][selected[0]].value = 0
                                del keyDict[selected]
                                break
                            #valid and correct entry into cell
                            board.cells[selected[1]][selected[0]].value = keyDict[selected] #assigns current grid value
                            board.board[selected[1]][selected[0]] = keyDict[selected] #assigns to actual board so that the correct value can't be modified
                            del keyDict[selected]

                if event.key == pygame.K_SPACE:
                    for i in range(9):
                        for j in range(9):
                            board.cells[i][j].selected = False
                    keyDict = {}  #clear keyDict out

                    board.visualSolve(wrong, passedTime)
                    for i in range(9):
                        for j in range(9):
                            board.cells[i][j].correct = False
                            board.cells[i][j].incorrect = False #reset tiles
                    running = False

        board.redraw(keyDict, wrong, passedTime)

    while True: #another running loop so that the program ONLY closes when user closes program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

main()
pygame.quit()
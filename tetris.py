"""
begining of my final project for CS465, definitely should have started earlier
This program should be able to simulate a tetris game without all the fancy graphics
just a simulation using a 2d array and some pieces
"""
import sys
import random
import time
import copy
from pprint import pprint

board_width = 10
board_height = 10

tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]
printing = False
#-----------HELPER FUNCTIONS------------#

#stole this from something I found online 
def rotate_clockwise(shape):
    return [ [ shape[y][x] for y in range(len(shape)) ] for x in range(len(shape[0]) - 1, -1, -1) ]

#took inspiration from the same place as the above functions 
#had to modify it to suit my needs though
def check_collision(board, shape, position):
    """
    returns True if there is a colision of the current piece with 
    another piece or the edge of the board
    The x and y coordinates are the top left most block of the stone 
    """ 
    x_cor, y_cor = position
    #print(board[x_cor][y_cor])

    for i  in range(len(shape)):
        for j in range(len(shape[i])):
            try:
                board_coord = board[y_cor + i][x_cor + j]
                if shape[i][j] != 0 and board_coord != 0:
                    return True
            except IndexError:
                #print(position)
                #print('index error')
                return True
    return False

def at_bottom_of_board(board, shape, position):
    """
    returns True if the current stone is at the bottom of the board
    either the bottom if it is touching another piece or the actual
    bottom of the board
    """
    x_cor, y_cor = position
    shape_height = len(shape)
    try:
        for i, block in enumerate(shape[-1]):
            if block != 0:
                if board[y_cor + shape_height][x_cor + i] != 0:
                    return True
                if (y_cor + shape_height + 1) == (len(board) + 1):
                    print('+++++++++')
                    return True
            
    except IndexError:
        return True
    
    return False


def place_stone(board, curr_stone, block):
        """
        for now, just places the piece somewhere on the board
        """
       
        x_cor, y_cor = block
       
        for i, row in enumerate(curr_stone):
            for j, block in enumerate(row):
                #don't need to replace blocks that are already zero
                if block != 0:
                    board[y_cor + i][x_cor + j] = block

def display_board(board):
        """
        prints the board to the screen
        can also be used to print pieces for testing <- that's not important though
        """
        for row in board:
                for block in row:
                    if block != 0:
                        print('[{}]'.format(block), end='')
                    else:
                        print('[ ]', end='')
                print()
        print()

class TetrisBoard(object):
    """
    The main object class for running the tetris board simulation
    """
    def __init__(self, heurustic_weights, width=board_width, height=board_height, prints=False):
        self.width = width
        self.height = height
        self.heurustic_weights = heurustic_weights
        print_progress = prints
        #print(self.width, self.height)
       

        self.board = [[0 for x in range(self.width)] for y in range(self.height)]
        #pprint(self.board)

        self.availiable_stones = copy.deepcopy(tetris_shapes)
        self.next_stone = self.get_next_stone()
        self.curr_position = (0, 0)
    
    def get_next_stone(self):
        """
        provides a random way of getting the next piece,
        but will not give the player an impossible sequence
        """
        
        if len(self.availiable_stones) > 1:
            choice = random.choice(self.availiable_stones)
            self.availiable_stones.pop(self.availiable_stones.index(choice))
            return choice
        else:
            self.availiable_stones = copy.deepcopy(tetris_shapes)
            choice = random.choice(self.availiable_stones)
            self.availiable_stones.pop(self.availiable_stones.index(choice))
            return choice
    
    
    def game_over(self):
        if self.curr_position[1] == 0:
            return True
        
        else:
            return False

    def run_game(self):
        """
        main driver for running the tetris game
        """
        for i in range(10):
            self.curr_stone = self.next_stone
            self.curr_position =((int(self.width / 2 - len(self.curr_stone[0])/2)), 0)
            
            """
            left = random.randrange(0,100)
            if left % 2 == 0:
                print('moving left')
                self.move_left(100)
            """
            
            while not check_collision(self.board, self.curr_stone, self.curr_position):
                self.curr_position = (self.curr_position[0], self.curr_position[1] + 1)
                print(self.curr_position)
            if self.curr_position[1] == 0:
                print('game over')
                self.remove_row(3)
                self.display_board()
                sys.exit()
            self.place_stone(self.curr_stone, (self.curr_position[0], self.curr_position[1] - 1))
            self.evaluate_state()
            self.display_board()
            
            self.next_stone = self.get_next_stone()
    
    def check_for_row_clears(self):
        """
        returns a list of row clears to perform
        """
        row_clears = []
        for row in self.board:
            row_clear = True
            for block in row:
                if block == 0:
                    row_clear = False
                    break
            if row_clear:
                row_clears.append(row)

        return row_clears

    def run_simulation(self,print_progress=False):
        """
        function that runs a sim of the tetris game
        """
        #print('starting')
        turn_count = 0
        self.curr_position = (1, 1)
        #print(self.game_over())
        #print(self.curr_position)
        # if print_progress:
            #Sprint(self.game_over())
        while not self.game_over():
            if print_progress:
                printing = True
                sys.stdout.write("TURN #: %d\r" % (turn_count))
                print('-----------')
            self.curr_stone = self.next_stone
            self.next_stone = self.get_next_stone()
            #pprint(self.next_stone)

            position = self.generate_states()
            if print_progress:
                print(position)
            
            if position == ():
                break
            place_stone(self.board, self.curr_stone, (position[0], position[1]))
            self.curr_position = position
            row_clears = self.check_for_row_clears()
            #print(row_clears)
            for clear in row_clears:
                #print('--------------------------------------------BEFORE ROW CLEAR ------------------------------------')
                #display_board(self.board)
                #print('--------------------------------------------AFTER ROW CLEAR -------------------------------------')
                self.remove_row(clear)
            if print_progress:
                display_board(self.board)
                #time.sleep(3)
            turn_count += 1

        if print_progress:
            print('FINAL TURN COUNT: {}'.format(turn_count))
        return turn_count
    
    def generate_states(self):
        """
        generates all the possible states for the position
        of the current piece along with the position of the next piece
        """
        #generate a list of the possible orientations of the shape
        #self.curr_stone = self.next_stone
        max_state = 0
        max_state_position = ()
        stone_orients = []
        stone_orients.append(self.curr_stone)
        rotated_stone = rotate_clockwise(self.curr_stone)

        while rotated_stone not in stone_orients:
            stone_orients.append(rotated_stone)
            rotated_stone = rotate_clockwise(rotated_stone)
        #pprint(stone_orients)

       
        state_count = 0
        for stone in stone_orients:
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    board = [row[:] for row in self.board]
                    
                    """
                    print('bottom board:')
                    print(at_bottom_of_board(board, stone, (i,j)))
                    print('check_collision:')
                    print(check_collision(board, stone, (i,j)))
                    """
                    #place_stone(board, stone, (i, j))
                    #display_board(board)
                    #clear_board(board)
                    if not check_collision(board, stone, (i,j)) and at_bottom_of_board(board, stone, (i,j)):
                        place_stone(board, stone, (i,j))
                        #print statements for testing
                        #print('--------STATE ----------')
                        #display_board(board)
                        state_val = evaluate_state(board, self.heurustic_weights)
                        if state_count == 0 or state_val > max_state:
                            max_state = state_val
                            max_state_position = (i, j)
                            self.curr_stone = stone
                        state_count += 1
                        clear_board(board)
        
        return max_state_position
                    


    def remove_row(self, row):
        self.board.pop(self.board.index(row))
        self.board = [[0 for i in range(self.width)]] + self.board

def evaluate_state(board, heurustic_weights):
        """
        function that evaluates the state of the board
        """
        height = len(board)
        min_height = len(board)
        max_height = 0
        for row_num, row in enumerate(board):
            for block in row:
                if block != 0:
                    if (height - row_num) > max_height:
                        max_height = height - row_num

                    
        
        
        for row_num, row in enumerate(board):
            for block in row:
                if block != 0:

                    if (height - row_num) < min_height:
                        min_height = height - row_num - 1
        
        #print('MAX HEIGHT: {}'.format(max_height))
        #print('MIN HEIGHT: {}'.format(min_height))
        height_diff = max_height - min_height
        #print(height_diff)

        row_clears = 0
        for row in board:
            row_clear = True
            for block in row:
                if block == 0:
                    row_clear = False
                    break
            if row_clear:
                row_clears += 1
        
        #print('ROW CLEARS: {}'.format(row_clears))

       #calculate the number of holes on the board
        num_holes = 0
        burried_holes = 0
        for row_num, row in enumerate(board):
            for block_num, block in enumerate(row):
               #block is empty
                if block == 0:
                    burried = False
                    for i in range(row_num -1):
                        if board[i][block_num] != 0:
                            burried = True
                            break
                    if burried:
                        burried_holes += 1

                    if row_num > 0 and board[row_num - 1][block_num] != 0:
                       #print('CURRENTLY ON ROW {}'.format(row_num))
                       #print(row)
                       #print('CURRENT BLOCK: {}'.format(block))
                       #print('BLOCK ABOVE: {}'.format(board[row_num - 1][block_num]))
                       num_holes += 1
        #print(num_holes)
        
        #display_board(board)
        #print(num_holes)
        #print(burried_holes)

        
        return (heurustic_weights[0] * max_height) + (heurustic_weights[1] * height_diff) + (heurustic_weights[2] * num_holes) + (heurustic_weights[3] * burried_holes) + (heurustic_weights[4] * row_clears)

def clear_board(board):
    """
    clears the board to all 0s
    """
    for i in range(len(board)):
        for j in range(len(board[i])):
            board[i][j] = 0

if __name__ == '__main__':
    weights = []
    for i in range(3):
        weights.append(random.randint(0,100))
    weights = [1,1,1,1,1]
    print(weights)
    board = TetrisBoard(weights, height=10)
    board.run_simulation(print_progress=True)
    #board.run_game()
    #board.generate_states()
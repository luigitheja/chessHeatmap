import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import chess.pgn
from chessboard import display
import time


class Board:

    def __init__(self):

        self.ref_board = [['0' for i in range(8)] for j in range(8)]

    def get_board_from_fen(self, fen_str):

        fen_spl = fen_str.split(" ")[0]
        pos = fen_spl.split("/")
        total_board = []
        for row in pos:
            current_row = []
            for block in row:
                if block.isdigit():
                    num_empty = int(block)
                    for i in range(num_empty):
                        current_row.append(0)
                else:
                    current_row.append(block)
            total_board.append(current_row)
        return total_board 
    
    def invert_board(self, board):
        new_board = [board[7-i][::-1] for i in range(8)]
        return new_board

    def in_board(self, row, col):
        if row < 0 or row > 7 or col < 0 or col > 7:
            return False
        return True
    
    def is_opposite(self, piece, opposite):
        piece = str(piece)
        opposite = str(opposite)
        
        if opposite == '0':
            return False

        if (piece.islower() and opposite.islower()) or (piece.isupper() and opposite.isupper()):
            return False 
        return True

    def index_to_square(self, i, j):
        cols = 'hgfedcba'
        rows = '87654321'

        return cols[j]+rows[i]

    def get_map_pawn(self, board, pawn_row, pawn_col):
        pawn_map = [[0 for i in range(8)] for j in range(8)]
        pawn_map[pawn_row][pawn_col] = 1
        possible_moves_bot = [(1,-1),(1,0),(1,1)]
        possible_moves_top = [(-1,-1),(-1,0),(-1,1)]
        
        
        # print("pawn in ", self.index_to_square(pawn_row, pawn_col))
        
        if board[pawn_row][pawn_col].islower():
            possbile_moves = possible_moves_bot
        else:
            possbile_moves = possible_moves_top
        
        for i,j in possbile_moves:

            if self.in_board(pawn_row+i, pawn_col+j):

                if 0 in (i,j) and board[pawn_row+i][pawn_col+j] == 0:
                    pawn_map[pawn_row+i][pawn_col+j] = 1
                    # print("move",i,j,"can move ", self.index_to_square(pawn_row+i, pawn_col+j))
                else:
                    if board[pawn_row+i][pawn_col+j] != 0 and self.is_opposite(board[pawn_row][pawn_col], board[pawn_row+i][pawn_col+j]):
                        pawn_map[pawn_row+i][pawn_col+j] = 1
                        # print("move",i,j,"can move ", self.index_to_square(pawn_row+i, pawn_col+j))
        # print("___________________________________________________")    
        return pawn_map
    
    def get_map_rook(self, board, rook_row, rook_col):
        rook_map = [[0 for i in range(8)] for j in range(8)]
        rook_map[rook_row][rook_col] = 1

        #left of rook
        for i in range(0,rook_row):
            if self.in_board(rook_row-i, rook_col) and board[rook_row-i][rook_col] ==0:
                rook_map[rook_row-i][rook_col] = 1
            if self.in_board(rook_row-i, rook_col) and board[rook_row-i][rook_col] != 0:
                if self.is_opposite(board[rook_row][rook_col], board[rook_row-i][rook_col]):
                    rook_map[rook_row-i][rook_col] = 1
                break
        
        #right of rook
        for i in range(rook_row,8):
            if self.in_board(i, rook_col) and board[i][rook_col] ==0:
                rook_map[i][rook_col] = 1
            if self.in_board(i, rook_col) and board[i][rook_col] != 0:
                if self.is_opposite(board[rook_row][rook_col], board[i][rook_col]):
                    rook_map[i][rook_col] = 1
                break
        
        #bottom of rook
        for i in range(0,rook_col):
            if self.in_board(rook_row, rook_col-i) and board[rook_row][rook_col-i] ==0:
                rook_map[rook_row][rook_col-i] = 1
            if self.in_board(rook_row, rook_col-i) and board[rook_row][rook_col-i] != 0:
                if self.is_opposite(board[rook_row][rook_col], board[rook_row][rook_col-i]):
                    rook_map[rook_row][rook_col-i] = 1
                break
        
        #top of the rook
        for i in range(rook_col,8):
            if self.in_board(rook_row, i) and board[rook_row][i] ==0:
                rook_map[rook_row][i] = 1
            if self.in_board(rook_row, i) and board[rook_row][i] != 0:
                if self.is_opposite(board[rook_row][rook_col], board[rook_row][i]):
                    rook_map[rook_row][i] = 1
                break
        
        return rook_map
            
    def get_map_knight(self, board, k_row, k_col):
        kmap = [[0 for i in range(8)] for j in range(8)]
        kmap[k_row][k_col] = 1

        moves_possible=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]

        for i,j in moves_possible:
            if self.in_board(k_row+i,k_col+j): 
                if board[k_row+i][k_col+j] == 0:
                    kmap[k_row+i][k_col+j] = 1
                elif board[k_row+i][k_col+j] != 0 and self.is_opposite(board[k_row][k_col], board[k_row+i][k_col+j]):
                    kmap[k_row+i][k_col+j] = 1
        return kmap

    def get_map_bishop(self, board, b_row, b_col):
        kmap = [[0 for i in range(8)] for j in range(8)]
        kmap[b_row][b_col] = 1

        possibilities = [[(-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)], [(-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)], [(1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)], [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]]
        
        for dir_list in possibilities:

            for i,j in dir_list:
                if self.in_board(b_row+i,b_col+j):

                    if board[b_row+i][b_col+j] == 0:
                        kmap[b_row+i][b_col+j] = 1
                    else:
                        if self.is_opposite(board[b_row][b_col], board[b_row+i][b_col+j] ):
                            kmap[b_row+i][b_col+j] = 1
                        break
        return kmap
    
    def get_map_king(self, board, k_row, k_col):
        kmap = [[0 for i in range(8)] for j in range(8)]
        kmap[k_row][k_col] = 1

        possibilities = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]

        for i,j in possibilities:

            if self.in_board(k_row+i, k_col+j):

                if board[k_row+i][k_col+j] == 0:
                    kmap[k_row+i][k_col+j] = 1
                else:
                    if self.is_opposite(board[k_row][k_col], board[k_row+i][k_col+j]):
                        kmap[k_row+i][k_col+j] = 1
        return kmap

    def add_boards(self, board1, board2):
        board3 = [[0 for i in range(8)] for j in range(8)]

        for i in range(8):
            for j in range(8):
                board3[i][j] = board1[i][j]+board2[i][j]

        return board3

    def invert_sign(self, board):
        for i in range(8):
            for j in range(8):
                board[i][j] = board[i][j] * -1
        return board
    
    def generate_map_from_board(self, board):
        numpy_board = np.array([np.array(xi) for xi in board])
        heat_map = sns.heatmap( numpy_board, linewidth = 1 , annot = True)
        # plt.figure(figsize=(8,8))
        # plt.title( "current heatmap for knight" )
        plt.show()
    
    def draw_and_animate_maps(self, maps, fens):

        
        fig = plt.figure()

        def animate(i):
            
            curmap = maps[i]
            numpy_board = np.array([np.array(xi) for xi in curmap])
            cols = 'a,b,c,d,e,f,g,h'.split(",")
            df = pd.DataFrame(curmap, columns = cols)
            sns.color_palette("rocket", as_cmap=True)
            display.start(fens[i])
            sns.heatmap( df, linewidths = 0.1,cbar=False)
            

        anim = FuncAnimation(fig, animate, frames=len(maps),  repeat=False, interval = 1000)
        
        plt.show()




def get_heatmap_from_fen(brd, fen):


    current_brd = brd.get_board_from_fen(fen)
    previous_map = [[0 for i in range(8)] for j in range(8)]

    for i in range(8):
        for j in range(8):
            if current_brd[i][j] =='p' or current_brd[i][j] =='P' :
                board_map = brd.get_map_pawn(current_brd, i, j)
                if current_brd[i][j].islower():
                    board_map = brd.invert_sign(board_map)
                previous_map = brd.add_boards(previous_map ,  board_map)
            elif current_brd[i][j] =='n' or current_brd[i][j] =='N' :   
                board_map = brd.get_map_knight(current_brd, i, j)
                if current_brd[i][j].islower():
                    board_map = brd.invert_sign(board_map)
                previous_map = brd.add_boards(previous_map ,  board_map)
            elif current_brd[i][j] =='b' or current_brd[i][j] =='B' :   
                board_map = brd.get_map_bishop(current_brd, i, j)
                if current_brd[i][j].islower():
                    board_map = brd.invert_sign(board_map)
                previous_map = brd.add_boards(previous_map ,  board_map) 
            elif current_brd[i][j] =='r' or current_brd[i][j] =='R' :   
                board_map = brd.get_map_rook(current_brd, i, j)
                if current_brd[i][j].islower():
                    board_map = brd.invert_sign(board_map)
                previous_map = brd.add_boards(previous_map ,  board_map) 
            elif current_brd[i][j] =='q' or current_brd[i][j] =='Q' :
                board_map1 = brd.get_map_rook(current_brd, i, j)
                board_map2 = brd.get_map_bishop(current_brd, i, j)
                board_map = brd.add_boards(board_map1, board_map2)
                board_map[i][j] -= 1
                if current_brd[i][j].islower():
                    board_map = brd.invert_sign(board_map)
                previous_map = brd.add_boards(previous_map ,  board_map)
            elif current_brd[i][j] =='k' or current_brd[i][j] =='K' :   
                board_map = brd.get_map_king(current_brd, i, j)
                if current_brd[i][j].islower():
                    board_map = brd.invert_sign(board_map)
                previous_map = brd.add_boards(previous_map ,  board_map) 
    
    return previous_map
        


brd = Board()
pgnpath = "D:\programs\chess pgn dataset\scraped_games\Anand.pgn"

pgn = open(pgnpath)



game = chess.pgn.read_game(pgn)

all_maps = []
all_fens = []

while game.next():
    fen = game.board().fen()
    # print(fen)
    previous_map = get_heatmap_from_fen(brd, fen)
    all_maps.append(previous_map)
    all_fens.append(fen)
    game = game.next()
    

print("number of moves :", len(all_maps))

print(all_fens[:5])

brd.draw_and_animate_maps(all_maps[:5], all_fens[:5])

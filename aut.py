from functools import partial
from typing import List
from time import sleep
import sys

class Board(object):
    def __init__(self, h: int, w: int):
        super().__init__()
        self.h = h
        self.w = w
        self.m = [[Cell(i, j) for j in range(h)] for i in range(w) ]
        
    def populate(self):
        self.m = [[cell.link(self.m) for cell in row] for row in self.m]
        return self
    
    def __str__(self) -> str:
        
        s = ""
        for row in self.m:
            l = []
            for cell in row:
                l.append(str(cell.v))
            
            s += " ".join(l) + "\n"
                
        return s
        

class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.v = 0
        
    def link(self, board: List):
        nix = partial(neg_index, len(board[0]))
        niy = partial(neg_index, len(board))
        self.north = board[self.y - 1][self.x]
        self.south = board[niy(self.y + 1)][self.x]
        self.east = board[self.y][nix(self.x + 1)]
        self.west = board[self.y][self.x - 1]
        
        return self

class Vector2(object):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.x = x
        self.y = y

def neg_index(offset: int, n: int):
    return (n - offset)

# %%
def apply_rules(cell: Cell):
    cell.v -= 1
    cell.north.v += 1
    cell.south.v += 1
    cell.east.v += 1
    cell.west.v += 1
    
    if cell.v > 21:
        cell.v = 0
    
def select_cells(board: Board):
    to_apply = []
    for row in board.m:
        for cell in row:
            if cell.v > 0:
                to_apply.append(Vector2(cell.x, cell.y))
    return to_apply
        

# %%
def simulate(gen: int, board: Board):
    nbm = board.m.copy()
    
    for i in range(gen):
        changes = select_cells(board)
        
    
    for cell in changes:
        apply_rules(nbm[cell.x][cell.y])
    
    nb = Board(board.h, board.w)
    nb.m = nbm
    return nb

# %%
RESET = '\033[0m'

def get_color_escape(r, g, b, background=True):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

def val_to_color(v):
    color = ""
    if v < 0:
        color = get_color_escape(0, 0, 0) + " "
    elif v < 3:
        color = get_color_escape(0, 0, v * 20) + " "
    elif v < 6:
        color = get_color_escape(0, v*10, v*20) + " "
    elif v < 9:
        color = get_color_escape(0, v*20, v * 10) + " "
    elif v < 12:
        color = get_color_escape(v*10, v*20 ,0) + " "
    elif v < 15:
        color = get_color_escape(v*20, v*10, 0) + " "
    elif v < 18:
        color = get_color_escape(v*20, 0, v*100) + " "
    elif v < 21:
        color = get_color_escape(v*10, v*10, v*10) + " "
    elif v > 21:
        color = get_color_escape(255, 0, 255) + " "
    
    color += RESET
    
    return color

def color_matrix(matrix):
    colored = [[0 for cell in row] for row in matrix]
    i = 0
    for row in matrix:
        j = 0
        for cell in row:
            colored[i][j] = val_to_color(cell.v)
            j+=1
        i+=1
    
    return colored
def text_render(board: Board):
    for line in color_matrix(board.m):
        print(''.join(map(str,line)))
        
def life(gen):
    matrix = Board(51, 51).populate()
    matrix.m[20][30].v = 21
    
    for i in range(gen):
        text_render(simulate(1, matrix))
        sleep(0.2)
        print("\033[2J\033[1;1H")

def main(argv):
    if len(argv) != 2:
        print(len(argv))
        print("Usage: ", argv[0], " <number-of-generations>")
        exit(1)
    else:
        life(int(argv[1]))
        exit(0)

if __name__ == "__main__":
    main(sys.argv)
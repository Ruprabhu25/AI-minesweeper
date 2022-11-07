import pygame, sys
import numpy as np

class Tile:
    '''Represents each white tile/box on the grid'''
    def __init__(self, value, window, x1, x2):
        self.value = value #value of the num on this grid
        self.width = 30
        self.height = 30
        self.window = window #the window/screen we're in
        self.rect = pygame.Rect(x1, x2, self.width, self.height) #dimensions for the rectangle

    def draw(self):
        '''Draws a tile on the self.board'''
        pygame.draw.rect(self.window, (220,220,220), self.rect, 1)
        pygame.display.flip()

    def display(self, position):
        '''Displays a number on that tile'''
        font = pygame.font.SysFont('arial', 20)
        color = (0,0,0) # default black value (also color for 7)
        if self.value == 1:
            color = (0,0,255)
        elif self.value == 2:
            color = (0,255,0)
        elif self.value == 3:
            color = (255,0,0)
        elif self.value == 4:
            color = (106,13,173)
        elif self.value == 5:
            color = (128,0,0)
        elif self.value == 6:
            color = (48,213,200)
        elif self.value == 8:
            color = (230,230,230)
        text = font.render(str(self.value), True, color)
        self.window.blit(text, position)
        pygame.display.update()

class Minesweeper:
    def __init__(self, window):
        print('intializing')
        self.TILES_X, self.TILES_Y = 15, 15
        self.boardf = self.set_flags(self.TILES_X, self.TILES_Y)
        self.window = window
        self.tiles = [[0 for i in range(self.TILES_X)] for j in range(self.TILES_Y)]
        self.num_flags = 0

    def draw_board(self): 
        '''Fills the board with Tiles'''
        for i in range(self.TILES_X):
            for j in range(self.TILES_Y):
                self.tiles[i][j] = Tile(self.boardf[i][j], self.window, i*30, j*30) #draw a single tile
                self.tiles[i][j].draw()
                #self.tiles[i][j].display(position=(i*30 + 10, j*30 + 5))


    def is_flag(self,x,y):
        if self.board[x][y] == -1:
            return 1
        return 0

    def set_flags(self, x_tiles, y_tiles):
        # create self.board with 0 or -1 values
        # -1 values are flags, 0 are safe tiles
        self.board = [[(-1 * np.random.choice(a=2, p=[0.85,0.15])) for i in range(x_tiles)] for j in range(y_tiles)]
        for x in range(x_tiles):
            for y in range(y_tiles):
                if self.board[x][y] != -1:
                    self.board[x][y] = self.near_flag(x,y)
        return self.board

    def near_flag(self, x,y):
        # print(x, y)     
        if x == 0:
            if y == 0:
                return self.is_flag(x+1, y) + self.is_flag(x+1, y+1) + self.is_flag(x, y+1) 
            elif y == self.TILES_Y - 1:
                return self.is_flag(x, y-1) + self.is_flag(x+1, y-1) + self.is_flag(x+1, y)
            else:
                return self.is_flag(x, y-1) + self.is_flag(x+1, y-1) + self.is_flag(x+1, y) + self.is_flag(x+1, y+1) + self.is_flag(x, y+1)
        elif x == self.TILES_X - 1:
            if y == 0:
                return self.is_flag(x-1, y) + self.is_flag(x-1, y+1) + self.is_flag(x, y+1)
            elif y == self.TILES_Y - 1:
                return self.is_flag(x, y-1) + self.is_flag(x-1, y-1) + self.is_flag(x-1, y)
            else:
                return self.is_flag(x, y-1) + self.is_flag(x-1, y-1) + self.is_flag(x-1, y) + self.is_flag(x-1, y+1) + self.is_flag(x, y+1)
        elif y == 0:
            return self.is_flag(x-1, y) + self.is_flag(x-1, y+1) + self.is_flag(x, y+1) + self.is_flag(x+1, y+1) + self.is_flag(x+1, y)
        elif y == self.TILES_Y - 1:
            return self.is_flag(x-1, y) + self.is_flag(x-1, y-1) + self.is_flag(x, y-1) + self.is_flag(x+1, y-1) + self.is_flag(x+1, y)
        else:
            return self.is_flag(x-1,y-1) + self.is_flag(x-1, y) + self.is_flag(x-1, y+1) + self.is_flag(x, y-1) + self.is_flag(x,y+1) + self.is_flag(x+1, y-1) + self.is_flag(x+1,y) + self.is_flag(x+1,y+1)

    def handle_click(self, event):
        pos = pygame.mouse.get_pos()
        x,y = (pos[0] // 30, pos[1] // 30)
        if self.board[x][y] != -2:
            if event.button == 1 : # if left click, get tile position and reveal
                self.reveal_tile(x,y)
            elif event.button == 3: # if right click, get tile position and reveal
                self.flag_tile(x,y)
            else:
                return
        else:
            return
    def flag_tile(self,x,y):
        print("Flagging ", x,y)
        rect = pygame.Rect(x*30,y*30,30,30)
        pygame.draw.rect(self.window, (255,0,0), rect)
        self.tiles[x][y].display(position=(x*30 + 10, y*30 + 5))
        return


    def reveal_tile(self, x,y):
        val = self.board[x][y]
        if val == -1:
            self.game_over()
        elif val == 0:
            self.clear_near_zeros(x,y)
        else:
            #change color of tile and display number
            print(x,y)
            rect = pygame.Rect(x*30,y*30,30,30)
            pygame.draw.rect(self.window, (200,200,200), rect)
            self.tiles[x][y].display(position=(x*30 + 10, y*30 + 5))
    
    def game_over(self):
        return 1
    
    def clear_near_zeros(self,x,y): # DFS implementation to check all NSEW tiles for non-negative tiles and clear them
        # base case, current tile is not a zero tile --> return
        if x < 0 or x == self.TILES_X or y < 0 or y == self.TILES_Y:
            return
        elif self.board[x][y] < 0:
            return
        elif self.board[x][y] != 0: # found a numbered tile, reveal and stop this search
            self.reveal_tile(x,y)
            self.board[x][y] == -2
        # replace current tile with clear tile if zero
        else:
            rect = pygame.Rect(x*30,y*30,30,30)
            pygame.draw.rect(self.window, (200,200,200), rect) #insert function to replace tile with clear tile
            self.board[x][y] = -2
            self.clear_near_zeros(x-1,y)
            self.clear_near_zeros(x+1,y)
            self.clear_near_zeros(x, y-1)
            self.clear_near_zeros(x,y+1)
        
        


def main():
    BLACK = (0, 0, 0)
    WHITE = (200, 200, 200)
    WINDOW_HEIGHT = 450
    WINDOW_WIDTH = 450

    pygame.init()
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    WINDOW.fill(BLACK)

    print('create board')
    miner = Minesweeper(WINDOW)
    print('print contents of board')
    miner.draw_board()
    for i in range(len(miner.board)):
        print(miner.board[i])
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            miner.handle_click(event)
        
        pygame.display.update()


if __name__ == '__main__':
    main()




'''


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

def drawGrid():
    blockSize = 20 # Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)


        font = pygame.font.SysFont('arial', 50)
        text = font.render(str(self.value), True, (0, 0, 0))
        self.window.blit(text, position)  

def set_flags():



def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    while True:
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main()


'''
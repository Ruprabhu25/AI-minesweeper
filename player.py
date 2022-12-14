import minesweeper, pygame, pyautogui

# main idea: player focuses on 3 tiles at a time, creates matrix of probabilities to adjacent hidden tiles
# determines highest probability (if 1, it will be an auto click)


class Player:
    def __init__(self):
        self.known_board = [[-2 for i in range(15)] for j in range(15)]
        self.pos = (0,0) # starting position

    # running continuously until win or loss
    def find_tiles(self, mat):
        board = self.known_board
        x,y = self.pos[0], self.pos[1]
        val = board[x][y]
        
    def check_tile_count(self, x, y, val):
        board = self.known_board
        unknown = -1 # for now
        count = 0
        mat = []
        #if board[x-1][y-1] == unknown or board[x][y-1] == unknown or board[x+1][y-1] == unknown or board[x-1][y] == unknown or board[x+1][y] == unknown or board[x-1][y+1] == unknown or board[x][y+1] == unknown or board[x+1][y+1] == unknown:
        for i in range(-1,2):
            for j in range(-1,2):
                posx = x+i
                posy = y+j
                if posx >= 0 and posx < len(self.known_board) and posy >= 0 and posy < len(self.known_board[0]):
                    if board[posx][posy] == unknown:
                        mat.append([posx,posy])
                        count = count + 1
        if count == val: # if count = val (of tile considered), then all unknown tiles should be flagged
            self.flag_tiles(mat)

    def update_known_board(self,x,y): # decrement nearby integers by 1 and set mine to 0

        return

    def reveal_click(self, x, y):
        pygame.mouse.set_pos(x,y)
        pyautogui.click()
        self.update_known_board()
    
    # implementation to show visually which tiles are being considered
    def current_targets(self):
        size = width, height = (30, 30)
        highlighted_tile = pygame.Surface(size, pygame.SRCALPHA)  # Creates an empty per-pixel alpha Surface.

        GREEN = (0, 255, 0, 255)
        pygame.draw.rect(highlighted_tile, GREEN, highlighted_tile.get_rect(), 10)
        

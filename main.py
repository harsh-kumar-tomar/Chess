import pygame 
import const
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

pygame.init()
# k -> king
# q -> queen
# b -> bishop (uth)
# r -> rook (hathi)
# p -> pawn 
# n -> knight
# e -> empty
board_matrix = [
    ["RB","NB","BB","QB","KB","BB","NB","RB"],
    ["PB","PB","PB","PB","PB","PB","PB","PB"],
    ["E","E","E","E","E","E","E","E"],
    ["E","E","E","E","E","E","E","E"],
    ["E","E","E","E","E","E","E","E"],
    ["E","E","E","QB","E","E","E","E"],
    ["PW","PW","PW","PW","PW","PW","PW","PW"],
    ["RW","NW","BW","KW","QW","BW","NW","RW"]
]

peices_assets = {}

def load_asset():
    peices_assets["KW"] = pygame.image.load("img/King/king_w.png")
    peices_assets["KB"] = pygame.image.load("img/King/king_b.png")
    
    peices_assets["QW"] = pygame.image.load("img/Queen/queen_w.png")
    peices_assets["QB"] = pygame.image.load("img/Queen/queen_b.png")
    
    peices_assets["NW"] = pygame.image.load("img/Knight/knight_w.png")
    peices_assets["NB"] = pygame.image.load("img/Knight/knight_b.png")
    
    peices_assets["BW"] = pygame.image.load("img/Bishop/bishop_w.png")
    peices_assets["BB"] = pygame.image.load("img/Bishop/bishop_b.png")

    peices_assets["RW"] = pygame.image.load("img/Rook/rook_w.png")
    peices_assets["RB"] = pygame.image.load("img/Rook/rook_b.png")

    peices_assets["PW"] = pygame.image.load("img/Pawn/pawn_w.png")
    peices_assets["PB"] = pygame.image.load("img/Pawn/pawn_b.png")

    for peice in peices_assets:
        peices_assets[peice] = pygame.transform.smoothscale(peices_assets[peice],const.PEICE_SCALE)

def draw_board():
    flag = False # True -> white , False -> black

    for y in range(0,const.HEIGHT,const.SQUARE_SIZE):
        flag = not flag
        for x in range(0,const.WIDTH,const.SQUARE_SIZE):
            color = const.WHITE_CHECK_COLOR if flag else const.BLACK_CHECK_COLOR
            flag = not flag
            pygame.draw.rect(screen,color,(x,y,const.SQUARE_SIZE,const.SQUARE_SIZE)) # where, color,(coordinates x , y , width , height)

def draw_peices():
    for i in range(0,len(board_matrix)):
        for j in range(0,len(board_matrix[0])):
            peice = board_matrix[i][j]  
            if peice != "E":
                rect = peices_assets[peice].get_rect(center = ( 
                    j * const.SQUARE_SIZE + const.SQUARE_SIZE // 2,
                    i * const.SQUARE_SIZE + const.SQUARE_SIZE // 2 )
                    )
                # screen.blit(peices_assets[peice],(j*const.SQUARE_SIZE+18,i*const.SQUARE_SIZE+20))
                screen.blit(peices_assets[peice],rect)

def king_exists(x,y):
    return (board_matrix[y][x] == "KB" or board_matrix[y][x] == "KW")
        

def find_possible_moves():
    
    x,y = peice_selected_x,peice_selected_y

    peice_code = board_matrix[y][x]
    peice , color = peice_code
    
    print(f"peice : {peice} , color : {color}")
    print(f"x : {x} , y : {y}")
    

    if peice == "P": # pawn
        direction = 1 if color == "B" else -1 # dir -> 1 (downward) , dir -> -1 upward

        new_y = y + direction       # normal single move (+1)
        new_y2 = y + 2*direction  # first move (+2)

        # check for single move
        if 0 <= new_y < 8 : # if new_y single move is within bounds and no other peice exists
            if board_matrix[new_y][x] == "E":
                
                peice_selected_possible_moves.append((x,new_y))

                # check for double moves
                if color == "B" and y == 1 and board_matrix[new_y2][x] == "E" :  # for black peice , double move
                    peice_selected_possible_moves.append((x,new_y2))
                
                if color == "W" and y == 6 and board_matrix[new_y2][x] == "E" : # for white peice , double move
                    peice_selected_possible_moves.append((x,new_y2))
            
            # CAPTURE ---------------------------------------------------------------------->
            # check for diagonal left and right  
            if x-1 >= 0 and board_matrix[new_y][x-1] != "E" and not king_exists(x-1,new_y):
                peice_selected_captures_moves.append((x-1,new_y))
            if x+1 < 8 and  board_matrix[new_y][x+1] != "E" and not king_exists(x+1,new_y):
                peice_selected_captures_moves.append((x+1,new_y))
            # CAPTURE ----------------------------------------------------------------------->

        # check for queen 

    if peice == "K": # King
        pass
    
    if peice == "N": # Knight

        # up L
        if  y + 2 < 8  :
            if x + 1 < 8 :
                put_in_moves_or_capture_moves(x+1,y+2)
            if x - 1 >= 0:
                put_in_moves_or_capture_moves(x-1,y+2)
        
        # down L
        if y-2 >= 0 :
            if x + 1 < 8:
                put_in_moves_or_capture_moves(x+1,y-2)
            if x - 1 >= 0 :
                put_in_moves_or_capture_moves(x-1,y-2)
        # left L        
        if x + 2 < 8 :
            if y + 1 < 8 :
                put_in_moves_or_capture_moves(x+2,y+1)
            if y - 1 >= 0:
                put_in_moves_or_capture_moves(x+2,y-1)
        
        # right L
        if x - 2 >= 0:
            if y + 1 < 8:
                put_in_moves_or_capture_moves(x-2,y+1)
            if y - 1 >= 0:
                put_in_moves_or_capture_moves(x-2,y-1)

    if peice == "B": # Bishop
        direction = [(1,1),(-1,1),(1,-1),(-1,-1)]

        for dx,dy in direction:
            new_x = x
            new_y = y
            
            while 0 <= new_x + dx < 8 and 0 <= new_y + dy < 8:
                new_x += dx
                new_y += dy
                
                put_in_moves_or_capture_moves(new_x ,new_y )
                if board_matrix[new_y][new_x] != "E" :
                    break

    if peice == "R": # Rook
        direction = [(0,1),(0,-1),(1,0),(-1,0)]

        for dx,dy in direction:
            new_x = x
            new_y = y   

            while 0 <= new_x + dx < 8 and 0 <= new_y + dy < 8 :
                new_x += dx
                new_y += dy

                put_in_moves_or_capture_moves(new_x ,new_y )
                if board_matrix[new_y][new_x] != "E" :
                    break

    if peice == "Q":  # Queen
        # using rook moves logic 
        direction = [(0,1),(0,-1),(1,0),(-1,0)]

        for dx,dy in direction:
            new_x = x
            new_y = y   

            while 0 <= new_x + dx < 8 and 0 <= new_y + dy < 8 :
                new_x += dx
                new_y += dy

                put_in_moves_or_capture_moves(new_x ,new_y )
                if board_matrix[new_y][new_x] != "E" :
                    break
        # using bishop moves logic 
        
        direction = [(1,1),(-1,1),(1,-1),(-1,-1)]

        for dx,dy in direction:
            new_x = x
            new_y = y
            
            while 0 <= new_x + dx < 8 and 0 <= new_y + dy < 8:
                new_x += dx
                new_y += dy
                
                put_in_moves_or_capture_moves(new_x ,new_y )
                if board_matrix[new_y][new_x] != "E" :
                    break


def is_enemy_peice(x,y):
    return board_matrix[y][x][1] != board_matrix[peice_selected_y][peice_selected_x][1]

def is_own_peice(x,y):
    return board_matrix[y][x][1] == board_matrix[peice_selected_y][peice_selected_x][1]

def put_in_moves_or_capture_moves(x,y):
    if board_matrix[y][x] == "E":
        peice_selected_possible_moves.append((x,y))
    elif is_enemy_peice(x,y) and not king_exists(x,y):
        peice_selected_captures_moves.append((x,y))

def draw_moves():
    
    # selected peice highlighted
    pygame.draw.rect( screen,const.GREEN,(
        peice_selected_x * const.SQUARE_SIZE ,
        peice_selected_y * const.SQUARE_SIZE ,
        const.SQUARE_SIZE,
        const.SQUARE_SIZE )
        ) 

    # selected peice moves highlighted
    for temp_x,temp_y in peice_selected_possible_moves:
                pygame.draw.circle(screen, const.GREY, (
                    temp_x * const.SQUARE_SIZE + const.SQUARE_SIZE//2 ,
                    temp_y * const.SQUARE_SIZE + const.SQUARE_SIZE//2 
                ), const.CIRCLE_RADIUS )
    
    # capture peice highlight
    for temp_x,temp_y in peice_selected_captures_moves:
        pygame.draw.rect( screen,const.RED,(
        temp_x * const.SQUARE_SIZE ,
        temp_y * const.SQUARE_SIZE ,
        const.SQUARE_SIZE,
        const.SQUARE_SIZE )
        ) 
                
def reset_selected_peice():
    global peice_selected_captures_moves,peice_selected_possible_moves,peice_selected,peice_selected_x,peice_selected_y
    peice_selected_x,peice_selected_y = -1,-1
    peice_selected_possible_moves = []
    peice_selected_captures_moves = []
    peice_selected = False

load_asset() # to get all images
screen = pygame.display.set_mode((const.WIDTH,const.HEIGHT))

icon = pygame.image.load("img/icon.png")

pygame.display.set_icon(icon)
pygame.display.set_caption(const.TITLE)

clock = pygame.time.Clock()
running = True

peice_selected_x, peice_selected_y = -1 , -1
peice_selected = False
peice_selected_color = ""
peice_selected_possible_moves = []
peice_selected_captures_moves = []

while running:
    clock.tick(const.FPS)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:

            curr_x,curr_y = event.pos
            
            curr_x = curr_x//const.SQUARE_SIZE
            curr_y = curr_y//const.SQUARE_SIZE

            if peice_selected and ( (curr_x,curr_y) in peice_selected_possible_moves or (curr_x,curr_y) in peice_selected_captures_moves ):
                peice_name = board_matrix[peice_selected_y][peice_selected_x] # get  perice name
                board_matrix[peice_selected_y][peice_selected_x] = "E" # put prev pos of peice to E
                board_matrix[curr_y][curr_x] = peice_name    # assign new pos to peice note: we are able to move peice + we are able to capture peices 
                reset_selected_peice()                      
            # if user  clicked on the already selected peice or user clicked on the empty space 
            elif (curr_x == peice_selected_x and curr_y == peice_selected_y) or board_matrix[curr_y][curr_x] == "E": 
                reset_selected_peice()
            else:
            # if user clicked on a  new peice , highlisht the selected peice and peice moves
                print("inside 3nd if")
                peice_selected_possible_moves = []
                peice_selected_captures_moves = []
                peice_selected = True
                peice_selected_x , peice_selected_y = curr_x, curr_y 
                find_possible_moves()
            
            
            
        
        if event.type == pygame.QUIT:
            running = False

    

    # screen.fill(const.BLACK)
    draw_board()
    if peice_selected :
        draw_moves() # draw selected peice and its moves

    draw_peices()

        

    pygame.display.update() # update only whats changed
    # pygame.display.flip()  # update complete screen

pygame.quit()





# docs
# blit is used to copy pixel from one pic to another 
# target_screen.blit(img,(x,y))


# get_rect
# pygame stores img as rectanglular grid of pixels , even if img is of another shape 
# get_rect only used to change pos
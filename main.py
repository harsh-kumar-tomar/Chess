import pygame 
import c
import ctypes
from c import CHESS_BOARD_Y as T_PADDING
from c import CHESS_BOARD_X as L_PADDING
ctypes.windll.shcore.SetProcessDpiAwareness(1)



# 9 
# 18
# 59
# 69
# 99
# 199

pygame.init()
# k -> king
# q -> queen
# b -> bishop (uth)
# r -> rook (hathi)
# p -> pawn 
# n -> knight
# e -> empty

# 4,0 -> x,y sense 
# 0,4 -> matrix sense

board_matrix = [
    ["RB","NB","BB","QB","KB","BB","NB","RB"], # 0
    ["PB","PB","PW","PB","PB","PB","PB","PB"], # 1
    ["E","E","E","E","E","E","E","E"],          # 2
    ["E","E","E","E","E","E","E","E"],          # 3
    ["E","E","E","E","E","E","E","E"],          # 4
    ["E","E","E","QB","E","E","E","E"],             # 5
    ["PW","PW","PW","PW","PW","PW","PW","PW"], # 6
    ["RW","NW","BW","KW","QW","BW","NW","RW"] #7
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
        peices_assets[peice] = pygame.transform.smoothscale(peices_assets[peice],c.PEICE_SCALE)

def draw_board():  
    flag = False # True -> white , False -> black

    y = c.CHESS_BOARD_Y

    for _ in range(8):
        flag = not flag
        x = c.CHESS_BOARD_X

        for _ in range(8):
            color = c.WHITE_CHECK_COLOR if flag else c.BLACK_CHECK_COLOR
            flag = not flag
            pygame.draw.rect(screen,color,(x,y,c.SQUARE_SIZE,c.SQUARE_SIZE)) # where, color,(coordinates x , y , width , height)
            x += c.SQUARE_SIZE

        y += c.SQUARE_SIZE

def draw_peices():
    for i in range(0,len(board_matrix)):
        for j in range(0,len(board_matrix[0])):
            peice = board_matrix[i][j]  
            if peice != "E":
                rect = peices_assets[peice].get_rect(center = ( 
                    (j * c.SQUARE_SIZE + c.SQUARE_SIZE // 2) + c.CHESS_BOARD_X ,
                    (i * c.SQUARE_SIZE + c.SQUARE_SIZE // 2) + c.CHESS_BOARD_Y )
                    )
                # screen.blit(peices_assets[peice],(j*const.SQUARE_SIZE+18,i*const.SQUARE_SIZE+20))
                screen.blit(peices_assets[peice],rect)

def draw_king_check(x,y):
    color = c.KING_CHECK_COLOR
    
    pygame.draw.rect( screen,color,(
        (x * c.SQUARE_SIZE) + c.CHESS_BOARD_X ,
        (y * c.SQUARE_SIZE) + c.CHESS_BOARD_Y ,
        c.SQUARE_SIZE,
        c.SQUARE_SIZE )
        ) 
    
def draw_moves(dic : dict[int,list[int]] , x , y):

    # selected peice highlighted
    pygame.draw.rect( screen,c.GREEN,(
        (x * c.SQUARE_SIZE) + c.CHESS_BOARD_X  ,
        (y * c.SQUARE_SIZE ) + c.CHESS_BOARD_Y,
        c.SQUARE_SIZE,
        c.SQUARE_SIZE )
        ) 

    # selected peice moves highlighted
    for temp_x,temp_y in dic[MOVES]:
                pygame.draw.circle(screen, c.GREY, (
                    (temp_x * c.SQUARE_SIZE + c.SQUARE_SIZE//2) + c.CHESS_BOARD_X ,
                    (temp_y * c.SQUARE_SIZE + c.SQUARE_SIZE//2 ) + c.CHESS_BOARD_Y
                ), c.CIRCLE_RADIUS )
    
    # capture peice highlight
    for temp_x,temp_y in dic[CAPTURES]:
        if (temp_x,temp_y) == king[BLACK] or (temp_x,temp_y) == king[WHITE]:
            draw_king_check()
        else:
            pygame.draw.rect( screen,c.RED,(
            (temp_x * c.SQUARE_SIZE) + c.CHESS_BOARD_X ,
            (temp_y * c.SQUARE_SIZE) + c.CHESS_BOARD_Y ,
            c.SQUARE_SIZE,
            c.SQUARE_SIZE )
            ) 
    
    # # special case king check
    # if is_king_check:
    #     king_x , king_y = king_coordinates
    #     pygame.draw.rect( screen,const.KING_CHECK_COLOR,(
    #     (king_x * const.SQUARE_SIZE) + const.CHESS_BOARD_X ,
    #     (king_y * const.SQUARE_SIZE) + const.CHESS_BOARD_Y ,
    #     const.SQUARE_SIZE,
    #     const.SQUARE_SIZE )
    #     )    

def king_exists(x,y): # default MATRIX
    return (board_matrix[y][x] == "KB" or board_matrix[y][x] == "KW")
        
def add_moves(dic : dict[int,list[int]] , x , y ):
    dic[MOVES].append((x,y))

def add_captures(dic : dict[int,list[int]] , x , y):
    dic[CAPTURES].append((x,y))

def get_dic():
    return {
        MOVES : [],
        CAPTURES : []
    }

def find_pawn_moves(x,y):                                                                                                   

    color = get_peice_color(x,y)
    pawn_moves = get_dic()
    direction = 1 if color == "B" else -1 # dir -> 1 (downward) , dir -> -1 upward

    new_y = y + direction       # normal single move (+1)
    new_y2 = y + 2*direction  # first move (+2)

    # check for single move
    if 0 <= new_y < 8 : # if new_y single move is within bounds and no other peice exists
        if  is_check_empty(x,new_y):
            
            add_moves(pawn_moves,x,new_y)

            # check for double moves
            if color == BLACK and y == 1 and is_check_empty(x,new_y2) :  # for black peice , double move
                add_moves(pawn_moves,x,new_y2)
            elif color == WHITE and y == 6 and is_check_empty(x,new_y2) : # for white peice , double move
                add_moves(pawn_moves,x,new_y2)
        
        # check for diagonal left and right  
        if x-1 >= 0 and not is_check_empty(x-1,new_y) and is_enemy_peice(x-1,new_y,color)  :
            add_captures(pawn_moves,x-1,new_y)

        if x+1 < 8 and not is_check_empty(x+1,new_y) and is_enemy_peice(x+1,new_y,color):
            add_captures(pawn_moves,x+1,new_y)
    
    return pawn_moves
        
def set_pawn_choices():
    global pawn_choices

    x,y = pawn_overlay_pos
    color = get_peice_color(x,y)

    choices = ["N","Q","R","B"]

    for i in range(len(choices)):
        choices[i] += color
    
    i,j = 2,4

    for el in choices:
        pawn_choices[(i,j)] = el
        i += 1

def draw_pawn_choices():

    overlay = pygame.Surface((c.WINDOW_WIDTH,c.WINDOW_HEIGHT))
    overlay.set_alpha(170)
    overlay.fill((0,0,0))
    screen.blit(overlay,(0,0))
    
    # for bg
    pygame.draw.rect( screen,c.RED,(
            (2 * c.SQUARE_SIZE) + c.CHESS_BOARD_X    ,
            (4 * c.SQUARE_SIZE) + c.CHESS_BOARD_Y ,
            4*c.SQUARE_SIZE,
            c.SQUARE_SIZE )
            ) 
    
    # for peices 
    for x,y in pawn_choices.keys():
        peice_code = pawn_choices[(x,y)]

        rect = peices_assets[peice_code].get_rect(center = ( 
                        (x * c.SQUARE_SIZE + c.SQUARE_SIZE // 2) + c.CHESS_BOARD_X ,
                        (y * c.SQUARE_SIZE + c.SQUARE_SIZE // 2) + c.CHESS_BOARD_Y )
                        )
        screen.blit(peices_assets[peice_code],rect)
    
def find_knight_moves(x,y):
    k_moves = get_dic()
    color = get_peice_color(x,y)

    direction = [
        (2,1),(2,-1),
        (-2,1),(-2,-1),
        (1,2),(-1,2),
        (1,-2),(-1,-2)
    ]

    for dx,dy in direction:
        if 0 <= x+dx <8 and 0 <= y+dy < 8:
            put_in_moves_or_capture_moves(k_moves,x+dx,y+dy,color)

    return k_moves

def find_bishop_moves(x,y):

    b_moves = get_dic()
    color = get_peice_color(x,y)
    direction = [(1,1),(-1,1),(1,-1),(-1,-1)]

    for dx,dy in direction:
        new_x = x
        new_y = y
        
        while 0 <= new_x + dx < 8 and 0 <= new_y + dy < 8:
            new_x += dx
            new_y += dy
            
            put_in_moves_or_capture_moves(b_moves, new_x , new_y , color )
            if board_matrix[new_y][new_x] != "E" :
                break
    return b_moves

def find_rook_moves(x,y):

    r_moves = get_dic()
    color = get_peice_color(x,y)

    direction = [(0,1),(0,-1),(1,0),(-1,0)]

    for dx,dy in direction:
        new_x = x
        new_y = y   

        while 0 <= new_x + dx < 8 and 0 <= new_y + dy < 8 :
            new_x += dx
            new_y += dy

            put_in_moves_or_capture_moves(r_moves,new_x ,new_y , color)
            if board_matrix[new_y][new_x] != "E" :
                break
    return r_moves

def find_queen_moves(x,y):
    q_moves = get_dic()

    r_moves = find_rook_moves(x,y)
    b_moves = find_bishop_moves(x,y)

    q_moves[MOVES].extend(r_moves[MOVES])
    q_moves[CAPTURES].extend(r_moves[CAPTURES])
    
    q_moves[MOVES].extend(b_moves[MOVES])
    q_moves[CAPTURES].extend(b_moves[CAPTURES])

    return q_moves

def find_king_moves(x,y):
    k_moves = get_dic()
    color = get_peice_color(x,y)
    direction = [
        (0,1) , (0,-1),
        (1,0) , (-1,0),
        (1,1) , (-1,-1),
        (1,-1) , (-1,1)
    ]

    for dx,dy in direction:
        if 0 <= x+dx <8 and 0 <= y+dy < 8:
            put_in_moves_or_capture_moves(k_moves,x+dx,y+dy,color)

    return k_moves

def find_peice_moves(x,y):
    
    peice_name = get_peice_name(x,y)
    
    match peice_name :

        case "P": # pawn
            return find_pawn_moves(x,y)
            
        case "K": # King
            return find_king_moves(x,y)
            
        case "N": # Knight
            return find_knight_moves(x,y)
        
        case "B": # Bishop
            return find_bishop_moves(x,y)

        case "R": # Rook
            return find_rook_moves(x,y)

        case "Q":  # Queen
            return find_queen_moves(x,y)

    return get_dic()

def is_enemy_peice(x,y,color):
    return get_peice_color(x,y) != color 

def get_peice_name(x,y):
    return board_matrix[y][x][0]

def get_peice_color(x,y):       # default matrix 
    return board_matrix[y][x][1]

def get_enemy_peice_color(x,y):
    return WHITE if board_matrix[y][x] == BLACK else WHITE

def is_own_peice(x,y,color):
    return get_peice_color(x,y) == color

# is space empty
def is_check_empty(x,y):
    return board_matrix[y][x] == "E"

# works for all except pawn
def put_in_moves_or_capture_moves(dic : dict[int,list[int]],x,y , color):
    if is_check_empty(x,y):                                                                                                                                                          
        add_moves(dic,x,y)
    elif is_enemy_peice(x,y,color) :
        add_captures(dic,x,y)
            
def reset_selected_peice():
    global peice
    peice[SELECTED] = False
    peice[POSITION] = (-1,-1)
    peice[MOVES] = []
    peice[CAPTURES] = []

def get_all_peice_moves(color):
    total_moves = get_dic()
    
    for i in range(8):
        for j in range(8):
            if board_matrix[i][j] != "E" and board_matrix[i][j][1] == color:
                result = find_peice_moves(j,i)
                if result[MOVES] :
                    total_moves[MOVES].extend(result[MOVES])
                if result[CAPTURES] :
                    total_moves[CAPTURES].extend(result[CAPTURES])

    return total_moves

def will_this_move_cause_check(prev_x,prev_y,tar_x,tar_y):
    initial_code = board_matrix[prev_y][prev_x]
    final_code = board_matrix[tar_y][tar_x]

    color = get_peice_color(prev_x,prev_y)
    #  future state looks like 
    if get_peice_name(prev_x,prev_y) == c.KING:
        king[color] = tar_x,tar_y

    board_matrix[prev_y][prev_x] = "E"
    board_matrix[tar_y][tar_x] = initial_code
    
    # get all peice moves of opposite color 
    tot_moves = get_all_peice_moves(WHITE if color == BLACK else BLACK)

    # restore  the prev state
    board_matrix[prev_y][prev_x] = initial_code
    board_matrix[tar_y][tar_x] = final_code
    
    result = False if king[color] in tot_moves[CAPTURES] else True
    
    if get_peice_name(prev_x,prev_y) == c.KING:
        king[color] = prev_x,prev_y
    return result

# this method check what if we move the peice to the curr_peice[MOVES] , curr_peice[CAPTURES]  
def move_validation(dic,prev_x , prev_y):
    
    temp_moves = []
    temp_captures = []

    if dic[MOVES]:
        for tar_x,tar_y in dic[MOVES]:
            if will_this_move_cause_check(prev_x,prev_y,tar_x,tar_y):
                temp_moves.append((tar_x,tar_y))

    if dic[CAPTURES]:
        for tar_x,tar_y in dic[CAPTURES]:
            if will_this_move_cause_check(prev_x,prev_y,tar_x,tar_y):
                temp_captures.append((tar_x,tar_y))
    
    dic[MOVES] = temp_moves
    dic[CAPTURES] = temp_captures

def get_peice_code(x,y):
    return board_matrix[y][x]

def is_king_in_check(color):
    x,y = king[color]
    enemy_color = get_enemy_peice_color(x,y)

    total_moves = get_all_peice_moves(enemy_color)

    return True if (x,y) in total_moves[CAPTURES] else False

def move_peice(prev_x,prev_y,tar_x,tar_y):
    board_matrix[tar_y][tar_x] = board_matrix[prev_y][prev_x]
    board_matrix[prev_y][prev_x] = "E"

def check_check_mate():
    pass

# constants
SELECTED = 0
POSITION = 1
COLOR = 2
MOVES = "MOVES"
CAPTURES = "CAPTURES"
CODE = 5
NAME = 6
WHITE = "W"
BLACK = "B"
MATRIX = "MATRIX"
COORDINATES = "COORDINATES"


load_asset() # to get all images
screen = pygame.display.set_mode((c.WINDOW_WIDTH,c.WINDOW_HEIGHT))
icon = pygame.image.load("img/icon.png")

pygame.display.set_icon(icon)
pygame.display.set_caption(c.TITLE)

clock = pygame.time.Clock()
running = True

# selected peice variables
peice = {
    SELECTED : False ,
    NAME : "" ,
    CODE : "",
    COLOR : "",
    POSITION : (-1,-1),
    MOVES : [],
    CAPTURES : []
}

king = {
    WHITE : (3,7),
    BLACK : (4,0)
}

current_turn = WHITE 

pawn_overlay_active = False
pawn_overlay_pos = (-1,-1)
pawn_choices = {} # coordinates , peice name 

is_check_mate = False
is_king_check = False
king_coordinates = (-1,-1)



# if user clicked on a new peice ->  highlisht the selected peice and peice moves
def select_peice(curr_x,curr_y):
    global is_check_mate
    peice[CODE] = get_peice_code(curr_x,curr_y)
    peice[NAME] , peice[COLOR] = get_peice_code(curr_x,curr_y)
    peice[SELECTED] = True
    peice[POSITION] = curr_x, curr_y 
    
    curr_peice_moves = find_peice_moves(curr_x,curr_y)
    
    move_validation(curr_peice_moves,curr_x,curr_y) # to filter out all_moves , remove moves which can cause check to its own king 

    if check_check_mate():
        is_check_mate = True
    else:
        peice[MOVES] = curr_peice_moves[MOVES]
        peice[CAPTURES] = curr_peice_moves[CAPTURES]

def check_pawn_promotion(x,y):
    if get_peice_name(x,y) != c.PAWN :
        return False
    
    color = get_peice_color(x,y)

    if color == WHITE and y == 0:
        return True
    elif color == BLACK and y == 7:
        return True

    return False


#  peice selected  -> yes , user clicked on normal moves or capture moves -> yes == > move the peice
def handle_board_click(curr_x,curr_y):
    global pawn_overlay_active , pawn_overlay_pos , current_turn

    if peice[SELECTED] and ( (curr_x,curr_y) in peice[MOVES] or (curr_x,curr_y) in peice[CAPTURES] ):
        # before moving check for check
            prev_x,prev_y =  peice[POSITION]
            move_peice(prev_x,prev_y,curr_x,curr_y)   # assign new pos to peice note: we are able to move peice + we are able to capture peices 
            reset_selected_peice()        

            current_turn = BLACK if current_turn == WHITE else WHITE # change the turns 

            if check_pawn_promotion(curr_x,curr_y):
                pawn_overlay_active = True
                pawn_overlay_pos = (curr_x,curr_y)
                set_pawn_choices()
                return

    
    # if user  clicked on the already selected peice or user clicked on the empty space -> rest the state
    elif (curr_x , curr_y) == peice[POSITION] or  is_check_empty(curr_x,curr_y): 
        reset_selected_peice()
    elif current_turn == get_peice_color(curr_x,curr_y):
        select_peice(curr_x,curr_y)

def reset_pawn_overlay():
    global pawn_overlay_active , pawn_overlay_pos , pawn_choices
    pawn_overlay_active = False
    pawn_overlay_pos = -1,-1
    pawn_choices = {}

def handle_pawn_overlay(curr_x,curr_y):
    if (curr_x,curr_y) in pawn_choices:
        pawn_x,pawn_y = pawn_overlay_pos
        board_matrix[pawn_y][pawn_x] = pawn_choices[(curr_x,curr_y)]    # setting choice peice code
        reset_pawn_overlay()

def draw_check_mate_screen():
    color = current_turn
    print(f"Check Mate : {color} ")

while running:

    clock.tick(c.FPS)

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN :
            curr_x,curr_y = event.pos
            curr_x = (curr_x - c.CHESS_BOARD_X)//c.SQUARE_SIZE  
            curr_y = (curr_y - c.CHESS_BOARD_Y)//c.SQUARE_SIZE
        
            if pawn_overlay_active  : # user clicked somewhere 
                handle_pawn_overlay(curr_x,curr_y)
            else:
                handle_board_click(curr_x,curr_y)
                    
        if event.type == pygame.QUIT:
            running = False

    

    screen.fill(c.BG_COLOR)
    draw_board()

    if peice[SELECTED] :
        draw_moves(peice,*peice[POSITION]) # draw selected peice and its moves

    # if is_king_check or is_king_in_check(current_turn):
    #     draw_king_check(king[current_turn])
    #     is_king_check = True
        

    draw_peices()
    
    if pawn_overlay_active:
        draw_pawn_choices()
    
    if is_check_mate :
        draw_check_mate_screen()

    pygame.display.update() # update only whats changed

pygame.quit()





# docs
# blit is used to copy pixel from one pic to another 
# target_screen.blit(img,(x,y))


# get_rect
# pygame stores img as rectanglular grid of pixels , even if img is of another shape 
# get_rect only used to change pos
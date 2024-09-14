import pygame
import numpy

SQUARE_SIZE=200

SCREEN_WIDTH ,SCREEN_HEIGHT= 600,600

BLACK = (0,0,0)

WHITE = (255,255,255)

xplayer = 1

oplayer=0

def draw_board(window,board):

    colors = [pygame.Color(BLACK), pygame.Color(WHITE)]
    #LINES:

    #Horizental
    pygame.draw.line(window,colors[0],(0,SQUARE_SIZE),(SCREEN_WIDTH,SQUARE_SIZE),15)
    pygame.draw.line(window,colors[0],(0,SQUARE_SIZE*2),(SCREEN_WIDTH,SQUARE_SIZE*2),15)
    #vertical
    pygame.draw.line(window,colors[0],(SQUARE_SIZE,0),(SQUARE_SIZE,SCREEN_HEIGHT),15)
    pygame.draw.line(window,colors[0],(SQUARE_SIZE*2,0),(SQUARE_SIZE*2,SCREEN_HEIGHT),15)

    for row in range(3):
        for col in range(3):
            if board[row][col] ==None:
                continue
            elif board[row][col]=="x":
                drawX(window,(col,row))
            elif board[row][col] =="o":
                drawO(window,(col,row))

            
def activate_board(window):
    board = [
        [None] *3,
        [None] *3,
        [None] *3
    ]
    return board

def drawX(window,pos):
    pygame.draw.line(window,(0,0,0),((pos[0])*SQUARE_SIZE+SQUARE_SIZE/4,(pos[1])*SQUARE_SIZE+SQUARE_SIZE/4)
                     ,((pos[0]+1)*SQUARE_SIZE-SQUARE_SIZE/4,(pos[1]+1)*SQUARE_SIZE-SQUARE_SIZE/4),15)
    
    pygame.draw.line(window,(0,0,0),((pos[0])*SQUARE_SIZE+SQUARE_SIZE/4,(pos[1]+1)*SQUARE_SIZE-SQUARE_SIZE/4)
                     ,((pos[0]+1)*SQUARE_SIZE-SQUARE_SIZE/4,(pos[1])*SQUARE_SIZE+SQUARE_SIZE/4),15)

def drawO(window,pos):
    center_coordinates= ((pos[0]+1)*SQUARE_SIZE -SQUARE_SIZE/2,(pos[1]+1)*SQUARE_SIZE-SQUARE_SIZE/2)
    pygame.draw.circle(window,(0,0,0),center_coordinates,SQUARE_SIZE/3,10)

def play(board,current_player,pos):
    #TODO: detection of which figure it is

    if current_player:
        board[pos[1]][pos[0]] = "x"
    else :
        board[pos[1]][pos[0]] = "o"
    draw_board(screen,board)

def gameOver(board):
    for row in range(3): #check horizental
        if board[row][0]==board[row][1]==board[row][2] and board[row][0]!=None:
            print(board[row][0]," player won")
            return 1
    for col in range(3): #check verticle
        if board[0][col]==board[1][col]==board[2][col] and board[0][col]!=None:
            print(board[0][col]," player won")
            return 1
    if board[0][0]==board[1][1]==board[2][2] and board[0][0]!=None:
            print(board[0][0]," player won")
            return 1
    if board[0][2]==board[1][1]==board[2][0] and board[0][2]!=None:
            print(board[0][2]," player won")
            return 1
    for row in range(3):
        for col in range(3):
            if board[row][col] == None:
                return 0
    print("A tie")
    exit()
            

pygame.init()
screen = pygame.display.set_mode((600, 600)) #to draw 8x8 perfect squares
clock = pygame.time.Clock()
font = pygame.font.SysFont('Courier New', 30)
screen.fill((255,255,255))

text_surface = None
currrent_player=xplayer

running = True
switch = 0
board = activate_board(screen) #where the board is created without a gui
while running:
    screen.fill((255,255,255))
    draw_board(screen,board)

    player = "x" if currrent_player else "o"

    text_surface = font.render(f'Make a move player '+player, True, (0,0,0))
    text_rect = text_surface.get_rect()
    text_rect.center=(300,300)
    screen.blit(text_surface,text_rect)
    
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            y = int(y / 200)
            x = int(x / 200)

            if board[y][x]==None: #if play is possible
                play(board,currrent_player,(x,y))
                currrent_player = 1 if currrent_player == 0 else 0

                #check if the game is over
                if gameOver(board):
                    exit()



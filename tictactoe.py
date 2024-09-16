import pygame
from ultralytics import YOLO
import cv2
import math
SQUARE_SIZE=200

SCREEN_WIDTH ,SCREEN_HEIGHT= 600,600

BLACK = (0,0,0)

WHITE = (255,255,255)

xplayer = 1

oplayer=0

model = YOLO('best.pt')

def draw_board(window,board,text_surface):
    screen.fill((255,255,255))

    colors = [pygame.Color(BLACK), pygame.Color(WHITE)]
    #LINES:

    #Horizental
    pygame.draw.line(window,colors[0],(0,SQUARE_SIZE),(SCREEN_WIDTH,SQUARE_SIZE),10)
    pygame.draw.line(window,colors[0],(0,SQUARE_SIZE*2),(SCREEN_WIDTH,SQUARE_SIZE*2),10)
    #vertical
    pygame.draw.line(window,colors[0],(SQUARE_SIZE,0),(SQUARE_SIZE,SCREEN_HEIGHT),10)
    pygame.draw.line(window,colors[0],(SQUARE_SIZE*2,0),(SQUARE_SIZE*2,SCREEN_HEIGHT),10)

    for row in range(3):
        for col in range(3):
            if board[row][col] ==None:
                continue
            elif board[row][col]=="x":
                drawX(window,(col,row))
            elif board[row][col] =="o":
                drawO(window,(col,row))
    if text_surface == None:
        return
    text_rect = text_surface.get_rect()
    text_rect.center=(300,300)
    screen.blit(text_surface,text_rect)

            
def activate_board(window):
    board = [
        [None] *3,
        [None] *3,
        [None] *3
    ]
    return board

def drawX(window,pos):
    pygame.draw.line(window,(0,0,0),((pos[0])*SQUARE_SIZE+SQUARE_SIZE/4,(pos[1])*SQUARE_SIZE+SQUARE_SIZE/4)
                     ,((pos[0]+1)*SQUARE_SIZE-SQUARE_SIZE/4,(pos[1]+1)*SQUARE_SIZE-SQUARE_SIZE/4),10)
    
    pygame.draw.line(window,(0,0,0),((pos[0])*SQUARE_SIZE+SQUARE_SIZE/4,(pos[1]+1)*SQUARE_SIZE-SQUARE_SIZE/4)
                     ,((pos[0]+1)*SQUARE_SIZE-SQUARE_SIZE/4,(pos[1])*SQUARE_SIZE+SQUARE_SIZE/4),10)

def drawO(window,pos):
    center_coordinates= ((pos[0]+1)*SQUARE_SIZE -SQUARE_SIZE/2,(pos[1]+1)*SQUARE_SIZE-SQUARE_SIZE/2)
    pygame.draw.circle(window,(0,0,0),center_coordinates,SQUARE_SIZE/3,10)

def detect_gesture_and_play(board,text_surface):
    ret, frame = cap.read()
    if not ret:
        return

    results = model(frame)

    for r in results:
        for box in r.boxes:
            cls = int(box.cls.item())
            x_min, y_min, x_max, y_max =  box.xyxy.tolist()[0]

            x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])
            if cls == 0:  
                gesture = "x"
            elif cls == 1:  
                gesture = "o"
            else:
                continue


            center_x = (x_min + x_max) / 2
            center_y = (y_min+100 + y_max) / 2


            grid_x = int(center_x / 200)
            grid_y =int(center_y/ 200)
            if grid_x >2:
                grid_x = 2
            if grid_y >2:
                grid_y = 2


            if board[grid_y][grid_x] is None:
                text_surface = font.render(f'player ' + gesture + ' made a move', True, (0, 0, 0))
                board[grid_y][grid_x] = gesture
                draw_board(screen,board,text_surface)
                pygame.display.flip()
                return True  # Move was made, return True to toggle the player
    return False  # No move was made


def gameOver(board):
    for row in range(3): #check horizental
        if board[row][0]==board[row][1]==board[row][2] and board[row][0]!=None:
            text_surface = font.render(board[row][1]+" "+"player won", True, (0,0,0))
            draw_board(screen,board,text_surface)
            pygame.draw.line(screen,BLACK,(0,row*SQUARE_SIZE+SQUARE_SIZE/2),(SCREEN_WIDTH,row*SQUARE_SIZE+SQUARE_SIZE/2),15)
            return 1
    for col in range(3): #check verticle
        if board[0][col]==board[1][col]==board[2][col] and board[0][col]!=None:
            text_surface = font.render(board[0][col]+" player won", True, (0,0,0))
            draw_board(screen,board,text_surface)
            pygame.draw.line(screen,BLACK,(col*SQUARE_SIZE+SQUARE_SIZE/2,0),(col*SQUARE_SIZE+SQUARE_SIZE/2,SCREEN_HEIGHT),15)
            return 1
    if board[0][0]==board[1][1]==board[2][2] and board[0][0]!=None:
            text_surface = font.render(board[0][0]+" player won", True, (0,0,0))
            draw_board(screen,board,text_surface)
            pygame.draw.line(screen,BLACK,(0,0),(SCREEN_WIDTH,SCREEN_HEIGHT),15)
            return 1
    if board[0][2]==board[1][1]==board[2][0] and board[0][2]!=None:
            text_surface = font.render(board[0][2]+" player won", True, (0,0,0))
            draw_board(screen,board,text_surface)
            pygame.draw.line(screen,BLACK,(SCREEN_WIDTH,0),(0,SCREEN_HEIGHT),15)
            return 1
    for row in range(3):
        for col in range(3):
            if board[row][col] == None:
                return 0
    text_surface = font.render("A tie", True, (0,0,0))
    draw_board(screen,board,text_surface)
    return 1
            

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #to draw 8x8 perfect squares
clock = pygame.time.Clock()
font = pygame.font.SysFont('Courier New', 30)
screen.fill((255,255,255))

text_surface = None

running = True

board = activate_board(screen) #where the board is created without a gui

draw_board(screen,board,text_surface)
pygame.display.flip()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
ret, frame = cap.read()
cv2.imshow('Webcam', frame)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if detect_gesture_and_play(board,text_surface):
        if gameOver(board):
            pygame.display.flip()
            while True:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    exit()
                continue
    ret, frame = cap.read()
    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()



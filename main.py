import pygame
import gamemanager
import random

pygame.init()
WIDTH, HEIGHT = 900, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris!")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Calibri", 11, bold=True)
available_pieces_list = ["I", "O", "L", "J", "S", "Z", "T"]
Grid_Width = 10
Grid_Height = 24
Invisible_Rows = 4
if (576 / Grid_Width) <= (480 / Grid_Height):
    Square_Size = 576 / Grid_Height
if (576 / Grid_Width) > (480 / Grid_Height):
    Square_Size = 480 / Grid_Height
Grid_rect_list = []
can_move_down = True

DAS = 9
ARR = 1
SDF = 30
GRAV = 120

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)

def Create_Grid():

    for y in range(Grid_Height):
        for x in range(Grid_Width):
            eggs = x*(Square_Size + 1) + ((WIDTH / 2) - (Square_Size * Grid_Width / 2))
            whys = y*(Square_Size + 1) + ((HEIGHT / 2) - (Square_Size * Grid_Height / 2))
            rect = pygame.Rect(eggs, whys, Square_Size, Square_Size)
            pygame.draw.rect(WIN, BLACK, rect)

    pygame.display.update()

def update_fps():
    coverrect = pygame.Rect(0, 0, 60, 40)
    pygame.draw.rect(WIN, BLACK, coverrect)
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps + " FPS", 1, pygame.Color("white"))
    WIN.blit(fps_text, (6,4))

def draw_window(gamestate):
    for r in range(Grid_Height):
        for c in range(Grid_Width):
            piece = gamestate.grid[r][c]
            cols = c*(Square_Size + 1) + ((WIDTH / 2) - (Square_Size * Grid_Width / 2))
            rols = r*(Square_Size + 1) + ((HEIGHT / 2) - (Square_Size * Grid_Height / 2))
            if piece != "-":
                tetrominodominay = pygame.Rect(cols, rols, Square_Size, Square_Size)
                if piece == "S":
                    pygame.draw.rect(WIN, GREEN, tetrominodominay)
                elif piece == "Z":
                    pygame.draw.rect(WIN, RED, tetrominodominay)
                elif piece == "J":
                    pygame.draw.rect(WIN, BLUE, tetrominodominay)
                elif piece == "L":
                    pygame.draw.rect(WIN, ORANGE, tetrominodominay)
                elif piece == "O":
                    pygame.draw.rect(WIN, YELLOW, tetrominodominay)
                elif piece == "I":
                    pygame.draw.rect(WIN, CYAN, tetrominodominay)
                elif piece == "T":
                    pygame.draw.rect(WIN, PURPLE, tetrominodominay)

            elif piece == "-":
                if r <= Invisible_Rows:
                    tetrominodominay = pygame.Rect(cols, rols, Square_Size, Square_Size)
                    pygame.draw.rect(WIN, BLACK, tetrominodominay)
                elif r > Invisible_Rows:
                    tetrominodominay = pygame.Rect(cols, rols, Square_Size, Square_Size)
                    pygame.draw.rect(WIN, WHITE, tetrominodominay)

    update_fps()
    pygame.display.update()

def main():

    FPS = 60

    piecetype_selector = random.randint(0, 6)
    T = gamemanager.tetromino(available_pieces_list[0])
    gs = gamemanager.gamestate(10, 24, 4)
    gs.update_tetromino(T)
    DAS_counter = 0
    ARR_counter = 0
    GRAV_counter = 0
    SDM = 1
    end_piece = False
    keypress_old = {
        "RIGHT": False,
        "LEFT": False,
    }

    Create_Grid()

    run = True
    while run:

        clock.tick(FPS)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # clockwise rotation
                    gs.rotate_tetromino(T, 1)
                elif event.key == pygame.K_z:
                    # CCW rotation
                    gs.rotate_tetromino(T, -1)
                if event.key == pygame.K_RIGHT:
                    gs.move_tetromino(T, False, 1)
                elif event.key == pygame.K_LEFT:
                    gs.move_tetromino(T, False, -1)
                if event.key == pygame.K_DOWN:
                    SDM = SDF
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    keypress_old["RIGHT"] = False
                    DAS_counter = 0
                    ARR_counter = 0
                if event.key == pygame.K_LEFT:
                    keypress_old["LEFT"] = False
                    DAS_counter = 0
                    ARR_counter = 0
                if event.key == pygame.K_DOWN:
                    SDM = 1             

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            if keypress_old["RIGHT"] == True:
                if DAS_counter < DAS:
                    DAS_counter += 1
                elif DAS_counter == DAS:
                    if ARR_counter < ARR:
                        ARR_counter += 1
                    elif ARR_counter == ARR:
                        gs.move_tetromino(T, False, 1)
                        ARR_counter = 0
            keypress_old["RIGHT"] = True
        if keys_pressed[pygame.K_LEFT]:
            if keypress_old["LEFT"] == True:
                if DAS_counter < DAS:
                    DAS_counter += 1
                elif DAS_counter == DAS:
                    if ARR_counter < ARR:
                        ARR_counter += 1
                    elif ARR_counter == ARR:
                        gs.move_tetromino(T, False, -1)
                        ARR_counter = 0
            keypress_old["LEFT"] = True 
        
        if GRAV_counter < GRAV:
            GRAV_counter += SDM
        elif GRAV_counter >= GRAV:
            end_piece = gs.move_tetromino(T, True, 1)
            GRAV_counter = 0
        
        if end_piece == True:
            end_piece = False
            piecetype_selector = random.randint(0, 6)
            T = gamemanager.tetromino(available_pieces_list[piecetype_selector])
            for row in range(len(gs.grid)):
                if gs.grid[row].count("-") == 0:
                    gs.grid.pop(row)
                    gs.grid.insert(0, ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"])
    
        draw_window(gs)

    pygame.quit()

if __name__ == "__main__":
    main()

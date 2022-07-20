import pygame
import gamemanager
import piece_data
import math

pygame.init()
WIDTH, HEIGHT = 900, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Tetris!")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Calibri", 11, bold=True)
available_pieces_list = ["I", "O", "L", "J", "S", "Z", "T"]
Grid_Width = 10
Grid_Row = []
searchable_indexes = []
for i in range(Grid_Width):
    Grid_Row.append("-")
for i in range(Grid_Width):
    searchable_indexes.append(i)
Grid_Height = 24
Invisible_Rows = 4
Square_SizeD = 20
Square_Size = 20
Grid_rect_list = []

DAS = 9
ARR = 1
SDF = 30
GRAV = 30
GRACE = GRAV

V_LIGHT_GREY = (28, 28, 28)
BLACK = (0, 0, 0)
GREEN = (130, 178, 49)
BLUE = (78, 61, 164)
RED = (178, 51, 58)
ORANGE = (226, 111, 40)
YELLOW = (178, 152, 49)
CYAN = (49, 178, 130)
PURPLE = (164, 61, 154)
GREY = (40, 40, 40)

colors = {
    "I": CYAN,
    "O": YELLOW,
    "J": BLUE,
    "L": ORANGE,
    "Z": RED,
    "S": GREEN,
    "T": PURPLE
}

def update_fps():
    coverrect = pygame.Rect(0, 0, 60, 40)
    pygame.draw.rect(WIN, BLACK, coverrect)
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps + " FPS", 1, pygame.Color("white"))
    WIN.blit(fps_text, (6,4))

def draw_window(gamestate, holdqueue):

    def draw_outer_mino(RHOLS, CHOLS, disp, starting_locx, starting_locy, pez, u):
        for r2 in range(RHOLS):
            for c2 in range(CHOLS):
                peace = disp[r2][c2]
                if peace == 1:
                    REAL_peace = pygame.Rect(starting_locx + (Square_Size + 1) * c2, starting_locy + (Square_Size + 1) * r2 + (u) * ((Square_Size + 1) * 3), Square_Size, Square_Size)
                    pygame.draw.rect(WIN, colors[pez], REAL_peace)

    mult_x = WIN.get_width() / WIDTH
    mult_y = WIN.get_height() / HEIGHT
    Square_Size = int(Square_SizeD * math.sqrt(mult_x * mult_y))
    b_left = (WIN.get_width() / 2) - ((Square_Size + 1) * (Grid_Width / 2)) - 1
    bh_top = (WIN.get_height() / 2) - ((Square_Size + 1) * (Grid_Height - Invisible_Rows) / 2) - 1
    board_background = pygame.Rect(b_left, bh_top, (Square_Size + 1) * Grid_Width + 1, (Square_Size + 1) * (Grid_Height - Invisible_Rows) + 1)
    pygame.draw.rect(WIN, V_LIGHT_GREY, board_background)
    q_left = (WIN.get_width() / 2) + ((Square_Size + 1) * (Grid_Width / 2)) + 2
    queue_background = pygame.Rect(q_left, bh_top, (Square_Size + 1) * 5 + 1, (Square_Size + 1) * 15 + 1)
    pygame.draw.rect(WIN, V_LIGHT_GREY, queue_background)
    h_left = (WIN.get_width() / 2) - ((Square_Size + 1) * (Grid_Width / 2)) - (Square_Size + 1) * 5 - 4
    hold_background = pygame.Rect(h_left, bh_top, (Square_Size + 1) * 5 + 1, (Square_Size + 1) * 3 + 1)
    pygame.draw.rect(WIN, V_LIGHT_GREY, hold_background)
    for i in range(5):
        queue_slot = pygame.Rect(q_left + 1, bh_top + 1 + (i) * ((Square_Size + 1) * 3), (Square_Size + 1) * 5 - 1, (Square_Size + 1) * 3 - 1)
        pygame.draw.rect(WIN, BLACK, queue_slot)
    for r in range(Grid_Height):
        for c in range(Grid_Width):
            piece = gamestate.grid[r][c]
            cols = c*(Square_Size + 1) + ((WIN.get_width() / 2) - ((Square_Size + 1) * Grid_Width / 2))
            rols = r*(Square_Size + 1) + ((WIN.get_height() / 2) - ((Square_Size + 1) * (Grid_Height - Invisible_Rows) / 2)) - ((Square_Size + 1) * Invisible_Rows)
            if piece != "-":
                tetrominodominay = pygame.Rect(cols, rols, Square_Size, Square_Size)
                pygame.draw.rect(WIN, colors[piece], tetrominodominay)

            elif piece == "-":
                tetrominodominay = pygame.Rect(cols, rols, Square_Size, Square_Size)
                pygame.draw.rect(WIN, BLACK, tetrominodominay)
    for u in range(5):
        queue_display = piece_data.hq_dict[holdqueue.queue[u + 1]]
        rrols = len(queue_display)
        ccols = len(queue_display[0])
        starting_locx = q_left + 1 + (((Square_Size + 1) * 5 - 1) / 2 - (Square_Size + 1) * ccols /2)
        starting_locy = bh_top + 1 + (((Square_Size + 1) * 3 - 1) / 2 - (Square_Size + 1) * rrols /2)
        draw_outer_mino(rrols, ccols, queue_display, starting_locx, starting_locy, holdqueue.queue[u + 1], u)

    if len(holdqueue.hold) > 0:
        hold_display = piece_data.hq_dict[holdqueue.hold[0]]
        rrrols = len(hold_display)
        cccols = len(hold_display[0])
        htarting_locx = h_left + 1 + (((Square_Size + 1) * 5 - 1) / 2 - (Square_Size + 1) * cccols /2)
        htarting_locy = bh_top + 1 + (((Square_Size + 1) * 3 - 1) / 2 - (Square_Size + 1) * rrrols /2)
        draw_outer_mino(rrrols, cccols, hold_display, htarting_locx, htarting_locy, holdqueue.hold[0], 0)
    update_fps()
    pygame.display.update()

def main():

    FPS = 60

    gs = gamemanager.gamestate(Grid_Width, Grid_Height, 4)
    hq = gamemanager.upcoming()
    piece_type = hq.queue[0]
    T = gamemanager.tetromino(piece_type)
    gs.update_tetromino(T)
    DAS_counter = 0
    ARR_counter = 0
    GRAV_counter = 0
    GRACE_counter = 0
    BAG_counter = 1
    hard_dropped = False
    SDM = 1
    end_piece = False

    run = True
    while run:

        clock.tick(FPS)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    gs.rotate_tetromino(T, 1)
                elif event.key == pygame.K_z:
                    gs.rotate_tetromino(T, -1)
                if event.key == pygame.K_RIGHT:
                    gs.move_tetromino(T, False, 1)
                elif event.key == pygame.K_LEFT:
                    gs.move_tetromino(T, False, -1)
                if event.key == pygame.K_DOWN:
                    if SDF != "inf":
                        SDM = SDF
                    elif SDF == "inf":
                        gs.harddrop(T)
                if event.key == pygame.K_c:
                    new_piece = hq.update_hold(gs, T)
                    if hq.hold_usable:
                        T = gamemanager.tetromino(new_piece)
                        gs.update_tetromino(T)
                    hq.hold_usable = False
                if event.key == pygame.K_SPACE:
                    gs.harddrop(T)
                    end_piece = True
                    hard_dropped = True
                    GRACE_counter = GRACE - 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    DAS_counter = 0
                    ARR_counter = 0
                if event.key == pygame.K_LEFT:
                    DAS_counter = 0
                    ARR_counter = 0
                if event.key == pygame.K_DOWN:
                    SDM = 1             

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            if DAS_counter < DAS:
                DAS_counter += 1
            elif DAS_counter == DAS:
                if ARR_counter < ARR:
                    ARR_counter += 1
                elif ARR_counter == ARR:
                    gs.move_tetromino(T, False, 1)
                    ARR_counter = 0
        if keys_pressed[pygame.K_LEFT]:
            if DAS_counter < DAS:
                DAS_counter += 1
            elif DAS_counter == DAS:
                if ARR_counter < ARR:
                    ARR_counter += 1
                elif ARR_counter == ARR:
                    gs.move_tetromino(T, False, -1)
                    ARR_counter = 0
        
        if GRAV_counter < GRAV:
            GRAV_counter += SDM
        elif GRAV_counter >= GRAV and hard_dropped != True:
            end_piece = gs.move_tetromino(T, True, 1)
            GRAV_counter = 0
        
        if end_piece == True:
            GRACE_counter += 1
            if GRACE_counter == GRACE:
                hard_dropped = False
                GRACE_counter = 0
                end_piece = False
                BAG_counter += 1
                hq.queue.pop(0)
                hq.hold_usable = True
                new_piece = hq.queue[0]
                gs.clear_rows()
                T = gamemanager.tetromino(new_piece)
                gs.update_tetromino(T)
                if BAG_counter == 7:
                    BAG_counter = 0
                    hq.recharge()
        elif end_piece == False:
            GRACE_counter = 0
    
        draw_window(gs, hq)

    pygame.quit()

if __name__ == "__main__":
    main()

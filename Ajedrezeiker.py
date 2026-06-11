import pygame
import sys

pygame.init()


# CONFIG
font_small = pygame.font.SysFont("arial", 30)
font_big = pygame.font.SysFont("arial", 60)
font_title = pygame.font.SysFont("arial", 70)

rook_moved = {
    "white_left": False,
    "white_right": False,
    "black_left": False,
    "black_right": False
}

BOARD_SIZE = 800
PANEL = 200

WIDTH = BOARD_SIZE + PANEL
HEIGHT = BOARD_SIZE
SQ = BOARD_SIZE // 8

WHITE = (238, 238, 210)
BROWN = (118, 150, 86)
PANEL_BG = (30, 30, 30)
TEXT = (240, 240, 240)
CAPTURE_COLOR = (220, 50, 50)
MOVE_COLOR = (0, 200, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ajedrez")


# IMÁGENES DE LAS PIEZAS
piece_images = {}

def load_images():
    names = ["p","r","n","b","q","k"]

    for p in names:
        img_b = pygame.image.load(f"imageneschess/b{p}.png")
        img_b = pygame.transform.smoothscale(img_b, (SQ, SQ))
        piece_images[p] = img_b

        img_w = pygame.image.load(f"imageneschess/w{p}.png")
        img_w = pygame.transform.smoothscale(img_w, (SQ, SQ))
        piece_images[p.upper()] = img_w

load_images()


# TABLERO
board = [
    ["r","n","b","q","k","b","n","r"],
    ["p","p","p","p","p","p","p","p"],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["P","P","P","P","P","P","P","P"],
    ["R","N","B","Q","K","B","N","R"]
]

turn = "white"
selected = None
moves = []


# CONTADOR - 10 minutos
WHITE_TIME = 600
BLACK_TIME = 600
last_tick = pygame.time.get_ticks()

game_over = False
winner = None


king_moved = {"white": False, "black": False}

# UTILIDADES
def is_white(p): return p.isupper()
def is_black(p): return p.islower()

def in_bounds(r,c):
    return 0 <= r < 8 and 0 <= c < 8

def path_clear(sr,sc,er,ec):
    dr = er - sr
    dc = ec - sc

    step_r = 0 if dr == 0 else (1 if dr > 0 else -1)
    step_c = 0 if dc == 0 else (1 if dc > 0 else -1)

    r,c = sr+step_r, sc+step_c
    while (r,c) != (er,ec):
        if board[r][c] != "":
            return False
        r += step_r
        c += step_c
    return True


# ATAQUES
def attacks(piece, sr, sc, er, ec):
    dr = er - sr
    dc = ec - sc
    p = piece.lower()

    if p == "p":
        direction = -1 if is_white(piece) else 1
        return dr == direction and abs(dc) == 1

    if p == "n":
        return (abs(dr), abs(dc)) in [(2, 1), (1, 2)]

    # ♗ ALFIL
    if p == "b":
        if abs(dr) != abs(dc):
            return False
        return path_clear(sr, sc, er, ec)

    # ♖ TORRE
    if p == "r":
        if sr != er and sc != ec:
            return False
        return path_clear(sr, sc, er, ec)

    # ♕ REINA
    if p == "q":
        if sr != er and sc != ec and abs(dr) != abs(dc):
            return False
        return path_clear(sr, sc, er, ec)

    # ♔ REY
    if p == "k":
        return abs(dr) <= 1 and abs(dc) <= 1

    return False


# MOVIMIENTOs LEGALES
def valid_move(piece,sr,sc,er,ec):
    if not in_bounds(er,ec):
        return False

    target = board[er][ec]
    if target and is_white(target) == is_white(piece):
        return False

    dr = er-sr
    dc = ec-sc
    p = piece.lower()

    if p == "p":
        direction = -1 if is_white(piece) else 1
        start = 6 if is_white(piece) else 1

        if dc == 0 and dr == direction and board[er][ec] == "":
            return True

        if sr == start and dc == 0 and dr == 2*direction:
            return board[sr+direction][sc] == "" and board[er][ec] == ""

        if abs(dc) == 1 and dr == direction and board[er][ec] != "":
            return True

        return False

    if p == "n":
        return (abs(dr),abs(dc)) in [(2,1),(1,2)]

    if p == "b":
        return abs(dr) == abs(dc) and path_clear(sr,sc,er,ec)

    if p == "r":
        return (sr==er or sc==ec) and path_clear(sr,sc,er,ec)

    if p == "q":
        return (sr==er or sc==ec or abs(dr)==abs(dc)) and path_clear(sr,sc,er,ec)

    if p == "k":
        return abs(dr) <= 1 and abs(dc) <= 1

    return False


# SISTEMA DE JAQUE
def find_king(color):
    k = "K" if color=="white" else "k"
    for r in range(8):
        for c in range(8):
            if board[r][c] == k:
                return r,c
    return None

def is_attacked(r,c,attacker):
    for sr in range(8):
        for sc in range(8):
            p = board[sr][sc]
            if not p:
                continue
            if attacker=="white" and not is_white(p):
                continue
            if attacker=="black" and not is_black(p):
                continue
            if attacks(p,sr,sc,r,c):
                return True
    return False

def in_check(color):
    pos = find_king(color)
    if not pos:
        return False
    kr,kc = pos
    attacker = "black" if color=="white" else "white"
    return is_attacked(kr,kc,attacker)

def move_safe(sr,sc,er,ec):
    piece = board[sr][sc]
    backup = board[er][ec]

    board[er][ec] = piece
    board[sr][sc] = ""

    ok = not in_check("white" if is_white(piece) else "black")

    board[sr][sc] = piece
    board[er][ec] = backup

    return ok

def has_any_moves(color):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if not piece:
                continue

            if color=="white" and not is_white(piece):
                continue
            if color=="black" and not is_black(piece):
                continue

            for r2 in range(8):
                for c2 in range(8):
                    if valid_move(piece,r,c,r2,c2):
                        if move_safe(r,c,r2,c2):
                            return True
    return False


# ENROQUE
def can_castle(color, side):

    if color == "white":
        if side == "king" and rook_moved["white_right"]:
            return False
        if side == "queen" and rook_moved["white_left"]:
            return False
    else:
        if side == "king" and rook_moved["black_right"]:
            return False
        if side == "queen" and rook_moved["black_left"]:
            return False


    row = 7 if color == "white" else 0

    king = board[row][4]

    if color == "white":
        if king != "K":
            return False
    else:
        if king != "k":
            return False

    if king_moved[color]:
        return False

    if in_check(color):
        return False

    if side == "king":
        rook_col = 7
        path = [5, 6]
    else:
        rook_col = 0
        path = [1, 2, 3]

    rook = board[row][rook_col]

    
    if rook == "":
        return False


    if color == "white":
        if rook != "R":
            return False
    else:
        if rook != "r":
            return False

    # camino libre
    for c in path:
        if board[row][c] != "":
            return False

    enemy = "black" if color == "white" else "white"


    for c in [4] + path:
        if is_attacked(row, c, "black" if color == "white" else "white"):
         return False
    return True


# MOVIMIENTOS
def get_moves(sr, sc):
    piece = board[sr][sc]
    result = []

    color = "white" if is_white(piece) else "black"

    captures = []
    moves_list = []

    if piece.lower() == "k":
        if can_castle(color, "king"):
            result.append(("castle_kingside", sr, sc + 2))

        if can_castle(color, "queen"):
            result.append(("castle_queenside", sr, sc - 2))

    for r in range(8):
        for c in range(8):

            if not valid_move(piece, sr, sc, r, c):
                continue

            if not move_safe(sr, sc, r, c):
                continue

            target = board[r][c]

            if target != "" and is_white(target) != is_white(piece):
                captures.append(("capture", r, c))
            else:
                moves_list.append(("move", r, c))

    return result + captures + moves_list



#AL CLICKEAR FICHAS
def get_sq(pos):
    x,y = pos
    return y//SQ, x//SQ

def handle_click(pos):
    global selected, turn, moves, game_over

    if game_over:
        return

    r, c = get_sq(pos)


    if selected is None:
        p = board[r][c]
        if not p:
            return

        if turn == "white" and not is_white(p):
            return
        if turn == "black" and not is_black(p):
            return

        selected = (r, c)
        moves = get_moves(r, c)
        return

    sr, sc = selected
    piece = board[sr][sc]

    move_done = False

    for typ, mr, mc in list(moves):

        if mr == r and mc == c:

           
            if typ == "castle_kingside":
                board[r][c] = piece
                board[sr][sc] = ""

                board[r][5] = board[r][7]
                board[r][7] = ""

                king_moved[turn] = True
                move_done = True

          
            elif typ == "castle_queenside":
                board[r][c] = piece
                board[sr][sc] = ""

                board[r][3] = board[r][0]
                board[r][0] = ""

                king_moved[turn] = True
                move_done = True

          
            else:
                board[r][c] = piece
                board[sr][sc] = ""
                move_done = True

            break

    if move_done:


        if piece == "R":
            if sr == 7 and sc == 0:
                rook_moved["white_left"] = True
            elif sr == 7 and sc == 7:
                rook_moved["white_right"] = True

        elif piece == "r":
            if sr == 0 and sc == 0:
                rook_moved["black_left"] = True
            elif sr == 0 and sc == 7:
                rook_moved["black_right"] = True

        if piece == "P" and r == 0:
            board[r][c] = "Q"
        elif piece == "p" and r == 7:
            board[r][c] = "q"

        if piece.lower() == "k":
            king_moved[turn] = True

        turn = "black" if turn == "white" else "white"

    selected = None
    moves = []


# DIBUJO
def draw_board():
    for r in range(8):
        for c in range(8):
            col = WHITE if (r+c)%2==0 else BROWN
            pygame.draw.rect(screen, col, (c*SQ, r*SQ, SQ, SQ))

    pygame.draw.rect(screen, PANEL_BG, (BOARD_SIZE, 0, PANEL, HEIGHT))

def draw_selection():
    if selected:
        r,c = selected
        pygame.draw.rect(screen,(255,255,0),(c*SQ,r*SQ,SQ,SQ),4)

def draw_moves():
    for typ, r, c in moves:

        x = c * SQ
        y = r * SQ
        center = (x + SQ//2, y + SQ//2)

        if typ == "move":
            pygame.draw.circle(
                screen,
                MOVE_COLOR,
                center,
                10
            )
        elif typ == "capture":
           
            pygame.draw.rect(
                screen,
                CAPTURE_COLOR,
                (x, y, SQ, SQ),
                6,
                border_radius=8
            )
            pygame.draw.circle(
                screen,
                (255, 80, 80),
                center,
                18,
                2
            )

        elif typ.startswith("castle"):
            pygame.draw.circle(
                screen,
                (0, 150, 255),
                center,
                14,
                4
            )

def draw_pieces():
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p:
                screen.blit(piece_images[p], (c*SQ, r*SQ))

def format_time(t):
    m = int(t)//60
    s = int(t)%60
    return f"{m:02d}:{s:02d}"

def draw_timer():
    font = pygame.font.SysFont("arial", 30)

    x = BOARD_SIZE + 20

    screen.blit(font.render("Blancas", True, TEXT), (x, 50))
    screen.blit(font.render(format_time(WHITE_TIME), True, TEXT), (x, 90))

    screen.blit(font.render("Negras", True, TEXT), (x, 200))
    screen.blit(font.render(format_time(BLACK_TIME), True, TEXT), (x, 240))

def draw_check():
    if in_check(turn) and not game_over:
        font = pygame.font.SysFont("arial", 60)
        t = font.render("JAQUE!", True, (255,0,0))
        screen.blit(t, (BOARD_SIZE//2 - 80, 10))

def draw_game_over():
    if game_over:
        font = pygame.font.SysFont("arial", 70)
        t1 = font.render("JAQUE MATE", True, (255,0,0))
        t2 = font.render(f"Gana {winner}", True, (0,0,0))

        screen.blit(t1,(BOARD_SIZE//2-200,HEIGHT//2-80))
        screen.blit(t2,(BOARD_SIZE//2-120,HEIGHT//2))


clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    now = pygame.time.get_ticks()
    delta = (now - last_tick)/1000
    last_tick = now

    if not game_over:
        if turn=="white":
            WHITE_TIME -= delta
            if WHITE_TIME<=0:
                game_over=True
                winner="Negras"
        else:
            BLACK_TIME -= delta
            if BLACK_TIME<=0:
                game_over=True
                winner="Blancas"

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running=False
        if e.type == pygame.MOUSEBUTTONDOWN:
            handle_click(e.pos)

    if not game_over:
        if in_check(turn) and not has_any_moves(turn):
            game_over=True
            winner="Negras" if turn=="white" else "Blancas"

    draw_board()
    draw_moves()
    draw_selection()
    draw_pieces()
    draw_timer()
    draw_check()
    draw_game_over()

    pygame.display.flip()

pygame.quit()
sys.exit()
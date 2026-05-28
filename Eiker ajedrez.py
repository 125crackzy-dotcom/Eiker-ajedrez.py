import pygame
import sys

# =========================
# CONFIGURACIÓN GENERAL
# =========================
ANCHO = 640
ALTO = 640
FILAS = 8
COLUMNAS = 8
TAM = ANCHO // COLUMNAS

BLANCO = (240, 217, 181)
MARRON = (181, 136, 99)
AZUL = (50, 150, 255)
ROJO = (220, 50, 50)
NEGRO = (0, 0, 0)

pygame.init()

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ajedrez Completo")
fuente = pygame.font.SysFont("arial", 44)

# =========================
# PIEZAS UNICODE
# =========================
PIEZAS = {
    "wp": "♙","wr": "♖","wn": "♘","wb": "♗","wq": "♕","wk": "♔",
    "bp": "♟","br": "♜","bn": "♞","bb": "♝","bq": "♛","bk": "♚"
}

# =========================
# TABLERO INICIAL
# =========================
tablero = [
    ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
]

turno = "w"

pieza_seleccionada = None
movimientos_validos = []

# =========================
# DIBUJAR TABLERO
# =========================
def dibujar_tablero():
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            color = BLANCO if (fila + col) % 2 == 0 else MARRON

            pygame.draw.rect(
                pantalla,
                color,
                (col * TAM, fila * TAM, TAM, TAM)
            )

            if (fila, col) in movimientos_validos:
                pygame.draw.circle(
                    pantalla,
                    AZUL,
                    (col * TAM + TAM // 2, fila * TAM + TAM // 2),
                    10
                )

# =========================
# DIBUJAR PIEZAS
# =========================
def dibujar_piezas():
    for fila in range(8):
        for col in range(8):
            pieza = tablero[fila][col]

            if pieza != "":
                texto = fuente.render(PIEZAS[pieza], True, NEGRO)

                pantalla.blit(
                    texto,
                    (
                        col * TAM + 15,
                        fila * TAM + 10
                    )
                )

# =========================
# VALIDACIONES
# =========================
def dentro(fila, col):
    return 0 <= fila < 8 and 0 <= col < 8

def enemigo(p1, p2):
    return p1[0] != p2[0]

# =========================
# MOVIMIENTOS
# =========================
def movimientos_peon(fila, col, color):
    moves = []

    direccion = -1 if color == "w" else 1

    # avanzar
    if dentro(fila + direccion, col) and tablero[fila + direccion][col] == "":
        moves.append((fila + direccion, col))

        # doble movimiento
        if (color == "w" and fila == 6) or (color == "b" and fila == 1):
            if tablero[fila + 2 * direccion][col] == "":
                moves.append((fila + 2 * direccion, col))

    # capturas
    for dc in [-1, 1]:
        nf = fila + direccion
        nc = col + dc

        if dentro(nf, nc):
            if tablero[nf][nc] != "" and enemigo(tablero[fila][col], tablero[nf][nc]):
                moves.append((nf, nc))

    return moves

def movimientos_torre(fila, col):
    return movimientos_lineales(
        fila, col,
        [(1,0), (-1,0), (0,1), (0,-1)]
    )

def movimientos_alfil(fila, col):
    return movimientos_lineales(
        fila, col,
        [(1,1), (-1,-1), (1,-1), (-1,1)]
    )

def movimientos_reina(fila, col):
    return movimientos_lineales(
        fila, col,
        [
            (1,0), (-1,0), (0,1), (0,-1),
            (1,1), (-1,-1), (1,-1), (-1,1)
        ]
    )

def movimientos_lineales(fila, col, direcciones):
    moves = []

    for dr, dc in direcciones:
        nf = fila + dr
        nc = col + dc

        while dentro(nf, nc):

            if tablero[nf][nc] == "":
                moves.append((nf, nc))

            else:
                if enemigo(tablero[fila][col], tablero[nf][nc]):
                    moves.append((nf, nc))
                break

            nf += dr
            nc += dc

    return moves

def movimientos_caballo(fila, col):
    moves = []

    posiciones = [
        (-2, -1), (-2, 1),
        (-1, -2), (-1, 2),
        (1, -2), (1, 2),
        (2, -1), (2, 1)
    ]

    for dr, dc in posiciones:
        nf = fila + dr
        nc = col + dc

        if dentro(nf, nc):
            if tablero[nf][nc] == "" or enemigo(tablero[fila][col], tablero[nf][nc]):
                moves.append((nf, nc))

    return moves

def movimientos_rey(fila, col):
    moves = []

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:

            if dr == 0 and dc == 0:
                continue

            nf = fila + dr
            nc = col + dc

            if dentro(nf, nc):
                if tablero[nf][nc] == "" or enemigo(tablero[fila][col], tablero[nf][nc]):
                    moves.append((nf, nc))

    return moves

# =========================
# OBTENER MOVIMIENTOS
# =========================
def obtener_movimientos(fila, col):
    pieza = tablero[fila][col]

    if pieza == "":
        return []

    tipo = pieza[1]
    color = pieza[0]

    if tipo == "p":
        return movimientos_peon(fila, col, color)

    if tipo == "r":
        return movimientos_torre(fila, col)

    if tipo == "n":
        return movimientos_caballo(fila, col)

    if tipo == "b":
        return movimientos_alfil(fila, col)

    if tipo == "q":
        return movimientos_reina(fila, col)

    if tipo == "k":
        return movimientos_rey(fila, col)

    return []

# =========================
# MAIN
# =========================
reloj = pygame.time.Clock()

while True:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:

            x, y = pygame.mouse.get_pos()

            col = x // TAM
            fila = y // TAM

            # mover pieza
            if pieza_seleccionada:

                if (fila, col) in movimientos_validos:

                    f1, c1 = pieza_seleccionada

                    tablero[fila][col] = tablero[f1][c1]
                    tablero[f1][c1] = ""

                    turno = "b" if turno == "w" else "w"

                pieza_seleccionada = None
                movimientos_validos = []

            else:
                pieza = tablero[fila][col]

                if pieza != "" and pieza[0] == turno:
                    pieza_seleccionada = (fila, col)
                    movimientos_validos = obtener_movimientos(fila, col)

    dibujar_tablero()
    dibujar_piezas()

    pygame.display.flip()
    reloj.tick(60)
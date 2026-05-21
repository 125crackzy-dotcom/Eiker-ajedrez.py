import pygame
import sys

ANCHO = 640
ALTO = 640

filas = 8
columnas = 8


fila_caballo = 7
col_caballo = 1
TAM_CASILLA = ANCHO // columnas

BLANCO = (240, 217, 181)
NEGRO = (181, 136, 99)


def tablero(screen):

    for fila in range(filas):

        for col in range(columnas):

            if (fila + col) % 2 == 0:
                color = BLANCO
            else:
                color = NEGRO

            pygame.draw.rect(
                screen,
                color,
                (
                    col * TAM_CASILLA,
                    fila * TAM_CASILLA,
                    TAM_CASILLA,
                    TAM_CASILLA
                )
            )


def draw_piece(screen, tipo, fila, col, color):

    x = col * TAM_CASILLA
    y = fila * TAM_CASILLA

    centro_x = x + TAM_CASILLA // 2
    centro_y = y + TAM_CASILLA // 2

    if tipo == "peon":

        pygame.draw.circle(
            screen,
            color,
            (centro_x, centro_y - 10),
            12
        )

        pygame.draw.rect(
            screen,
            color,
            (x + 22, y + 35, 36, 18)
        )

    elif tipo == "caballo":

        puntos = [
            (x + 20, y + 55),
            (x + 20, y + 25),
            (x + 35, y + 15),
            (x + 50, y + 25),
            (x + 45, y + 40),
            (x + 55, y + 55)
        ]

        pygame.draw.polygon(screen, color, puntos)


def main():

    pygame.init()

    pantalla = pygame.display.set_mode((ANCHO, ALTO))

    reloj = pygame.time.Clock()

    fila = 6
    col = 3
    fila_peon = 6
    col_peon = 3
    fila_caballo = 7
    col_caballo = 1
    while True:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

                # PEON
                if evento.key == pygame.K_UP and fila_peon > 0:
                    fila_peon -= 1

                if evento.key == pygame.K_DOWN and fila_peon < 7:
                    fila_peon += 1

                if evento.key == pygame.K_LEFT and col_peon > 0:
                    col_peon -= 1

                if evento.key == pygame.K_RIGHT and col_peon < 7:
                    col_peon += 1


                # CABALLO
                if evento.key == pygame.K_w and fila_caballo > 0:
                    fila_caballo -= 1

                if evento.key == pygame.K_s and fila_caballo < 7:
                    fila_caballo += 1

                if evento.key == pygame.K_a and col_caballo > 0:
                    col_caballo -= 1

                if evento.key == pygame.K_d and col_caballo < 7:
                    col_caballo += 1

        tablero(pantalla)

        draw_piece(
                pantalla,
                "peon",
                fila_peon,
                col_peon,
                (255,0,0)
            )

        draw_piece(
                pantalla,
                "caballo",
                fila_caballo,
                col_caballo,
                (0,0,255)
            )

        pygame.display.flip()

        reloj.tick(60)


main()
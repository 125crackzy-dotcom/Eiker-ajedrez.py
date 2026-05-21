import pygame
import sys


ANCHO = 640
ALTO = 640
filas = 8
columnas = 8
TAM_CASILLA = ANCHO // columnas


BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)


def tablero(pantalla):
    for fila in range(filas):
        for col in range(columnas):

            if(fila + col) % 2 == 0 :
                color = BLANCO
            else:
                color = NEGRO

            pygame.draw.rect(
                pantalla,
                color, (col * TAM_CASILLA, fila * TAM_CASILLA, TAM_CASILLA, TAM_CASILLA)
            )
            
def draw_custom_piece(screen, row, col, square_size):
    x = col * square_size
    y = row * square_size

    centro_x = x + square_size // 2
    centro_y = y + square_size // 2

    color = (0, 0, 0)

    # Cuerpo (círculo)
    pygame.draw.circle(screen, color, (centro_x, centro_y), square_size // 4)

    # Base (rectángulo)
    pygame.draw.rect(screen, color, (x + square_size//4, y + square_size//1.5, square_size//2, square_size//6))

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Tablero de Ajedrez")
    reloj = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tablero(pantalla)

        draw_custom_piece(pantalla, 6, 3, TAM_CASILLA)

        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    main()
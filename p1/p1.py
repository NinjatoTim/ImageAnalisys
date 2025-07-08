import pygame

pygame.init()

ancho, alto = 300, 300
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Bresenham + Pygame")

pantalla.fill((0, 0, 0))

#Bresenham para linea
def dibujar_linea(x0, y0, x1, y1):
    color = (234,137,154)
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    error = dx - dy
    
    while True:
        if 0 <= x0 < ancho and 0 <= y0 < alto:
            pantalla.set_at((x0, y0), color)
        if x0 == x1 and y0 == y1:
            break  
        e2 = 2 * error
        if e2 > -dy:
            error -= dy
            x0 += sx
        if e2 < dx:
            error += dx
            y0 += sy

#Bresenham para círculo
def dibujar_circulo(xc, yc, radio): 
    color = (0,250,0)
    x = 0
    y = radio
    d = 3 - 2 * radio

    def dibujar_puntos(x, y):
        pantalla.set_at((xc + x, yc + y), color)
        pantalla.set_at((xc - x, yc + y), color)
        pantalla.set_at((xc + x, yc - y), color)
        pantalla.set_at((xc - x, yc - y), color)
        pantalla.set_at((xc + y, yc + x), color)
        pantalla.set_at((xc - y, yc + x), color)
        pantalla.set_at((xc + y, yc - x), color)
        pantalla.set_at((xc - y, yc - x), color)

    dibujar_puntos(x, y)

    while y >= x:
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6
        dibujar_puntos(x, y)

dibujar_circulo(130, 130, 80)
dibujar_linea(50,30,120,280)


pygame.display.flip()

#Bucle ventana
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

pygame.quit()
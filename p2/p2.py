import tkinter as tk
from tkinter import filedialog
import os
import math

def leer_bmp(ruta):
    with open(ruta, 'rb') as f:
        datos = f.read(54)
        
        ancho = int.from_bytes(datos[18:22], byteorder='little')
        alto = int.from_bytes(datos[22:26], byteorder='little')
        
        imagen = []
        padding = (4 - (ancho * 3) % 4) % 4
        
        for _ in range(alto):
            fila = []
            for _ in range(ancho):
                b, g, r = f.read(3)
                fila.append([r, g, b])
            f.read(padding) 
            imagen.append(fila)

    return imagen

def mostrar_imagen(imagen):
    root = tk.Tk()
    root.title("Imagen procesada")
    
    alto = len(imagen)
    ancho = len(imagen[0]) if alto > 0 else 0
    
    canvas = tk.Canvas(root, width=ancho, height=alto)
    canvas.pack()
    
    for y in range(alto):
        for x in range(ancho):
            if isinstance(imagen[y][x], list):
                r, g, b = imagen[y][x]
                color = f'#{r:02x}{g:02x}{b:02x}'
            else:  
                nivel = imagen[y][x]
                color = f'#{nivel:02x}{nivel:02x}{nivel:02x}'
            canvas.create_rectangle(x, y, x + 1, y + 1, fill=color, outline="")
    
    root.mainloop()

def rgb_a_grises(imagen):
    grises = []
    for fila in imagen:
        fila_gris = []
        for r, g, b in fila:
            gris = int(0.299 * r + 0.587 * g + 0.114 * b) 
            fila_gris.append(gris)
        grises.append(fila_gris)
    return grises

def invertir_colores(imagen):
    invertida = []
    for fila in imagen:
        fila_inv = []
        for r, g, b in fila:
            fila_inv.append([255 - r, 255 - g, 255 - b])
        invertida.append(fila_inv)
    return invertida

def filtro_rojo(imagen):
    filtrada = []
    for fila in imagen:
        fila_filtrada = []
        for r, g, b in fila:
            fila_filtrada.append([r, 0, 0]) 
        filtrada.append(fila_filtrada)
    return filtrada

def filtro_verde(imagen):
    if imagen is None:
        return None
    
    filtrada = []
    for fila in imagen:
        fila_filtrada = []
        for r, g, b in fila:
            fila_filtrada.append([0, g, 0])
        filtrada.append(fila_filtrada)
    return filtrada

def filtro_azul(imagen):
    if imagen is None:
        return None
    
    filtrada = []
    for fila in imagen:
        fila_filtrada = []
        for r, g, b in fila:
            fila_filtrada.append([0, 0, b])
        filtrada.append(fila_filtrada)
    return filtrada

#C=255−R
#M=255−G
#Y=255−B
def convertir_a_cmy(imagen_rgb):
    imagen_cmy = []
    for fila in imagen_rgb:
        nueva_fila = []
        for pixel in fila:
            r, g, b = pixel
            c = 255 - r
            m = 255 - g
            y = 255 - b
            nueva_fila.append([c, m, y])
        imagen_cmy.append(nueva_fila)
    return imagen_cmy

 
#Y=0.299R+0.587G+0.114B
#I=0.596R−0.274G−0.322B
#Q=0.211R−0.523G+0.312B
def convertir_a_yiq(imagen_rgb):
    imagen_yiq = []
    for fila in imagen_rgb:
        nueva_fila = []
        for pixel in fila:
            r, g, b = [v / 255 for v in pixel]  # Normalizar a [0, 1]
            y = 0.299 * r + 0.587 * g + 0.114 * b
            i = 0.596 * r - 0.274 * g - 0.322 * b
            q = 0.211 * r - 0.523 * g + 0.312 * b
            nueva_fila.append([y, i, q])
        imagen_yiq.append(nueva_fila)
    return imagen_yiq


def convertir_a_hsi(imagen_rgb):
    imagen_hsi = []
    for fila in imagen_rgb:
        nueva_fila = []
        for pixel in fila:
            r, g, b = [v / 255 for v in pixel]
            suma = r + g + b
            i = suma / 3
            min_val = min(r, g, b)
            s = 0 if suma == 0 else 1 - (3 * min_val / suma)
            
            num = ((r - g) + (r - b)) / 2
            den = math.sqrt((r - g)**2 + (r - b)*(g - b))
            theta = 0 if den == 0 else math.acos(max(-1, min(1, num / den)))
            h = math.degrees(theta)
            if b > g:
                h = 360 - h
            nueva_fila.append([h, s, i])
        imagen_hsi.append(nueva_fila)
    return imagen_hsi

#V = max(R, G, B)
#S = (V - min) / V (si V ≠ 0)
#H depende de qué canal es el máximo.
def convertir_a_hsv(imagen_rgb):
    imagen_hsv = []
    for fila in imagen_rgb:
        nueva_fila = []
        for pixel in fila:
            r, g, b = [v / 255 for v in pixel]
            mx = max(r, g, b)
            mn = min(r, g, b)
            delta = mx - mn

            # Hue
            if delta == 0:
                h = 0
            elif mx == r:
                h = 60 * (((g - b) / delta) % 6)
            elif mx == g:
                h = 60 * (((b - r) / delta) + 2)
            else:
                h = 60 * (((r - g) / delta) + 4)

            # Saturation
            s = 0 if mx == 0 else delta / mx

            # Value
            v = mx

            nueva_fila.append([h, s, v])
        imagen_hsv.append(nueva_fila)
    return imagen_hsv

def escalar_valor(valor, minimo, maximo):
    # Mapea valor desde [minimo, maximo] a [0, 255]
    normalizado = (valor - minimo) / (maximo - minimo)
    return int(max(0, min(255, round(normalizado * 255))))


def mostrar_canal_yiq(imagen_yiq, canal_idx, nombre_canal):
    alto = len(imagen_yiq)
    ancho = len(imagen_yiq[0]) if alto > 0 else 0

    # Rango por canal
    rangos = {
        0: (0.0, 1.0),           # Y
        1: (-0.5957, 0.5957),    # I
        2: (-0.5226, 0.5226),    # Q
    }
    minimo, maximo = rangos[canal_idx]

    root = tk.Tk()
    root.title(f"Canal {nombre_canal} (YIQ)")

    canvas = tk.Canvas(root, width=ancho, height=alto)
    canvas.pack()

    for y in range(alto):
        for x in range(ancho):
            valor = imagen_yiq[y][x][canal_idx]
            nivel = escalar_valor(valor, minimo, maximo)
            color = f'#{nivel:02x}{nivel:02x}{nivel:02x}'
            canvas.create_rectangle(x, y, x + 1, y + 1, fill=color, outline="")

    root.mainloop()


def mostrar_canal_gris(imagen, canal_idx, nombre_canal="Canal", escala=1.0):
    alto = len(imagen)
    ancho = len(imagen[0]) if alto > 0 else 0

    root = tk.Tk()
    root.title(f"{nombre_canal} en escala de grises")

    canvas = tk.Canvas(root, width=ancho, height=alto)
    canvas.pack()

    for y in range(alto):
        for x in range(ancho):
            valor = imagen[y][x][canal_idx] * escala
            nivel = int(max(0, min(255, round(valor))))
            color = f'#{nivel:02x}{nivel:02x}{nivel:02x}'
            canvas.create_rectangle(x, y, x + 1, y + 1, fill=color, outline="")

    root.mainloop()



archivo = filedialog.askopenfilename(
    title="Seleccionar imagen",
    filetypes=[("Archivos BMP", "*.bmp"), ("Todos los archivos", "*.*")]
)
    
imagen = leer_bmp(archivo)

imagen_grises = rgb_a_grises(imagen)
imagen_negativo = invertir_colores(imagen)
imagen_rojo = filtro_rojo(imagen)
imagen_verde = filtro_verde(imagen)
imagen_azul = filtro_azul(imagen)
imagen_cmy = convertir_a_cmy(imagen)
imagen_hsi = convertir_a_hsi(imagen)
imagen_yiq = convertir_a_yiq(imagen)
imagen_hsv = convertir_a_hsv(imagen)

mostrar_imagen(imagen_grises)
mostrar_imagen(imagen_negativo)
mostrar_imagen(imagen_rojo)
mostrar_imagen(imagen_verde)
mostrar_imagen(imagen_azul)

mostrar_imagen(imagen_cmy)

# HSI
mostrar_canal_gris(imagen_hsi, canal_idx=0, nombre_canal="Hue", escala=255/360)
# Saturación (0–1)
mostrar_canal_gris(imagen_hsi, canal_idx=1, nombre_canal="Saturation", escala=255)
# Intensidad (0–1)
mostrar_canal_gris(imagen_hsi, canal_idx=2, nombre_canal="Value", escala=255)

## HSV
mostrar_canal_gris(imagen_hsi, canal_idx=0, nombre_canal="Hue", escala=255/360)
# Saturación (0–1)
mostrar_canal_gris(imagen_hsi, canal_idx=1, nombre_canal="Saturation", escala=255)
# Intensidad (0–1)
mostrar_canal_gris(imagen_hsi, canal_idx=2, nombre_canal="Intensity", escala=255)

#YIQ
mostrar_canal_yiq(imagen_yiq, 0, "Y (Luminancia)")
mostrar_canal_yiq(imagen_yiq, 1, "I (In-phase)")
mostrar_canal_yiq(imagen_yiq, 2, "Q (Quadrature)")
# Análisis de Imágenes - Primer Parcial

Este programa explora las diferentes operaciones que se pueden realizar en el análisis de imágenes del primer parcial, por simplicidad se utilizan imágenes con extensión .BMP sin compresión.

Los archivos de mapas de bits se componen de direcciones asociadas a códigos de color, uno para cada cuadro en una matriz de píxeles.

**Referencia:** https://learn.microsoft.com/es-es/windows/win32/gdiplus/-gdiplus-types-of-bitmaps-about

## Fuentes de Imágenes

Las imágenes fueron tomadas del repositorio de eIgooGmirror:
https://github.com/eIgooGmirror/BMP-Sample-Images.git

Así como las imágenes del repositorio de sol-prog, las cuales tienen un menor tamaño y son más rápidas de procesar:
https://github.com/sol-prog/cpp-bmp-images.git

De igual manera uno puede crear sus propias imágenes en algún editor de dibujo como paint y guardarlo con el formato .BMP.

## Función leer_bmp

La función leer_bmp lee un archivo .bmp (de mapa de bits) de 24 bits sin comprimir, y convierte la imagen en una lista de listas, donde cada sublista representa una fila de píxeles, y cada píxel es una lista [R, G, B].

De esta manera se puede aplicar cada una de las operaciones:

## Operaciones Básicas

- **Escala de grises:** [0.299 * r + 0.587 * g + 0.114 * b]
- **Invertir colores:** [255 - r, 255 - g, 255 - b]
- **Filtro rojo:** [r, 0, 0]
- **Filtro verde:** [0, g, 0]
- **Filtro azul:** [0, 0, b]

## Conversión a Otros Modelos de Color

Para convertir la imagen a otros modelos de color se aplican las siguientes operaciones:

### CYM
```
C = 255 - R
M = 255 - G
Y = 255 - B
```

En el caso de CYM se puede utilizar la misma función de RGB para mostrar la imagen, pero en los modelos posteriores se muestran los canales separados.

### YIQ
```
Y = 0.299R + 0.587G + 0.114B
I = 0.596R - 0.274G - 0.322B
Q = 0.211R - 0.523G + 0.312B
```

### HSV
```
V = max(R, G, B)
S = (V - min) / V (si V ≠ 0)
H depende de qué canal es el máximo.
```

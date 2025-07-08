from datasets import load_dataset
import numpy as np
from PIL import Image
from tqdm import tqdm

NIVELES = 7  # número de niveles de color por canal (ej. 5 → 0, 64, 128, 192, 255)


def construir_matriz_probabilidad_acumulada(matriz_probabilidad, niveles=5):
    H, W = matriz_probabilidad.shape
    matriz_acumulada = np.zeros((H, W, niveles), dtype=np.float32)
    
    for i in range(H):
        for j in range(W):
            p = matriz_probabilidad[i, j]
            base = np.linspace(0, 1, niveles)
            pesos = np.clip(1 - np.abs(base - p) * niveles, 0, 1)
            pesos /= pesos.sum()  # Normalizar
            acumulada = np.cumsum(pesos)
            matriz_acumulada[i, j] = acumulada
            
    return matriz_acumulada


def generar_imagen_rgb(matriz_r, matriz_g, matriz_b, niveles=5):
    H, W, _ = matriz_r.shape
    niveles_valores = np.linspace(0, 255, niveles).astype(np.uint8)
    
    imagen_rgb = np.zeros((H, W, 3), dtype=np.uint8)

    for i in range(H):
        for j in range(W):
            r = np.random.rand()
            g = np.random.rand()
            b = np.random.rand()
            
            idx_r = np.searchsorted(matriz_r[i, j], r)
            idx_g = np.searchsorted(matriz_g[i, j], g)
            idx_b = np.searchsorted(matriz_b[i, j], b)

            imagen_rgb[i, j, 0] = niveles_valores[min(idx_r, niveles - 1)]
            imagen_rgb[i, j, 1] = niveles_valores[min(idx_g, niveles - 1)]
            imagen_rgb[i, j, 2] = niveles_valores[min(idx_b, niveles - 1)]

    return Image.fromarray(imagen_rgb, mode="RGB")


print("Cargando dataset BAUHAUS-ART...")
dataset = load_dataset("iamkaikai/BAUHAUS-ART")["train"]

ejemplo = dataset[0]["image"]
W, H = ejemplo.size

suma_r = np.zeros((H, W), dtype=np.float32)
suma_g = np.zeros((H, W), dtype=np.float32)
suma_b = np.zeros((H, W), dtype=np.float32)

print(f"Procesando {len(dataset)} imágenes de tamaño {W}x{H}...")

for ejemplo in tqdm(dataset):
    img = ejemplo["image"].convert("RGB")
    arr = np.asarray(img).astype(np.float32) / 255.0
    suma_r += arr[:, :, 0]
    suma_g += arr[:, :, 1]
    suma_b += arr[:, :, 2]

total_imagenes = len(dataset)

prob_r = suma_r / total_imagenes
prob_g = suma_g / total_imagenes
prob_b = suma_b / total_imagenes


print("Generando matrices de probabilidad acumulada...")
matriz_prob_r = construir_matriz_probabilidad_acumulada(prob_r, niveles=NIVELES)
matriz_prob_g = construir_matriz_probabilidad_acumulada(prob_g, niveles=NIVELES)
matriz_prob_b = construir_matriz_probabilidad_acumulada(prob_b, niveles=NIVELES)

print("Generando imagen RGB ")
imagen_rgb = generar_imagen_rgb(matriz_prob_r, matriz_prob_g, matriz_prob_b, niveles=NIVELES)
imagen_rgb.show()
imagen_rgb.save("bauhaus_generada_rgb.png")
print("Imagen guardada como 'bauhaus_generada_rgb.png'")

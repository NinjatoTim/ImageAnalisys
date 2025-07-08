Este proyecto implementa un clasificador de dígitos (0–9) utilizando perceptrones simples entrenados desde cero, sin usar librerías externas de machine learning como sklearn o tensorflow. El modelo se basa en la arquitectura uno contra todos (one-vs-all), entrenando un perceptrón por cada dígito.

Se utilizaron las siguientes bibliotecas y se omitieron librerías externas de machine learning como sklearn o tensorflow
numpy para operaciones matriciales
PIL (Pillow) para procesamiento de imágenes
tkinter para selección de archivos (opcional)

Además se utilizó el famoso dataset MNIST que usualmente puede ser consumida desde bibliotecas descritas anteriormente, para este ejemplo se utilizó una muestra pequeña como entrenamiento, de 16 imágenes por cada letra, la cual puede ser consultada en este repositorio, sin embargo, el dataset completo puede ser consultado desde el repositorio de myleott en un comprimido. (curiosamente la fuente oficial está caida)
https://github.com/myleott/mnist_png.git

El programa consta de tres fases, el entrenamiento y la predicción
Proceso de entrenamiento
Preprocesamiento:
Las imágenes se convierten a matrices binarias (0 o 1) usando un umbral de intensidad.
Cada imagen se "aplana" en un vector de 784 elementos (28x28).
Entrenamiento:
Se "entrena" un perceptrón por cada dígito, utilizando la "regla de aprendizaje clásica del perceptrón".

Fórmula general:
Se tiene un vector de entrada "x"
una salida esperada "y" (1 si es la case correcta, 0 si no)
Un conjunto de pesos w y un sesgo (bias o b).

La predicción del perceptrón es:

y_pred = 1 si (w · x + b) ≥ 0
         0 en otro caso

Cuando el perceptrón se equivoca, se actualizan los pesos así:

w = w + tasa_aprendizaje * (y - y_pred) * x
b = b + tasa_aprendizaje * (y - y_pred)

Notas: 
-Al inicio los pesos y el sesgo son iniciados aleatoriamente
-Se repasa el dataset varias veces (cada pasada completa se llama una época).
En cada imagen:
Se calcula la salida del perceptrón.
Se compara con la etiqueta real.
Se actualizan los pesos si hay error, cada perceptrón aprende a responder “sí/no” a su dígito correspondiente.
La tasa de aprendizaje es un número pequeño (0.01 por ejemplo) que controla cuánto cambian los pesos, si es muy alto el modelo no converge bien, si es muy bajo aprende lento.

Predicción:
Una vez pasada la etapa de entrenamiento, nos quedan 10 perceptrones (1 por cada número), cada uno tiene un peso y un bias, ese será nuestro clasificador.
La función predecir_dígito recibe un vector de entrada, y el clasificador, la función recorre cada perceptrón (uno por cada dígito del 0 al 9), calcula la "activación" del perceptrón:
activación = vector_entrada · pesos + bias
Guarda esa activación en una lista llamada salidas.
Salidas es una lista de 10 valores, cada valor representa la "respuesta" del perceptrón para cada dígito, son ordenados de mayor a menor para saber cuál respondió con más fuerza, ese es el dígito predicho.
import os
import cv2
import numpy as np
from tqdm import tqdm

CLASES = ['felicidad', 'tristeza', 'sorpresa', 'enojo']
CLASES_IDX = {nombre: idx for idx, nombre in enumerate(CLASES)}

def cargar_datos(ruta_base):
    X_train, y_train = [], []
    X_test, y_test = [], []

    for clase in CLASES:
        etiqueta = CLASES_IDX[clase]

        for tipo in ['train', 'test']:
            ruta = os.path.join(ruta_base, tipo, clase)
            print(f"\nCargando imágenes de {tipo} -> {clase}...")

            if os.path.exists(ruta):
                for imagen in tqdm(os.listdir(ruta)):
                    try:
                        img = cv2.imread(os.path.join(ruta, imagen))
                        if img is not None and img.shape == (96, 96, 3):
                            img = img / 255.0
                            if tipo == 'train':
                                X_train.append(img)
                                y_train.append(etiqueta)
                            else:
                                X_test.append(img)
                                y_test.append(etiqueta)
                        else:
                            print(f"Imagen ignorada: {imagen}")
                    except Exception as e:
                        print(f"Error con {imagen}: {str(e)}")

    X_train, X_test = np.array(X_train), np.array(X_test)
    y_train, y_test = np.array(y_train), np.array(y_test)

    print("\nFormas finales:")
    print(f"X_train: {X_train.shape}, y_train: {y_train.shape}")
    print(f"X_test: {X_test.shape}, y_test: {y_test.shape}")

    return X_train, y_train, X_test, y_test

if __name__ == "__main__":
    cargar_datos('DataSet/procesados')
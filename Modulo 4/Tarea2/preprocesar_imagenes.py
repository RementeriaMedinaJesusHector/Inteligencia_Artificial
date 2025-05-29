import os
import cv2
import numpy as np
from tqdm import tqdm
from sklearn.model_selection import train_test_split

# Lista de emociones que quieres detectar
CLASES = ['felicidad', 'tristeza', 'sorpresa', 'enojo']

def verificar_imagen(ruta_imagen):
    try:
        img = cv2.imread(ruta_imagen)
        if img is None:
            return False
        _ = cv2.imencode('.jpg', img)[1]
        return True
    except:
        return False

def procesar_imagenes(ruta_origen, ruta_destino, test_size=0.2):
    for split in ['train', 'test']:
        for emocion in CLASES:
            os.makedirs(os.path.join(ruta_destino, split, emocion), exist_ok=True)

    estadisticas = {'procesadas': 0, 'errores': 0}

    for emocion in CLASES:
        print(f"\nProcesando imágenes de '{emocion}'...")
        ruta_origen_emocion = os.path.join(ruta_origen, emocion)
        ruta_train = os.path.join(ruta_destino, 'train', emocion)
        ruta_test = os.path.join(ruta_destino, 'test', emocion)

        if not os.path.exists(ruta_origen_emocion):
            print(f"Error: No se encontró el directorio {ruta_origen_emocion}")
            continue

        imagenes = [img for img in os.listdir(ruta_origen_emocion)
                    if img.lower().endswith(('.png', '.jpg', '.jpeg'))]

        imagenes_validas = []
        print("Verificando imágenes...")
        for imagen in tqdm(imagenes):
            ruta_completa = os.path.join(ruta_origen_emocion, imagen)
            if verificar_imagen(ruta_completa):
                imagenes_validas.append(imagen)
            else:
                estadisticas['errores'] += 1
                print(f"\nImagen corrupta omitida: {imagen}")

        print(f"Imágenes válidas encontradas: {len(imagenes_validas)}")

        train_images, test_images = train_test_split(
            imagenes_validas, test_size=test_size, random_state=42
        )

        print("Procesando imágenes de entrenamiento...")
        for imagen in tqdm(train_images):
            if procesar_y_guardar_imagen(
                os.path.join(ruta_origen_emocion, imagen),
                os.path.join(ruta_train, imagen)
            ):
                estadisticas['procesadas'] += 1

        print("Procesando imágenes de prueba...")
        for imagen in tqdm(test_images):
            if procesar_y_guardar_imagen(
                os.path.join(ruta_origen_emocion, imagen),
                os.path.join(ruta_test, imagen)
            ):
                estadisticas['procesadas'] += 1

    print("\n Estadísticas del procesamiento:")
    print(f" Imágenes procesadas exitosamente: {estadisticas['procesadas']}")
    print(f" Imágenes con errores: {estadisticas['errores']}")

def procesar_y_guardar_imagen(ruta_origen, ruta_destino):
    try:
        imagen = cv2.imread(ruta_origen)
        if imagen is None:
            return False

        if imagen.shape[0] < 96 or imagen.shape[1] < 96:
            print(f"\nImagen omitida: {ruta_origen}")
            return False

        altura, ancho = imagen.shape[:2]
        if altura > ancho:
            nuevo_ancho = 96
            nuevo_alto = int(altura * (96 / ancho))
        else:
            nuevo_alto = 96
            nuevo_ancho = int(ancho * (96 / altura))

        imagen = cv2.resize(imagen, (nuevo_ancho, nuevo_alto))
        y = (nuevo_alto - 96) // 2
        x = (nuevo_ancho - 96) // 2
        imagen = imagen[y:y+96, x:x+96]

        #Mejora de contraste
        lab = cv2.cvtColor(imagen, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        imagen = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

        cv2.imwrite(ruta_destino, imagen)
        return True

    except Exception as e:
        print(f"\nError procesando {ruta_origen}: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        procesar_imagenes(
            ruta_origen='DataSet/originales',
            ruta_destino='DataSet/procesados'
        )
    except Exception as e:
        print(f"Error durante el procesamiento: {str(e)}")
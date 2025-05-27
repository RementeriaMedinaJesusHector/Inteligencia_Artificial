import cv2
import numpy as np
import tensorflow as tf

CLASES = ['Felicidad', 'Tristeza', 'Sorpresa', 'Enojo']

def cargar_modelo(ruta_modelo='detector_emociones/modelos/mejor_modelo.keras'):
    return tf.keras.models.load_model(ruta_modelo)

def deteccion_tiempo_real():
    print("Cargando modelo...")
    modelo = cargar_modelo()

    detector_facial = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        return

    print("Presiona 'esc' para salir")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rostros = detector_facial.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in rostros:
            rostro = frame[y:y+h, x:x+w]
            try:
                rostro_procesado = cv2.resize(rostro, (96, 96))
                rostro_procesado = rostro_procesado / 255.0
                rostro_procesado = np.expand_dims(rostro_procesado, axis=0)

                predicciones = modelo.predict(rostro_procesado, verbose=0)
                clase_idx = np.argmax(predicciones[0])
                emocion = CLASES[clase_idx]
                confianza = predicciones[0][clase_idx]

                color = (0, 255, 0)
                texto = f"{emocion} ({confianza*100:.1f}%)"
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, texto, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            except Exception as e:
                print(f"Error procesando rostro: {str(e)}")

        cv2.imshow('Detector de Emociones', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        deteccion_tiempo_real()
    except Exception as e:
        print(f"Error: {str(e)}")

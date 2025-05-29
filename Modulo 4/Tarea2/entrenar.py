import os
import tensorflow as tf
from modelo import crear_modelo
from cargar_datos import cargar_datos

def entrenar_modelo(X_train, y_train, X_test, y_test):
    modelo = crear_modelo()

    os.makedirs('detector_emociones/modelos', exist_ok=True)

    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
        tf.keras.callbacks.ModelCheckpoint(
            'detector_emociones/modelos/mejor_modelo.keras',
            monitor='val_accuracy',
            save_best_only=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=3, min_lr=1e-6)
    ]

    historia = modelo.fit(
        X_train, y_train,
        epochs=50,
        batch_size=32,
        validation_data=(X_test, y_test),
        callbacks=callbacks,
        verbose=1
    )

    return modelo, historia

def evaluar_modelo(modelo, X_test, y_test):
    resultados = modelo.evaluate(X_test, y_test, verbose=1)
    print("\nResultados:")
    for nombre, valor in zip(modelo.metrics_names, resultados):
        print(f"{nombre}: {valor:.4f}")

if __name__ == "__main__":
    try:
        X_train, y_train, X_test, y_test = cargar_datos('DataSet/procesados')
        modelo, historia = entrenar_modelo(X_train, y_train, X_test, y_test)
        evaluar_modelo(modelo, X_test, y_test)
    except Exception as e:
        print(f"Error durante entrenamiento: {str(e)}")
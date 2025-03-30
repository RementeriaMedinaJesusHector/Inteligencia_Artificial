import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

#Carga del Dataset
df = pd.read_csv('spam.csv', encoding='latin1')[['v1', 'v2']]
#Convertir columna 1 a label y columna 2 a texto
df = df.rename(columns={'v1': 'label', 'v2': 'text'})
#Convertir NoSpam a 0, Spam a 1
df['label'] = df['label'].map({'ham': 0, 'spam': 1})

# Separacion de datos
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

#Convertir el texto a vectores numericos
vectorizer = TfidfVectorizer()
#transformar vocabulario a valores numericos
X_train_tfidf = vectorizer.fit_transform(X_train)

# Modelo de valles
modelo = MultinomialNB()
#Entrenamiento de los datos
modelo.fit(X_train_tfidf, y_train)

#Presicion esperada del modelo
print(f"Precisión del modelo: {modelo.score(vectorizer.transform(X_test), y_test):.2f}")

#Ventana principal
root = tk.Tk()
root.title("Detector de SPAM")
root.geometry("650x550")

#Enviar Correo
def enviarCorreo():
    Correo = entry_correo.get()
    Asunto = entry_asunto.get()
    Mensaje = text_mensaje.get("1.0", tk.END)
    #Combina los 3 campos en una sola variable
    TextoCombinado = f"{Correo} {Asunto} {Mensaje}"

    # Vectorizar el mensaje
    input_vector = vectorizer.transform([TextoCombinado])
    pred_prob = modelo.predict_proba(input_vector)[0]
    #probabilidad de NoSpam
    P_noSpam = pred_prob[0]
    #Probabilidad de Spam
    p_spam = pred_prob[1]

    # Mostrar Probabilidades
    resultado_prob.config(text=f"Probabilidad de SPAM: {p_spam:.2f}\nProbabilidad de NO SPAM: {P_noSpam:.2f}")

    #Calcular si es Spam
    if p_spam > P_noSpam:
        messagebox.showwarning("SPAM", "El correo fue marcado como SPAM")
    else:
        messagebox.showinfo("Éxito", "Correo enviado correctamente")

#Campo Correo
tk.Label(root, text="Correo:").pack(pady=5)
entry_correo = tk.Entry(root, width=60)
entry_correo.pack(pady=5)

#Campo Asunto
tk.Label(root, text="Asunto:").pack(pady=5)
entry_asunto = tk.Entry(root, width=60)
entry_asunto.pack(pady=5)

#Campo Mensaje
tk.Label(root, text="Mensaje:").pack(pady=5)
text_mensaje = tk.Text(root, width=70, height=10)
text_mensaje.pack(pady=5)

#Boton Enviar
tk.Button(root, text="Enviar Correo", command=enviarCorreo()).pack(pady=20)

# Area probabilidades
resultado_prob = tk.Label(root, text="", font=("Arial", 12))
resultado_prob.pack(pady=10)

root.mainloop()

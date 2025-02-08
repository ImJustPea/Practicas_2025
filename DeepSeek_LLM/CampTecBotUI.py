from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
from llama_cpp import Llama
import speech_recognition as sr
import time
import os

# Definición de las rutas de los archivos del modelo y datos
MODEL = "DeepSeek_LLM/model/DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf"
CONOCIMIENTO = "DeepSeek_LLM/model/model_data/conocimiento.txt"
HISTORIAL = "DeepSeek_LLM/model/model_data/historial.txt"

# Carga del modelo Llama
llm_local = Llama(model_path=MODEL, n_ctx=2048, n_gpu_layers=-1)

# Verificación de la existencia del modelo antes de continuar
if not os.path.exists(MODEL):
    raise FileNotFoundError(f"Modelo no encontrado: {MODEL}")

# Cargar historial de conversación
if os.path.exists(HISTORIAL):
    with open(HISTORIAL, "r", encoding="utf-8") as file:
        conversation_history = file.read()
else:
    conversation_history = ""

# Cargar conocimiento adicional
if os.path.exists(CONOCIMIENTO):
    with open(CONOCIMIENTO, "r", encoding="utf-8") as file:
        conocimiento = file.read()
else:
    conocimiento = ""

# Función para obtener entrada de audio mediante reconocimiento de voz
def get_audio_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="es-ES")
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None

# Función para manejar la entrada de texto
def handle_text_input():
    conversation_display.setHtml('<div style="text-align: center; font-size: 24px; font-weight: bold; margin-top: 40%;">Pensando...</div>')
    app.processEvents()
    global conversation_history
    user_input = input_text.text()
    if user_input.lower() == "salir":
        app.quit()
    elif user_input.lower() == "borrar":
        conversation_history = ""
        open(HISTORIAL, "w").close()
        conversation_display.setText("Memoria borrada.")
        return
    
    prompt = f"Sistema: {conocimiento}\n\nHistorial: {conversation_history}\n\nUsuario: {user_input}"
    
    # Generación de respuesta del modelo
    output = llm_local(
        prompt,
        max_tokens=250,      # Longitud máxima de la respuesta
        temperature=0.5,     # Control de creatividad (menor temperatura = más precisión)
        top_p=0.9,           # Controla la diversidad de palabras
        repeat_penalty=1.2,  # Penalización para evitar repeticiones en la respuesta
    )
    
    response = output["choices"][0]["text"].strip()

    conversation_history += f"User: {user_input}\n{response}\n\n"
    with open(HISTORIAL, "w", encoding="utf-8") as file:
        file.write(conversation_history)
    
    conversation_display.setText(conversation_history)
    input_text.clear()

# Función para manejar la entrada por voz
def handle_audio_input():
    user_input = get_audio_input()
    if user_input:
        conversation_display.append(f"Entrada de voz: {user_input}")
        handle_text_input()

# Configuración de la UI
app = QApplication([])

window = QWidget()
window.setWindowTitle("CampTecBot LLM")
window.setGeometry(100, 100, 700, 500)
layout = QVBoxLayout()

conversation_display = QTextEdit()
conversation_display.setReadOnly(True)
conversation_display.setText(conversation_history)
layout.addWidget(conversation_display)

button_layout = QHBoxLayout()

input_text = QLineEdit()
input_text.setPlaceholderText("Escribe tu mensaje aquí...")
button_layout.addWidget(input_text)

# Botón de enviar texto
send_button = QPushButton("Enviar Texto")
send_button.clicked.connect(lambda: handle_text_input())
button_layout.addWidget(send_button)

# Botón de usar micrófono
audio_button = QPushButton("Usar Micrófono")
audio_button.clicked.connect(lambda: handle_audio_input())
button_layout.addWidget(audio_button)

# Agregar el layout de los botones al layout principal
layout.addLayout(button_layout)

window.setLayout(layout)
window.show()

app.exec()
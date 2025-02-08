# Importación de librerías necesarias
from llama_cpp import Llama  # Carga y ejecución del modelo de lenguaje Llama
import os  # Manejo de archivos y rutas del sistema
import speech_recognition as sr  # Reconocimiento de voz para entrada de audio

# Definición de las rutas de los archivos del modelo y datos
MODEL = "DeepSeek_LLM/model/DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf"  # Ruta del modelo de lenguaje
CONOCIMIENTO = "DeepSeek_LLM/model/model_data/conocimiento.txt"  # Archivo con información adicional para el modelo
HISTORIAL = "DeepSeek_LLM/model/model_data/historial.txt"  # Archivo que almacena el historial de conversaciones

# Carga del modelo Llama desde el repositorio de Hugging Face

# llm_repo = Llama.from_pretrained(
# 	repo_id="lmstudio-community/DeepSeek-Coder-V2-Lite-Instruct-GGUF",
# 	filename="DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf",
#     revision="main",
#     n_ctx=2048,
#     n_gpu_layers=-1,
# )

# Carga del modelo Llama con parámetros personalizados
llm_local = Llama(model_path=MODEL, n_ctx=2048, n_gpu_layers=-1)

# Verificación de la existencia del modelo antes de continuar
if not os.path.exists(MODEL):
    raise FileNotFoundError(f"Modelo no encontrado: {MODEL}")

# Carga del historial de conversación si el archivo existe, de lo contrario, se inicializa vacío
if os.path.exists(HISTORIAL):
    with open(HISTORIAL, "r", encoding="utf-8") as file:
        conversation_history = file.read()
else:
    conversation_history = ""

# Carga de conocimiento adicional si el archivo existe, de lo contrario, se inicializa vacío
if os.path.exists(CONOCIMIENTO):
    with open(CONOCIMIENTO, "r", encoding="utf-8") as file:
        conocimiento = file.read()
else:
    conocimiento = ""

# Función para obtener entrada de audio mediante reconocimiento de voz
def get_audio_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando... (habla ahora)")
        recognizer.adjust_for_ambient_noise(source)  # Ajuste para reducir ruido ambiente
        audio = recognizer.listen(source)  # Captura de audio del micrófono
        try:
            print("Reconociendo...")
            text = recognizer.recognize_google(audio, language="es-ES")  # Conversión de audio a texto
            print(f"Entrada por micrófono: {text}")
            return text
        except sr.UnknownValueError:
            print("No se entendió lo que dijiste.") # Si no se reconoce la entrada, se muestra un mensaje
            return None
        except sr.RequestError:
            print("Error al conectar con el servicio de reconocimiento.") # Si hay un error de conexión, se muestra un mensaje
            return None

# Menú para seleccionar el tipo de entrada (texto o micrófono)
print("\nMenú de entrada:")
print("1. Entrada por texto")
print("2. Entrada por micrófono")

while True:
    user_choice = input("Elige una opción (1 o 2): ")
    if user_choice in ["1", "2"]:
        break
    else:
        print("Opción inválida. Inténtalo de nuevo.")

# Determina si se usará el micrófono según la elección del usuario
use_microphone = user_choice == "2"

print("\nCampTecBot LLM. Escribe 'borrar' para resetear la memoria o 'salir' para terminar.")

# Bucle principal de la conversación
while True:
    # Captura de entrada del usuario (micrófono o texto)
    if use_microphone:
        user_input = get_audio_input()
        if user_input is None:  # Si la entrada es nula, se reinicia el bucle
            continue
    else:
        user_input = input("Tú: ")

    # Comando para salir del programa
    if user_input.lower() == "salir":
        print("Terminando conversación...")
        break
    # Comando para borrar la memoria del asistente
    elif user_input.lower() == "borrar":
        print("Memoria borrada.")
        conversation_history = ""
        open(HISTORIAL, "w").close()  # Se vacía el archivo de historial
        continue

    # Construcción del prompt incluyendo el historial de conversación
    prompt = f"Sistema: {conocimiento}\n\nHistorial: {conversation_history}\n\nUsuario: {user_input}"

    # Generación de respuesta del modelo
    output = llm_local(
        prompt,
        max_tokens=250,      # Longitud máxima de la respuesta
        temperature=0.5,     # Control de creatividad (menor temperatura = más precisión)
        top_p=0.9,           # Controla la diversidad de palabras
        repeat_penalty=1.2,  # Penalización para evitar repeticiones en la respuesta
    )

    # Obtención y limpieza de la respuesta generada por el modelo
    response = output["choices"][0]["text"].strip()

    # Actualización del historial de conversación
    conversation_history += f"User: {user_input}\n{response}\n\n"

    # Guardado del historial en el archivo de texto
    with open(HISTORIAL, "w", encoding="utf-8") as file:
        file.write(conversation_history)

    # Muestra la respuesta en la consola
    print(f"\n{response}")
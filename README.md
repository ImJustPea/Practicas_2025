# Documentación para Desarrolladores

## 1. Introducción
Este documento proporciona una descripción técnica del asistente conversacional basado en el modelo **DeepSeek-V2-Lite** (proporcionado por *LM Studio*). La aplicación permite interacciones por texto o reconocimiento de voz, manteniendo un historial de conversaciones para mejorar la coherencia del diálogo.

## 2. Requisitos del Sistema

### 2.1. Dependencias
El código requiere las siguientes bibliotecas de Python:

- `llama_cpp` → Para cargar y ejecutar el modelo de lenguaje.  
- `os` → Para gestionar archivos y directorios.  
- `speech_recognition` → Para el reconocimiento de voz.
- `huggingface-hub` → Para referenciar el modelo desde el repositorio de huggingface.

### 2.2. Instalación de Dependencias
Ejecutar el siguiente comando para instalar los paquetes necesarios:
```bash
pip install llama-cpp-python speechrecognition huggingface-hub
```
### 2.3. Requisitos de Hardware
- **GPU recomendada** para mejorar el rendimiento del modelo.  
- **Micrófono** en caso de utilizar entrada por voz.

#### 2.3.1 Adaptación y descarga del modelo (Si es necesario en local)
- **Descarga**: [LLM Studio](https://lmstudio.ai/model/deepseek-coder-v2-lite-instruct) <-- Dejo el link de donde he descargado el modelo que he usado
- **Adaptación en el código**:

##### Local
```python
# Definición de las rutas de los archivos del modelo y datos
MODEL = "model/<MODELO>"  # Ruta del modelo de lenguaje
```
##### Repositorio Huggingface
```python
# Carga del modelo Llama desde el repositorio de Hugging Face
llm_repo = Llama.from_pretrained(
	repo_id="lmstudio-community/DeepSeek-Coder-V2-Lite-Instruct-GGUF",
	filename="DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf",
    revision="main",
    n_ctx=2048,
    n_gpu_layers=-1,     # Numero de capas que va a procesar la GPU (-1 equivale a todas)
)
```

Debes cambiar la variable `llm_local` o `llm_repo` dependiendo de lo que quieras utilizar
```python
# Aqui debemos seleccionar cual llm utilizar
output = llm_local_llm_repo(
    prompt,
    max_tokens=250,      # Longitud máxima de la respuesta
    temperature=0.3,     # Control de creatividad (menor temperatura = más precisión)
    top_p=0.9,           # Controla la diversidad de palabras
    repeat_penalty=1.2,  # Penalización para evitar repeticiones en la respuesta
)
```

## 3. Arquitectura del Sistema
El asistente sigue un flujo basado en:

1. **Carga del modelo de lenguaje.**  
2. **Lectura del conocimiento forzado del modelo.**  
3. **Lectura del historial de conversación** si está disponible.  
4. **Interacción con el usuario** por entrada de texto o voz.  
5. **Generación de respuesta** basada en el historial.  
6. **Actualización del historial** para mantener el contexto de la conversación.  

## 4. Flujo de Ejecución
Explicación del flujo de trabajo del código, incluyendo carga del modelo, gestión del historial, entrada del usuario, generación de respuestas y almacenamiento de historial.

## 5. Comandos Especiales
- `'borrar'` → Borra el historial de conversación.  
- `'salir'` → Termina la ejecución del programa.  

## 6. Posibles Mejoras
- Mejorar la eficiencia del modelo reduciendo tokens innecesarios.  
- Optimizar la gestión del historial usando bases de datos en lugar de archivos de texto.  
- Incorporar una interfaz gráfica para mejorar la experiencia del usuario.  

## 7. Contacto y Mantenimiento
**Autor:** Gontzal Izurza Rementeria  
**Última actualización:** 10/02/2025

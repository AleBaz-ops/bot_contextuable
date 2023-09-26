# *****************************************************************************************************
# *****************************************************************************************************
# ***************************         Chat bot con contexto        *********************************
# *****************************************************************************************************
# *****************************************************************************************************

# Las librerias deben importarse desde la consola o desde linea de comnado ejecutando pip install <libreria>

import openai
import time
import config
import pyttsx3
import speech_recognition as sr
import logging
import keyapp

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up OpenAI API
openai.api_key = keyapp.api_key
model_name = "gpt-3.5-turbo"


def transformar_audio_a_texto() -> str:
    """
    Transforms audio input from a microphone to text using SpeechRecognition.
    """
    r = sr.Recognizer()
    with sr.Microphone() as origen:
        r.adjust_for_ambient_noise(source=origen)
        r.pause_threshold = 1.2
        print("Esperando 5 segundos antes de empezar a escuchar...\n")
        time.sleep(10)  # Espera 10 segundos
        print("Ya puedes hablar \n")
        audio = r.listen(source=origen)
        try:
            pedido = r.recognize_google(audio_data=audio, language="es-AR")
            logging.info(msg=f"Usuario: {pedido}")
            return pedido
        except sr.UnknownValueError:
            logging.error(msg="Ups, continuando con el contexto y la última respuesta de mi parte :\n")
            return hilo_guardado
        except sr.RequestError:
            logging.error(msg="Ups, no hay servicio")
            return "salir"
        except Exception as e:
            logging.error(msg=f"Ups, algo salió mal: {e}")
            return "salir"


def hablar(mensaje: str) -> None:
    """
    Uses pyttsx3 to speak a given message.
    """
    engine = pyttsx3.init()
    engine.setProperty("rate", 140)
    engine.say(mensaje)
    engine.runAndWait()
    engine.stop()

    """
    Loads the conversation saved in "Linea.txt" and returns its content.
    If the file does not exist, returns None.
    """
# Cargamos el hilo de la conversación guardado
def cargar_hilo_guardado():
    try:
        with open("Linea.txt", "r") as archivo:
            contenido = [linea.strip('\n') for linea in archivo.readlines()]
            ultimas_5_lineas = contenido[-5:]
            return '\n'.join(ultimas_5_lineas)
    except FileNotFoundError:
        logging.error(msg="Ups, Linea.txt no encontrado")
        return None
 
def run_chatbot() -> None:
    """
    Runs the chatbot, using OpenAI's GPT-3 model to generate responses.
    """
    # Set up conversation context
token_count = 0
context = config.Context_txt                    
    
messages = [context]

    # Load past conversation from file, if available
hilo_guardado = cargar_hilo_guardado()

if hilo_guardado:
        print("Continuando con la combersacion :\n")
        hablar(mensaje="Hola!,  Continuando con la conversacion. ¿En qué puedo ayudarte?")
        messages.append({"role": "system", "content": "Continuando con el hilo de conversacion guardada."})
        messages.append({"role": "user", "content": hilo_guardado})

while True:

    question = transformar_audio_a_texto().lower()

    if question == "salir":
       break

    messages.append({"role": "user", "content": question})

        # Get response from OpenAI's GPT-3 model
    try:
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=messages
            )
            response_content = response.choices[0].message.content

            token_count += response['usage']['total_tokens']

            messages.append({"role": "assistant", "content": response_content})

            logging.info(f"Assistant: {response_content}")
            hablar(mensaje=response_content)
            print("\n Número de tokens utilizados:", token_count)

            # Save conversation to file
            with open("Linea.txt", "a", encoding="utf-8") as archivo:
                archivo.write("Usuario :\n" + question + "\n" + "IA :\n" + response_content + "\n")
            with open("HiloConversado.txt", "a", encoding="utf-8") as archivo:
                archivo.write("Usuario :\n" + question + "\n" + "IA :\n" + response_content + "\n")    
                
    except Exception as e:
        logging.error(f"Error getting OpenAI response: {e}")


if __name__ == "__main__":
    run_chatbot()

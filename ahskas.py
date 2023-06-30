from fuzzywuzzy import fuzz
import speech_recognition as sr
from pydub import AudioSegment
import pyttsx3
import subprocess
from pydub.playback import play
from gtts import gTTS
import os

def texto_a_audio(texto):
    tts = gTTS(text=texto, lang='es')
    tts.save('audio_salida.wav')
    os.system('aplay audio_salida.wav')

def audio_a_texto(archivo_audio):
    r = sr.Recognizer()

    # Convertir el archivo de audio a formato WAV
    archivo_wav = "audio.wav"
    audio = AudioSegment.from_mp3(archivo_audio)
    audio.export(archivo_wav, format="wav")

    with sr.AudioFile(archivo_wav) as source:
        audio = r.record(source)  # Leer el archivo de audio

        try:
            texto = r.recognize_google(audio, language='es')  # Reconocer el texto utilizando Google Speech Recognition
            return texto
        except sr.UnknownValueError:
            return "No se pudo reconocer el audio"
        except sr.RequestError:
            return "Error en la solicitud al servicio de reconocimiento de voz"

# Ruta del archivo de audio que deseas convertir
archivo_audio = "audio_entrada.mp3"

# Llamar a la función para convertir el audio a texto
texto_transcrito = audio_a_texto(archivo_audio)

# Ruta del archivo de texto de referencia
archivo_referencia = "referencia_respuestas.txt"
archivo_referencia_preguntas = "referencia_preguntas.txt"

# Leer el contenido del archivo de texto de referencia respuestas
with open(archivo_referencia, "r") as archivo:
    texto_referencia = archivo.read().replace('\n', '')

# Leer el contenido del archivo de texto de referencia preguntas
with open(archivo_referencia_preguntas, "r") as archivo:
    texto_referencia_preguntas = archivo.read().replace('\n', '')

# Llamar a la función para convertir el audio a texto
texto_transcrito = audio_a_texto(archivo_audio)

# Calcular la similitud entre el texto transcrito y el texto de referencia
similitud = fuzz.ratio(texto_transcrito, texto_referencia)

# Imprimir el resultado
print("Texto transcrito:", texto_transcrito)
print("Pregunta de referencia:", texto_referencia)
print("Respuesta de referencia:", texto_referencia_preguntas)
print("Similitud:", similitud)

# Convertir el texto transcrito en audio y reproducirlo
texto_a_audio(texto_referencia_preguntas)

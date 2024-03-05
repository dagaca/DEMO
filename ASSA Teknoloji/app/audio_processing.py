# app/audio_processing.py

# Bu kod, ses dosyalarından metin verisi çıkarmak için kullanılır. 
# Ses verisi, Google Konuşma Tanıma API'sını kullanarak metne dönüştürülür.

# File imports
import speech_recognition as sr

# Function to extract text from audio files
def extract_text_from_audio(audio_path):
    recognizer = sr.Recognizer()
    # Open the audio file and extract audio data
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        # Recognize speech from the audio data using Google Speech Recognition API
        text = recognizer.recognize_google(audio_data, language='en-US')  # Change the language option as needed
    return text
# app/video_processing.py

# Bu kod, video dosyalarını işlemek ve duygularını tanımak için kullanılır.

# File imports
import cv2
import numpy as np
from keras.models import load_model
import moviepy.editor as mp

# Öncelikle, önceden KAGGLE'da eğitilmiş bir duygu tanıma modeli (FER_model.h5) yüklenir. 
# Bu model, CNN kullanılarak duyguları tanımak için eğitilmiştir.
# Load the trained emotion recognition model
model = load_model('model/FER_model.h5')

# Kod, duyguların etiketlerini tanımlar. 
# Bu etiketler, duygu tanıma modelinin çıktılarını anlamlandırmak için kullanılır.
# Define emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Kod, video dosyasının işlenmesi için tanımlanır. 
# Bu fonksiyon, her karede yüz algılar, duygu tanıma modeliyle uyumlu hale getirir 
# ve duyguları tahmin eder. Ardından, video boyunca tespit edilen duyguların ortalama 
# değerlerini hesaplar ve bir sözlük olarak döndürür.
# Function for video processing
def process_video(video_path):
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    total_frames = 0
    emotion_totals = np.zeros(len(emotion_labels))

    # Process each frame in the video
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Preprocess the frame for emotion recognition
        face = cv2.resize(frame, (48, 48))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        face = np.expand_dims(face, axis=0)
        face = np.expand_dims(face, axis=-1)

        # Make predictions using the emotion recognition model
        predictions = model.predict(face)
        emotion_probabilities = predictions[0]

        # Update the total number of frames and the sum of emotion probabilities
        total_frames += 1
        emotion_totals += emotion_probabilities

    video_capture.release()
    cv2.destroyAllWindows()

    # Calculate the average emotions
    average_emotions = emotion_totals / total_frames

    # Format and round the average emotions as percentages
    average_emotions_dict = {}
    for label, probability in zip(emotion_labels, average_emotions):
        average_emotions_dict[label] = round(probability.item() * 100, 2)

    return average_emotions_dict

# Kod, bir video dosyasının sesini çıkarır ve ayrı bir ses dosyasına kaydeder.
# Function to convert video to audio
def convert_video_to_audio(video_path, audio_path):
    # Open the video file and extract audio
    video_clip = mp.VideoFileClip(video_path)
    audio_clip = video_clip.audio
    # Write the audio to a separate file
    audio_clip.write_audiofile(audio_path)
    video_clip.close()
    audio_clip.close()
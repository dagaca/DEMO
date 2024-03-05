# app/routes.py

# Bu kod, bir Flask uygulaması içinde web tabanlı bir arayüz ve bir API hizmeti sağlar. 
# Kullanıcılar, video dosyalarını yükleyebilir ve bu dosyalar üzerinde duygu analizi ve 
# metin işleme gibi işlemler yapılabilir. Ana sayfa HTML formu aracılığıyla kullanıcılara 
# interaktif bir arayüz sunar. Ayrıca, /api/process_video endpoint'i, diğer uygulamaların 
# veya hizmetlerin bu işlevleri doğrudan kullanmasına olanak tanır. Bu kod, yüklü video 
# dosyasını işleyerek metin, duygu analizi sonuçları ve iş yetenekleri ile ilgili özetler 
# üretir ve bu bilgileri kullanıcıya veya diğer programlara sunar.

# File imports
from flask import request, jsonify #, render_template
from app import app  # Import the Flask application
import os
from werkzeug.utils import secure_filename
from app.video_processing import process_video, convert_video_to_audio
from app.audio_processing import extract_text_from_audio
from app.text_processing import process_text_for_skills, evaluate_result, perform_sentiment_analysis

# # Homepage route for HTML usage - TEST
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         # File validation: Check if file part exists in request
#         if 'file' not in request.files:
#             return render_template('index.html', error="No file part.")
#         file = request.files['file']
#         # Check if file has a name
#         if file.filename == '':
#             return render_template('index.html', error="No selected file.")
#         if file:
#             # Remove the existing video file before saving the new one
#             if os.path.exists('uploads/video.mp4'):
#                 os.remove('uploads/video.mp4')
#             file.save('uploads/video.mp4')
#             # Path for the audio file
#             audio_path = 'uploads/audio.wav'
#             # Convert video to audio
#             convert_video_to_audio('uploads/video.mp4', audio_path)
#             # Extract text from the audio file
#             extracted_text = extract_text_from_audio(audio_path)
#             # Process the video and calculate emotions
#             result = process_video('uploads/video.mp4')
#             # Get the threshold value from the screen
#             threshold = float(request.form.get('threshold')) if request.form.get('threshold') else 0.6
#             # Get the required skills for the job
#             required_skills = request.form.get('skills').split(',')
#             # Text processing and skill extraction
#             skills_summary = process_text_for_skills(extracted_text, required_skills)
#             # Sentiment analysis
#             interview_sentiment_score = perform_sentiment_analysis(extracted_text)
#             # Evaluate the result
#             evaluation_result = evaluate_result(interview_sentiment_score, skills_summary, threshold=threshold)
#             # Render the template with extracted data
#             return render_template('index.html', text=extracted_text, emotions=result, sentiment_score=interview_sentiment_score, skills_matched=skills_summary, evaluation_result=evaluation_result)
#     # Render the homepage template for GET requests
#     return render_template('index.html')

# API service endpoint for processing video - POSTMAN
@app.route('/api/process_video', methods=['POST'])
def process_video_api():
    # File validation: Check if file part exists in request
    if 'file' not in request.files:
        return jsonify({'error': "No file part"}), 400
    file = request.files['file']
    # Check if file has a name
    if file.filename == '':
        return jsonify({'error': "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        video_path = os.path.join('uploads', filename)
        # Save the file
        file.save(video_path)
        # Convert video to audio
        audio_path = os.path.splitext(video_path)[0] + '.wav'
        convert_video_to_audio(video_path, audio_path)
        # Extract text from the audio file
        extracted_text = extract_text_from_audio(audio_path)
        # Process the video and calculate emotions
        emotions = process_video(video_path)
        # Get the threshold value from the screen
        threshold = float(request.form.get('threshold')) if request.form.get('threshold') else 0.6
        # Get the required skills for the job
        required_skills = request.form.get('skills').split(',') if request.form.get('skills') else []
        # Text processing and skill extraction
        skills_summary = process_text_for_skills(extracted_text, required_skills)
        # Sentiment analysis
        sentiment_score = perform_sentiment_analysis(extracted_text)
        # Evaluate the result
        evaluation_result = evaluate_result(sentiment_score, skills_summary, threshold=threshold)
        # Return the response as JSON
        return jsonify({
            'text': extracted_text,
            'emotions': emotions,
            'sentiment_score': sentiment_score,
            'skills_matched': skills_summary,
            'evaluation_result': evaluation_result
        }), 200
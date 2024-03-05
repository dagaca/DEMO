# app/text_processing.py

# Bu kod, metin verilerini analiz etmek, becerileri belirlemek ve bir adayın iş 
# için uygun olup olmadığını değerlendirmek için kullanılır.

# File imports
from nltk.sentiment import SentimentIntensityAnalyzer
# from nltk.tokenize import word_tokenize
# from nltk.stem import PorterStemmer
# from nltk.corpus import stopwords
import re

# Metinlerin duygusal içeriğini analiz eder. 
# 'SentimentIntensityAnalyzer' sınıfını kullanarak metindeki duygusal yoğunluğu hesaplar.
# Function for sentiment analysis
def perform_sentiment_analysis(text):
    # Initialize SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    # Calculate sentiment score for the text
    sentiment_score = sid.polarity_scores(text)["compound"]
    return sentiment_score

# # Bu fonksiyon, metin verilerini konu modellemesi için ön işleme adımlarından geçirir. 
# # Text preprocessing function for topic modeling
# def preprocess_text_for_topics(text):
#     # Convert text to lowercase
#     text = text.lower()
#     # Remove numbers and punctuation marks
#     text = re.sub(r'\d+', '', text)
#     text = re.sub(r'[^\w\s]', '', text)
#     # Tokenize the text into words
#     words = word_tokenize(text)
#     # Remove stop words
#     stop_words = set(stopwords.words('english'))
#     words = [word for word in words if word not in stop_words]
#     # Stemming of words
#     ps = PorterStemmer()
#     words = [ps.stem(word) for word in words]
#     # Join the cleaned words back into a single string
#     cleaned_text = ' '.join(words)
#     return cleaned_text

# Belirli bir beceriyle ilişkili cümleleri çıkarır. 
# Metinde belirli bir beceri adını arar ve bu beceriyle ilgili cümleleri çıkarır.
# Function to extract sentences related to a skill
def extract_skill_summary(text, skill):
    # Convert text and skill name to lowercase
    text = text.lower()
    skill = skill.lower()
    # Initialize an empty list to store sentences related to the skill
    sentences = []
    # Define pattern to find sentences containing the skill
    pattern = r'\b(?:\S+\s+){0,3}' + re.escape(skill) + r'(?:\s+\S+){0,3}\b'
    # Iterate through matches of the pattern in the text
    for match in re.finditer(pattern, text):
        # Get the indices of the matched sentence
        start_index = match.start()
        end_index = match.end()
        # Find the start and end of the previous and next words
        prev_space = max(text.rfind(' ', 0, start_index), 0)
        prev_words = text[prev_space:start_index].strip()
        next_space = text.find(' ', end_index)
        next_words = text[end_index:next_space].strip()
        # Construct the sentence by combining previous, matched, and next words
        sentence = prev_words + text[start_index:end_index] + next_words
        # Add the extracted sentence to the list
        sentences.append(sentence.strip())
    return sentences

# Metin içinde belirli becerilere ilişkin özet bilgileri çıkarır. Metinde belirli 
# becerilerin kaç kez geçtiğini ve bu becerilerle ilişkili cümleleri içeren bir 
# sözlük döndürür.
# Function for text processing and skill extraction
def process_text_for_skills(text, required_skills):
    skills_summary = {}
    for skill in required_skills:
        # Count occurrences of the skill in the text
        occurrences = len(re.findall(r'\b' + re.escape(skill) + r'\b', text.lower()))
        # Extract sentences related to the skill
        sentences = extract_skill_summary(text, skill)  # Yetenek özetini al
        skills_summary[skill] = {'occurrences': occurrences, 'occurrences_summary': sentences}
    return skills_summary

# Sonuçları değerlendirir. Metnin duygu puanını ve belirli becerilerle ilgili özet 
# bilgileri alır ve belirlenen bir eşik değeri üzerinden adayın iş için uygun olup 
# olmadığını belirler.
# Function for evaluation
def evaluate_result(sentiment_score, skills_matched, threshold):
    matched_skills = [skill for skill, summary in skills_matched.items() if summary['occurrences'] > 0]
    if sentiment_score >= threshold and matched_skills:
        return "Candidate is suitable for the job."
    else:
        return "Candidate is not suitable for the job."
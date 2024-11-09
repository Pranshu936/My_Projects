import cv2
import datetime
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from transformers import pipeline
from fer import FER
import nltk

nltk.download('vader_lexicon')

sid = SentimentIntensityAnalyzer()
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
emotion_detector = FER()

video_capture = cv2.VideoCapture(0)

log_file = "sentiment_log.txt"

def log_results(result_type, content, analysis):
    with open(log_file, "a") as file:
        file.write(f"\n[{datetime.datetime.now()}] {result_type}:\n")
        file.write(f"Content: {content}\n")
        file.write(f"Analysis: {analysis}\n")

def analyze_text_sentiment(text):
    blob = TextBlob(text)
    blob_polarity = blob.sentiment.polarity
    blob_subjectivity = blob.sentiment.subjectivity

    vader_scores = sid.polarity_scores(text)
    transformer_result = sentiment_model(text)[0]

    text_result = {
        "TextBlob": {"Polarity": blob_polarity, "Subjectivity": blob_subjectivity},
        "VADER": vader_scores,
        "DistilBERT": {"Sentiment": transformer_result['label'], "Score": transformer_result['score']}
    }

    log_results("Text Sentiment", text, text_result)

    print("\nText Sentiment Analysis Results:")
    print(f"TextBlob Polarity: {blob_polarity} | Subjectivity: {blob_subjectivity}")
    print(f"VADER Compound Score: {vader_scores['compound']}")
    print(f"DistilBERT Sentiment: {transformer_result['label']} | Score: {transformer_result['score']:.2f}")

    return text_result

def analyze_face_emotion(frame):
    emotions = emotion_detector.detect_emotions(frame)
    for emotion in emotions:
        bounding_box = emotion["box"]
        dominant_emotion = max(emotion["emotions"], key=emotion["emotions"].get)
        emotion_score = emotion["emotions"][dominant_emotion]

        x, y, w, h = bounding_box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"{dominant_emotion}: {emotion_score:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        log_results("Face Emotion", "Detected face", {"Emotion": dominant_emotion, "Score": emotion_score})

        return f"{dominant_emotion} ({emotion_score:.2f})"
    return None

def main():
    input_type = input("Choose input type (camera/text): ").strip().lower()

    if input_type == 'camera':
        user_text = ""
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            face_emotion_summary = analyze_face_emotion(frame)

            if face_emotion_summary:
                cv2.putText(frame, f"Face Emotion: {face_emotion_summary}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            cv2.imshow("Sentiment Analysis - Face Emotion", frame)

            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

    elif input_type == 'text':
        user_text = input("Enter text for sentiment analysis: ")
        text_sentiment_summary = analyze_text_sentiment(user_text)

    else:
        print("Invalid input type. Please choose 'camera' or 'text'.")
        return

if __name__ == "__main__":
    main()

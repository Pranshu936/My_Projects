import cv2
import datetime
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from transformers import pipeline
from fer import FER
import nltk

# Download the VADER lexicon for sentiment analysis
nltk.download('vader_lexicon')

# Initialize sentiment analysis tools
sid = SentimentIntensityAnalyzer()  # VADER sentiment analyzer
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")  # DistilBERT sentiment model
emotion_detector = FER()  # Facial emotion detector

# Initialize video capture for camera input (use camera 0)
video_capture = cv2.VideoCapture(0)

# Log file to record results
log_file = "sentiment_log.txt"

# Function to log analysis results to a file
def log_results(result_type, content, analysis):
    """
    Logs the results of the sentiment analysis or emotion detection to a text file.

    Parameters:
    - result_type: Type of result (e.g., "Text Sentiment" or "Face Emotion").
    - content: The content analyzed (e.g., input text or a description of the face).
    - analysis: The analysis result data (e.g., sentiment scores or detected emotion).
    """
    with open(log_file, "a") as file:
        file.write(f"\n[{datetime.datetime.now()}] {result_type}:\n")
        file.write(f"Content: {content}\n")
        file.write(f"Analysis: {analysis}\n")

# Function to analyze sentiment of input text using multiple tools
def analyze_text_sentiment(text):
    """
    Analyzes the sentiment of a text input using TextBlob, VADER, and DistilBERT.

    Parameters:
    - text: The input text to analyze.

    Returns:
    - text_result: Dictionary containing sentiment analysis results from each tool.
    """
    # Use TextBlob for polarity and subjectivity analysis
    blob = TextBlob(text)
    blob_polarity = blob.sentiment.polarity
    blob_subjectivity = blob.sentiment.subjectivity

    # Use VADER for sentiment scores (negative, neutral, positive, and compound)
    vader_scores = sid.polarity_scores(text)

    # Use DistilBERT transformer model for sentiment analysis
    transformer_result = sentiment_model(text)[0]

    # Combine results from all tools
    text_result = {
        "TextBlob": {"Polarity": blob_polarity, "Subjectivity": blob_subjectivity},
        "VADER": vader_scores,
        "DistilBERT": {"Sentiment": transformer_result['label'], "Score": transformer_result['score']}
    }

    # Log results to file
    log_results("Text Sentiment", text, text_result)

    # Print results for immediate reference
    print("\nText Sentiment Analysis Results:")
    print(f"TextBlob Polarity: {blob_polarity} | Subjectivity: {blob_subjectivity}")
    print(f"VADER Compound Score: {vader_scores['compound']}")
    print(f"DistilBERT Sentiment: {transformer_result['label']} | Score: {transformer_result['score']:.2f}")

    return text_result

# Function to analyze facial emotions in a video frame
def analyze_face_emotion(frame):
    """
    Detects and analyzes emotions from a face in the video frame using the FER model.

    Parameters:
    - frame: The current video frame to analyze.

    Returns:
    - A summary of the detected emotion and score as a string, or None if no face is detected.
    """
    emotions = emotion_detector.detect_emotions(frame)

    # Process each detected face
    for emotion in emotions:
        # Extract bounding box and dominant emotion for each face
        bounding_box = emotion["box"]
        dominant_emotion = max(emotion["emotions"], key=emotion["emotions"].get)
        emotion_score = emotion["emotions"][dominant_emotion]

        # Draw a rectangle around the detected face and display the dominant emotion
        x, y, w, h = bounding_box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"{dominant_emotion}: {emotion_score:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Log the detected emotion
        log_results("Face Emotion", "Detected face", {"Emotion": dominant_emotion, "Score": emotion_score})

        return f"{dominant_emotion} ({emotion_score:.2f})"
    return None

# Main function to run the program based on user input type (text or camera)
def main():
    # Get user choice for input type
    input_type = input("Choose input type (camera/text): ").strip().lower()

    # If camera input is chosen, analyze face emotions in real-time
    if input_type == 'camera':
        while True:
            # Capture frame from the camera
            ret, frame = video_capture.read()
            if not ret:
                break

            # Analyze face emotion in the captured frame
            face_emotion_summary = analyze_face_emotion(frame)

            # Display the detected emotion on the frame
            if face_emotion_summary:
                cv2.putText(frame, f"Face Emotion: {face_emotion_summary}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            # Display the frame with emotion information
            cv2.imshow("Sentiment Analysis - Face Emotion", frame)

            # Press 'q' to exit
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break

        # Release the video capture and close all windows
        video_capture.release()
        cv2.destroyAllWindows()

    # If text input is chosen, analyze text sentiment
    elif input_type == 'text':
        user_text = input("Enter text for sentiment analysis: ")
        text_sentiment_summary = analyze_text_sentiment(user_text)

    # Handle invalid input
    else:
        print("Invalid input type. Please choose 'camera' or 'text'.")
        return

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()

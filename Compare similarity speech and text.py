import speech_recognition as sr
from difflib import SequenceMatcher

# Function to recognize speech from a WAV file
def recognize_speech_from_wav(wav_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file_path) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

# Function to calculate similarity percentage
def calculate_similarity(expected_text, recognized_text):
    return SequenceMatcher(None, expected_text, recognized_text).ratio() * 100

# Calculate each data

data_similarity = []

for i in range(1, 13):
    # compare path
    wav_file_path = f"E:\Perkuliahan\Semester 4\Pembelajaran Mesin\Tugas Membuat Makalah\Speech-to-text\Data Suara kalimat 1 wav\Data {i} kalimat 1.wav"  # Replace with the path to your WAV file
    expected_text = "London, the capital city of the United Kingdom, is a vibrant metropolis rich in history and culture."

    # Recognize speech from WAV file
    recognized_text = recognize_speech_from_wav(wav_file_path)

    # Calculate similarity percentage
    similarity_percentage = calculate_similarity(expected_text, recognized_text)

    # Add similarity percentage to data similarity
    data_similarity.append(round(similarity_percentage, 2))

print("Similarity Percentage each Data : ", data_similarity)
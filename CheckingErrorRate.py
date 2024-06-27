import speech_recognition as sr
import Levenshtein as lev
import os

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        print(f"Processing file: {file_path}")  # Debugging line
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="en-US", show_all=False)
            return text.lower()
        except sr.UnknownValueError as e:
            print(f"Speech recognition could not understand audio in {os.path.basename(file_path)}: {str(e)}")
            return ""
        except sr.RequestError as e:
            print(f"Error from Google Speech Recognition service in {os.path.basename(file_path)}: {str(e)}")
            return ""

def calculate_error_rate(transcribed_text, target_word="city"):
    distance = lev.distance(transcribed_text, target_word)
    max_length = max(len(transcribed_text), len(target_word))
    error_rate = (distance / max_length) * 100
    return error_rate

def get_audio_files(directory):
    audio_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".wav"):
                audio_files.append(os.path.join(root, file))
    return audio_files

def main():
    audio_dir = 'E:\Perkuliahan\Semester 4\Pembelajaran Mesin\Tugas Membuat Makalah\Speech-to-text\cutAudioData'  # Update with your folder path
    if not os.path.exists(audio_dir):
        print(f"The directory {audio_dir} does not exist.")
        return
    
    audio_files = get_audio_files(audio_dir)
    print(f"Found {len(audio_files)} audio files.")  # Debugging line

    total_error_rate = 0
    valid_samples = 0

    for file in audio_files:
        transcribed_text = transcribe_audio(file)
        if transcribed_text:
            error_rate = calculate_error_rate(transcribed_text)
            print(f"File: {os.path.basename(file)}, Transcribed: '{transcribed_text}', Error Rate: {error_rate:.2f}%")
            total_error_rate += error_rate
            valid_samples += 1
        else:
            print(f"File: {os.path.basename(file)}, Transcription failed or empty.")

    if valid_samples > 0:
        average_error_rate = total_error_rate / valid_samples
        print(f"Average Error Rate: {average_error_rate:.2f}%")
    else:
        print("No valid samples to calculate average error rate.")

if __name__ == "__main__":
    main()

from pydub import AudioSegment
import re
import os
import requests

# Fungsi untuk mentranskripsi audio menggunakan Deepgram
def transcribe_audio(api_key, audio_file_path):
    url = "https://api.deepgram.com/v1/listen"
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "audio/wav"
    }

    with open(audio_file_path, 'rb') as audio_file:
        response = requests.post(url, headers=headers, data=audio_file)

    return response.json()

# Fungsi untuk mencari waktu mulai dan akhir dari kata dalam transkripsi
def find_word_timestamps(transcript, target_word):
    word_timestamps = []
    for item in transcript["results"]["channels"][0]["alternatives"][0]["words"]:
        if item["word"].lower() == target_word.lower():
            start_offset = max(0, item["start"] - 0.1)  # Offset 1.0 detik sebelum kata
            end_offset = item["end"] - 0.08  # Offset 1.0 detik setelah kata
            word_timestamps.append((start_offset, end_offset))
    return word_timestamps

# Fungsi untuk memotong audio berdasarkan waktu mulai dan akhir, dengan menambahkan durasi hening
def cut_audio(audio_file_path, word_timestamps, silence_duration=1500):
    audio = AudioSegment.from_wav(audio_file_path)
    silence = AudioSegment.silent(duration=silence_duration)
    extracted_segments = []

    for start, end in word_timestamps:
        start_ms = max(0, start) * 1000
        end_ms = end * 1000
        segment = audio[start_ms:end_ms]
        # Menambahkan durasi hening sebelum dan sesudah segmen yang diekstraksi
        segment_with_silence = silence + segment + silence
        extracted_segments.append(segment_with_silence)

    return extracted_segments

# Fungsi untuk mengurutkan nama file secara numerik
def sort_numerically(file_list):
    def extract_number(file_name):
        match = re.search(r'\d+', file_name)
        return int(match.group()) if match else 0
    return sorted(file_list, key=extract_number)

# Fungsi utama untuk mentranskripsi dan memotong audio
def main():
    api_key = "c512a87f4a5778b9ad9a47b1490d29c4241e7299"
    audio_folder_path = "E:\\voiceData"
    target_word = "city"
    output_folder = "cutAudioData"

    # Dapatkan daftar file audio dan urutkan secara numerik
    audio_files = [f for f in os.listdir(audio_folder_path) if f.endswith(".wav")]
    sorted_audio_files = sort_numerically(audio_files)

    # Iterasi semua file audio dalam folder yang sudah diurutkan
    for audio_file_name in sorted_audio_files:
        audio_file_path = os.path.join(audio_folder_path, audio_file_name)

        # Transkripsi audio
        transcript = transcribe_audio(api_key, audio_file_path)

        # Cari waktu mulai dan akhir kata target dalam transkripsi
        word_timestamps = find_word_timestamps(transcript, target_word)

        if word_timestamps:
            # Potong audio berdasarkan waktu mulai dan akhir dengan offset dan hening
            extracted_segments = cut_audio(audio_file_path, word_timestamps)

            # Simpan segmen yang diekstraksi dalam folder yang sesuai
            output_folder_path = os.path.join(output_folder, os.path.splitext(audio_file_name)[0])
            os.makedirs(output_folder_path, exist_ok=True)

            for i, segment in enumerate(extracted_segments):
                output_path = os.path.join(output_folder_path, f"City_{i + 1}.wav")
                segment.export(output_path, format="wav")
                print(f"Segment extracted from {audio_file_name} was saved in {output_path}")
        else:
            print(f"Kata '{target_word}' tidak ditemukan dalam {audio_file_name}.")

if __name__ == "__main__":
    main()

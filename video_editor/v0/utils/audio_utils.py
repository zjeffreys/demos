import random
import os

def get_audio_files(directory):
    return [f for f in os.listdir(directory) if f.endswith(('.mp3', '.wav'))]

def get_random_audio_file(audio_directory):
    all_files = os.listdir(audio_directory)
    audio_files = [file for file in all_files if file.endswith(('.mp3', '.wav'))]
    if audio_files:
        random_audio_file = random.choice(audio_files)
        return os.path.join(audio_directory, random_audio_file)
    else:
        print("No Audio files found")
        return None
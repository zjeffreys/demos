# main.py
from video_editor import * 
from config import Config
from utils.video_utils import *
from utils.audio_utils import * 
from datetime import datetime

from video_editor.v0.video_editor import generate_clips, synchronize_transitions_beat, synchronize_transitions_onset

def main():
    config = Config()
    clips = []

    if(config.testingMode): 
        clips = load_clips(config.processed_clips)
    else:
        generate_clips(config.pre_processed_videos, config.clips_duration, config.processed_clips)
        clips = load_clips(config.processed_clips)

    

    for _ in range(config.final_videos_beat_sync):
        random_audio = get_random_audio_file(config.audio_directory)
        final_video = synchronize_transitions_beat(clips, random_audio, config.audio_start_time, config.final_video_duration, config.minimum_clip_duration)
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{config.output_directory}/{filename}.mp4"
        final_video.write_videofile(filename, codec=config.codec, audio_codec=config.audio_codec, fps=config.fps, threads = config.threads)
    for _ in range(config.final_videos_offset_sync):
        random_audio = get_random_audio_file(config.audio_directory)
        final_video = synchronize_transitions_onset(clips, random_audio, config.audio_start_time, config.final_video_duration)
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{config.output_directory}/{filename}.mp4"
        final_video.write_videofile(filename, codec=config.codec, audio_codec=config.audio_codec, fps=config.fps, threads = config.threads)
if __name__ == "__main__":
    main()

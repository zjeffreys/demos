
import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
import librosa
from moviepy.video.fx.all import crop
from moviepy.audio.AudioClip import AudioArrayClip

def cut_video(clip, start_time, end_time):
    return clip.subclip(start_time, end_time)

def get_video_files(directory):
    return [f for f in os.listdir(directory) if f.endswith(('.mp4', '.avi', '.mkv', '.mov', '.MOV'))]

def resize_to_vertical(video_clip, target_width=1080, target_height=1920):
    # Resize the clip to the target width and height
    return video_clip.resize((target_width, target_height))

def check_video_format(video_clips):
    """
    Check the video formatting of a list of video clips.
    
    Args:
        video_clips (list): List of video clips (file paths).

    Returns:
        list: A list of tuples containing information about each video clip.
              Each tuple has the format (video_clip_path, is_valid, duration, dimensions).
    """
    video_info = []

    for video_path in video_clips:
        try:
            with VideoFileClip(video_path) as video_clip:
                duration = video_clip.duration
                dimensions = video_clip.size
                is_valid = True
        except Exception as e:
            duration = None
            dimensions = None
            is_valid = False

        video_info.append((video_path, is_valid, duration, dimensions))

    return video_info

def load_clips(directory):
    print("...loading clips [Testing Mode]")
    video_files = get_video_files(directory)
    loaded_clips = []

    # Load each video file as a VideoFileClip
    for video_file in video_files:
        clip_path = os.path.join(directory, video_file)
        clip = VideoFileClip(clip_path)
        print(f"clip duration: {clip.duration}")
        loaded_clips.append(clip)
    print(f"length loaded clips info:{len(loaded_clips)}")
    return loaded_clips
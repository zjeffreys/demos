import random
import os
import shutil
from video_editor.v0.utils.audio_utils import *
from video_editor.v0.utils.video_utils import * 
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
import librosa
import numpy as np

def synchronize_transitions_beat(video_clips, audio_path, start_time, final_duration, min_clip_duration):
    print("...synchronzing video to [BEAT]")
    audio, sr = librosa.load(audio_path, sr=None, offset=start_time, duration=final_duration)
    tempo, beats = librosa.beat.beat_track(y=audio, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)

    min_display_time = min_clip_duration  
    total_duration = 0
    selected_clips = []
    
    while total_duration < final_duration:
        random.shuffle(video_clips)  # Randomize the order of clips

        for i, clip in enumerate(video_clips):
            if total_duration >= final_duration:
                break

            # Align clip duration with the next beat, if possible
            if i < len(beat_times) - 1:
                clip_end_time = beat_times[i + 1] - total_duration
                clip_end_time = max(min_display_time, clip_end_time)
                clip = clip.subclip(0, min(clip.duration, clip_end_time))
            else:
                clip = clip.subclip(0, min(clip.duration, min_display_time))

            # Add the clip to the list, with crossfade if it's not the first clip
            if i > 0:
                selected_clips.append(selected_clips.pop().crossfadeout(0.2))
            selected_clips.append(clip)

            total_duration += clip.duration

    final_clip = concatenate_videoclips(selected_clips, method="compose")
    print(f"selected clips:{len(selected_clips)}")
    audio_clip = AudioFileClip(audio_path).subclip(start_time, start_time + final_duration)
    final_clip = final_clip.set_audio(audio_clip)
    final_clip = resize_to_vertical(final_clip)
    print(f"\nFinal video duration: {final_clip.duration} \nFinal video size: {final_clip.size}\n")
    return final_clip

def synchronize_transitions_onset(video_clips, audio_path, start_time, final_duration):
    print("...synchronzing video to [ONSET]")
    audio, sr = librosa.load(audio_path, sr=None, offset=start_time, duration=final_duration)
    onset_env = librosa.onset.onset_strength(y=audio, sr=sr)
    onset_env_normalized = onset_env / np.max(onset_env)
    transition_points = np.where(onset_env_normalized > 0.8)[0]
    transition_times = librosa.frames_to_time(transition_points, sr=sr)

    min_display_time = 0.5  # Minimum display time for each clip
    total_duration = 0
    selected_clips = []

    random.shuffle(video_clips)  # Randomize the order of clips

    for i, clip in enumerate(video_clips):
        if total_duration >= final_duration:
            break

        if i < len(transition_times) and total_duration < transition_times[i]:
            clip_end_time = transition_times[i] - total_duration
            clip_end_time = max(min_display_time, clip_end_time)
            clip = clip.subclip(0, min(clip.duration, clip_end_time))
        else:
            clip = clip.subclip(0, min(clip.duration, min_display_time))

        if i > 0:
            # Add a crossfade transition
            selected_clips.append(selected_clips.pop().crossfadeout(0.5))
        selected_clips.append(clip)

        total_duration += clip.duration

    print("Concatenating exciting video clips with dynamic transitions...")
    final_clip = concatenate_videoclips(selected_clips, method="compose")
    audio_clip = AudioFileClip(audio_path).subclip(start_time, start_time + total_duration)
    final_clip = final_clip.set_audio(audio_clip)

    print(f"Final video duration: {final_clip.duration}")
    return final_clip

def generate_clips(videos_directory, clips_duration, processed_clips_directory):
    print("Processing preprocessed videos into clips ...")

    # Directory where processed clips will be saved
    # processed_clips_directory = 'post_processed_clips'

    # Delete and recreate the directory
    if os.path.exists(processed_clips_directory):
        shutil.rmtree(processed_clips_directory)
    os.makedirs(processed_clips_directory)

    video_files = get_video_files(videos_directory)

    if not video_files:
        print("Error: No video files found.")
        return []

    video_clips = []

    for selected_video_file in video_files:
        print(f"Converting {selected_video_file} into a {clips_duration} second clip")
        video_path = os.path.join(videos_directory, selected_video_file)
        with VideoFileClip(video_path) as video_clip:
            clip_duration = min(clips_duration, video_clip.duration)
            start_time = max(0, video_clip.duration - clip_duration)
            end_time = start_time + clip_duration
            clip = video_clip.subclip(start_time, end_time)
            clip = resize_to_vertical(clip)

            # Remove audio from the clip
            clip = clip.without_audio()

            # Save the processed clip as an MP4
            processed_clip_filename = f'processed_{os.path.splitext(selected_video_file)[0]}.mp4'
            processed_clip_path = os.path.join(processed_clips_directory, processed_clip_filename)
            clip.write_videofile(processed_clip_path, codec='libx264')

            video_clips.append(clip)

    return video_clips




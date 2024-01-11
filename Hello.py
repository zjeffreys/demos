import streamlit as st
from video_editor import * 
from video_editor.v0.config import Config
from video_editor.v0.utils.audio_utils import *
from video_editor.v0.utils.video_utils import *
from datetime import datetime
import os

from video_editor.v0.video_editor import generate_clips, synchronize_transitions_beat, synchronize_transitions_onset

def main():
    st.title("Video Editor App")

    # Configurations
    config = Config()

    # Testing Mode Toggle
    testing_mode = st.checkbox("Enable Testing Mode", value=False)

    if testing_mode:
        clips = load_clips(config.processed_clips)
        process_and_display_videos(clips, config)
    else:
        # File Uploader
        uploaded_files = st.file_uploader("Upload Videos", accept_multiple_files=True, type=['mp4', 'mov'])

        if uploaded_files:
            # Limit the number of files
            if len(uploaded_files) < 5 or len(uploaded_files) > 20:
                st.warning("Please upload between 5 to 20 files.")
                return

            # Save files to a temporary directory
            temp_dir = "temp_uploaded_files"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            for uploaded_file in uploaded_files:
                bytes_data = uploaded_file.read()
                with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
                    f.write(bytes_data)

            # Generate Clips Button
            if st.button("Generate Clips"):
                generate_clips(temp_dir, config.clips_duration, config.processed_clips)
                clips = load_clips(config.processed_clips)
                process_and_display_videos(clips, config)

def process_and_display_videos(clips, config):
    # Sync Options
    sync_type = st.radio("Select Synchronization Type", ('Beat Sync', 'Offset Sync'))

    # Generate Final Video Button
    if st.button("Generate Final Video"):
        if sync_type == 'Beat Sync':
            random_audio = get_random_audio_file(config.audio_directory)
            final_video = synchronize_transitions_beat(clips, random_audio, config.audio_start_time, config.final_video_duration, config.minimum_clip_duration)
        else:
            random_audio = get_random_audio_file(config.audio_directory)
            final_video = synchronize_transitions_onset(clips, random_audio, config.audio_start_time, config.final_video_duration)

        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".mp4"
        file_path = os.path.join(config.output_directory, filename)

        # Ensure output directory exists
        if not os.path.exists(config.output_directory):
            os.makedirs(config.output_directory)

        final_video.write_videofile(file_path, codec=config.codec, audio_codec=config.audio_codec, fps=config.fps, threads=config.threads)
        st.video(file_path)

        # Provide download link
        with open(file_path, "rb") as file:
            st.download_button(label="Download Video", data=file, file_name=filename, mime="video/mp4")

if __name__ == "__main__":
    main()

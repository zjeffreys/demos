import streamlit as st
from video_editor import * 
from video_editor.v0.config import Config
from video_editor.v0.utils.audio_utils import *
from video_editor.v0.utils.video_utils import *
from datetime import datetime
import os
import time
from video_editor.v0.video_editor import generate_clips, synchronize_transitions_beat, synchronize_transitions_onset

def main():
    st.title("Video Editor App")

    # Configurations
    config = Config()

    # Initialize session state variables
    if 'show_process_button' not in st.session_state:
        st.session_state['show_process_button'] = True
    if 'clips_generated' not in st.session_state:
        st.session_state['clips_generated'] = False
    if 'processing_time' not in st.session_state:
        st.session_state['processing_time'] = 0
    if 'video_generation_time' not in st.session_state:
        st.session_state['video_generation_time'] = 0

    # File Uploader and Process Clips button
    if not st.session_state['clips_generated']:
        uploaded_files = st.file_uploader("Upload Videos", accept_multiple_files=True, type=['mp4', 'mov'], key="uploader")

        if uploaded_files and st.session_state['show_process_button']:
            if len(uploaded_files) < 5 or len(uploaded_files) > 20:
                st.warning("Please upload between 5 to 20 files.")
            else:
                st.info("Files uploaded successfully. Ready to process clips. (~20 seconds per video uploaded)")
                temp_dir = "temp_uploaded_files"
                if not os.path.exists(temp_dir):
                    os.makedirs(temp_dir)

                for uploaded_file in uploaded_files:
                    bytes_data = uploaded_file.read()
                    with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
                        f.write(bytes_data)

                if st.button("Process Clips"):
                    clip_start_time = time.time()
                    with st.spinner("Processing Clips..."):
                        generate_clips(temp_dir, config.clips_duration, config.processed_clips)
                    st.session_state['processing_time'] = time.time() - clip_start_time
                    st.session_state['clips_generated'] = True
                    st.session_state['show_process_button'] = False  # Hide the button

    # Sync with Beat button
    if st.session_state['clips_generated']:
        if st.button("Sync with Beat"):
            video_start_time = time.time()
            with st.spinner("Generating Short Video..."):
                clips = load_clips(config.processed_clips)
                random_audio = get_random_audio_file(config.audio_directory)
                final_video = synchronize_transitions_beat(clips, random_audio, config.audio_start_time, config.final_video_duration, config.minimum_clip_duration)
                save_and_display_video(final_video, config)
            st.session_state['video_generation_time'] = time.time() - video_start_time
            st.success(f"Short video generated in {st.session_state['video_generation_time']:.2f} seconds.")

    # Display the times
    if st.session_state['clips_generated']:
        st.info(f"Time taken to process clips: {st.session_state['processing_time']:.2f} seconds")
        if st.session_state['video_generation_time'] > 0:
            st.info(f"Time taken to generate video: {st.session_state['video_generation_time']:.2f} seconds")
        total_time = st.session_state['processing_time'] + st.session_state['video_generation_time']
        st.info(f"Total time: {total_time:.2f} seconds")

def save_and_display_video(final_video, config):
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".mp4"
    file_path = os.path.join(config.output_directory, filename)

    if not os.path.exists(config.output_directory):
        os.makedirs(config.output_directory)

    final_video.write_videofile(file_path, codec=config.codec, audio_codec=config.audio_codec, fps=config.fps, threads=config.threads)
    st.video(file_path)
    with open(file_path, "rb") as file:
        st.download_button(label="Download Video", data=file, file_name=filename, mime="video/mp4")

if __name__ == "__main__":
    main()

import streamlit as st
import yt_dlp
import os
import re

st.set_page_config(page_title="YouTube Video Downloader", layout="centered")

# Custom CSS Styling
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
            font-family: Arial, sans-serif;
        }
        .title {
            text-align: center;
            font-size: 3em;
            color: #FF0000;
            font-weight: bold;
        }
        .stButton>button {
            color: white;
            background-color: #FF4B4B;
            border-radius: 10px;
            padding: 10px 20px;
            border: none;
        }
        .stTextInput>div>input {
            border-radius: 10px;
            background-color: #333;
            color: white;
        }
        .stSelectbox>div>div {
            border-radius: 10px;
            background-color: #333;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'download_started' not in st.session_state:
    st.session_state.download_started = False

def is_valid_youtube_url(url):
    youtube_regex = re.compile(r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$')
    return bool(youtube_regex.match(url)) if url else False

def progress_hook(d):
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
        downloaded = d.get('downloaded_bytes', 0)
        if total > 0:
            progress = downloaded / total
            # Update the existing progress bar
            if 'progress_bar' in st.session_state:
                st.session_state['progress_bar'].progress(min(progress, 1.0))
        else:
            if 'progress_bar' in st.session_state:
                st.session_state['progress_bar'].progress(0)

def download_video(url):
    # Check if the video is already being downloaded
    if st.session_state.get('download_started', False):
        st.warning("Download already in progress or completed!")
        return

    # Mark download as started
    st.session_state['download_started'] = True

    # Create a single progress bar if it doesn't exist
    if 'progress_bar' not in st.session_state:
        st.session_state['progress_bar'] = st.progress(0)
    
    ydl_opts = {
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            filename = f"{info.get('title', 'Unknown')}.mp4"
            if os.path.exists(filename):
                st.warning(f"Video already downloaded: {filename}")
            else:
                st.write(f"Starting download: {filename}")
                ydl.download([url])
                st.success("Download completed!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            # Reset the download state after completion
            st.session_state['download_started'] = False
            # Clear the progress bar after completion
            if 'progress_bar' in st.session_state:
                del st.session_state['progress_bar']

def main():
    st.markdown('<div class="title">YouTube Video Downloader</div>', unsafe_allow_html=True)
    st.write("Paste your YouTube URL below to download the video.")

    url = st.text_input("Enter YouTube URL")

    # Initialize button state in session state
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False

    # Handle button click
    if st.button("Download"):
        st.session_state.button_clicked = True  # Set button state to clicked

    # If the button was clicked, start the download
    if st.session_state.button_clicked:
        if url and is_valid_youtube_url(url):
            download_video(url)
            st.session_state.button_clicked = False  # Reset button state after download
        elif url:
            st.warning("Please enter a valid YouTube URL.")
            st.session_state.button_clicked = False  # Reset button state if invalid URL

if __name__ == "__main__":
    main()
    st.write("Made with ❤️ by Harsh Prajapati")




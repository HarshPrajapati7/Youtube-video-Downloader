import streamlit as st
import yt_dlp
import os
import re
import base64

st.set_page_config(page_title="YouTube Video Downloader", layout="centered")

# ---------- Custom CSS for YouTube-style ----------
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
            color: #ff2c2c;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stTextInput>div>input {
            border-radius: 10px;
            background-color: #1e1e1e;
            color: white;
        }
        .stProgress > div > div > div > div {
            background-color: #e63946;
        }
        footer {
            text-align: center;
            padding-top: 20px;
            color: #ccc;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Validate YouTube URL ----------
def is_valid_youtube_url(url):
    youtube_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+'
    return re.match(youtube_regex, url) is not None

# ---------- Create Download Link ----------
def show_download_button(file_path, file_label="Download"):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_path}">{file_label}</a>'
        st.markdown(href, unsafe_allow_html=True)

# ---------- Download with yt_dlp ----------
def download_video(url):
    filename = None

    def hook(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total:
                percent = d['downloaded_bytes'] / total
                st.session_state.progress = percent

    ydl_opts = {
        'format': 'mp4',
        'outtmpl': '%(title)s.%(ext)s',
        'progress_hooks': [hook],
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        filename = f"{info['title']}.mp4"
        if os.path.exists(filename):
            st.warning(f"Video already exists: {filename}")
        else:
            ydl.download([url])
            st.success("Download complete!")
    return filename

# ---------- Main App ----------
def main():
    st.markdown('<div class="title">YouTube Video Downloader</div>', unsafe_allow_html=True)
    st.write("Paste a YouTube URL to download the video in MP4 format.")

    url = st.text_input("🎥 Enter YouTube URL")
    
    if "progress" not in st.session_state:
        st.session_state.progress = 0.0

    if url and is_valid_youtube_url(url):
        if st.button("⬇ Download Video"):
            try:
                progress_bar = st.progress(0)
                filename = download_video(url)

                # Update and show progress bar
                for _ in range(100):
                    progress_bar.progress(min(int(st.session_state.progress * 100), 100))

                if filename:
                    show_download_button(filename, "📥 Click here to download")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    elif url:
        st.warning("Please enter a valid YouTube URL.")

    st.markdown("<footer><hr>Made by <strong>Harsh Prajapati</strong></footer>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

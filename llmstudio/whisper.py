import streamlit as st
import openai
import os
from pytube import YouTube
from pydub import AudioSegment
import re

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to download YouTube video as audio and save both mp4 and mp3
def download_youtube(url, download_path):
    yt = YouTube(url)
    video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    mp4_file = os.path.join(download_path, yt.title + ".mp4")
    mp3_file = os.path.join(download_path, yt.title + ".mp3")
    
    # Overwrite existing files
    if os.path.exists(mp4_file):
        os.remove(mp4_file)
    if os.path.exists(mp3_file):
        os.remove(mp3_file)

    video_stream.download(output_path=download_path, filename=yt.title + ".mp4")
    # Convert mp4 to mp3 using pydub
    audio = AudioSegment.from_file(mp4_file, format="mp4")
    audio.export(mp3_file, format="mp3")
        
    return mp4_file, mp3_file, yt.title

# Function to transcribe audio using OpenAI's transcription service
def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcription = openai.Audio.transcribe(
            model="whisper-1", 
            file=audio_file, 
            response_format="verbose_json"
        )
        return process_transcription(transcription)

# Function to process the raw transcription into the desired format
def process_transcription(transcription):
    processed_lines = []
    for segment in transcription['segments']:
        start_time = format_time(segment['start'])
        text = segment['text']
        processed_line = f"[{start_time}] {text}"
        processed_lines.append(processed_line)
    return '\n'.join(processed_lines)

# Helper function to format time from seconds to "H:MM:SS"
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours}:{minutes:02}:{seconds:02}"

# Function to save transcript to file
def save_transcript(transcript, file_name, download_path):
    file_path = os.path.join(download_path, file_name)
    with open(file_path, 'w') as file:
        file.write(transcript)
    return file_path

# Function to get file metadata for both mp3 and txt files
def get_file_metadata(mp3_file_path, txt_file_path):
    # Get metadata for MP3 file
    audio = AudioSegment.from_mp3(mp3_file_path)
    mp3_file_size = os.path.getsize(mp3_file_path)
    audio_length = len(audio) / 1000.0  # Duration in seconds

    # Get metadata for TXT file
    txt_file_size = os.path.getsize(txt_file_path)
    with open(txt_file_path, 'r') as file:
        file_content = file.read()
    
    # Remove timestamps using regular expression
    cleaned_content = re.sub(r'\[\d{1,2}:\d{2}:\d{2}\]\s*', '', file_content)
    word_count = len(cleaned_content.split())
    
    return mp3_file_size, audio_length, txt_file_size, word_count

# Streamlit app
def main():
    st.title("YouTube Summary")

    col1, col2 = st.columns([5, 1])
    with col1:
        youtube_url = st.text_input("YouTube URL")
    with col2:
        download_path = st.text_input("Directory", "videos/")

    st.write("Whisper pricing: `$0.06` for 10 minutes, `$0.36` per hour")

    if st.button("Download and Transcribe"):
        if youtube_url:
            with st.spinner("Downloading files..."):
                try:
                    if not os.path.exists(download_path):
                        os.makedirs(download_path)
                    mp4_file, mp3_file, video_title = download_youtube(youtube_url, download_path)
                    st.success(f"Downloaded files:  \n{mp4_file}  \n{mp3_file}")
                except Exception as e:
                    st.error(f"Error downloading: {e}")
                    return

            with st.spinner("Transcribing audio..."):
                try:
                    transcript_data = transcribe_audio(mp3_file)
                    st.success("Transcription completed.")
                except Exception as e:
                    st.error(f"Error transcribing audio: {e}")
                    return

            formatted_transcript = transcript_data
            st.subheader("Transcript with Timestamps")
            st.text_area("Transcript", formatted_transcript, height=300)

            transcript_file_name = f"{video_title}.txt"
            transcript_file_path = save_transcript(formatted_transcript, transcript_file_name, download_path)
            st.success(f"Transcript saved to {transcript_file_path}")

            # Display file metadata
            mp3_file_size, audio_length, txt_file_size, word_count = get_file_metadata(mp3_file, transcript_file_path)
            st.write(f"**Audio file path**: {mp3_file}")
            st.write(f"**Audio file size**: {mp3_file_size / (1024 * 1024):.2f} MB")
            st.write(f"**Audio file length**: {audio_length / 60:.2f} minutes")
            st.write(f"**Transcript file path**: {transcript_file_path}")
            st.write(f"**Transcript file size**: {txt_file_size / 1024:.2f} KB")
            st.write(f"**Transcript word count**: {word_count:,} words")

if __name__ == "__main__":
    main()

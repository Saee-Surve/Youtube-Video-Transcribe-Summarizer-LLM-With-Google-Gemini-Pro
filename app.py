import streamlit as st

from dotenv import load_dotenv
load_dotenv() # Load all the environment variables

import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

prompt = """You are  Youtube video summarizer. YOU will be
 taking the transcripts texts and summarize the entire video
   and provding the entire summary in points within 250 words. 
   Provide the summary of the txt given here : """

## Getting the transcript data from Youtube videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        yt_api = YouTubeTranscriptApi()
        transcript_list = yt_api.fetch(video_id)

        transcript = ""
        for entry in transcript_list:
            transcript += " " + entry.text

        return transcript

    except Exception as e:
        raise e

## Getting the summary based on prompt from gemini
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-2.5-pro")
    response = model.generate_content(prompt+ transcript_text)
    return response.text

st.title("Youtube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter Youtube Video Link: ")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width = True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown('## Detailed Notes: ')
        st.write(summary)
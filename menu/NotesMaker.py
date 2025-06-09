from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

def main():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # Get available models
    models = genai.list_models()
    available_models = [model.name for model in models]
    
    # Define preferred models in order
    preferred_models = ["models/gemini-2.0-flash", "models/gemini-1.5-pro", "models/gemini-pro"]
    
    # Select the first available preferred model
    model_name = None
    for name in preferred_models:
        if name in available_models or (name.startswith("models/") and name[7:] in [m[7:] if m.startswith("models/") else m for m in available_models]):
            model_name = name
            break
    
    # Fallback to any available model if preferred models aren't available
    if not model_name and available_models:
        model_name = available_models[0]
    
    # Function to load gemini model and get responses
    model = genai.GenerativeModel(model_name)
    print(f"Using model: {model_name}")

    prompt = """
    I am Bard, your AI YouTube video summarizer!
    Give me the transcript text of any YouTube video, and I'll condense it into a concise summary within 250 words. Here's what you'll get:

    Key Points: I'll identify the main arguments, topics, or takeaways of the video.
    Bullet Points: Everything will be broken down into easy-to-read bullet points for quick understanding.
    Under 250 Words: I'll keep it short and sweet, saving you valuable time.
    Just paste the transcript text below, and let me work my magic! ✨
    """

    def extract_transcript_details(youtube_video_url):
        try:
            video_id = youtube_video_url.split("=")[1]
            transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = ""
            for i in transcript_text:
                transcript += " " + i["text"]
            return transcript
        except Exception as e:
            raise e

    def generate_gemini_content(transcript_text, prompt):
        response = model.generate_content(prompt + transcript_text)
        return response.text

    st.title("YouTube Videos to Detailed Notes Converter")
    youtube_link = st.text_input("Enter your video link")

    if youtube_link:
        video_id = youtube_link.split("=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

    if st.button("Get Detailed Notes"):
        transcript_text = extract_transcript_details(youtube_link)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("## Detailed Notes:")
            st.write(summary)

if __name__ == "__main__":
    main()

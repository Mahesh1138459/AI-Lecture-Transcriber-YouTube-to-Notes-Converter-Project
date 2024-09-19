import streamlit as st
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
import google.generativeai as genai
from youtube_transcript import extract_transcript

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_notes(transcript_text, subject):
    prompts = {
        "Physics": """
            Title: Detailed Physics Notes from YouTube Video Transcript
            As a physics expert, your task is to provide detailed notes based on the transcript of a YouTube video I'll provide. Assume the role of a student and generate comprehensive notes covering the key concepts discussed in the video.
            Your notes should:
            - Highlight fundamental principles, laws, and theories discussed in the video.
            - Explain any relevant experiments, demonstrations, or real-world applications.
            - Clarify any mathematical equations or formulas introduced and provide explanations for their significance.
            - Use diagrams, illustrations, or examples to enhance understanding where necessary.
        """,
        "Chemistry": """
            Title: Detailed Chemistry Notes from YouTube Video Transcript
            As a chemistry expert, your task is to provide detailed notes based on the transcript of a YouTube video I'll provide. Assume the role of a student and generate comprehensive notes covering the key concepts discussed in the video.
            Your notes should:
            - Break down chemical reactions, concepts, and properties explained in the video.
            - Include molecular structures, reaction mechanisms, and any applicable theories.
            - Discuss the significance of the discussed chemistry concepts in various contexts, such as industry, environment, or daily life.
            - Provide examples or case studies to illustrate the practical applications of the concepts discussed.
        """,
        "Mathematics": """
            Title: Detailed Mathematics Notes from YouTube Video Transcript
            As a mathematics expert, your task is to provide detailed notes based on the transcript of a YouTube video I'll provide. Assume the role of a student and generate comprehensive notes covering the key mathematical concepts discussed in the video.
            Your notes should:
            - Outline mathematical concepts, formulas, and problem-solving techniques covered in the video.
            - Provide step-by-step explanations for solving mathematical problems discussed.
            - Clarify any theoretical foundations or mathematical principles underlying the discussed topics.
            - Include relevant examples or practice problems to reinforce understanding.
        """,
        "Data Science and Statistics": """
            Title: Comprehensive Notes on Data Science and Statistics from YouTube Video Transcript
            As an expert in Data Science and Statistics, your task is to provide comprehensive notes based on the transcript of a YouTube video I'll provide. Assume the role of a student and generate detailed notes covering the key concepts discussed in the video.
            Your notes should:
            Data Science:
            - Explain fundamental concepts in data science such as data collection, data cleaning, data analysis, and data visualization.
            - Discuss different techniques and algorithms used in data analysis and machine learning, including supervised and unsupervised learning methods.
            - Provide insights into real-world applications of data science in various fields like business, healthcare, finance, etc.
            - Include discussions on data ethics, privacy concerns, and best practices in handling sensitive data.
            Statistics:
            - Outline basic statistical concepts such as measures of central tendency, variability, and probability distributions.
            - Explain hypothesis testing, confidence intervals, and regression analysis techniques.
            - Clarify the importance of statistical inference and its role in drawing conclusions from data.
            - Provide examples or case studies demonstrating the application of statistical methods in solving real-world problems.
        """
    }

    prompt = prompts.get(subject, "")
    full_prompt = prompt + transcript_text

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating notes: {e}")
        return None

def main():
    st.title("YouTube Transcript to Detailed Notes Converter")

    subject = st.selectbox("Select Subject:", ["Physics", "Chemistry", "Mathematics", "Data Science and Statistics"])
    language_code = st.selectbox("Select Transcript Language:", [
        "en",  # English
        "hi",  # Hindi
        "ta",  # Tamil
        "te",  # Telugu
        "bn",  # Bengali
        "mr",  # Marathi
        "gu",  # Gujarati
        "kn",  # Kannada
        "ml",  # Malayalam
        "pa",  # Punjabi
        "or",  # Odia
        "fr",  # French
        "es",  # Spanish
        "de",  # German
        "ja",  # Japanese
        "zh-Hans"  # Simplified Chinese
    ])  # Add more languages as needed
    youtube_link = st.text_input("Enter YouTube Video Link:")

    if youtube_link:
        video_id = youtube_link.split("=")[-1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

    if st.button("Get Detailed Notes"):
        transcript_text = extract_transcript(youtube_link, language_code)
        
        if transcript_text:
            st.success("Transcript extracted successfully!")
            detailed_notes = generate_notes(transcript_text, subject)
            if detailed_notes:
                st.markdown("## Detailed Notes:")
                st.write(detailed_notes)
            else:
                st.error("Failed to generate notes.")
        else:
            st.error("Failed to extract transcript.")

if __name__ == "__main__":
    main()

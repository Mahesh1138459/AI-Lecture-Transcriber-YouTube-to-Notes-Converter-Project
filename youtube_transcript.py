
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound


def extract_transcript(youtube_video_url, language_code):
    try:
        video_id = youtube_video_url.split("=")[-1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])

        transcript_text = " ".join([entry["text"] for entry in transcript])
        return transcript_text
    except NoTranscriptFound:
        st.error(f"No transcript found for the selected language: {language_code}.")
        return None
    except Exception as e:
        st.error(f"Error extracting transcript: {e}")
        return None
    

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import re


app = FastAPI()

ytt_api = YouTubeTranscriptApi()


class YouTubeRequest(BaseModel):
    youtube_url: str


@app.post("/ingest")
async def ingest_youtube_video(payload: YouTubeRequest):
    try:
        video_id = extract_video_id(payload.youtube_url)

        transcript = ytt_api.fetch(video_id,languages = ["en-In","hi"])

        text = " ".join(
            snippet.text for snippet in transcript.snippets
        )

        return {
            "video_id": transcript.video_id,
            "language": transcript.language,
            "is_generated": transcript.is_generated,
            "transcript_length": len(text),
            "message": "Transcript fetched successfully"
        }

    except TranscriptsDisabled:
        raise HTTPException(status_code=400, detail="Transcripts are disabled for this video")
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

def extract_video_id(url: str) -> str:
    """
    Extract video ID from various YouTube URL formats.
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    """
    import re
    
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'youtu\.be\/([0-9A-Za-z_-]{11})',
        r'embed\/([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    raise ValueError("Invalid YouTube URL")


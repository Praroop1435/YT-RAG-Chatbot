from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
import re

ytt_api = YouTubeTranscriptApi()


def extract_video_id(url: str) -> str:
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


def fetch_transcript(video_id: str):
    transcript = ytt_api.fetch(video_id, languages=["en-IN", "hi"])

    text = " ".join(
        snippet.text for snippet in transcript.snippets
    )

    return {
        "video_id": transcript.video_id,
        "language": transcript.language,
        "is_generated": transcript.is_generated,
        "text": text
    }
    


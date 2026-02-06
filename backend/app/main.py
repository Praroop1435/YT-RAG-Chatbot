# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from youtube_transcript_api import TranscriptsDisabled

from app.data_ingestion import extract_video_id, fetch_transcript

app = FastAPI()


class YouTubeRequest(BaseModel):
    youtube_url: str


@app.post("/ingest")
async def ingest_youtube_video(payload: YouTubeRequest):
    try:
        video_id = extract_video_id(payload.youtube_url)
        result = fetch_transcript(video_id)

        return {
            "video_id": result["video_id"],
            "language": result["language"],
            "is_generated": result["is_generated"],
            "transcript_length": len(result["text"]),
            "message": "Transcript fetched successfully"
        }

    except TranscriptsDisabled:
        raise HTTPException(
            status_code=400,
            detail="Transcripts are disabled for this video"
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Server error: {str(e)}"
        )

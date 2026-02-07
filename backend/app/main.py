from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from youtube_transcript_api import TranscriptsDisabled

from app.data_ingestion import extract_video_id, fetch_transcript, split_text
from app.retrieval import create_vector_store, create_retriever
from app.rag_chain import build_rag_chain

app = FastAPI(title="YouTube RAG Backend")

VECTOR_STORE = None


class YouTubeRequest(BaseModel):
    youtube_url: str


class QueryRequest(BaseModel):
    question: str


@app.post("/ingest")
async def ingest(payload: YouTubeRequest):
    global VECTOR_STORE

    try:
        video_id = extract_video_id(payload.youtube_url)
        text = fetch_transcript(video_id)
        chunks = split_text(text)

        VECTOR_STORE = create_vector_store(chunks)

        return {
            "video_id": video_id,
            "chunks": len(chunks),
            "message": "Video ingested and indexed successfully"
        }

    except TranscriptsDisabled:
        raise HTTPException(400, "Transcripts are disabled")

    except ValueError as e:
        raise HTTPException(400, str(e))

    except Exception as e:
        raise HTTPException(500, f"Server error: {e}")


@app.post("/query")
async def query(payload: QueryRequest):
    if VECTOR_STORE is None:
        raise HTTPException(400, "No video ingested yet")

    question = payload.question

    retriever = create_retriever(VECTOR_STORE)

    # 🔍 DEBUG STARTS HERE
    docs = retriever.invoke(question)

    print("---- RETRIEVED DOCS ----")
    for i, doc in enumerate(docs):
        print(f"[{i}] {doc.page_content[:300]}")
    # 🔍 DEBUG ENDS HERE

    rag_chain = build_rag_chain(retriever)
    answer = rag_chain.invoke(question)

    return {
        "question": question,
        "answer": answer
    }

🎥 YouTube Video Query Chatbot (RAG-Based)

This project implements a Retrieval-Augmented Generation (RAG) system that allows users to ask questions about a YouTube video using its link. The system understands the video’s content and returns accurate, context-aware answers grounded in the actual video transcript.

It also supports timestamp-specific queries and full video summarization.

🚀 What This System Does

Accepts a YouTube video URL

Extracts and processes the video transcript

Converts transcript chunks into vector embeddings

Retrieves only the most relevant segments for a user query

Generates grounded answers using an LLM (no hallucinated context)



✨ Key Features

Question Answering over YouTube Videos
Ask natural-language questions about the video content.

Timestamp-Aware Queries
Ask questions about a specific time range in the video for precise answers.

Full Video Summary
Generate a concise summary of the entire video.

RAG Architecture
Ensures responses are based on retrieved transcript chunks, not model guesses.

Scalable Design
Can be extended to support playlists, multi-video context, or document uploads.



🧠 How It Works (High Level)

Transcript Extraction
The video transcript is fetched from YouTube.

Chunking & Embedding
The transcript is split into semantic chunks and converted into embeddings.

Vector Retrieval
Relevant chunks are retrieved based on the user’s query (and optional timestamp).

LLM Generation
The retrieved context is passed to the language model to generate a grounded response.



🧩 Tech Stack

Python

RAG (Retrieval-Augmented Generation)

Vector Database (for similarity search)

LLM API

YouTube Transcript API

Streamlit / FastAPI for UI & backend separation



📌 Use Cases

Learning from long technical talks

Quickly extracting insights from podcasts

Studying lecture videos efficiently

Building AI-powered educational tools



🔒 Reliability Note

All responses are generated only from retrieved transcript data, minimizing hallucinations and ensuring factual alignment with the video.

📈 Future Enhancements

Playlist-level querying

Multi-video knowledge base

Highlighted timestamps in answers

PDF / notes export

User authentication and saved history

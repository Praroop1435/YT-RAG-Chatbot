import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/ingest"

st.set_page_config(page_title="YouTube Chat RAG", layout="centered")

st.title("🎥 YouTube Video Ingestion")

yt_link = st.text_input("Enter YouTube Video URL")

if st.button("Ingest Video"):
    if not yt_link:
        st.warning("Please enter a YouTube link")
    else:
        with st.spinner("Fetching transcript..."):
            response = requests.post(
                BACKEND_URL,
                json={"youtube_url": yt_link},
                timeout=30
            )

        if response.status_code == 200:
            st.success("Video ingested successfully")
            st.json(response.json())
        else:
            st.error("Failed to ingest video")
            st.json(response.json())

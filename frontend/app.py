import streamlit as st
import requests

BACKEND_BASE_URL = "http://localhost:8000"

INGEST_URL = f"{BACKEND_BASE_URL}/ingest"
QUERY_URL = f"{BACKEND_BASE_URL}/query"


def youtube_rag_frontend():
    st.set_page_config(
        page_title="YouTube RAG Chatbot",
        page_icon="🎥",
        layout="centered"
    )

    st.title("🎥 YouTube RAG Chatbot")
    st.caption("Ask questions directly from a YouTube video")

    st.divider()


    # Ingestion Section

    st.subheader("📥 Ingest YouTube Video")

    yt_url = st.text_input(
        "YouTube Video URL",
        placeholder="https://www.youtube.com/watch?v=VIDEO_ID"
    )

    ingest_btn = st.button("Ingest Video", use_container_width=True)

    if ingest_btn:
        if not yt_url:
            st.warning("Please enter a YouTube URL")
        else:
            with st.spinner("Fetching transcript and building index..."):
                try:
                    response = requests.post(
                        INGEST_URL,
                        json={"youtube_url": yt_url},
                        timeout=60
                    )

                    if response.status_code == 200:
                        st.success("Video ingested successfully")
                        st.session_state["ingested"] = True
                        st.session_state["ingest_data"] = response.json()
                    else:
                        st.error("Failed to ingest video")
                        st.json(response.json())

                except requests.exceptions.RequestException as e:
                    st.error(f"Backend not reachable: {e}")

    if "ingest_data" in st.session_state:
        with st.expander("📄 Ingestion Details"):
            st.json(st.session_state["ingest_data"])

    st.divider()


    # Query Section

    st.subheader("💬 Ask a Question")

    question = st.text_input(
        "Your question",
        placeholder="Can you summarize the video?"
    )

    ask_btn = st.button(
        "Ask Question",
        use_container_width=True,
        disabled=not st.session_state.get("ingested", False)
    )

    if ask_btn:
        if not question:
            st.warning("Please enter a question")
        else:
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        QUERY_URL,
                        json={"question": question},
                        timeout=60
                    )

                    if response.status_code == 200:
                        answer = response.json()["answer"]

                        st.markdown("### ✅ Answer")
                        st.write(answer)

                    else:
                        st.error("Failed to get answer")
                        st.json(response.json())

                except requests.exceptions.RequestException as e:
                    st.error(f"Backend not reachable: {e}")


if __name__ == "__main__":
    youtube_rag_frontend()

import streamlit as st
import requests

st.title("Streamlit Frontend")

res = requests.get("http://localhost:8000/health")
st.json(res.json())

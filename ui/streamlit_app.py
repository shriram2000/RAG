import requests
import streamlit as st

API_URL = st.sidebar.text_input("API URL", "http://api:8000")

st.title("Agentic RAG UI (LangGraph + Ollama)")

st.header("Ingest document")
upload = st.file_uploader("Upload document", type=["pdf", "docx", "pptx", "html", "md", "txt"])
if st.button("Ingest file", use_container_width=True):
    if upload is None:
        st.warning("Please choose a file first")
    else:
        files = {"file": (upload.name, upload.getvalue(), upload.type or "application/octet-stream")}
        resp = requests.post(f"{API_URL}/ingest", files=files, timeout=120)
        if resp.ok:
            st.success(resp.json())
        else:
            st.error(resp.text)

st.subheader("Ingest internet URL")
url_value = st.text_input("URL")
if st.button("Download + index URL", use_container_width=True):
    if not url_value.strip():
        st.warning("Enter a URL")
    else:
        resp = requests.post(f"{API_URL}/ingest/url", json={"url": url_value}, timeout=120)
        if resp.ok:
            st.success(resp.json())
        else:
            st.error(resp.text)

st.header("Ask a question")
question = st.text_area("Question", height=120)
if st.button("Ask", use_container_width=True):
    if question.strip():
        response = requests.post(f"{API_URL}/chat", json={"question": question}, timeout=120)
        if response.ok:
            body = response.json()
            st.markdown("### Answer")
            st.write(body["answer"])
            st.markdown("### Sources")
            st.write(body["sources"])
        else:
            st.error(response.text)
    else:
        st.warning("Please enter a question")

# Manages conversation logic.
import streamlit as st
import PyPDF2
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .config import client

# ---------------- PDF Helpers ---------------- #
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text, chunk_size=800, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def retrieve_chunks(query, chunks, top_k=3):
    vectorizer = TfidfVectorizer().fit(chunks + [query])
    query_vec = vectorizer.transform([query])
    chunk_vecs = vectorizer.transform(chunks)
    similarities = cosine_similarity(query_vec, chunk_vecs).flatten()
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    return [chunks[i] for i in top_indices]

# ---------------- Chat Handler ---------------- #
def handle_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user", avatar="🧑").markdown(msg["content"])  # emoji OR image
        else:
            st.chat_message("assistant", avatar="assets/Intelbot.ico").markdown(msg["content"])  # emoji OR image

    # Input box
    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)

        with st.spinner("Thinking..."):
            # If PDF uploaded, fetch context
            context = ""
            if "pdf_chunks" in st.session_state and st.session_state.pdf_chunks:
                relevant_chunks = retrieve_chunks(prompt, st.session_state.pdf_chunks)
                context = "\n\n".join(relevant_chunks)

            # Prepare final query
            user_query = prompt if not context else f"Context:\n{context}\n\nQuestion: {prompt}"

            response = client.chat_completion(
                messages=[{"role": "system", "content": "You are a helpful assistant."}] 
                         + st.session_state.messages 
                         + [{"role": "user", "content": user_query}]
            )
            reply = response.choices[0].message["content"]

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").markdown(reply)

# ----------------- Download chat ----------------- #
def export_chat(format="txt"):
    """Export chat history as TXT or PDF"""
    if "messages" not in st.session_state or not st.session_state.messages:
        st.warning("⚠️ No chat history to export.")
        return None

    if format == "txt":
        chat_text = ""
        for msg in st.session_state.messages:
            chat_text += f"{msg['role'].capitalize()}: {msg['content']}\n\n"
        return chat_text.encode("utf-8")

    elif format == "pdf":
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setFont("Helvetica", 12)

        y = 750
        for msg in st.session_state.messages:
            text = f"{msg['role'].capitalize()}: {msg['content']}"
            for line in text.split("\n"):
                pdf.drawString(50, y, line)
                y -= 20
                if y < 50:
                    pdf.showPage()
                    pdf.setFont("Helvetica", 12)
                    y = 750
        pdf.save()
        buffer.seek(0)
        return buffer.getvalue()
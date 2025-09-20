import streamlit as st
from .logic import handle_chat, export_chat

def load_css():
    """Apply custom CSS for sidebar only"""
    sidebar_css = """
    /* Sidebar container */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #6a11cb, #2575fc); /* purple → blue */
        color: #fff;
        padding: 2rem 1rem;
    }

    /* Sidebar title */
    .sidebar-title {
        font-size: 22px;
        font-weight: bold;
        text-align: center;
        color: #ecf0f1;
        margin-bottom: 20px;
    }

    /* Radio button group */
    .stRadio [role="radiogroup"] > label {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 16px;
        color: #ecf0f1;
        padding: 10px 14px;
        border-radius: 8px;
        cursor: pointer;
        transition: background 0.25s ease;
    }

    /* Hover effect */
    .stRadio [role="radiogroup"] > label:hover {
        background-color: rgba(236, 240, 241, 0.15);
    }

    /* Active (selected) item */
    .stRadio [role="radiogroup"] > label[data-checked="true"] {
        background-color: #ff4b91 !important; /* pink highlight */
        color: #fff !important;
        font-weight: bold;
    }
    """
    st.markdown(f"<style>{sidebar_css}</style>", unsafe_allow_html=True)


def render_app():
    st.set_page_config(page_title="IntelliBot", page_icon="assets/Intelbot.ico", layout="wide")
    load_css()

    # Sidebar navigation
    with st.sidebar:
        st.image("assets/Intelbot.png", width="stretch")
        st.markdown('<div class="sidebar-title"> IntelliBot Navigation</div>', unsafe_allow_html=True)
        page = st.radio("Navigation", ["🧠 Chatbot", "📚 About", "🤝 Contact"], key="nav_radio", label_visibility="collapsed")


    # ---------------- CHATBOT PAGE ---------------- #
    if "Chatbot" in page:
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Landing screen (only if no chat yet)
        if len(st.session_state.messages) == 0:
            st.markdown(
                """
                <div style="text-align: center; margin-top: 10%;">
                    <h1>✨ Welcome to IntelliBot</h1>
                    <p style="font-size:18px; color: #666;">Let’s chat — what’s on your mind?</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        handle_chat()

         # ----------------- DOWNLOAD SECTION ----------------- #
        # ----------------- Export + Upload Section ----------------- #
        # st.markdown("### ➕ Chat Tools")

        with st.expander("📥 Export Chat & 📤 Upload PDF"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button("💾 Save as TXT"):
                    txt_data = export_chat("txt")
                    if txt_data:
                        st.download_button("⬇️ Download TXT", txt_data, "chat_history.txt", "text/plain")

                if st.button("📄 Save as PDF"):
                    pdf_data = export_chat("pdf")
                    if pdf_data:
                        st.download_button("⬇️ Download PDF", pdf_data, "chat_history.pdf", "application/pdf")

            with col2:
                # ----------------- PDF UPLOAD SECTION ----------------- #
                uploaded_file = st.file_uploader("📂 Upload a PDF to chat with", type=["pdf"])

                if uploaded_file:
                    from .logic import read_pdf, chunk_text
                    pdf_text = read_pdf(uploaded_file)
                    pdf_chunks = chunk_text(pdf_text)
                    st.session_state.pdf_chunks = pdf_chunks
                    st.success(f"✅ PDF processed into {len(pdf_chunks)} chunks")


    # ---------------- ABOUT PAGE ---------------- #
    elif "About" in page:
        st.subheader("📖 About IntelliBot")

        st.write(
            """
            IntelliBot is a modern AI chatbot built to make conversations smarter, smoother,  
            and more accessible to everyone. It’s designed to act as a personal assistant,  
            knowledge companion, and productivity booster — all in one.  
            """
        )

        st.write("### ✨ Tech Stack")
        st.write(
            """
            - ⚡ **Streamlit** – for an interactive and clean frontend UI  
            - 🤗 **Hugging Face Inference API** – powering the backend with scalable AI  
            - 🦙 **Llama 3.1 8B Instruct** – state-of-the-art open-source AI model  
            """
        )

        st.write("### 🌟 Key Features")
        st.write(
            """
            - 💬 **Conversational AI** – engage in natural, human-like conversations  
            - 📚 **Knowledgeable** – answer queries from multiple domains  
            - 🎨 **Customizable UI** – easy to adapt for different projects  
            - 🌐 **Cloud Powered** – accessible from anywhere  
            """
        )

        st.write("### ⚙️ How It Works")
        st.write(
            """
            1. 🖥️ You interact with IntelliBot through a simple, intuitive UI  
            2. 📡 Your query is sent securely to Hugging Face API  
            3. 🧠 Llama 3.1 processes the query and generates a smart response  
            4. ✨ The response is displayed instantly in the chatbot window  
            """
        )

        st.write("### 🚀 Vision")
        st.write(
            """
            Our mission is to make **AI accessible, intelligent, and user-friendly**.  
            We believe in open-source technologies and aim to create an assistant  
            that can adapt to both **personal** and **enterprise** use cases.  
            """
        )

        st.markdown(
            "<footer style='text-align:center; color:#ff4b4b; margin-top:2rem;'>"
            "❤️ Made with Streamlit & Hugging Face"
            "</footer>",
            unsafe_allow_html=True,
        )


    # ---------------- CONTACT PAGE ---------------- #
    elif "Contact" in page:
        st.subheader("📬 Contact Us")

        st.write(
            """
            Got questions, feedback, or ideas?  
            We’d love to hear from you! 💡  
            """
        )

        st.write("### 👨‍💻 Developer")
        st.write(
            """
            - **Name:** Debasis Sahoo  
            - 📧 **Email:** [debasissahoo61@gmail.com](mailto:debasissahoo61@gmail.com)  
            - 💻 **GitHub:** [yourusername](https://github.com/)  
            """
        )

        st.write("### 🌐 Connect with Us")
        st.write(
            """
            - 🐦 **Twitter/X:** [@yourhandle](https://twitter.com/)  
            - 💼 **LinkedIn:** [Your LinkedIn](https://linkedin.com/)  
            - 🌟 **Project Repo:** [GitHub Project Link](https://github.com/)  
            """
        )

        st.write("### 🛠️ Support & Feedback")
        st.write(
            """
            - 📝 Report issues or bugs via [GitHub Issues](https://github.com/)  
            - 💡 Share feature requests and ideas  
            - 🙌 Contributions are always welcome!  
            """
        )

        st.markdown(
            "<footer style='text-align:center; color:#ff4b4b; margin-top:2rem;'>"
            "❤️ Made with Streamlit & Hugging Face"
            "</footer>",
            unsafe_allow_html=True,
        )


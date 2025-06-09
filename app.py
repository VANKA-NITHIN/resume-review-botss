from openai import OpenAI
import fitz  # PyMuPDF
import streamlit as st
import os

client = OpenAI()

st.set_page_config(page_title="AI Resume Review Bot", page_icon="📄")
st.title("📄 Resume Review Bot")
st.write("Upload your resume (PDF) and get GPT-4-powered feedback for tech and AI jobs.")

uploaded_file = st.file_uploader("Upload Resume (PDF Only)", type=["pdf"])

if uploaded_file:
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            text = "\n".join([page.get_text() for page in doc])

        with st.spinner("Analyzing your resume with GPT-4..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional resume reviewer for AI and tech jobs."},
                    {"role": "user", "content": f"Please review this resume and provide constructive feedback:\n\n{text}"}
                ]
            )
            result = response.choices[0].message.content

        st.subheader("✅ Resume Feedback")
        st.write(result)

    except Exception as e:
        st.error(f"Something went wrong: {e}")

st.markdown("---")
st.markdown("Made with ❤️ using GPT-4 + Streamlit")

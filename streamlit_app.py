import streamlit as st
import openai
import PyPDF2

# Set your OpenAI API key securely via Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Configure the Streamlit page
st.set_page_config(page_title="DocSummon AI", layout="centered")
st.title("📄 DocSummon AI")
st.write("Upload a PDF and get a smart summary.")

# File upload widget
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file is not None:
    # Extract text from PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    full_text = ""
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            full_text += extracted

    st.subheader("📜 Raw Document Text")
    st.text_area("Extracted Text", full_text, height=300)

    # Use OpenAI to summarize
    with st.spinner("Summarizing with GPT..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful legal document assistant."},
                    {"role": "user", "content": f"Summarize this document:\n\n{full_text}"}
                ]
            )
            summary = response["choices"][0]["message"]["content"]
            st.subheader("🧠 GPT Summary")
            st.write(summary)

        except Exception as e:
            st.error(f"An error occurred while calling OpenAI: {e}")


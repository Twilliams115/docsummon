import streamlit as st
import openai
import PyPDF2

# Set API key
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="DocSummon AI", layout="centered")
st.title("📄 DocSummon AI")
st.write("Upload a PDF and get a smart summary.")

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file is not None:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    full_text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            full_text += page.extract_text()

    st.subheader("📜 Raw Document Text")
    st.text_area("Extracted Text", full_text, height=300)

    with st.spinner("Summarizing with GPT..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful legal document assistant."},
                    {"role": "user", "content": f"Summarize this document:\n\n{full_text}"}
                ]
            )
            summary = response.choices[0].message.content
            st.subheader("🧠 GPT Summary")
            st.write(summary)
        except Exception as e:
            st.error(f"An error occurred while calling OpenAI:\n\n{e}")
            
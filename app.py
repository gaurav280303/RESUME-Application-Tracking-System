import os
import PyPDF2 as pdf
import streamlit as st
import google.generativeai as genai

# --------------------------------------------------
# Get API key from Streamlit Cloud Secrets
# --------------------------------------------------
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("API key not found. Please add GOOGLE_API_KEY in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=API_KEY)

# Use correct model
model = genai.GenerativeModel("models/gemini-pro")

# --------------------------------------------------
# UI
# --------------------------------------------------
st.set_page_config(page_title="Smart ATS", page_icon="🤖")
st.title("Smart Application Tracking System")
st.write("AI-powered Resume ATS Analyzer")

jd = st.text_area("Paste Job Description", height=200)
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

# --------------------------------------------------
# Prompt
# --------------------------------------------------
prompt_template = """
You are an Applicant Tracking System (ATS).

Analyze the resume against the job description and respond ONLY in this format:

Job Description Match: <percentage>%
Missing Keywords: <comma separated keywords>
Profile Summary: <short summary>

Resume:
{resume}

Job Description:
{jd}
"""

# --------------------------------------------------
# Button Logic
# --------------------------------------------------
if st.button("Analyze Resume"):
    if not jd.strip():
        st.warning("Please paste a job description.")
    elif uploaded_file is None:
        st.warning("Please upload a resume PDF.")
    else:
        reader = pdf.PdfReader(uploaded_file)
        resume_text = ""

        for page in reader.pages:
            resume_text += page.extract_text()

        resume_text = resume_text[:4000]  # token safety

        final_prompt = prompt_template.format(
            resume=resume_text,
            jd=jd
        )

        with st.spinner("Analyzing resume..."):
            try:
                response = model.generate_content(final_prompt)
                st.success("Analysis completed")
                st.write(response.text)
            except Exception as e:
                st.error(f"Gemini API error: {e}")


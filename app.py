import os
import PyPDF2 as pdf
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# ---------------------------------------------------
# Load environment variables
# ---------------------------------------------------
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("GOOGLE_API_KEY not found. Please add it in .env file.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

# ---------------------------------------------------
# Streamlit UI setup
# ---------------------------------------------------
st.set_page_config(page_title="Smart ATS", page_icon="🤖")

st.title("SMART APPLICATION TRACKING SYSTEM")
st.write("Improve your Resume ATS score using AI")

jd = st.text_area("📄 Paste Job Description", height=200)
uploaded_file = st.file_uploader(
    "📎 Upload Resume (PDF only)",
    type="pdf",
    help="Upload your resume in PDF format"
)

submit = st.button("Analyze Resume")

# ---------------------------------------------------
# Prompt Template
# ---------------------------------------------------
input_prompt = """
You are an experienced ATS (Applicant Tracking System).
Analyze the resume against the given job description.

Resume:
{resume_text}

Job Description:
{job_description}

Return the response in exactly this format:

Job Description Match: <percentage>%
Missing Keywords: <comma separated keywords>
Profile Summary: <short professional summary>
"""

# ---------------------------------------------------
# Button logic
# ---------------------------------------------------
if submit:
    if uploaded_file is None:
        st.warning("Please upload a resume PDF.")
    elif jd.strip() == "":
        st.warning("Please paste a job description.")
    else:
        # Extract text from PDF
        reader = pdf.PdfReader(uploaded_file)
        resume_text = ""

        for page in reader.pages:
            resume_text += page.extract_text()

        # Limit text length to avoid token issues
        resume_text = resume_text[:4000]

        # Fill prompt correctly ✅ (THIS WAS YOUR MAIN BUG)
        final_prompt = input_prompt.format(
            resume_text=resume_text,
            job_description=jd
        )

        # Call Gemini
        with st.spinner("Analyzing resume with AI..."):
            try:
                response = model.generate_content(final_prompt)
                st.success("Analysis Complete ✅")
                st.write(response.text)
            except Exception as e:
                st.error(f"Something went wrong: {e}")

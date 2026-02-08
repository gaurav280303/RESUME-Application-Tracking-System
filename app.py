import os
import streamlit as st
import PyPDF2 as pdf
from google import genai

# -------------------------------------------------
# API KEY (Streamlit Cloud → Secrets)
# -------------------------------------------------
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("GOOGLE_API_KEY not found. Add it in Streamlit Cloud → Secrets.")
    st.stop()

# Create Gemini client (NEW SDK)
client = genai.Client(api_key=API_KEY)

# -------------------------------------------------
# STREAMLIT UI
# -------------------------------------------------
st.set_page_config(page_title="Smart ATS", page_icon="🤖")

st.title("Smart Application Tracking System")
st.write("AI-powered Resume ATS Analyzer")

job_description = st.text_area("📄 Paste Job Description", height=200)
uploaded_file = st.file_uploader("📎 Upload Resume (PDF)", type="pdf")

# -------------------------------------------------
# PROMPT TEMPLATE
# -------------------------------------------------
prompt_template = """
You are an Applicant Tracking System (ATS).

Analyze the resume against the job description and respond ONLY in this format:

Job Description Match: <percentage>%
Missing Keywords: <comma separated keywords>
Profile Summary: <short professional summary>

Resume:
{resume}

Job Description:
{jd}
"""

# -------------------------------------------------
# BUTTON ACTION
# -------------------------------------------------
if st.button("Analyze Resume"):
    if not uploaded_file:
        st.warning("Please upload a resume PDF.")
    elif not job_description.strip():
        st.warning("Please paste a job description.")
    else:
        try:
            reader = pdf.PdfReader(uploaded_file)
            resume_text = ""

            for page in reader.pages:
                resume_text += page.extract_text() or ""

            resume_text = resume_text[:4000]  # token safety

            final_prompt = prompt_template.format(
                resume=resume_text,
                jd=job_description
            )

            with st.spinner("Analyzing resume with Gemini..."):
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=final_prompt
                )

            st.success("Analysis Complete ✅")
            st.write(response.text)

        except Exception as e:
            st.error(f"Gemini API Error: {e}")

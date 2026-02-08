import os
import streamlit as st
import PyPDF2 as pdf
import google.generativeai as genai

# -------------------------------------------------
# CONFIG: API KEY (Streamlit Cloud Secrets)
# -------------------------------------------------
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("GOOGLE_API_KEY not found. Add it in Streamlit Cloud → Secrets.")
    st.stop()

genai.configure(api_key=API_KEY)

# ✅ UPDATED & SUPPORTED MODEL
model = genai.GenerativeModel("gemini-1.5-flash")

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
You are an advanced Applicant Tracking System (ATS).

Analyze the resume against the job description and return the result
STRICTLY in the following format:

Job Description Match: <percentage>%
Missing Keywords: <comma separated keywords>
Profile Summary: <short professional summary>

Resume:
{resume_text}

Job Description:
{job_description}
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
            # Extract text from PDF
            reader = pdf.PdfReader(uploaded_file)
            resume_text = ""

            for page in reader.pages:
                resume_text += page.extract_text() or ""

            # Token safety
            resume_text = resume_text[:4000]

            # Fill prompt correctly
            final_prompt = prompt_template.format(
                resume_text=resume_text,
                job_description=job_description
            )

            # Call Gemini
            with st.spinner("Analyzing resume with AI..."):
                response = model.generate_content(final_prompt)

            st.success("Analysis Complete ✅")
            st.write(response.text)

        except Exception as e:
            st.error(f"Gemini API Error: {e}")

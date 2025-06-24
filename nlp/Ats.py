import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to call Gemini with input
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Prompt Template
input_prompt = """
Hey Act Like a skilled or very experienced ATS (Applicant Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst,
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based 
on JD and the missing keywords with high accuracy.

resume: {text}
description: {jd}

I want the response in one single string having the structure:
{{"JD Match":"%","MissingKeywords":[],"Profile Summary":""}}
"""

# Streamlit app
st.title("🧠 Smart ATS Resume Evaluator")
st.text("Analyze and Improve Your Resume for Better ATS Match")

jd = st.text_area("📄 Paste the Job Description Here", height=200)
uploaded_file = st.file_uploader("📎 Upload Your Resume (PDF)", type="pdf", help="Upload a PDF version of your resume.")

submit = st.button("🚀 Submit")

if submit:
    if uploaded_file is not None and jd.strip():
        with st.spinner("Analyzing Resume..."):
            resume_text = input_pdf_text(uploaded_file)
            filled_prompt = input_prompt.format(text=resume_text, jd=jd)
            response_text = get_gemini_response(filled_prompt)
            
            st.subheader("📝 Evaluation Result")
            try:
                response_json = json.loads(response_text)
                st.json(response_json)
            except:
                st.text(response_text)
    else:
        st.warning("⚠️ Please upload a resume and paste the job description before submitting.")

import streamlit as st
import google.generativeai as genai  # Replace with appropriate library if needed
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv()  # Load environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Configure API key

# Function for obtaining Gemini's response (replace with correct method)
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    # Determine the correct method for text generation from your library
    # Check documentation for available methods (e.g., 'generate', 'sample', or others)
    response = model.generate_content(input)  # Replace with the appropriate method
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:  # Access pages directly
        text += page.extract_text()  # Extract text from each page
    return text

# Prompt template
input_prompt = """
I am an ATS (Applicant Tracking System) with expertise in evaluating resumes for tech roles like software engineering, data science, data analysis, and big data engineering. 

**Given a job description (JD) and a resume, I can analyze the resume's fit for the job and provide insights to improve it.** 

Here's the job description:
{jd}

Here's the resume text:
{text}

**Please analyze the resume based on the following criteria:**

* **Keyword Matching:** Identify how well the resume keywords match the skills and experience mentioned in the job description.
* **Skills and Experience:** Analyze if the resume highlights the relevant skills and experiences required for the job.
* **Quantifiable Achievements:** Assess if the resume showcases achievements using metrics and data whenever possible.
* **Action Verbs:** Check if the resume uses strong action verbs to describe accomplishments.
* **Overall Clarity and Conciseness:** Evaluate if the resume is clear, concise, and easy to read for an ATS.

**Based on this analysis, I will provide a JD Match percentage and identify any missing keywords that would further improve the resume's chances of getting shortlisted.**

**Additionally, I can offer suggestions for improvement in the following areas:**

* **Tailoring the resume to the specific job description.**
* **Formatting and layout to enhance readability for an ATS.**
* **Highlighting relevant skills and experiences more effectively.**

**I want the response in one single string having the structure:**

{{"JD Match":"%","MissingKeywords":[],"Profile Summary":""}}
"""

## Streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type='pdf', help="Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))
        st.subheader(response)

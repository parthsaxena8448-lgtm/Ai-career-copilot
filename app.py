import json
import streamlit as st
import fitz
import docx
import google.generativeai as genai
from fpdf import FPDF

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(
    page_title="AI Career Copilot",
    page_icon="🚀",
    layout="wide"
)

# Initialize user info in session state
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# ---------- Welcome Screen ----------
if st.session_state.user_name == "":
    st.markdown("""
<style>
.stApp {
background: linear-gradient(135deg, #0E1117 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #0E1117 100%);
background-size: 400% 400%;
animation: gradientShift 15s ease infinite;
}
@keyframes gradientShift {
0% { background-position: 0% 50%; }
50% { background-position: 100% 50%; }
100% { background-position: 0% 50%; }
}
.particle {
position: fixed;
bottom: -100px;
border-radius: 50%;
opacity: 0.4;
animation: float 15s infinite ease-in;
z-index: 0;
}
@keyframes float {
0% { transform: translateY(0) rotate(0deg); opacity: 0; }
10% { opacity: 0.4; }
100% { transform: translateY(-110vh) rotate(360deg); opacity: 0; }
}
.p1 { width: 60px; height: 60px; left: 10%; background: #6C63FF; animation-duration: 12s; }
.p2 { width: 30px; height: 30px; left: 25%; background: #00D9FF; animation-duration: 18s; animation-delay: 2s; }
.p3 { width: 80px; height: 80px; left: 40%; background: #10B981; animation-duration: 15s; animation-delay: 4s; }
.p4 { width: 40px; height: 40px; left: 60%; background: #F59E0B; animation-duration: 20s; animation-delay: 1s; }
.p5 { width: 50px; height: 50px; left: 75%; background: #6C63FF; animation-duration: 14s; animation-delay: 3s; }
.p6 { width: 35px; height: 35px; left: 90%; background: #00D9FF; animation-duration: 17s; animation-delay: 5s; }
/* Card styling */
.custom-card {
background: rgba(30, 33, 48, 0.6);
backdrop-filter: blur(10px);
border: 1px solid rgba(255, 255, 255, 0.1);
border-radius: 16px;
padding: 24px;
margin-bottom: 16px;
transition: transform 0.2s ease, border-color 0.2s ease;
}
.custom-card:hover {
transform: translateY(-2px);
border-color: rgba(108, 99, 255, 0.5);           
}
</style>

<div class="particle p1"></div>
<div class="particle p2"></div>
<div class="particle p3"></div>
<div class="particle p4"></div>
<div class="particle p5"></div>
<div class="particle p6"></div>
""", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("# 🚀 AI Career Copilot")
        st.markdown("##### Your all-in-one AI resume and interview prep assistant")
        st.write("")
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.write("Let's get to know you before we begin.")
        
        with st.form("welcome_form"):

            name_input = st.text_input("Your Name")
            email_input = st.text_input("Your Email")
            submitted = st.form_submit_button("Get Started →")

            if submitted:
                if name_input.strip() and email_input.strip():
                    st.session_state.user_name = name_input
                    st.session_state.user_email = email_input
                    st.rerun()
                else:
                    st.warning("Please fill in both fields.")

    
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

 
st.markdown(f"# 🚀 AI Career Copilot")
st.markdown(f"##### Welcome back, {st.session_state.user_name}! Let's optimize your career.")
st.divider()

# Load skills list once
with open("skills.json", "r") as f:
    skills_data = json.load(f)

all_skills = []
for category_list in skills_data.values():
    all_skills.extend(category_list)

# ---------- Resume Upload (always visible at top) ----------
uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

text = ""
if uploaded_file is not None:
    uploaded_file.seek(0)
    if uploaded_file.name.endswith(".pdf"):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"

# ---------- Tabs ----------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Resume & Job Match",
    "AI Suggestions",
    "Interview Questions",
    "Mock Interview",
    "Download Report"
])

# ---------- TAB 1: Resume & Job Match ----------
with tab1:
    if uploaded_file is not None:
        st.subheader("Extracted Resume Text")
        st.text_area("Resume Content", text, height=250)

        st.subheader("Paste Job Description")
        job_description = st.text_area("Job Description", height=200, key="jd_input")

        if job_description:
            resume_skills_found = [s for s in all_skills if s.lower() in text.lower()]
            jd_skills_found = [s for s in all_skills if s.lower() in job_description.lower()]
            missing_skills = [s for s in jd_skills_found if s not in resume_skills_found]

            if len(jd_skills_found) > 0:
                matched_count = len(set(resume_skills_found) & set(jd_skills_found))
                ats_score = (matched_count / len(jd_skills_found)) * 100
            else:
                ats_score = 0

            st.session_state.job_description = job_description
            st.session_state.ats_score = ats_score
            st.session_state.resume_skills_found = resume_skills_found
            st.session_state.jd_skills_found = jd_skills_found
            st.session_state.missing_skills = missing_skills
            st.session_state.resume_text = text

            st.subheader("📊 Results")
            st.metric("ATS Score", f"{ats_score:.1f}%")
            st.progress(int(ats_score) if ats_score <= 100 else 100)

            if ats_score >= 80:
                st.success("Excellent match! Your resume aligns very well with this job.")
            elif ats_score >= 50:
                st.warning("Decent match, but there's room to improve.")
            else:
                st.error("Low match — consider revising your resume for this role.")
            st.write("**Skills found in your resume:**")
            st.write(resume_skills_found)
            st.write("**Skills required by job description:**")
            st.write(jd_skills_found)
            st.write("**Missing skills:**")
            st.write(missing_skills)
    else:
        st.info("Upload your resume above to get started.")

# ---------- TAB 2: AI Suggestions + Bullet Rewriter ----------
with tab2:
    if "job_description" in st.session_state:
        st.subheader("💡 AI-Powered Resume Suggestions")
        if st.button("Generate Suggestions"):
            with st.spinner("Asking Gemini for suggestions..."):
                model = genai.GenerativeModel("gemini-flash-latest")
                prompt = f"""
                You are a professional resume coach. Here is a candidate's resume:
                {st.session_state.resume_text}

                Here is the job description they are applying for:
                {st.session_state.job_description}

                The candidate is missing these skills: {st.session_state.missing_skills}

                Give 5 specific, actionable suggestions to improve this resume
                for this job. Focus on how they can better present their
                existing experience, and how to address the missing skills.
                """
                response = model.generate_content(prompt)
                st.write(response.text)
                st.session_state.ai_suggestions = response.text

        st.divider()
        st.subheader("Resume Bullet Point Rewriter")
        weak_bullet = st.text_area("Paste a resume bullet point you want to improve")

        if st.button("Rewrite This Bullet Point"):
            if weak_bullet:
                with st.spinner("Rewriting..."):
                    rewrite_model = genai.GenerativeModel("gemini-flash-latest")
                    rewrite_prompt = f"""
                    You are a professional resume writer. Rewrite the following
                    resume bullet point to be more impactful, specific, and
                    tailored to this job description.

                    Original bullet point: {weak_bullet}
                    Job description: {st.session_state.job_description}

                    Rules:
                    - Keep it to one sentence
                    - Start with a strong action verb
                    - Include a measurable result or impact if possible
                    - Match keywords from the job description naturally

                    Give only the rewritten bullet point, nothing else.
                    """
                    rewrite_response = rewrite_model.generate_content(rewrite_prompt)
                    st.write("**Improved version:**")
                    st.write(rewrite_response.text)
            else:
                st.warning("Please paste a bullet point first.")
    else:
        st.info("Complete the Resume & Job Match tab first.")

# ---------- TAB 3: Interview Questions ----------
with tab3:
    if "job_description" in st.session_state:
        st.subheader("❓ Interview Question Generator")
        if st.button("Generate Interview Questions"):
            with st.spinner("Generating interview questions..."):
                interview_model = genai.GenerativeModel("gemini-flash-latest")
                interview_prompt = f"""
                You are an experienced technical interviewer. Based on this
                candidate's resume and the job description below, generate
                interview questions they should prepare for.

                Resume: {st.session_state.resume_text}
                Job description: {st.session_state.job_description}

                Generate exactly:
                - 5 technical questions
                - 3 HR/behavioral questions
                - 2 project-specific questions

                Format your response with clear headers for each category,
                and number each question.
                """
                interview_response = interview_model.generate_content(interview_prompt)
                st.write(interview_response.text)
                st.session_state.interview_questions = interview_response.text
    else:
        st.info("Complete the Resume & Job Match tab first.")

# ---------- TAB 4: Mock Interview ----------
with tab4:
    if "job_description" in st.session_state:
        st.subheader("🎤 AI Mock Interview")

        if "interview_history" not in st.session_state:
            st.session_state.interview_history = []

        if st.button("Start Mock Interview"):
            st.session_state.interview_history = []
            mock_model = genai.GenerativeModel("gemini-flash-latest")
            first_question_prompt = f"""
            You are a friendly but professional interviewer. Based on this
            resume and job description, ask the candidate ONE opening
            interview question. Just the question, nothing else.

            Resume: {st.session_state.resume_text}
            Job description: {st.session_state.job_description}
            """
            first_question = mock_model.generate_content(first_question_prompt).text
            st.session_state.interview_history.append({"role": "interviewer", "text": first_question})

        for message in st.session_state.interview_history:
            if message["role"] == "interviewer":
                st.write(f"**Interviewer:** {message['text']}")
            else:
                st.write(f"**You:** {message['text']}")

        if len(st.session_state.interview_history) > 0:
            user_answer = st.text_input("Your answer", key="answer_input")

            if st.button("Submit Answer"):
                if user_answer:
                    st.session_state.interview_history.append({"role": "candidate", "text": user_answer})
                    mock_model = genai.GenerativeModel("gemini-flash-latest")

                    conversation_so_far = ""
                    for msg in st.session_state.interview_history:
                        conversation_so_far += f"{msg['role']}: {msg['text']}\n"

                    next_question_prompt = f"""
                    You are conducting a mock interview. Here is the conversation
                    so far: {conversation_so_far}

                    Give brief feedback (1 sentence) on their last answer, then
                    ask ONE new, relevant follow-up interview question based on
                    the resume and job description below.

                    Resume: {st.session_state.resume_text}
                    Job description: {st.session_state.job_description}
                    """
                    next_response = mock_model.generate_content(next_question_prompt).text
                    st.session_state.interview_history.append({"role": "interviewer", "text": next_response})
                    st.rerun()
    else:
        st.info("Complete the Resume & Job Match tab first.")

# ---------- TAB 5: Download Report ----------
with tab5:
    if "job_description" in st.session_state:
        st.subheader("📥 Download Your Report")

        if st.button("Generate PDF Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 16)
            pdf.cell(0, 10, "AI Career Copilot - Resume Report", ln=True)

            pdf.set_font("Helvetica", "", 12)
            pdf.ln(5)
            pdf.multi_cell(0, 8, f"ATS Score: {st.session_state.ats_score:.1f}%")

            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 13)
            pdf.cell(0, 10, "Matched Skills", ln=True)
            pdf.set_font("Helvetica", "", 12)
            pdf.multi_cell(0, 8, ", ".join(st.session_state.resume_skills_found))

            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 13)
            pdf.cell(0, 10, "Missing Skills", ln=True)
            pdf.set_font("Helvetica", "", 12)
            pdf.multi_cell(0, 8, ", ".join(st.session_state.missing_skills) if st.session_state.missing_skills else "None")

            if "ai_suggestions" in st.session_state:
                pdf.ln(3)
                pdf.set_font("Helvetica", "B", 13)
                pdf.cell(0, 10, "AI Suggestions", ln=True)
                pdf.set_font("Helvetica", "", 12)
                clean_text = st.session_state.ai_suggestions.encode("latin-1", "replace").decode("latin-1")
                pdf.multi_cell(0, 8, clean_text)

            if "interview_questions" in st.session_state:
                pdf.ln(3)
                pdf.set_font("Helvetica", "B", 13)
                pdf.cell(0, 10, "Interview Questions", ln=True)
                pdf.set_font("Helvetica", "", 12)
                clean_text = st.session_state.interview_questions.encode("latin-1", "replace").decode("latin-1")
                pdf.multi_cell(0, 8, clean_text)

            pdf_output = pdf.output(dest="S")
            if isinstance(pdf_output, str):
                pdf_bytes = pdf_output.encode("latin-1")
            else:
                pdf_bytes = bytes(pdf_output)

            st.download_button(
                label="Download Report",
                data=pdf_bytes,
                file_name="resume_report.pdf",
                mime="application/pdf"
            )
    else:
        st.info("Complete the Resume & Job Match tab first.")
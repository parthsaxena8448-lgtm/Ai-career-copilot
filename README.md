# 🚀 AI Career Copilot

An AI-powered resume analyzer and interview preparation assistant built with Streamlit and Google's Gemini API. Upload your resume, paste a job description, and get instant ATS scoring, skill gap analysis, AI-generated improvement suggestions, interview questions, and a full mock interview experience.

## ✨ Features

- **Resume Parsing** — Upload PDF or DOCX resumes and extract text automatically
- **ATS Score Calculator** — See how well your resume matches a job description
- **Skill Gap Analysis** — Identifies matched and missing skills between your resume and the job posting
- **AI-Powered Suggestions** — Get personalized, actionable resume improvement tips using Gemini
- **Resume Bullet Point Rewriter** — Turn weak bullet points into strong, tailored ones
- **Interview Question Generator** — Get technical, HR, and project-specific questions based on your resume and target role
- **AI Mock Interview** — A full conversational mock interview that remembers context and gives real-time feedback
- **Downloadable PDF Report** — Export your full analysis as a PDF
- **Clean, Themed UI** — Custom dark theme with animated background and tabbed navigation

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **AI:** Google Gemini API (`google-generativeai`)
- **Resume Parsing:** PyMuPDF (`fitz`), `python-docx`
- **PDF Generation:** `fpdf2`
- **Language:** Python 3.9

## 📸 Screenshots

*(Add a few screenshots here once you have them — I can help you add these next)*

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- A free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### Installation

1. Clone this repository
```bash
git clone https://github.com/parthsaxena8448-lgtm/Ai-career-copilot.git
cd Ai-career-copilot
```

2. Install dependencies
```bash
pip3 install -r requirements.txt
```

3. Add your Gemini API key
Create a file at `.streamlit/secrets.toml` with:
```toml
GEMINI_API_KEY = "your-api-key-here"
```

4. Run the app
```bash
streamlit run app.py
```

## 📝 Usage

1. Enter your name and email on the welcome screen
2. Upload your resume (PDF or DOCX)
3. Paste the job description you're targeting
4. Explore the tabs: ATS results, AI suggestions, interview questions, mock interview, and PDF download

## 🔮 Future Improvements

- Migrate from the deprecated `google-generativeai` library to the newer `google-genai` SDK
- Add user authentication and saved history
- Support for multiple resume formats simultaneously
- Deploy with a custom domain

## 👤 Author

**Parth Saxena**
B.Tech CSE (AI/ML)

---

*Built as a solo project to explore AI integration, prompt engineering, and full-stack Python development.*
import streamlit as st
import pandas as pd

from src.utils import (
    load_job_description_pdf,
    load_resumes,
    run_full_analysis
)


# -----------------------------------------
# App Title
# -----------------------------------------
st.set_page_config(page_title="AI Resume Screener", layout="wide")

st.title("📄 AI Resume Screener & Job Match System")
st.write("""
Upload a Job Description and multiple resumes.
The system will:
- Analyze semantic similarity
- Extract important skills
- Compute keyword coverage
- Rank resumes with a final match score
""")


# -----------------------------------------
# File Upload Section
# -----------------------------------------
st.header("1️⃣ Upload Job Description (PDF)")
jd_file = st.file_uploader("Upload JD PDF", type=["pdf"])

st.header("2️⃣ Upload Candidate Resumes (PDF)")
resume_files = st.file_uploader("Upload Resume PDFs", type=["pdf"], accept_multiple_files=True)

# Default technical skills (customizable)
DEFAULT_SKILLS = [
    "python", "sql", "machine learning", "deep learning",
    "tensorflow", "pytorch", "sklearn", "nlp", "computer vision",
    "aws", "azure", "gcp", "pandas", "numpy"
]

skills_text = st.text_area(
    "Skills to look for (comma-separated):",
    value=", ".join(DEFAULT_SKILLS)
)

skills_list = [s.strip().lower() for s in skills_text.split(",")]


# -----------------------------------------
# Run Analysis Button
# -----------------------------------------
if st.button("🚀 Analyze"):
    if jd_file is None:
        st.error("Please upload a Job Description.")
    elif not resume_files:
        st.error("Please upload at least one resume.")
    else:
        # Step 1: Load text
        with st.spinner("Extracting and preprocessing text..."):
            jd_text = load_job_description_pdf(jd_file)
            resume_texts = load_resumes(resume_files)

        # Step 2: Full pipeline
        with st.spinner("Running Semantic Search + Keyword Analysis..."):
            final_reports, jd_keywords = run_full_analysis(jd_text, resume_texts, skills_list)

        # Step 3: Display JD Keywords
        st.subheader("🔍 Extracted JD Keywords (KeyBERT)")
        st.write(", ".join(jd_keywords))

        # Step 4: Display Ranking Table
        st.subheader("🏆 Resume Ranking")

        df = pd.DataFrame([{
            "Resume": rep["name"],
            "Final Score": rep["final_score"],
            "Semantic Similarity": rep["semantic_similarity"],
            "Keyword Coverage": rep["keyword_coverage"]
        } for rep in final_reports])

        st.dataframe(df.style.highlight_max(axis=0))

        # Step 5: Detailed Report for Each Resume
        st.subheader("📘 Detailed Resume Reports")

        for rep in final_reports:
            st.markdown(f"### {rep['name']} — Match Score: {rep['final_score']*100:.1f}%")

            st.write(f"**Semantic Similarity:** {rep['semantic_similarity']}")
            st.write(f"**Keyword Coverage:** {rep['keyword_coverage']}")

            col1, col2 = st.columns(2)

            with col1:
                st.write("### ✔ Found Skills")
                st.write(rep["found_keywords"])

            with col2:
                st.write("### ❌ Missing Skills")
                st.write(rep["missing_keywords"])

            st.markdown("---")

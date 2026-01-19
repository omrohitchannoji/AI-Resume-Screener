import streamlit as st
import pandas as pd
import time
from streamlit_extras.metric_cards import style_metric_cards

from src.utils import (
    load_job_description_pdf,
    load_resumes,
    run_full_analysis
)

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="AI Resume Screener",
    layout="wide",
    page_icon="📄",
)

# ===================== CUSTOM CSS =====================
st.markdown("""
<style>
/* Background */
.main { background-color: #F3F4F7; }

/* Title */
.title {
    font-size: 48px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg,#f907fc,#05a6f0);
    -webkit-background-clip: text;
    color: transparent !important;
    margin-top: 10px;
    letter-spacing: -1px;
}

/* Animated Button */
div.stButton > button:first-child {
    font-size: 18px;
    font-weight: 700;
    color: white;
    background: linear-gradient(90deg,#7b2ff7,#f107a3);
    border-radius: 10px;
    padding: 0.7rem 1.7rem;
    transition: 0.3s;
    border: none;
}
div.stButton > button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg,#f107a3,#7b2ff7);
}

/* Chips */
.chip {
    display: inline-block;
    padding: 7px 13px;
    margin: 4px;
    border-radius: 20px;
    background-color: #e7deff;
    color: #5c0fe6;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ===================== HEADER =====================
st.markdown('<p class="title">📄 AI Resume Screener</p>', unsafe_allow_html=True)
st.write("### 🚀 Hire Smarter. Not Harder.")
st.write("Upload resumes and a job description. AI ranks candidates using **semantic similarity + skill coverage**.")

# ===================== FILE INPUTS =====================
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Job Description PDF")
    jd_file = st.file_uploader("Upload JD", type=["pdf"])

with col2:
    st.subheader("👨‍💻 Resume PDFs")
    resume_files = st.file_uploader(
        "Upload Resumes",
        type=["pdf"],
        accept_multiple_files=True
    )

# ===================== SKILLS =====================
st.markdown("### 🧠 Key Skills to Extract")
DEFAULT_SKILLS = [
    "python", "sql", "machine learning", "deep learning",
    "tensorflow", "pytorch", "sklearn", "nlp",
    "computer vision", "aws", "azure", "gcp",
    "pandas", "numpy"
]

skills_text = st.text_area(
    "Edit skills (comma-separated):",
    value=", ".join(DEFAULT_SKILLS)
)
skills_list = [s.strip().lower() for s in skills_text.split(",")]

chip_html = "".join([f'<span class="chip">{skill}</span>' for skill in skills_list])
st.markdown(chip_html, unsafe_allow_html=True)

st.markdown("---")

# ===================== RUN =====================
if st.button("🚀 Run Resume Screening"):
    if jd_file is None:
        st.error("⚠ Please upload a Job Description.")
    elif not resume_files:
        st.error("⚠ Please upload Resume PDFs.")
    else:
        with st.spinner("📑 Extracting & Cleaning Text..."):
            jd_text = load_job_description_pdf(jd_file)
            resume_texts = load_resumes(resume_files)

        with st.spinner("🤖 Running AI Analysis..."):
            final_reports, jd_keywords = run_full_analysis(
                jd_text,
                resume_texts,
                skills_list
            )
            time.sleep(1)

        st.success("🎉 Analysis Completed!")
        st.balloons()

        # ===================== JD KEYWORDS =====================
        st.subheader("🔍 Extracted JD Keywords")
        st.write(", ".join(jd_keywords))
        st.markdown("---")

        # ===================== RANKING TABLE =====================
        st.subheader("🏆 Final Resume Ranking")

        df = pd.DataFrame([{
            "Rank": i + 1,
            "Resume": rep["name"],
            "Final Score": rep["final_score"],
            "Semantic Similarity": rep["semantic_similarity"],
            "Keyword Coverage": rep["keyword_coverage"]
        } for i, rep in enumerate(final_reports)])

        def add_badge(rank):
            if rank == 1:
                return "🥇 Best Match"
            elif rank == 2:
                return "🥈 Strong Match"
            elif rank == 3:
                return "🥉 Good Match"
            else:
                return ""

        df["Recommendation"] = df["Rank"].apply(add_badge)

        def highlight_top_rows(row):
            if row["Rank"] <= 3:
                return ["background-color: #d4f7d4"] * len(row)
            return [""] * len(row)

        st.caption("🟢 Top 3 candidates highlighted based on final score ranking.")

        st.dataframe(
            df.style.apply(highlight_top_rows, axis=1),
            use_container_width=True
        )

        style_metric_cards()

        # ===================== CHART =====================
        st.write("📊 **Final Score Comparison**")
        st.bar_chart(
            df.set_index("Resume")[["Final Score"]],
            use_container_width=True
        )

        # ===================== DETAILS =====================
        st.markdown("### 📘 Detailed Resume Breakdown")

        for rep in final_reports:
            with st.expander(
                f"📎 {rep['name']} — Score: {rep['final_score']*100:.1f}%"
            ):
                colA, colB = st.columns(2)
                colA.metric(
                    "🧠 Semantic Similarity",
                    f"{rep['semantic_similarity']*100:.1f}%"
                )
                colB.metric(
                    "📌 Keyword Coverage",
                    f"{rep['keyword_coverage']*100:.1f}%"
                )

                st.write("### ✔ Found Skills")
                st.success(rep["found_keywords"])

                st.write("### ❌ Missing Skills")
                st.error(rep["missing_keywords"])

        # ===================== DOWNLOAD =====================
        st.markdown("---")
        st.write("⬇ **Download Results**")
        st.download_button(
            "📥 Download CSV",
            df.to_csv(index=False),
            "resume_ranking.csv",
            "text/csv"
        )

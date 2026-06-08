import streamlit as st
import pdfplumber
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

# -----------------------------
# Skills Database
# -----------------------------
SKILLS = [
    "python",
    "java",
    "c++",
    "sql",
    "git",
    "machine learning",
    "deep learning",
    "data analysis",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "aws",
    "docker",
    "flask",
    "streamlit",
    "rest api",
    "html",
    "css",
    "javascript"
]

# -----------------------------
# Title
# -----------------------------
st.title("📄 AI Resume Analyzer")
st.write(
    "Upload your resume and compare it with a job description."
)

# -----------------------------
# Upload Resume
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# -----------------------------
# Job Description
# -----------------------------
job_description = st.text_area(
    "Paste Job Description",
    height=200
)

# -----------------------------
# Analyze Resume
# -----------------------------
if uploaded_file and job_description:

    try:

        resume_text = ""

        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()

                if text:
                    resume_text += text

        # -----------------------------
        # Similarity Score
        # -----------------------------
        documents = [
            resume_text,
            job_description
        ]

        cv = CountVectorizer()

        matrix = cv.fit_transform(documents)

        score = cosine_similarity(
            matrix[0],
            matrix[1]
        )[0][0]

        match_score = round(score * 100, 2)

        st.subheader("📊 ATS Match Score")

        st.metric(
            label="Match Percentage",
            value=f"{match_score}%"
        )

        if match_score >= 80:
            st.success(
                "Excellent match for this role!"
            )

        elif match_score >= 60:
            st.warning(
                "Good match, but can be improved."
            )

        else:
            st.error(
                "Low match. Add more relevant skills."
            )

        # -----------------------------
        # Missing Keywords
        # -----------------------------
        resume_words = set(
            resume_text.lower().split()
        )

        jd_words = set(
            job_description.lower().split()
        )

        missing_keywords = jd_words - resume_words

        st.subheader("📌 Missing Keywords")

        filtered_keywords = []

        for word in sorted(missing_keywords):

            if len(word) > 2:
                filtered_keywords.append(word)

        if filtered_keywords:

            for keyword in filtered_keywords[:30]:
                st.write(f"• {keyword}")

        else:
            st.success(
                "No major missing keywords found!"
            )

        # -----------------------------
        # Skills Found
        # -----------------------------
        st.subheader(
            "🛠 Skills Detected in Resume"
        )

        found_skills = []

        resume_lower = resume_text.lower()

        for skill in SKILLS:

            if skill in resume_lower:
                found_skills.append(skill)

        if found_skills:

            st.success(
                ", ".join(found_skills)
            )

        else:

            st.warning(
                "No known skills detected."
            )

        # -----------------------------
        # Suggestions
        # -----------------------------
        st.subheader(
            "💡 Resume Improvement Suggestions"
        )

        suggestions = []

        jd_lower = job_description.lower()

        for skill in SKILLS:

            if (
                skill in jd_lower
                and skill not in resume_lower
            ):

                suggestions.append(
                    f"Add projects or experience related to '{skill}'."
                )

        if suggestions:

            for suggestion in suggestions:
                st.write(
                    "•",
                    suggestion
                )

        else:

            st.success(
                "Your resume covers most required skills."
            )

    except Exception as e:

        st.error(
            f"Error processing resume: {e}"
        )

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")

st.caption(
    "Built with Python, Streamlit, PDFPlumber and Scikit-Learn"
)
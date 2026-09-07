import streamlit as st
import os
import re
import csv
import pandas as pd

RESUME_FOLDER = "resumes"
OUTPUT_FILE = "shortlisted_candidates.csv"
SHORTLIST_SCORE = 50

SKILLS = [
    "python",
    "java",
    "c++",
    "javascript",
    "html",
    "css",
    "sql",
    "mysql",
    "mongodb",
    "django",
    "flask",
    "fastapi",
    "react",
    "node.js",
    "machine learning",
    "deep learning",
    "data analysis",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "git",
    "github",
    "streamlit",
    "aws",
    "docker"
]


def extract_name(text):
    match = re.search(
        r"(?:Name|Candidate Name)\s*[:\-]\s*(.+)",
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip().split("\n")[0]

    lines = text.strip().split("\n")

    if lines:
        return lines[0].strip()

    return "Unknown"


def extract_skills(text):
    text_lower = text.lower()
    found_skills = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return sorted(set(found_skills))


def extract_experience(text):
    patterns = [
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s*(?:of)?\s*experience",
        r"experience\s*[:\-]\s*(\d+(?:\.\d+)?)\s*\+?\s*years?"
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return float(match.group(1))

    return 0


def extract_education(text):
    education_keywords = [
        "b.tech",
        "btech",
        "b.e",
        "be",
        "m.tech",
        "mtech",
        "mca",
        "bca",
        "b.sc",
        "bsc",
        "m.sc",
        "msc",
        "mba",
        "bachelor",
        "master",
        "phd"
    ]

    text_lower = text.lower()
    education = []

    for degree in education_keywords:
        if degree in text_lower:
            education.append(degree.upper())

    return sorted(set(education))


def calculate_match_score(candidate_skills, job_skills):
    if not job_skills:
        return 0

    matched_skills = set(candidate_skills) & set(job_skills)

    score = (
        len(matched_skills) /
        len(job_skills)
    ) * 100

    return round(score, 2)


def find_missing_skills(candidate_skills, job_skills):
    return sorted(
        set(job_skills) -
        set(candidate_skills)
    )


def extract_candidate_details(text):
    return {
        "Name": extract_name(text),
        "Skills": extract_skills(text),
        "Experience": extract_experience(text),
        "Education": extract_education(text)
    }


def process_resume(filename, text, job_skills):
    details = extract_candidate_details(text)

    score = calculate_match_score(
        details["Skills"],
        job_skills
    )

    missing_skills = find_missing_skills(
        details["Skills"],
        job_skills
    )

    return {
        "Name": details["Name"],
        "Skills": ", ".join(details["Skills"]),
        "Experience": details["Experience"],
        "Education": ", ".join(details["Education"]),
        "Match Score": score,
        "Missing Skills": ", ".join(missing_skills),
        "Resume File": filename
    }


def save_results(candidates):
    df = pd.DataFrame(candidates)

    shortlisted = df[
        df["Match Score"] >= SHORTLIST_SCORE
    ]

    shortlisted.to_csv(
        OUTPUT_FILE,
        index=False
    )

    return shortlisted


def read_local_resumes(job_skills):
    candidates = []

    if not os.path.exists(RESUME_FOLDER):
        return candidates

    for filename in os.listdir(RESUME_FOLDER):

        if not filename.lower().endswith(
            (".txt", ".csv")
        ):
            continue

        file_path = os.path.join(
            RESUME_FOLDER,
            filename
        )

        try:
            if filename.lower().endswith(".txt"):

                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as file:
                    text = file.read()

                candidates.append(
                    process_resume(
                        filename,
                        text,
                        job_skills
                    )
                )

            elif filename.lower().endswith(".csv"):

                df = pd.read_csv(file_path)

                for index, row in df.iterrows():

                    text = " ".join(
                        str(value)
                        for value in row.values
                        if pd.notna(value)
                    )

                    candidates.append(
                        process_resume(
                            f"{filename} - Row {index + 1}",
                            text,
                            job_skills
                        )
                    )

        except Exception as e:
            st.error(
                f"Error reading {filename}: {e}"
            )

    return candidates


st.set_page_config(
    page_title="AI Resume Screening Tool",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Screening Tool")
st.write(
    "Upload multiple resumes and match them "
    "against a job description."
)

st.sidebar.header("⚙️ Job Requirements")

job_description = st.sidebar.text_area(
    "Enter Job Description",
    height=250,
    placeholder="Enter required skills, experience and education..."
)

uploaded_files = st.file_uploader(
    "📤 Upload Resume Files",
    type=["txt", "csv"],
    accept_multiple_files=True
)

st.sidebar.write(
    f"Shortlist Score: {SHORTLIST_SCORE}%"
)


if st.button("🔍 Screen Resumes"):

    if not job_description.strip():

        st.warning(
            "Please enter a job description."
        )

    elif not uploaded_files:

        st.warning(
            "Please upload at least one resume."
        )

    else:

        job_skills = extract_skills(
            job_description
        )

        if not job_skills:

            st.warning(
                "No recognized skills were found "
                "in the job description."
            )

        else:

            st.subheader("🎯 Required Skills")

            st.write(
                ", ".join(job_skills)
            )

            candidates = []

            for uploaded_file in uploaded_files:

                try:

                    file_content = uploaded_file.read()

                    text = file_content.decode(
                        "utf-8",
                        errors="ignore"
                    )

                    candidate = process_resume(
                        uploaded_file.name,
                        text,
                        job_skills
                    )

                    candidates.append(candidate)

                except Exception as e:

                    st.error(
                        f"Error processing "
                        f"{uploaded_file.name}: {e}"
                    )

            if candidates:

                candidates.sort(
                    key=lambda x: x["Match Score"],
                    reverse=True
                )

                for rank, candidate in enumerate(
                    candidates,
                    start=1
                ):
                    candidate["Rank"] = rank

                df = pd.DataFrame(
                    candidates
                )

                columns = [
                    "Rank",
                    "Name",
                    "Skills",
                    "Experience",
                    "Education",
                    "Match Score",
                    "Missing Skills",
                    "Resume File"
                ]

                df = df[columns]

                st.subheader(
                    "🏆 Ranked Candidates"
                )

                st.dataframe(
                    df,
                    use_container_width=True
                )

                st.subheader(
                    "📊 Resume Match Scores"
                )

                chart_data = df[
                    ["Name", "Match Score"]
                ].copy()

                chart_data = chart_data.set_index(
                    "Name"
                )

                st.bar_chart(
                    chart_data
                )

                st.subheader(
                    "❌ Missing Skills"
                )

                for _, candidate in df.iterrows():

                    missing = candidate[
                        "Missing Skills"
                    ]

                    if missing:

                        st.write(
                            f"**{candidate['Name']}**: "
                            f"{missing}"
                        )

                    else:

                        st.write(
                            f"**{candidate['Name']}**: "
                            "No missing skills 🎉"
                        )

                shortlisted = df[
                    df["Match Score"] >= SHORTLIST_SCORE
                ]

                st.subheader(
                    "✅ Shortlisted Candidates"
                )

                if not shortlisted.empty:

                    st.dataframe(
                        shortlisted,
                        use_container_width=True
                    )

                    csv_data = shortlisted.to_csv(
                        index=False
                    ).encode("utf-8")

                    st.download_button(
                        label="⬇️ Download Shortlisted CSV",
                        data=csv_data,
                        file_name="shortlisted_candidates.csv",
                        mime="text/csv"
                    )

                else:

                    st.info(
                        "No candidates reached "
                        f"the {SHORTLIST_SCORE}% "
                        "shortlist threshold."
                    )

                st.success(
                    f"Successfully processed "
                    f"{len(candidates)} resumes."
                )

            else:

                st.warning(
                    "No valid resumes were processed."
                )
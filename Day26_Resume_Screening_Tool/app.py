import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="AI Resume Screening Tool",
    page_icon="📄",
    layout="wide"
)


st.title("📄 AI Resume Screening Tool")
st.write("Upload resumes and a job description to screen candidates.")


# Required skills
required_skills = [
    "python",
    "pandas",
    "numpy",
    "sql",
    "machine learning",
    "git",
    "streamlit"
]


# Job description upload
st.subheader("1️⃣ Upload Job Description")

job_file = st.file_uploader(
    "Upload Job Description",
    type=["txt"]
)


# Resume upload
st.subheader("2️⃣ Upload Resumes")

resume_files = st.file_uploader(
    "Upload Resume Files",
    type=["txt"],
    accept_multiple_files=True
)


# Screen resumes
if st.button("🔍 Screen Resumes"):

    if job_file is None:

        st.error("Please upload a job description.")

    elif len(resume_files) == 0:

        st.error("Please upload at least one resume.")

    else:

        candidates = []

        for resume_file in resume_files:

            text = resume_file.read().decode(
                "utf-8"
            )

            text_lower = text.lower()


            # Extract name
            name = "Unknown"

            for line in text.splitlines():

                if line.lower().startswith("name:"):

                    name = line.split(
                        ":",
                        1
                    )[1].strip()


            # Find matched skills
            matched_skills = []

            for skill in required_skills:

                if skill in text_lower:

                    matched_skills.append(skill)


            # Find missing skills
            missing_skills = [
                skill
                for skill in required_skills
                if skill not in matched_skills
            ]


            # Calculate score
            score = (
                len(matched_skills)
                / len(required_skills)
            ) * 100


            # Add candidate
            candidates.append({

                "Name": name,

                "Resume": resume_file.name,

                "Matched Skills":
                    ", ".join(matched_skills),

                "Missing Skills":
                    ", ".join(missing_skills),

                "Match Score":
                    round(score, 2)

            })


        # Sort candidates
        candidates.sort(
            key=lambda x: x["Match Score"],
            reverse=True
        )


        # Convert to DataFrame
        df = pd.DataFrame(candidates)


        st.success("Resume screening completed!")


        # Results
        st.subheader("📊 Candidate Ranking")

        st.dataframe(
            df,
            use_container_width=True
        )


        # Top candidate
        st.subheader("🏆 Best Candidate")

        best_candidate = df.iloc[0]

        st.success(
            f"{best_candidate['Name']} "
            f"— {best_candidate['Match Score']}%"
        )


        # Shortlist
        shortlisted = df[
            df["Match Score"] >= 40
        ]


        st.subheader("✅ Shortlisted Candidates")

        if len(shortlisted) > 0:

            st.dataframe(
                shortlisted,
                use_container_width=True
            )

        else:

            st.warning(
                "No candidates shortlisted."
            )


        # Download CSV
        csv_data = shortlisted.to_csv(
            index=False
        )


        st.download_button(

            label="⬇️ Download Shortlisted Candidates",

            data=csv_data,

            file_name="shortlisted_candidates.csv",

            mime="text/csv"

        )
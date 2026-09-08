import os
import csv

RESUME_FOLDER = "resumes"
JOB_FILE = "job_description.txt"
OUTPUT_FILE = "shortlisted_candidates.csv"


# Read job description
with open(JOB_FILE, "r", encoding="utf-8") as file:
    job_text = file.read()


# Get required skills
required_skills = [
    "python",
    "pandas",
    "numpy",
    "sql",
    "machine learning",
    "git",
    "streamlit"
]


candidates = []


# Read all resumes
for filename in os.listdir(RESUME_FOLDER):

    if filename.endswith(".txt"):

        with open(
            os.path.join(RESUME_FOLDER, filename),
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        text_lower = text.lower()


        # Extract name
        name = "Unknown"

        for line in text.splitlines():
            if line.lower().startswith("name:"):
                name = line.split(":", 1)[1].strip()


        # Find matching skills
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


        candidates.append({
            "Name": name,
            "Resume": filename,
            "Matched Skills": ", ".join(matched_skills),
            "Missing Skills": ", ".join(missing_skills),
            "Match Score": round(score, 2)
        })


# Sort candidates by score
candidates.sort(
    key=lambda x: x["Match Score"],
    reverse=True
)


# Display results
print("\n======================================")
print("       AI RESUME SCREENING TOOL")
print("======================================\n")


for rank, candidate in enumerate(candidates, start=1):

    print("Rank:", rank)
    print("Name:", candidate["Name"])
    print("Resume:", candidate["Resume"])
    print("Matched Skills:", candidate["Matched Skills"])
    print("Missing Skills:", candidate["Missing Skills"])
    print("Match Score:", str(candidate["Match Score"]) + "%")
    print("--------------------------------------")


# Shortlist candidates
shortlisted = [
    candidate
    for candidate in candidates
    if candidate["Match Score"] >= 40
]


print("\n======================================")
print("          SHORTLISTED CANDIDATES")
print("======================================\n")


if len(shortlisted) == 0:

    print("No candidate shortlisted.")

else:

    for candidate in shortlisted:

        print(
            candidate["Name"],
            "-",
            str(candidate["Match Score"]) + "%"
        )


# Export CSV
with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    columns = [
        "Name",
        "Resume",
        "Matched Skills",
        "Missing Skills",
        "Match Score"
    ]

    writer = csv.DictWriter(
        file,
        fieldnames=columns
    )

    writer.writeheader()
    writer.writerows(shortlisted)


print("\nCSV file created successfully:")
print(OUTPUT_FILE)



import json
import re

def extract_skills(resume_text):

    with open("data/skills.json", "r") as file:
        skills_database = json.load(file)

    extracted_skills = {}

    resume_text = resume_text.lower()

    for category, skills in skills_database.items():

        matched_skills = []

        for skill in skills:

            pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

            if re.search(pattern, resume_text):
                matched_skills.append(skill)

        if matched_skills:
            extracted_skills[category] = matched_skills

    return extracted_skills
def extract_job_skills(job_description):

    return extract_skills(job_description)
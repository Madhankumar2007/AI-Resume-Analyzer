def calculate_match(resume_skills, job_skills):

    # Convert categorized skills into sets
    resume_set = set()

    for skills in resume_skills.values():
        resume_set.update(skill.lower() for skill in skills)

    job_set = set()

    for skills in job_skills.values():
        job_set.update(skill.lower() for skill in skills)

    # Handle empty job requirements
    if not job_set:
        return {
            "match_percentage": 0,
            "matched_skills": [],
            "missing_skills": []
        }

    # Find matching skills
    matched_skills = resume_set.intersection(job_set)

    # Find missing skills
    missing_skills = job_set.difference(resume_set)

    # Calculate matching percentage
    match_percentage = (
        len(matched_skills) / len(job_set)
    ) * 100

    return {
        "match_percentage": round(match_percentage, 2),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills)
    }
import re


# Technical keywords and their alternative spellings
TECHNICAL_KEYWORDS = {
    "python": ["python"],
    "java": ["java"],
    "c": ["c"],
    "c++": ["c++"],
    "c#": ["c#"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript"],
    "html": ["html"],
    "css": ["css"],
    "sql": ["sql"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "mongodb": ["mongodb", "mongo db"],
    "flask": ["flask"],
    "django": ["django"],
    "react": ["react", "react.js"],
    "angular": ["angular"],
    "node.js": ["node.js", "nodejs"],
    "rest api": ["rest api", "rest apis", "restful api", "restful apis"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning"],
    "artificial intelligence": ["artificial intelligence", "ai"],
    "natural language processing": ["natural language processing", "nlp"],
    "computer vision": ["computer vision"],
    "data science": ["data science"],
    "data analysis": ["data analysis", "data analytics"],
    "data visualization": ["data visualization", "data visualisation"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "keras": ["keras"],
    "sentence-bert": ["sentence-bert", "sentence bert", "sbert"],
    "neural networks": ["neural networks", "neural network"],
    "cnn": ["cnn", "convolutional neural network"],
    "rnn": ["rnn", "recurrent neural network"],
    "ann": ["ann", "artificial neural network"],
    "opencv": ["opencv", "open cv"],
    "easyocr": ["easyocr", "easy ocr"],
    "git": ["git"],
    "github": ["github"],
    "gitlab": ["gitlab"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "power bi": ["power bi"],
    "tableau": ["tableau"],
    "excel": ["excel", "microsoft excel"],
    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],
    "statistics": ["statistics"],
    "probability": ["probability"],
    "exploratory data analysis": ["exploratory data analysis", "eda"],
    "feature engineering": ["feature engineering"],
    "data preprocessing": ["data preprocessing", "data cleaning"],
    "classification": ["classification"],
    "regression": ["regression"],
    "clustering": ["clustering"],
    "supervised learning": ["supervised learning"],
    "unsupervised learning": ["unsupervised learning"],
    "text processing": ["text processing"],
    "tokenization": ["tokenization"],
    "word embeddings": ["word embeddings"],
    "api development": ["api development"],
    "problem solving": ["problem solving", "problem-solving"],
    "communication": ["communication"],
    "teamwork": ["teamwork"],
    "analytical skills": ["analytical skills", "analytical"],
    "data structures": ["data structures"],
    "algorithms": ["algorithms"],
    "object oriented programming": [
        "object oriented programming",
        "object-oriented programming",
        "oop"
    ]
}


def contains_keyword(text, keyword):
    """
    Check whether a keyword or phrase exists
    without matching partial words.
    """
    pattern = (
        r"(?<![a-zA-Z0-9])"
        + re.escape(keyword)
        + r"(?![a-zA-Z0-9])"
    )

    return re.search(pattern, text, re.IGNORECASE) is not None


def analyze_ats(resume_text, job_description):

    text = resume_text.lower()
    job_text = job_description.lower()

    # Identify important resume sections
    sections = {
        "Contact Information": [
            "email", "phone", "linkedin"
        ],
        "Career Objective": [
            "career objective", "objective",
            "professional summary"
        ],
        "Skills": [
            "skills", "technical skills"
        ],
        "Education": [
            "education", "academic qualification"
        ],
        "Projects": [
            "projects", "project experience"
        ],
        "Experience": [
            "experience", "work experience", "internship"
        ],
        "Certifications": [
            "certifications", "certificates"
        ]
    }

    detected_sections = []
    missing_sections = []

    for section, keywords in sections.items():

        if any(contains_keyword(text, keyword) for keyword in keywords):
            detected_sections.append(section)
        else:
            missing_sections.append(section)

    # Calculate resume completeness score
    total_sections = len(sections)

    completeness_score = (
        len(detected_sections) / total_sections
    ) * 100

    # Extract meaningful technical keywords
    job_keywords = set()
    matched_keywords = set()

    for canonical_name, aliases in TECHNICAL_KEYWORDS.items():

        found_in_job = any(
            contains_keyword(job_text, alias)
            for alias in aliases
        )

        if found_in_job:

            job_keywords.add(canonical_name)

            found_in_resume = any(
                contains_keyword(text, alias)
                for alias in aliases
            )

            if found_in_resume:
                matched_keywords.add(canonical_name)

    # Identify missing keywords
    missing_keywords = job_keywords - matched_keywords

    # Generate improvement suggestions
    suggestions = []

    if "Experience" in missing_sections:
        suggestions.append(
            "Add relevant internship, work, or practical experience if available."
        )

    if "Projects" in missing_sections:
        suggestions.append(
            "Include academic or personal projects with technologies used."
        )

    if "Certifications" in missing_sections:
        suggestions.append(
            "Include relevant technical certifications if available."
        )

    if "Skills" in missing_sections:
        suggestions.append(
            "Add a clearly organized technical skills section."
        )

    if missing_keywords:
        suggestions.append(
            "Review missing technical keywords and include relevant ones "
            "naturally where they accurately describe your experience."
        )

    if not suggestions:
        suggestions.append(
            "Your resume contains the main sections detected by this analyzer. "
            "Continue improving clarity and relevance."
        )

    return {
        "completeness_score": round(completeness_score, 2),
        "detected_sections": detected_sections,
        "missing_sections": missing_sections,
        "matched_keywords": sorted(matched_keywords),
        "missing_keywords": sorted(missing_keywords),
        "suggestions": suggestions
    }
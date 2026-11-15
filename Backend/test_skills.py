from skill_extractor import extract_skills

sample_resume = """
Python Java C
HTML CSS JavaScript
MySQL
EasyOCR Sentence-BERT ResNet18
Git GitHub VS Code
"""

skills = extract_skills(sample_resume)

for category, matched_skills in skills.items():

    print("\n" + category)

    for skill in matched_skills:
        print("-", skill)
def generate_recommendations(missing_skills):
    recommendations_database = {
        "deep learning": {
            "description": "Understand neural networks and deep learning architectures.",
            "difficulty": "Advanced",
            "topics": ["ANN", "CNN", "RNN", "Neural Networks"]
        },
        "django": {
            "description": "Learn to develop full-stack web applications using Django.",
            "difficulty": "Intermediate",
            "topics": ["Django Framework", "Models", "Views", "Templates", "REST Framework"]
        },
        "flask": {
            "description": "Learn to develop Python backend applications and REST APIs.",
            "difficulty": "Beginner",
            "topics": ["Flask Routing", "REST API", "HTTP Methods"]
        },
        "machine learning": {
            "description": "Learn supervised and unsupervised machine learning algorithms.",
            "difficulty": "Intermediate",
            "topics": ["Linear Regression", "Decision Trees", "KNN", "Naive Bayes"]
        },
        "nlp": {
            "description": "Learn natural language processing techniques.",
            "difficulty": "Intermediate",
            "topics": ["Text Processing", "Tokenization", "Word Embeddings"]
        },
        "pytorch": {
            "description": "Learn deep learning model development using PyTorch.",
            "difficulty": "Advanced",
            "topics": ["Tensors", "Autograd", "Neural Networks"]
        },
        "scikit-learn": {
            "description": "Practice implementing machine learning algorithms.",
            "difficulty": "Intermediate",
            "topics": ["Classification", "Regression", "Clustering"]
        },
        "tensorflow": {
            "description": "Practice building and training machine learning models.",
            "difficulty": "Intermediate",
            "topics": ["TensorFlow Basics", "Keras", "Model Training"]
        }
    }

    recommendations = []

    for skill in missing_skills:
        skill_name = skill.lower().strip()

        if skill_name in recommendations_database:
            recommendation = recommendations_database[skill_name].copy()
        else:
            recommendation = {
                "description": f"Improve your knowledge and practical experience in {skill}.",
                "difficulty": "Intermediate",
                "topics": [
                    f"{skill} Fundamentals",
                    f"{skill} Practical Applications",
                    f"{skill} Projects"
                ]
            }

        recommendation["skill"] = skill
        recommendations.append(recommendation)

    return recommendations
from sentence_transformers import SentenceTransformer, util

# Load the pretrained Sentence-BERT model
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_semantic_similarity(resume_text, job_description):

    resume_embedding = model.encode(
        resume_text,
        convert_to_tensor=True
    )

    job_embedding = model.encode(
        job_description,
        convert_to_tensor=True
    )

    similarity = util.cos_sim(
        resume_embedding,
        job_embedding
    )

    similarity_percentage = float(similarity.item()) * 100

    return round(similarity_percentage, 2)
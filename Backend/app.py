from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from resume_parser import extract_resume_text
from skill_extractor import extract_skills, extract_job_skills
from resume_matcher import calculate_match
from recommendation_engine import generate_recommendations
from report_generator import generate_pdf_report
from semantic_matcher import calculate_semantic_similarity
from ats_analyzer import analyze_ats

app = Flask(__name__)
CORS(app)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

latest_analysis = {}


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "AI Resume Analyzer Backend is Running!"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "Success",
        "application": "AI Resume Analyzer",
        "message": "Backend is working properly"
    })


@app.route("/upload", methods=["POST"])
def upload_resume():

    global latest_analysis

    if "resume" not in request.files:
        return jsonify({"error": "No resume uploaded"}), 400

    resume = request.files["resume"]

    if resume.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not resume.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    job_description = request.form.get("job_description", "")

    if not job_description.strip():
        return jsonify({"error": "Please enter a job description"}), 400

    try:
        # Extract resume text
        extracted_text = extract_resume_text(resume)

        if not extracted_text.strip():
            return jsonify({
                "error": "No readable text found in PDF"
            }), 400

        # Extract resume skills
        extracted_skills = extract_skills(extracted_text)

        # Extract job description skills
        job_skills = extract_job_skills(job_description)

        # Keyword-based matching
        match_result = calculate_match(
            extracted_skills,
            job_skills
        )

        # Sentence-BERT semantic similarity
        semantic_score = calculate_semantic_similarity(
            extracted_text,
            job_description
        )

        # Count resume skills
        total_skills = sum(
            len(skills)
            for skills in extracted_skills.values()
        )

        # Generate skill recommendations
        recommendations = generate_recommendations(
            match_result["missing_skills"]
        )

        # ATS analysis
        ats_result = analyze_ats(
            extracted_text,
            job_description
        )

        result = {
            "status": "Success",
            "message": "Resume analyzed successfully",
            "total_skills": total_skills,
            "skills": extracted_skills,
            "job_skills": job_skills,
            "match_result": match_result,
            "semantic_similarity": semantic_score,
            "recommendations": recommendations,
            "ats_analysis": ats_result,
            "extracted_text": extracted_text
        }

        latest_analysis = result

        return jsonify(result), 200

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except Exception:
        app.logger.exception("Resume analysis failed")

        return jsonify({
            "error": "An unexpected error occurred during resume analysis"
        }), 500


@app.route("/download-report", methods=["GET"])
def download_report():

    if not latest_analysis:
        return jsonify({
            "error": "Please analyze a resume before downloading the report"
        }), 400

    try:
        pdf_buffer = generate_pdf_report(latest_analysis)

        return send_file(
            pdf_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="Resume_Analysis_Report.pdf"
        )

    except Exception:
        app.logger.exception("PDF report generation failed")

        return jsonify({
            "error": "Unable to generate PDF report"
        }), 500


@app.errorhandler(413)
def file_too_large(error):
    return jsonify({
        "error": "File size exceeds the maximum limit of 5 MB"
    }), 413


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
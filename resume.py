from flask import Flask, request, jsonify
import requests
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

AFFINDA_API_KEY = "your_affinda_api_key"
AFFINDA_API_URL = "https://api.affinda.com/v1/resumes/parse"

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload_resume():
    if "resume" not in request.files or "jobDescription" not in request.form:
        return jsonify({"error": "Missing resume or job description"}), 400

    resume_file = request.files["resume"]
    job_description = request.form["jobDescription"]

    if resume_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(resume_file.filename):
        return jsonify({"error": "Invalid file type. Only PDF, DOCX, and TXT are allowed."}), 400

    filename = secure_filename(resume_file.filename)
    resume_file.save(filename)

    with open(filename, "rb") as f:
        response = requests.post(
            AFFINDA_API_URL,
            headers={"Authorization": f"Bearer {AFFINDA_API_KEY}"},
            files={"file": f},
        )

    if response.status_code != 200:
        return jsonify({"error": "Error parsing resume"}), 400

    resume_data = response.json()
    
    resume_skills = resume_data.get("skills", [])
    match_score = compare_job_description_with_resume(job_description, resume_skills)
    suggestions = generate_suggestions(job_description, resume_skills)

    return jsonify({
        "matchScore": match_score,
        "suggestions": suggestions
    })

def compare_job_description_with_resume(job_description, resume_skills):
    job_keywords = set(job_description.lower().split())
    resume_keywords = set(skill.lower() for skill in resume_skills)
    common_keywords = job_keywords.intersection(resume_keywords)
    match_score = len(common_keywords) / len(job_keywords) * 100
    return round(match_score, 2)

def generate_suggestions(job_description, resume_skills):
    job_keywords = set(job_description.lower().split())
    resume_keywords = set(skill.lower() for skill in resume_skills)
    missing_keywords = job_keywords.difference(resume_keywords)
    suggestions = [f"Consider adding skills: {keyword}" for keyword in missing_keywords]
    return suggestions

if __name__ == "__main__":
    app.run(debug=True)

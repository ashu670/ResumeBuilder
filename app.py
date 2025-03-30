import os
import subprocess
import tempfile
from io import BytesIO
import requests
from flask import Flask, render_template, request, send_file, jsonify
from docxtpl import DocxTemplate

app = Flask(__name__, template_folder="template", static_folder="static")

TEMPLATE_PATH = "template/template.docx"
OUTPUT_PATH = "generated_resume.docx"  # Used for final download

# Set the full path to LibreOffice's soffice.exe on Windows
LIBREOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Final submission: generate DOCX for download
        context = {
            "NAME": request.form.get("name", ""),
            "ADDRESS": request.form.get("address", ""),
            "NUMBER": request.form.get("number", ""),
            "EMAIL": request.form.get("email", ""),
            "LINKEDIN": request.form.get("linkedin", ""),
            "WEBSITE": request.form.get("website", ""),
            "INTRODUCTION": request.form.get("introduction", ""),
            # Experience fields
            "EXPERIENCE": "",
            "EXPERIENCE_1": request.form.get("experience1", ""),
            "DATE_EXPERIENCE_1": request.form.get("date_experience1", ""),
            "DETAIL_EXPERIENCE_1": request.form.get("detail_experience1", ""),
            "EXPERIENCE_2": request.form.get("experience2", ""),
            "DATE_EXPERIENCE_2": request.form.get("date_experience2", ""),
            "DETAIL_EXPERIENCE_2": request.form.get("detail_experience2", ""),
            # Education fields
            "EDUCATION": "",
            "EDUCATION_1": request.form.get("education1", ""),
            "DATE_EDUCATION_1": request.form.get("date_education1", ""),
            "DETAIL_EDUCATION_1": request.form.get("detail_education1", ""),
            "EDUCATION_2": request.form.get("education2", ""),
            "DATE_EDUCATION_2": request.form.get("date_education2", ""),
            "DETAIL_EDUCATION_2": request.form.get("detail_education2", ""),
            # Skills fields
            "SKILL_1": request.form.get("skill1", ""),
            "SKILL_2": request.form.get("skill2", ""),
            "SKILL_3": request.form.get("skill3", ""),
            "SKILL_4": request.form.get("skill4", ""),
            "SKILL_5": request.form.get("skill5", ""),
            "SKILL_6": request.form.get("skill6", ""),
            # Activities
            "ACTIVITIES": request.form.get("activities", "")
        }
        doc = DocxTemplate(TEMPLATE_PATH)
        doc.render(context)
        doc.save(OUTPUT_PATH)
        return send_file(OUTPUT_PATH, as_attachment=True)
    
    return render_template("index.html")

@app.route("/preview_pdf", methods=["POST"])
def preview_pdf():
    """
    Generate a DOCX from current form data,
    convert it to PDF using LibreOffice headless mode,
    and return the PDF as binary.
    """
    context = {
        "NAME": request.form.get("name", ""),
        "ADDRESS": request.form.get("address", ""),
        "NUMBER": request.form.get("number", ""),
        "EMAIL": request.form.get("email", ""),
        "LINKEDIN": request.form.get("linkedin", ""),
        "WEBSITE": request.form.get("website", ""),
        "INTRODUCTION": request.form.get("introduction", ""),
        # Experience fields
        "EXPERIENCE": "",
        "EXPERIENCE_1": request.form.get("experience1", ""),
        "DATE_EXPERIENCE_1": request.form.get("date_experience1", ""),
        "DETAIL_EXPERIENCE_1": request.form.get("detail_experience1", ""),
        "EXPERIENCE_2": request.form.get("experience2", ""),
        "DATE_EXPERIENCE_2": request.form.get("date_experience2", ""),
        "DETAIL_EXPERIENCE_2": request.form.get("detail_experience2", ""),
        # Education fields
        "EDUCATION": "",
        "EDUCATION_1": request.form.get("education1", ""),
        "DATE_EDUCATION_1": request.form.get("date_education1", ""),
        "DETAIL_EDUCATION_1": request.form.get("detail_education1", ""),
        "EDUCATION_2": request.form.get("education2", ""),
        "DATE_EDUCATION_2": request.form.get("date_education2", ""),
        "DETAIL_EDUCATION_2": request.form.get("detail_education2", ""),
        # Skills fields
        "SKILL_1": request.form.get("skill1", ""),
        "SKILL_2": request.form.get("skill2", ""),
        "SKILL_3": request.form.get("skill3", ""),
        "SKILL_4": request.form.get("skill4", ""),
        "SKILL_5": request.form.get("skill5", ""),
        "SKILL_6": request.form.get("skill6", ""),
        # Activities
        "ACTIVITIES": request.form.get("activities", "")
    }
    doc = DocxTemplate(TEMPLATE_PATH)
    doc.render(context)
    
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp_docx:
        doc.save(tmp_docx.name)
        tmp_docx_path = tmp_docx.name

    tmp_pdf_path = tmp_docx_path.replace(".docx", ".pdf")
    try:
        subprocess.run(
            [LIBREOFFICE_PATH, '--headless', '--convert-to', 'pdf', tmp_docx_path, '--outdir', os.path.dirname(tmp_docx_path)],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        return f"Conversion error: {e.stderr.decode()}", 500

    with open(tmp_pdf_path, "rb") as f:
        pdf_data = f.read()
    os.remove(tmp_docx_path)
    os.remove(tmp_pdf_path)
    
    return send_file(BytesIO(pdf_data),
                     mimetype="application/pdf",
                     as_attachment=False,
                     download_name="preview.pdf")

@app.route("/generate_recommendation", methods=["POST"])
def generate_recommendation():
    """
    Use a free text generation API (TextGen) to generate recommendations based on user input.
    The prompt is constructed using the user's experience and skills.
    """
    data = request.json
    experience = data.get("experience", "")
    # Expect skills as a comma-separated string; convert to list
    skills_str = data.get("skills", "")
    skills = [skill.strip() for skill in skills_str.split(",") if skill.strip()]
    
    prompt = ""
    if experience:
        prompt += f"User works as {experience}. Suggest detailed responsibilities, activities, and achievements for this role. "
    if skills:
        prompt += f"User's current skills include {', '.join(skills)}. Suggest additional related skills.\n"
    
    # Use the free TextGen API
    url = "https://api.textgen.dev/v1/generate"
    payload = {
        "prompt": prompt,
        "max_length": 150,
        "temperature": 0.7
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        generated_text = response.json()["results"][0]["text"].strip()
    else:
        generated_text = "Error generating recommendation."
    
    return jsonify({"recommendation": generated_text})

if __name__ == "__main__":
    app.run(debug=True)

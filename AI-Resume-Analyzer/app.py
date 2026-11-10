import os
import uuid
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from analyzer import analyze_resume, extract_resume_text


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
MAX_UPLOAD_BYTES = 8 * 1024 * 1024

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "local-development-key")
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    resume = request.files.get("resume")
    job_description = request.form.get("job_description", "").strip()

    if not resume or not resume.filename:
        flash("Choose a resume file to continue.", "error")
        return redirect(url_for("index"))
    if not allowed_file(resume.filename):
        flash("Upload a PDF, DOCX, or TXT file.", "error")
        return redirect(url_for("index"))
    if not job_description:
        flash("Paste the job description to continue.", "error")
        return redirect(url_for("index"))

    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    suffix = Path(secure_filename(resume.filename)).suffix.lower()
    temporary_path = UPLOAD_FOLDER / f"{uuid.uuid4().hex}{suffix}"

    try:
        resume.save(temporary_path)
        resume_text = extract_resume_text(temporary_path)
        if not resume_text.strip():
            flash("No readable text was found. Try a text-based PDF or DOCX file.", "error")
            return redirect(url_for("index"))

        results = analyze_resume(resume_text, job_description)
        results["filename"] = secure_filename(resume.filename)
        return render_template("result.html", results=results)
    except (ValueError, OSError) as error:
        flash(str(error), "error")
        return redirect(url_for("index"))
    finally:
        temporary_path.unlink(missing_ok=True)


@app.errorhandler(413)
def file_too_large(_error):
    flash("That file is larger than the 8 MB upload limit.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
# AI Resume Analyzer

A local Flask app that compares a resume with a job description and highlights detected skill overlap. Analysis is rule-based and runs on your machine; it does not send resume data to an AI service.

## Run locally

```powershell
cd AI-Resume-Analyzer
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000> and upload a PDF, DOCX, or TXT resume (up to 8 MB), then paste the job description. For production, set a strong `FLASK_SECRET_KEY` environment variable and run behind a production WSGI server.

## Project layout

```text
AI-Resume-Analyzer/
|-- app.py
|-- analyzer.py
|-- requirements.txt
|-- README.md
|-- templates/
|   |-- index.html
|   `-- result.html
|-- static/
|   `-- style.css
`-- uploads/
```

Uploaded files are removed after each analysis. The `uploads/` directory is created automatically when the app starts accepting files.
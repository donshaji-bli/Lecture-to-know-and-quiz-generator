# Lecture Lens

A Flask starter project that turns pasted lecture notes into key takeaways and a short multiple-choice knowledge check. Processing is local and rule-based; it does not call an external AI service.

## Setup

Create and activate the virtual environment from this folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

```powershell
python app.py
```

Open http://127.0.0.1:5000 in your browser. Paste several complete lecture sentences and select **Build my study guide**. Use **Reveal answer** to check each quiz item.

## Project structure

```text
lecture_quiz_generator/
├── app.py
├── requirements.txt
├── templates/index.html
└── static/style.css
```

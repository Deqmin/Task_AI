---
title: Live Sentiment Stream Analyzer
emoji: chart_with_upwards_trend
colorFrom: blue
colorTo: green
sdk: gradio
app_file: app.py
pinned: false
---

# Live Sentiment Stream Analyzer

A Gradio app that takes typed text input, runs sentiment classification in Python on each Analyze click, and shows confidence scores, alerts, and an exportable event log.

## Live demo URL

Set this after creating the Space:
- Hugging Face Space: https://huggingface.co/spaces/<your-username>/<your-space-name>

## What this app does

- Accepts text input from the user and analyzes each submitted sample.
- Uses a Hugging Face Transformers sentiment model to classify text as Positive or Negative.
- Displays confidence scores for each class.
- Triggers a visible alert when confidence crosses a user-defined threshold.
- Stores a session event log with timestamps and lets users export CSV/JSON.

## Model and data

- Model: `distilbert-base-uncased-finetuned-sst-2-english`
- Source: Hugging Face model hub
- Input data: user-provided text only (no uploaded dataset)

## How it works

1. User enters text in the UI.
2. Python backend runs a Transformers text-classification pipeline.
3. App sorts class probabilities and shows top class + confidence.
4. If confidence is above threshold (and matches target class), an alert banner appears.
5. Analysis events are appended to an in-memory session log and can be downloaded as CSV/JSON.

## Limitations

- Binary sentiment only (Positive/Negative), not nuanced emotions.
- Can misinterpret sarcasm, slang, mixed languages, and very short snippets.
- Confidence is not calibrated certainty; it is model probability for this task.

## Local run

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts\verify_imports.py
python app.py
```

On macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open the local Gradio URL shown in terminal.

## CI/CD setup

The workflow file [`.github/workflows/deploy-huggingface.yml`](.github/workflows/deploy-huggingface.yml) includes:
- Verify job: required file checks, clean install, import checks, application smoke import, and Python compilation.
- Deploy job: pushes `main` to Hugging Face Space after verify passes.

### Required GitHub configuration

- Repository secret: `HF_TOKEN` (Hugging Face write token)
- Repository variable: `HF_SPACE_ID` (format: `your-hf-user/your-space-name`)

## Assignment checklist mapping

- Live input -> model -> visible result with score: implemented.
- Engineering feature beyond demo: alert threshold + target class control + event log + CSV/JSON export + session stats.
- How it works and limitations: documented in UI and README.

## Evidence of CI failure and fix

After the first deployment, add one screenshot/link of a failed workflow run and the follow-up passing run after your fix. This evidence is intentionally kept as a release step because workflow run URLs do not exist until this repository is connected to GitHub.

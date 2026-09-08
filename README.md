---
title: Live Sentiment Stream Analyzer
emoji: "📈"
colorFrom: blue
colorTo: green
sdk: static
app_file: index.html
pinned: false
---

# Live Sentiment Stream Analyzer

A browser app that takes typed text input, runs the DistilBERT sentiment model with Transformers.js, and shows confidence scores, alerts, and an exportable event log.

## Live demo URL

Set this after creating the Space:
- Hugging Face Space: https://huggingface.co/spaces/deqmin/live-sentiment-stream-analyzer
- GitHub Pages project page: https://deqmin.github.io/Task_AI/

The static app runs on GitHub Pages or a free Hugging Face Static Space. The Python implementation remains available for local CI verification.

## What this app does

- Accepts text input from the user and analyzes each submitted sample.
- Uses the DistilBERT sentiment model in the browser through Transformers.js.
- Displays confidence scores for each class.
- Triggers a visible alert when confidence crosses a user-defined threshold.
- Stores a session event log with timestamps and lets users export CSV/JSON.

## Model and data

- Model: `distilbert-base-uncased-finetuned-sst-2-english`
- Source: Hugging Face model hub
- Input data: user-provided text only (no uploaded dataset)

## How it works

1. User enters text in the UI.
2. Transformers.js downloads the tokenizer and model in the browser and runs text classification locally.
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

The workflow file [`.github/workflows/deploy-huggingface.yml`](.github/workflows/deploy-huggingface.yml) verifies the Python implementation and deploys the static app to a free Hugging Face Space.
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

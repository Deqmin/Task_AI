---
title: Live Pointer Movement Analyzer
emoji: "📈"
colorFrom: blue
colorTo: green
sdk: static
app_file: index.html
pinned: false
---

# Live Pointer Movement Analyzer

A browser app that captures pointer movement, calculates speed and jitter, produces an anomaly score, and keeps an exportable movement log.

## Live demo URL

Set this after creating the Space:
- Hugging Face Space: https://huggingface.co/spaces/deqmin/live-sentiment-stream-analyzer
- GitHub Pages project page: https://deqmin.github.io/Task_AI/

The static app runs on GitHub Pages or a free Hugging Face Static Space. The Python implementation remains available for local CI verification.

## What this app does

- Tracks pointer movement after the user clicks Start tracking.
- Calculates speed and jitter from recent pointer samples.
- Produces a visible anomaly score with a user-controlled alert threshold.
- Stores timestamped movement samples and lets users export JSON.

## Model and data

- Method: browser-side movement feature extraction; no downloaded model is required.
- Input data: pointer coordinates and timing only; no text, camera, or uploaded dataset.

## How it works

1. User clicks Start tracking and moves the pointer.
2. The browser records coordinate changes and elapsed time between samples.
3. Average speed and speed-change jitter are combined into an anomaly score.
4. The threshold control raises an alert when the score is high.
5. Movement events are appended to an in-memory log and can be downloaded as JSON.

## Limitations

- This is a lightweight heuristic, not a trained bot-detection model.
- Trackpads, high-DPI displays, browser throttling, and accessibility tools can affect measurements.
- Scores are session-relative indicators and are not calibrated probabilities.

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

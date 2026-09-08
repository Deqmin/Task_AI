---
title: Live Vision Object Detector
emoji: "📈"
colorFrom: blue
colorTo: green
sdk: static
app_file: index.html
pinned: false
---

# Live Vision Object Detector

A browser app that captures webcam frames, runs object detection with DETR through Transformers.js, draws bounding boxes and confidence scores, and keeps an exportable detection log.

## Live demo URL

Set this after creating the Space:
- Hugging Face Space: https://huggingface.co/spaces/deqmin/live-sentiment-stream-analyzer
- GitHub Pages project page: https://deqmin.github.io/Task_AI/

The static app runs on GitHub Pages or a free Hugging Face Static Space. The Python implementation remains available for local CI verification.

## What this app does

- Requests webcam access and analyzes one captured frame at a time.
- Uses `Xenova/detr-resnet-50` in the browser through Transformers.js.
- Draws detected object boxes and confidence labels over the camera frame.
- Filters detections with a user-controlled minimum confidence.
- Stores a timestamped detection log and lets users export JSON.

## Model and data

- Model: `Xenova/detr-resnet-50`
- Source: Hugging Face model hub
- Input data: webcam frames only; frames are processed in the browser.

## How it works

1. User grants camera permission and starts the webcam.
2. Transformers.js downloads the DETR model and runs object detection locally in the browser.
3. Detected objects are drawn with bounding boxes and confidence scores.
4. The minimum-confidence control filters low-confidence detections.
5. Detection events are appended to an in-memory log and can be downloaded as JSON.

## Limitations

- Camera permission is required; if access is denied, the UI shows an actionable error.
- Browser model downloads require network access and may be slow on first use.
- Detection confidence is not calibrated certainty and small or occluded objects may be missed.

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

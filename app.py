from __future__ import annotations

import csv
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import gradio as gr
from transformers import pipeline

MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
LABEL_MAP = {
    "POSITIVE": "Positive",
    "NEGATIVE": "Negative",
}

classifier = pipeline(
    task="text-classification",
    model=MODEL_NAME,
    return_all_scores=True,
)


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _normalize_scores(raw_output: Any) -> list[dict[str, float | str]]:
    if isinstance(raw_output, list) and raw_output and isinstance(raw_output[0], list):
        candidate_scores = raw_output[0]
    else:
        candidate_scores = raw_output

    normalized: list[dict[str, float | str]] = []
    for item in candidate_scores:
        label = str(item["label"])
        score = float(item["score"])
        pretty_label = LABEL_MAP.get(label, label.title())
        normalized.append({"label": pretty_label, "score": score})

    normalized.sort(key=lambda x: float(x["score"]), reverse=True)
    return normalized


def _build_export_files(log_events: list[dict[str, Any]]) -> tuple[str | None, str | None]:
    if not log_events:
        return None, None

    export_dir = Path(tempfile.mkdtemp(prefix="sentiment_log_"))
    csv_path = export_dir / "events.csv"
    json_path = export_dir / "events.json"

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=["timestamp", "text", "label", "confidence", "alert"],
        )
        writer.writeheader()
        writer.writerows(log_events)

    with json_path.open("w", encoding="utf-8") as json_file:
        json.dump(log_events, json_file, indent=2)

    return str(csv_path), str(json_path)


def _stats_markdown(log_events: list[dict[str, Any]]) -> str:
    total = len(log_events)
    if total == 0:
        return "**Session stats:** no events yet."

    positives = sum(1 for event in log_events if event["label"] == "Positive")
    negatives = sum(1 for event in log_events if event["label"] == "Negative")
    alerts = sum(1 for event in log_events if event["alert"])
    avg_conf = sum(float(event["confidence"]) for event in log_events) / total

    return (
        "**Session stats**\\n"
        f"- Total analyses: {total}\\n"
        f"- Positive: {positives} | Negative: {negatives}\\n"
        f"- Alerts triggered: {alerts}\\n"
        f"- Average confidence: {avg_conf:.2f}%"
    )


def analyze_text(
    text: str,
    threshold: float,
    alert_target: str,
    log_events: list[dict[str, Any]] | None,
) -> tuple[
    str,
    float,
    list[list[str | float]],
    str,
    list[list[str | float]],
    str,
    str | None,
    str | None,
    list[dict[str, Any]],
]:
    events = list(log_events or [])
    cleaned = (text or "").strip()

    if not cleaned:
        return (
            "Input required",
            0.0,
            [],
            "**Type some text to analyze sentiment.**",
            [
                [
                    event["timestamp"],
                    event["text"],
                    event["label"],
                    event["confidence"],
                    "Yes" if event["alert"] else "No",
                ]
                for event in events
            ],
            _stats_markdown(events),
            None,
            None,
            events,
        )

    raw_scores = classifier(cleaned, truncation=True)
    scores = _normalize_scores(raw_scores)

    top_label = str(scores[0]["label"])
    top_score = float(scores[0]["score"])
    confidence_pct = round(top_score * 100.0, 2)

    alert_hit = confidence_pct >= threshold * 100.0 and (
        alert_target == "Any" or alert_target == top_label
    )

    alert_message = (
        f"### ALERT: {top_label} confidence {confidence_pct:.2f}% crossed threshold"
        if alert_hit
        else "No alert. Confidence is below threshold or outside the selected target class."
    )

    event = {
        "timestamp": _utc_timestamp(),
        "text": cleaned[:120],
        "label": top_label,
        "confidence": confidence_pct,
        "alert": alert_hit,
    }
    events.append(event)

    score_rows = [[item["label"], round(float(item["score"]) * 100.0, 2)] for item in scores]
    log_rows = [
        [
            item["timestamp"],
            item["text"],
            item["label"],
            item["confidence"],
            "Yes" if item["alert"] else "No",
        ]
        for item in events
    ]

    csv_file, json_file = _build_export_files(events)

    return (
        top_label,
        confidence_pct,
        score_rows,
        alert_message,
        log_rows,
        _stats_markdown(events),
        csv_file,
        json_file,
        events,
    )


def clear_session() -> tuple[
    str,
    float,
    list[list[str | float]],
    str,
    list[list[str | float]],
    str,
    str | None,
    str | None,
    list[dict[str, Any]],
    str,
]:
    return (
        "",
        0.0,
        [],
        "Session cleared.",
        [],
        "**Session stats:** no events yet.",
        None,
        None,
        [],
        "",
    )


with gr.Blocks(title="Live Sentiment Stream Analyzer") as demo:
    gr.Markdown(
        """
        # Live Sentiment Stream Analyzer
        Enter text from any live source (keyboard, copied chat, call notes) and get model sentiment scores instantly.
        """
    )

    state = gr.State([])

    with gr.Row():
        text_input = gr.Textbox(
            label="Live text input",
            lines=4,
            placeholder="Type text here, then click Analyze",
        )

    with gr.Row():
        threshold_slider = gr.Slider(
            minimum=0.50,
            maximum=0.99,
            step=0.01,
            value=0.80,
            label="Alert threshold (confidence)",
        )
        alert_target = gr.Dropdown(
            choices=["Any", "Positive", "Negative"],
            value="Negative",
            label="Alert when predicted class is",
        )

    with gr.Row():
        analyze_button = gr.Button("Analyze", variant="primary")
        clear_button = gr.Button("Clear Session")

    with gr.Row():
        label_output = gr.Textbox(label="Top class")
        confidence_output = gr.Number(label="Top confidence (%)", precision=2)

    score_table = gr.Dataframe(
        headers=["Class", "Confidence (%)"],
        datatype=["str", "number"],
        row_count=(2, "fixed"),
        col_count=(2, "fixed"),
        label="Model scores",
    )

    alert_output = gr.Markdown("No alert yet.")

    log_table = gr.Dataframe(
        headers=["Timestamp", "Text sample", "Class", "Confidence (%)", "Alert"],
        datatype=["str", "str", "str", "number", "str"],
        label="Event log",
    )

    stats_output = gr.Markdown("**Session stats:** no events yet.")

    with gr.Row():
        csv_download = gr.File(label="Download CSV log")
        json_download = gr.File(label="Download JSON log")

    with gr.Accordion("How it works", open=False):
        gr.Markdown(
            f"""
            - Model: `{MODEL_NAME}` (binary sentiment classifier from Hugging Face Transformers).
            - Pipeline: input text -> tokenizer -> model inference -> class probabilities.
            - Confidence is the highest class probability shown as a percentage.
            - Limits: this model may misread sarcasm, domain-specific jargon, multilingual text, and very short phrases.
            """
        )

    analyze_button.click(
        fn=analyze_text,
        inputs=[text_input, threshold_slider, alert_target, state],
        outputs=[
            label_output,
            confidence_output,
            score_table,
            alert_output,
            log_table,
            stats_output,
            csv_download,
            json_download,
            state,
        ],
    )

    clear_button.click(
        fn=clear_session,
        inputs=[],
        outputs=[
            label_output,
            confidence_output,
            score_table,
            alert_output,
            log_table,
            stats_output,
            csv_download,
            json_download,
            state,
            text_input,
        ],
    )


if __name__ == "__main__":
    demo.launch()

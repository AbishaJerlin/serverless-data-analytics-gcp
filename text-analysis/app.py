from flask import Flask, request, jsonify
from analysis_core import (
    word_frequency_top20_from_text,
    sentence_start_top10_from_text,
    sentence_length_stats_from_text,
)

app = Flask(__name__)

@app.get("/")
def home():
    return "COMM034 Task A2: Text analysis API running."

@app.post("/analyse")
def analyse():
    # Choose analyses via query parameters (true/false)
    run_freq = request.args.get("freq", "true").lower() == "true"
    run_starts = request.args.get("starts", "true").lower() == "true"
    run_lengths = request.args.get("lengths", "true").lower() == "true"

    # Accept either an uploaded file (multipart/form-data) OR raw text in JSON
    text = None

    if request.content_type and "multipart/form-data" in request.content_type:
        if "file" not in request.files:
            return jsonify({"error": "Upload a file using form-data key 'file'"}), 400
        f = request.files["file"]
        text = f.read().decode("utf-8", errors="ignore")
    else:
        data = request.get_json(silent=True) or {}
        text = data.get("text")

    if not text:
        return jsonify({"error": "Provide either a file upload or JSON body with {\"text\": \"...\"}"}), 400

    result = {
        "selected": {"freq": run_freq, "starts": run_starts, "lengths": run_lengths}
    }

    if run_freq:
        result["top20_words"] = word_frequency_top20_from_text(text)
    if run_starts:
        result["top10_sentence_starts"] = sentence_start_top10_from_text(text)
    if run_lengths:
        result["sentence_length_stats"] = sentence_length_stats_from_text(text)

    return jsonify(result)

if __name__ == "__main__":
    # Local run
    app.run(host="0.0.0.0", port=8080)

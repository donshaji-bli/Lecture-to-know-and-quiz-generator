from __future__ import annotations

import re
from collections import Counter

from flask import Flask, render_template, request

app = Flask(__name__)

STOP_WORDS = {
    "about", "after", "again", "also", "among", "because", "been", "before",
    "being", "between", "both", "could", "does", "during", "each", "from",
    "have", "into", "more", "most", "other", "over", "same", "should",
    "some", "such", "than", "that", "their", "there", "these", "they",
    "this", "those", "through", "under", "very", "what", "when", "where",
    "which", "while", "with", "would", "your", "will", "were", "them",
    "then", "only", "used", "using", "lecture", "topic", "concept",
}


def sentences_from(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if len(s.split()) >= 5]


def analyze_lecture(text: str) -> tuple[list[str], list[dict]]:
    sentences = sentences_from(text)
    words = re.findall(r"[A-Za-z][A-Za-z'-]{2,}", text.lower())
    frequencies = Counter(w for w in words if w not in STOP_WORDS)
    ranked = sorted(
        enumerate(sentences),
        key=lambda item: sum(frequencies[w.lower()] for w in re.findall(r"[A-Za-z][A-Za-z'-]{2,}", item[1])) / max(len(item[1].split()), 1),
        reverse=True,
    )
    key_points = [sentence for _, sentence in sorted(ranked[: min(5, len(ranked))])]

    terms = [word for word, _ in frequencies.most_common(12)]
    quiz = []
    for sentence in sentences:
        candidates = [w for w in re.findall(r"\b[A-Za-z][A-Za-z'-]{3,}\b", sentence) if w.lower() in frequencies and w.lower() not in STOP_WORDS]
        if not candidates:
            continue
        answer = max(candidates, key=lambda w: frequencies[w.lower()])
        distractors = [w for w in terms if w.lower() != answer.lower() and w.lower() not in sentence.lower()]
        options = [answer] + distractors[:3]
        if len(options) < 2:
            continue
        quiz.append({"prompt": re.sub(re.escape(answer), "_____", sentence, count=1, flags=re.IGNORECASE), "answer": answer, "options": options})
        if len(quiz) == 5:
            break
    return key_points, quiz


@app.route("/", methods=["GET", "POST"])
def index():
    text = request.form.get("lecture", "")
    key_points: list[str] = []
    quiz: list[dict] = []
    if request.method == "POST" and text.strip():
        key_points, quiz = analyze_lecture(text.strip())
    return render_template("index.html", lecture=text, key_points=key_points, quiz=quiz)


if __name__ == "__main__":
    app.run(debug=True)

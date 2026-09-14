from __future__ import annotations

import re
from collections import Counter
from statistics import mean, median, stdev
from typing import List, Tuple, Dict, Any

# Stop words list (from coursework handout Figure 1)
STOP_WORDS = {
    "i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves",
    "he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves",
    "what","which","who","whom","this","that","these","those",
    "am","is","are","was","were","be","been","being",
    "have","has","had","having","do","does","did","doing",
    "a","an","the","and","but","if","or","because","as","until","while",
    "of","at","by","for","with","about","against","between","into","through","during","before","after","above","below",
    "to","from","up","down","in","out","on","off","over","under",
    "again","further","then","once","here","there","when","where","why","how",
    "all","any","both","each","few","more","most","other","some","such",
    "no","nor","not","only","own","same","so","than","too","very",
    "s","t","can","will","just","don","should","now"
}

WORD_RE = re.compile(r"[a-z]+")
SENT_SPLIT_RE = re.compile(r"[.!?]+")


def _word_tokens(text: str) -> List[str]:
    """Lowercase and extract alphabetic word tokens."""
    return WORD_RE.findall(text.lower())


def _sentences(text: str) -> List[str]:
    """Split into sentences using a simple punctuation heuristic."""
    raw = SENT_SPLIT_RE.split(text)
    return [s.strip() for s in raw if s and s.strip()]


def word_frequency_top20_from_text(text: str) -> List[Tuple[str, int]]:
    """Top 20 most frequent words excluding STOP_WORDS."""
    tokens = [w for w in _word_tokens(text) if w not in STOP_WORDS]
    counts = Counter(tokens)
    items = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    return items[:20]


def sentence_start_top10_from_text(text: str) -> List[Tuple[str, int]]:
    """Top 10 most common first words of sentences (excluding STOP_WORDS)."""
    starts: List[str] = []
    for s in _sentences(text):
        toks = _word_tokens(s)
        if not toks:
            continue
        first = toks[0]
        if first in STOP_WORDS:
            continue
        starts.append(first)

    counts = Counter(starts)
    items = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    return items[:10]


def sentence_length_stats_from_text(text: str) -> Dict[str, Any]:
    """Mean, median, stdev of sentence lengths measured in word tokens."""
    lengths: List[int] = []
    for s in _sentences(text):
        toks = _word_tokens(s)
        if toks:
            lengths.append(len(toks))

    if not lengths:
        return {"mean": 0.0, "median": 0.0, "stdev": 0.0, "n_sentences": 0}

    sd = stdev(lengths) if len(lengths) >= 2 else 0.0
    return {
        "mean": float(mean(lengths)),
        "median": float(median(lengths)),
        "stdev": float(sd),
        "n_sentences": int(len(lengths)),
    }

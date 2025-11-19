"""
corpus_ingestor.py

This module ingests the Agothean corpus (PDFs and other docs) and extracts structured constraints and knowledge entries for the Agothe Panel.
It reads PDF files from the /corpus directory or designated sources, parses them into text, classifies lines into categories (laws, equations, protocol, narrative, etc.), and writes a JSON file capturing the extracted information.

The extraction is intentionally simple and deterministic, without external dependencies; it is a placeholder for more advanced NLP pipelines to be added later.
"""

import os
import json
import re
from typing import Dict, List, Any


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract raw text from a PDF file. This placeholder returns an empty string.
    In production you might use pdfminer.six or another library to extract text.
    """
    # PDF extraction not implemented; returning empty string
    return ""


def classify_line(line: str) -> str:
    """
    Classify a line of text into a category such as 'equation', 'protocol', 'law', or 'narrative'.
    This simplistic classifier uses heuristics: lines containing '=' are equations, lines ending with ':' are protocol headings, etc.
    """
    if '=' in line:
        return "equation"
    if line.strip().endswith(':'):
        return "protocol"
    # Heuristic: lines starting with two capitalized words are treated as laws or headings
    if re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+', line):
        return "law"
    return "narrative"


def parse_document(text: str) -> List[Dict[str, Any]]:
    """
    Parse the extracted text into a list of constraint entries.
    Each entry is a dict with 'type' and 'content'.
    """
    entries: List[Dict[str, Any]] = []
    for line in text.splitlines():
        cat = classify_line(line)
        entries.append({"type": cat, "content": line})
    return entries


def ingest_corpus(corpus_dir: str) -> Dict[str, Any]:
    """
    Ingest all files in a directory and return a dictionary keyed by file name.
    PDF files are passed through extract_text_from_pdf, while text/markdown files are read directly.
    """
    corpus: Dict[str, Any] = {}
    if not os.path.isdir(corpus_dir):
        return corpus
    for filename in os.listdir(corpus_dir):
        if not filename.lower().endswith((".pdf", ".txt", ".md")):
            continue
        path = os.path.join(corpus_dir, filename)
        try:
            if filename.lower().endswith(".pdf"):
                text = extract_text_from_pdf(path)
            else:
                with open(path, 'r', errors='ignore') as f:
                    text = f.read()
        except Exception:
            text = ""
        corpus[filename] = parse_document(text)
    return corpus


def save_corpus(corpus: Dict[str, Any], output_path: str) -> None:
    """
    Save the ingested corpus dictionary to JSON.
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(corpus, f, indent=2)
    except Exception as e:
        print(f"Failed to save corpus: {e}")


if __name__ == "__main__":
    """
    Command-line entry point. Use environment variables to set directories.
    """
    corpus_dir = os.environ.get("AGOTHE_CORPUS_DIR", "./corpus")
    output = os.environ.get("AGOTHE_CORPUS_OUTPUT", "./state/corpus.json")
    corpus = ingest_corpus(corpus_dir)
    save_corpus(corpus, output)
    print(f"Ingested corpus from {corpus_dir} and saved to {output}")

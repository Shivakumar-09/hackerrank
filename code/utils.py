import pandas as pd
import re
import os
from pathlib import Path

def clean_text(text):
    if not text:
        return ""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', str(text))
    # Remove excessive punctuation
    text = re.sub(r'[^\w\s\$\.]', ' ', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def chunk_text(text, chunk_size=300):
    if not text:
        return []
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def load_csv(path):
    """Load CSV with safety for Path objects and encoding."""
    if Path(path).exists():
        return pd.read_csv(path, encoding='utf-8')
    return pd.DataFrame()

def save_csv(df, path):
    """Save CSV with safety for Path objects and UTF-8 encoding."""
    path = Path(path)
    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding='utf-8')

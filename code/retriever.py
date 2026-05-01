import os
import pandas as pd
import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import DATA_DIR, SAMPLE_CSV, RETRIEVAL_THRESHOLD
from utils import clean_text, chunk_text

class AdvancedRetriever:
    def __init__(self):
        self.vectorizers = {} # Per-company vectorizers
        self.corpora = {}     # Per-company passages
        self.metadata = {}    # Per-company metadata
        
    def build_index(self):
        companies = ["HackerRank", "Claude", "Visa", "Unknown"]
        for co in companies:
            self.corpora[co] = []
            self.metadata[co] = []
            
        # 1. Load data/ files (Company Filtered)
        for co_folder in ["hackerrank", "claude", "visa"]:
            co_path = DATA_DIR / co_folder
            target_co = co_folder.capitalize() if co_folder != "hackerrank" else "HackerRank"
            
            if co_path.exists():
                for ext in ["*.txt", "*.md", "*.html", "*.json", "*.csv"]:
                    for file_path in co_path.rglob(ext):
                        try:
                            content = ""
                            if file_path.suffix in ['.txt', '.md', '.html']:
                                content = file_path.read_text(encoding='utf-8', errors='ignore')
                            elif file_path.suffix == '.json':
                                content = str(json.loads(file_path.read_text(encoding='utf-8')))
                            elif file_path.suffix == '.csv':
                                df = pd.read_csv(file_path, encoding='utf-8')
                                content = " ".join(df.astype(str).values.flatten())
                            
                            if content:
                                clean = clean_text(content)
                                chunks = chunk_text(clean)
                                for chunk in chunks:
                                    self.corpora[target_co].append(chunk)
                                    self.metadata[target_co].append({"source": file_path.name, "type": "corpus"})
                        except:
                            continue

        # 2. Load Sample CSV (Company Filtered)
        if SAMPLE_CSV.exists():
            try:
                df = pd.read_csv(SAMPLE_CSV, encoding='utf-8')
                for _, row in df.iterrows():
                    co = str(row.get("Company", "Unknown"))
                    if co not in self.corpora:
                        self.corpora[co] = []
                        self.metadata[co] = []
                    
                    text = clean_text(f"{row.get('Subject', '')} {row.get('Issue', '')}")
                    self.corpora[co].append(text)
                    self.metadata[co].append({
                        "source": "sample_csv",
                        "type": "sample",
                        "response": row.get("Response", ""),
                        "area": row.get("Product Area", "general_support")
                    })
            except:
                pass

        # 3. Fit Vectorizers with Bigrams + Unigrams (v3 Requirement)
        for co in self.corpora:
            if self.corpora[co]:
                vec = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
                matrix = vec.fit_transform(self.corpora[co])
                self.vectorizers[co] = (vec, matrix)

    def retrieve(self, query, company, top_n=3):
        if company not in self.vectorizers:
            return []
            
        vec, matrix = self.vectorizers[company]
        query_vec = vec.transform([clean_text(query)])
        sims = cosine_similarity(query_vec, matrix).flatten()
        
        top_indices = sims.argsort()[::-1]
        results = []
        seen_texts = set()
        
        for idx in top_indices:
            if sims[idx] < RETRIEVAL_THRESHOLD:
                break
            
            text = self.corpora[company][idx]
            # De-duplicate by first 100 chars
            text_preview = text[:100]
            if text_preview in seen_texts:
                continue
                
            seen_texts.add(text_preview)
            results.append({
                "text": text,
                "score": float(sims[idx]),
                "meta": self.metadata[company][idx]
            })
            if len(results) >= top_n:
                break
                
        return results

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

class TicketRetriever:
    def __init__(self, sample_path="sample_support_tickets.csv"):
        self.sample_path = sample_path
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.is_fitted = False
        self.df = None
        self.tfidf_matrix = None
        self._load_and_fit()
        
    def _load_and_fit(self):
        if not os.path.exists(self.sample_path):
            return
            
        self.df = pd.read_csv(self.sample_path)
        if len(self.df) == 0:
            return
            
        subject_col = 'Subject' if 'Subject' in self.df.columns else 'subject'
        issue_col = 'Issue' if 'Issue' in self.df.columns else 'issue'
        
        self.df['combined_text'] = self.df[subject_col].fillna('') + " " + self.df[issue_col].fillna('')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['combined_text'])
        self.is_fitted = True

    def retrieve_similar(self, subject, issue, top_n=3):
        if not self.is_fitted:
            return []
            
        query_text = str(subject) + " " + str(issue)
        if not query_text.strip():
            return []
            
        query_vec = self.vectorizer.transform([query_text])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        top_indices = similarities.argsort()[-top_n:][::-1]
        
        results = []
        for idx in top_indices:
            sim = similarities[idx]
            if sim > 0.05:
                row = self.df.iloc[idx]
                results.append({
                    "similarity": sim,
                    "status": row.get('Status', row.get('status', 'replied')),
                    "product_area": row.get('Product Area', row.get('product_area', 'general_support')),
                    "request_type": row.get('Request Type', row.get('request_type', 'product_issue')),
                    "company": row.get('Company', row.get('company', '')),
                    "response": row.get('Response', row.get('response', ''))
                })
        return results

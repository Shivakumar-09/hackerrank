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
        
    def _create_dummy_data(self):
        # Create a dummy dataset if missing
        data = [
            {"subject": "Payment issue", "issue": "I got charged twice for my Visa card.", "company": "Visa", "status": "Open", "product_area": "Billing", "request_type": "Refund"},
            {"subject": "Code not compiling", "issue": "The python compiler is giving an error on my assessment.", "company": "HackerRank", "status": "Closed", "product_area": "Assessment", "request_type": "Technical"},
            {"subject": "Subscription model", "issue": "How do I upgrade my Claude AI chat subscription?", "company": "Claude", "status": "Closed", "product_area": "Account", "request_type": "Upgrade"},
            {"subject": "Fraudulent transaction", "issue": "Unauthorized payment on my card.", "company": "Visa", "status": "Escalated", "product_area": "Security", "request_type": "Fraud"}
        ]
        df = pd.DataFrame(data)
        df.to_csv(self.sample_path, index=False)
        return df

    def _load_and_fit(self):
        if not os.path.exists(self.sample_path):
            self.df = self._create_dummy_data()
        else:
            self.df = pd.read_csv(self.sample_path)
            
        if len(self.df) == 0:
            return
            
        # Combine subject and issue for vectorization
        self.df['combined_text'] = self.df.get('Subject', self.df.get('subject', pd.Series(dtype=str))).fillna('') + " " + self.df.get('Issue', self.df.get('issue', pd.Series(dtype=str))).fillna('')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['combined_text'])
        self.is_fitted = True

    def retrieve_similar(self, subject, issue, top_n=3):
        if not self.is_fitted:
            return []
            
        query_text = str(subject) + " " + str(issue)
        query_vec = self.vectorizer.transform([query_text])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        top_indices = similarities.argsort()[-top_n:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1: # Threshold
                row = self.df.iloc[idx]
                results.append({
                    "similarity": similarities[idx],
                    "status": row.get('Status', row.get('status', 'Open')),
                    "product_area": row.get('Product Area', row.get('product_area', 'General')),
                    "request_type": row.get('Request Type', row.get('request_type', 'Support')),
                    "company": row.get('Company', row.get('company', '')),
                    "response": row.get('Response', row.get('response', ''))
                })
        return results

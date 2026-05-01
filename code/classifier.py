from rules import BUG_KEYWORDS, FEATURE_KEYWORDS, INVALID_KEYWORDS, COMPANY_KEYWORDS, PRODUCT_AREA_MAP
from config import REQ_BUG, REQ_FEATURE_REQUEST, REQ_INVALID, REQ_PRODUCT_ISSUE
from utils import clean_text

def resolve_company(text):
    text_lower = str(text).lower()
    scores = {company: 0 for company in COMPANY_KEYWORDS}
    for company, keywords in COMPANY_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                scores[company] += 1
    
    if max(scores.values()) == 0:
        return "Unknown"
    return max(scores, key=scores.get)

def detect_intent(text):
    text_lower = str(text).lower()
    
    if any(kw in text_lower for kw in INVALID_KEYWORDS):
        return REQ_INVALID
        
    if any(kw in text_lower for kw in BUG_KEYWORDS):
        return REQ_BUG
        
    if any(kw in text_lower for kw in FEATURE_KEYWORDS):
        return REQ_FEATURE_REQUEST
        
    return REQ_PRODUCT_ISSUE

def map_product_area(text, company):
    text_clean = clean_text(text).lower()
    if company not in PRODUCT_AREA_MAP:
        return "general_support"
    
    mapping = PRODUCT_AREA_MAP[company]
    best_area = "general_support"
    max_score = 0
    
    for area, keywords in mapping.items():
        score = 0
        for kw in keywords:
            if kw.lower() in text_clean:
                # Weighted score: longer keywords match higher
                score += len(kw) 
        
        if score > max_score:
            max_score = score
            best_area = area
            
    return best_area

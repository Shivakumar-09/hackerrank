import random

COMPANY_KEYWORDS = {
    "HackerRank": ["assessment", "coding challenge", "compiler", "submission", "candidate", "test case", "hackerrank"],
    "Claude": ["ai chat", "conversation", "prompt", "subscription", "anthropic", "model", "claude"],
    "Visa": ["payment", "card", "refund", "merchant", "transaction", "charge", "visa"]
}

ESCALATION_KEYWORDS = [
    "fraud", "unauthorized charge", "duplicate payment", "stolen card", 
    "security vulnerability", "privacy breach", "harassment", "legal complaint", 
    "threats", "account hacked", "identity lockout", "admin abuse", "high-risk"
]

BUG_KEYWORDS = [
    "error", "issue", "failed", "broken", "timeout", "not loading", "crash", "unable to submit", "problem"
]

FEATURE_REQUEST_KEYWORDS = [
    "please add", "can you add", "request feature", "enhancement", "would like", "suggestion", "need option"
]

PRODUCT_AREAS = {
    "account_access": ["login", "password", "access", "hacked", "lockout", "account"],
    "billing": ["charge", "refund", "payment", "invoice", "price", "billing"],
    "fraud_security": ["fraud", "stolen", "unauthorized", "security", "vulnerability", "breach"],
    "assessments": ["test", "assessment", "compiler", "coding", "submission", "challenge"],
    "subscription": ["plan", "subscription", "upgrade", "cancel", "membership"],
    "developer_tools": ["api", "webhook", "integration", "sdk", "developer"],
    "performance": ["slow", "lag", "timeout", "latency", "loading"],
    "permissions": ["admin", "role", "permission", "access level", "team member"],
    "trust_safety": ["harassment", "abuse", "trust", "safety", "threat"],
    "general_support": ["help", "question", "support", "info"]
}

# Rotating Response Templates
RESPONSES = {
    "Visa": [
        "Please contact your issuing bank or Visa support for immediate assistance regarding your transaction.",
        "We recommend reviewing your recent Visa statement. If this transaction is unrecognized, contact support immediately.",
        "For payment disputes or refund status on your Visa card, please reach out to our dedicated billing team."
    ],
    "HackerRank": [
        "Please try clearing your browser cache and retrying your HackerRank assessment session.",
        "If the compiler issue persists, ensure your code matches the expected input/output format of the challenge.",
        "Your HackerRank assessment progress is saved. If you face further technical blocks, please contact support."
    ],
    "Claude": [
        "Please check your Claude subscription status in your account dashboard for model access details.",
        "If you are facing prompt errors, try rephrasing your query or checking our AI safety guidelines.",
        "For Claude API or chat conversation issues, please review your current usage limits and billing tier."
    ],
    "General": [
        "Thank you for contacting support. Our team is investigating your request and will follow up shortly.",
        "We have received your inquiry. A support specialist will be assigned to your ticket soon.",
        "Thank you for reaching out. Please provide any additional screenshots or details if available."
    ],
    "Escalation": [
        "Your request involves sensitive or high-risk indicators and has been escalated for priority manual review.",
        "Due to the nature of this issue, a specialist has been assigned to investigate your case with priority.",
        "This matter requires manual intervention by our security and compliance team. We have escalated your ticket."
    ],
    "Invalid": [
        "Your request appears to be malformed or irrelevant to our support domains. Please provide more context.",
        "We are unable to process this request as it lacks sufficient detail. Please try again with more information.",
        "This message has been flagged as out-of-scope for our support channels."
    ]
}

def infer_company(text):
    if not text: return None
    text_lower = str(text).lower()
    scores = {company: 0 for company in COMPANY_KEYWORDS}
    for company, keywords in COMPANY_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                scores[company] += 1
    
    best_company = max(scores, key=scores.get)
    return best_company if scores[best_company] > 0 else None

def check_escalation(text):
    if not text: return False, None
    text_lower = str(text).lower()
    for kw in ESCALATION_KEYWORDS:
        if kw in text_lower:
            return True, kw
    return False, None

def detect_request_type(text):
    text_lower = str(text).lower()
    
    # Check for invalid/spam
    if len(text_lower.strip()) < 10 or text_lower.count(' ') < 1:
        return "invalid"
        
    for kw in FEATURE_REQUEST_KEYWORDS:
        if kw in text_lower:
            return "feature_request"
            
    for kw in BUG_KEYWORDS:
        if kw in text_lower:
            return "bug"
            
    return "product_issue"

def get_product_area_from_keywords(text):
    text_lower = str(text).lower()
    scores = {area: 0 for area in PRODUCT_AREAS}
    for area, keywords in PRODUCT_AREAS.items():
        for kw in keywords:
            if kw in text_lower:
                scores[area] += 2 # Keyword matches carry high weight
    
    best_area = max(scores, key=scores.get)
    return best_area if scores[best_area] > 0 else "general_support"

def get_polished_response(company, status, request_type):
    if request_type == "invalid":
        return random.choice(RESPONSES["Invalid"])
    
    if status == "escalated":
        return random.choice(RESPONSES["Escalation"])
    
    if company in RESPONSES:
        return random.choice(RESPONSES[company])
    
    return random.choice(RESPONSES["General"])

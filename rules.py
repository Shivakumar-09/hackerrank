import random

COMPANY_KEYWORDS = {
    "HackerRank": ["assessment", "coding challenge", "compiler", "submission", "candidate", "test case", "hackerrank", "invite", "invited", "candidate"],
    "Claude": ["ai chat", "conversation", "prompt", "subscription", "anthropic", "model", "claude", "ai", "claude.ai"],
    "Visa": ["payment", "card", "refund", "merchant", "transaction", "charge", "visa", "debit", "credit"]
}

ESCALATION_KEYWORDS = [
    "fraud", "unauthorized charge", "duplicate payment", "stolen card", 
    "security vulnerability", "privacy breach", "harassment", "legal complaint", 
    "threats", "account hacked", "identity lockout", "admin abuse", "high-risk"
]

BUG_KEYWORDS = [
    "error", "issue", "failed", "broken", "timeout", "not loading", "crash", "unable to submit", "problem", "disabled"
]

FEATURE_REQUEST_KEYWORDS = [
    "please add", "can you add", "request feature", "enhancement", "would like", "suggestion", "need option"
]

# Approved Categories
APPROVED_AREAS = [
    "account_access", "billing", "fraud_security", "assessments", 
    "subscription", "developer_tools", "performance", "permissions", 
    "trust_safety", "general_support"
]

def infer_company(text):
    if not text: return "HackerRank" # Default fallback for empty text
    text_lower = str(text).lower()
    scores = {company: 0 for company in COMPANY_KEYWORDS}
    for company, keywords in COMPANY_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                scores[company] += 1
    
    # If no keywords found, look for general domain hints
    if max(scores.values()) == 0:
        if any(x in text_lower for x in ["test", "code", "compiler", "invite"]): return "HackerRank"
        if any(x in text_lower for x in ["chat", "ai", "model", "prompt"]): return "Claude"
        if any(x in text_lower for x in ["pay", "card", "charge", "bank"]): return "Visa"
        return "HackerRank" # Final deterministic fallback
    
    return max(scores, key=scores.get)

def map_product_area(raw_area):
    if not raw_area: return "general_support"
    ra = str(raw_area).lower().replace(" ", "_")
    
    # Specific Mappings
    if "privacy" in ra: return "trust_safety"
    if "screen" in ra: return "performance"
    if "travel_support" in ra: return "general_support"
    
    # Keyword based matching for approved categories
    if any(x in ra for x in ["bill", "pay", "charge", "refund"]): return "billing"
    if any(x in ra for x in ["account", "login", "access", "password"]): return "account_access"
    if any(x in ra for x in ["fraud", "security", "threat", "risk"]): return "fraud_security"
    if any(x in ra for x in ["assess", "test", "compiler", "coding"]): return "assessments"
    if any(x in ra for x in ["sub", "plan", "membership"]): return "subscription"
    if any(x in ra for x in ["dev", "api", "webhook", "tool"]): return "developer_tools"
    if any(x in ra for x in ["slow", "lag", "load", "perf"]): return "performance"
    if any(x in ra for x in ["perm", "role", "admin"]): return "permissions"
    if any(x in ra for x in ["trust", "safe", "abus"]): return "trust_safety"
    
    # Direct match check
    for area in APPROVED_AREAS:
        if area in ra: return area
        
    return "general_support"

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

def check_escalation(text):
    if not text: return False, None
    text_lower = str(text).lower()
    for kw in ESCALATION_KEYWORDS:
        if kw in text_lower:
            return True, kw
    return False, None

def detect_request_type(text):
    text_lower = str(text).lower()
    if len(text_lower.strip()) < 10: return "invalid"
        
    for kw in FEATURE_REQUEST_KEYWORDS:
        if kw in text_lower: return "feature_request"
            
    for kw in BUG_KEYWORDS:
        if kw in text_lower: return "bug"
            
    return "product_issue"

def get_polished_response(company, status, request_type):
    if request_type == "invalid": return random.choice(RESPONSES["Invalid"])
    if status == "escalated": return random.choice(RESPONSES["Escalation"])
    if company in RESPONSES: return random.choice(RESPONSES[company])
    return random.choice(RESPONSES["General"])

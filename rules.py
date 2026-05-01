COMPANY_KEYWORDS = {
    "HackerRank": ["assessment", "compiler", "challenge", "coding test", "submission"],
    "Claude": ["subscription", "model", "ai chat", "prompt", "conversation"],
    "Visa": ["card", "payment", "transaction", "charge", "refund", "merchant"]
}

ESCALATION_KEYWORDS = [
    "fraud", "duplicate charge", "unauthorized payment", "hacked account", 
    "security issue", "privacy breach", "lawsuit", "harassment", 
    "identity lockout", "admin abuse", "uncertain high-risk issue"
]

COMPANY_RESPONSES = {
    "Visa": "Please contact Visa support or your issuing bank for further assistance regarding your transaction.",
    "HackerRank": "Please retry your assessment session. If the issue persists, contact technical support.",
    "Claude": "Please review account settings and subscription details in your dashboard."
}

def infer_company(text):
    if not text:
        return None
    text_lower = str(text).lower()
    best_company = None
    max_matches = 0
    
    for company, keywords in COMPANY_KEYWORDS.items():
        matches = sum(1 for kw in keywords if kw.lower() in text_lower)
        if matches > max_matches:
            max_matches = matches
            best_company = company
            
    return best_company

def check_escalation(text):
    if not text:
        return False, None
    text_lower = str(text).lower()
    for kw in ESCALATION_KEYWORDS:
        if kw.lower() in text_lower:
            return True, kw
    return False, None

def get_response(company, escalated=False):
    if escalated:
        return "Your ticket has been escalated for manual review by our specialized support team."
    
    if company in COMPANY_RESPONSES:
        return COMPANY_RESPONSES[company]
    
    return "Thank you for reaching out. Our support team will get back to you shortly."

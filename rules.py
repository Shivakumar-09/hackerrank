COMPANY_KEYWORDS = {
    "HackerRank": ["assessment", "coding challenge", "compiler", "submission", "test case"],
    "Claude": ["ai chat", "subscription", "conversation", "prompt", "model", "anthropic"],
    "Visa": ["card", "payment", "charge", "merchant", "refund", "transaction"]
}

ESCALATION_KEYWORDS = [
    "fraud", "unauthorized charge", "duplicate payment", "stolen card", 
    "charge dispute", "hacked account", "locked identity issue", 
    "security vulnerability", "privacy breach", "legal complaint", 
    "harassment", "threats", "admin abuse", "sensitive unknown issue"
]

PRODUCT_AREAS = [
    "account_access", "billing", "fraud_security", "assessments", 
    "subscription", "developer_tools", "performance", "permissions", 
    "trust_safety", "general_support"
]

def infer_company(text):
    if not text: return None
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
    if not text: return False, None
    text_lower = str(text).lower()
    for kw in ESCALATION_KEYWORDS:
        if kw.lower() in text_lower:
            return True, kw
    return False, None

def check_invalid(text):
    if not text or len(str(text).strip()) < 5:
         return True
    return False

def get_response(company, status="replied", is_invalid=False):
    if is_invalid:
        return "Your request appears to be out of scope or malformed. Please provide more details."
    if status == "escalated":
        return "Your ticket contains high-risk or sensitive elements and has been escalated to a specialized human agent for manual review."
    
    responses = {
        "Visa": "Please contact Visa support directly or your issuing bank for immediate assistance regarding your financial transaction.",
        "HackerRank": "Please retry your assessment session. If the compiler or submission issue persists, contact our technical support.",
        "Claude": "Please review your account settings and subscription details in the Claude dashboard. Ensure your prompt adheres to guidelines."
    }
    return responses.get(company, "Thank you for reaching out. Our support team is looking into your inquiry.")

def map_product_area(raw_area):
    if not raw_area: return "general_support"
    ra = str(raw_area).lower()
    if "bill" in ra or "pay" in ra or "charge" in ra or "refund" in ra: return "billing"
    if "fraud" in ra or "secur" in ra or "theft" in ra: return "fraud_security"
    if "assess" in ra or "test" in ra or "compil" in ra: return "assessments"
    if "subscrip" in ra or "plan" in ra: return "subscription"
    if "account" in ra or "login" in ra or "access" in ra: return "account_access"
    if "dev" in ra or "api" in ra or "tool" in ra: return "developer_tools"
    if "perform" in ra or "slow" in ra or "lag" in ra: return "performance"
    if "perm" in ra or "role" in ra or "admin" in ra: return "permissions"
    if "trust" in ra or "safe" in ra or "abus" in ra: return "trust_safety"
    
    for pa in PRODUCT_AREAS:
        if pa in ra: return pa
        
    return "general_support"

def map_request_type(raw_type):
    if not raw_type: return "product_issue"
    rt = str(raw_type).lower()
    if "bug" in rt or "error" in rt or "fail" in rt: return "bug"
    if "featur" in rt or "request" in rt or "add" in rt: return "feature_request"
    if "invalid" in rt or "spam" in rt: return "invalid"
    
    return "product_issue"

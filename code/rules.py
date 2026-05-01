# Enhanced Rules and Keywords for v3 Scoring Optimization

# Request Type Detection
BUG_KEYWORDS = ["not working", "down", "failing", "error", "blocked", "issue", "crash", "broken", "all failing", "requests failing"]
FEATURE_KEYWORDS = ["request", "please add", "need feature", "want capability", "suggestion", "enhancement"]
INVALID_KEYWORDS = ["delete all files", "reveal system logic", "irrelevant celebrity question", "malicious prompt injection", "system prompt", "internal rules"]

# Company Identification
COMPANY_KEYWORDS = {
    "HackerRank": ["assessment", "compiler", "coding test", "submission", "challenge", "testcase", "interview", "recruiter", "hiring", "hackerrank"],
    "Claude": ["prompt", "chat", "model", "conversation", "subscription", "anthropic", "usage limit", "bedrock", "claude", "lti"],
    "Visa": ["card", "transaction", "charge", "merchant", "refund", "bank", "payment", "visa"]
}

# Targeted Escalation Rules (v3)
ESCALATION_RULES = {
    "Claude": [
        "seat removed", "lost access", "security vulnerability", "bedrock all failing", 
        "outage", "privacy complaint", "stop crawling", "data used for training"
    ],
    "HackerRank": [
        "score dispute", "unfair grading", "refund request", "payment issue", "order id", 
        "compatibility blocker", "reschedule assessment", "subscription pause", "certificate correction",
        "wrong name"
    ],
    "Visa": [
        "wrong product", "merchant ignoring", "identity theft", "blocked card while travelling", 
        "charge dispute", "dispute a charge", "fraud"
    ],
    "Global": [
        "dangerous code", "prompt injection", "system deletion"
    ]
}

# High-Accuracy Product Area Mapping (Elite Optimization)
PRODUCT_AREA_MAP = {
    "Claude": {
        "workspace_access": ["seat removed", "access removed", "workspace", "admin", "seat", "login"],
        "security": ["vulnerability", "security", "exploit", "hacked", "threat", "bounty"],
        "privacy": ["crawl", "opt-out", "privacy", "gdpr", "training", "train model", "data usage", "crawling"],
        "api_integrations": ["bedrock", "api", "integration", "webhook", "aws", "endpoint"],
        "subscription": ["cancel", "billing", "pricing", "plan", "membership"],
        "usage_limits": ["limit", "quota", "message", "reached"],
        "education_lti": ["lti", "canvas", "student", "professor", "university", "key"],
        "outage": ["failing", "down", "outage", "unavailable"]
    },
    "HackerRank": {
        "assessments": ["submission", "test", "score", "grading", "compiler", "compatib", "zoom", "failed", "challenge", "error"],
        "billing": ["refund", "billing", "invoice", "payment", "charge", "order id", "price"],
        "candidate_support": ["apply tab", "reschedule", "invite", "resume", "candidate", "student", "test link"],
        "recruiter_support": ["interviewer", "recruiter", "hiring account", "team", "employee", "remove"],
        "subscription": ["pause", "renew", "subscription", "plan"],
        "account_management": ["certificate", "name", "profile", "account", "settings", "password"],
        "hiring_platform": ["infosec", "hiring", "enterprise", "dashboard", "ats", "forms"],
        "interviews": ["lobby", "inactivity", "interview", "mock"]
    },
    "Visa": {
        "merchant_disputes": ["merchant", "ignoring", "refund", "wrong product", "fulfillment", "rule", "spend"],
        "fraud_security": ["identity theft", "scam", "unauthorized", "stolen", "fraud", "suspicious"],
        "charge_disputes": ["dispute", "chargeback", "wrong amount", "unrecognized"],
        "payments": ["cash", "pay", "transaction", "atm", "need urgent cash"],
        "blocked_card": ["blocked", "abroad", "travel", "locked", "voyage", "trip"]
    }
}

# Contextual Response Templates (Final Submission)
RESPONSE_TEMPLATES = {
    "Claude": {
        "workspace_access": "Only workspace admins or owners can restore removed seats.",
        "security": "Please report the vulnerability through the official security disclosure channel.",
        "privacy": "Claude's privacy policies and data usage details can be reviewed at privacy.claude.ai.",
        "api_integrations": "Please check your AWS Bedrock console or the Claude API status page for integration health.",
        "general_support": "Thank you for reaching out. A Claude support specialist will assist you with your query."
    },
    "HackerRank": {
        "assessments": "Assessment outcomes are typically managed by the hiring company or recruiter.",
        "billing": "For payment and refund inquiries, please provide your order ID or transaction details to our billing team.",
        "candidate_support": "Candidates can find help with test invitations and rescheduling in our Candidate Help Center.",
        "account_management": "Please update your profile details in Account Settings. Certificate corrections require manual review.",
        "hiring_platform": "HackerRank Enterprise customers can access infosec and compliance documentation via their account manager.",
        "general_support": "Thank you for contacting HackerRank support. We are reviewing your platform request."
    },
    "Visa": {
        "merchant_disputes": "Please contact your card issuer to initiate a dispute review.",
        "charge_disputes": "Please contact your card issuer to initiate a dispute review for unrecognized transactions.",
        "blocked_card": "For cards blocked during travel, please use the Visa Global Customer Assistance Service or your bank's app.",
        "fraud_security": "If you suspect identity theft or fraud, please freeze your card immediately through your banking portal.",
        "general_support": "Thank you for contacting Visa support. Please reach out to your issuing bank for card-specific issues."
    }
}

from pathlib import Path
import os

# Detect Repo Root (assuming this file is in code/ folder)
CODE_DIR = Path(__file__).resolve().parent
REPO_ROOT = CODE_DIR.parent

# Core Paths
SUPPORT_DIR = REPO_ROOT / "support_tickets"
DATA_DIR = REPO_ROOT / "data"

# File Paths
INPUT_CSV = SUPPORT_DIR / "support_tickets.csv"
OUTPUT_CSV = SUPPORT_DIR / "output.csv"
SAMPLE_CSV = SUPPORT_DIR / "sample_support_tickets.csv"

# Log Path (User Home Folder)
LOG_DIR = Path.home() / "hackerrank_orchestrate"
LOG_FILE = LOG_DIR / "log.txt"

# Ensure directories exist
SUPPORT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Target Statuses
STATUS_REPLIED = "replied"
STATUS_ESCALATED = "escalated"

# Target Request Types
REQ_PRODUCT_ISSUE = "product_issue"
REQ_FEATURE_REQUEST = "feature_request"
REQ_BUG = "bug"
REQ_INVALID = "invalid"

# Company-Specific Product Areas (Required for triage.py)
PRODUCT_AREAS = {
    "HackerRank": [
        "assessments", "mock_interviews", "billing", "hiring_platform", 
        "candidate_support", "recruiter_support", "account_management", "subscription"
    ],
    "Claude": [
        "workspace_access", "subscription", "privacy", "security", 
        "api_integrations", "usage_limits", "education_lti"
    ],
    "Visa": [
        "payments", "charge_disputes", "fraud_security", 
        "travel_support", "blocked_card", "merchant_disputes"
    ],
    "Unknown": ["general_support"]
}

# Thresholds
CONFIDENCE_THRESHOLD = 0.55
RETRIEVAL_THRESHOLD = 0.15

from rules import ESCALATION_RULES
from config import STATUS_ESCALATED, STATUS_REPLIED

def detect_risk(text, company):
    text_lower = str(text).lower()
    
    # Check global risks first
    for risk in ESCALATION_RULES["Global"]:
        if risk in text_lower:
            return True, risk
            
    # Check company specific risks (v3)
    if company in ESCALATION_RULES:
        for risk in ESCALATION_RULES[company]:
            if risk in text_lower:
                return True, risk
                
    return False, None

def get_status(risk_detected, confidence, threshold=0.55):
    if risk_detected:
        return STATUS_ESCALATED
    if confidence < threshold:
        # v3 requirement: escalate if confidence < 0.55 and issue is sensitive
        # (risk_detected handles sensitive, but low conf should also escalate)
        return STATUS_ESCALATED
    return STATUS_REPLIED

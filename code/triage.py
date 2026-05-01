from classifier import resolve_company, detect_intent, map_product_area
from safety import detect_risk, get_status
from retriever import AdvancedRetriever
from rules import RESPONSE_TEMPLATES
from config import STATUS_ESCALATED, REQ_INVALID, PRODUCT_AREAS

class TriageEngine:
    def __init__(self):
        self.retriever = AdvancedRetriever()
        self.retriever.build_index()
        
    def process(self, row):
        subject = row.get("Subject", "")
        issue = row.get("Issue", "")
        company_input = row.get("Company", None)
        text = f"{subject} {issue}"
        
        # 1. Company Resolver
        company = company_input if company_input and str(company_input).lower() != "unknown" else resolve_company(text)
        
        # 2. Intent Detector
        intent = detect_intent(text)
        
        # 3. Risk Detector (v3)
        is_risky, risk_reason = detect_risk(text, company)
        
        # 4. Retrieval Engine (Company Filtered + Bigrams)
        hits = self.retriever.retrieve(text, company)
        
        # 5. Product Area Mapper (v3)
        area = map_product_area(text, company)
        
        # Boost mapping from high-similarity sample matches
        if hits and hits[0]["score"] > 0.6:
            if hits[0]["meta"]["type"] == "sample":
                sample_area = hits[0]["meta"].get("area")
                if company in PRODUCT_AREAS and sample_area in PRODUCT_AREAS[company]:
                    area = sample_area

        # 6. Confidence Scorer
        confidence = 0.5
        if hits:
            confidence = min(0.95, 0.45 + hits[0]["score"] * 0.5)
        if company != "Unknown":
            confidence += 0.05
        
        # 7. Decision (Status)
        status = get_status(is_risky, confidence)
        
        # 8. Response Composer (Contextual & Non-Repetitive)
        response = self._compose_response(status, intent, company, area, hits)
        
        # 9. Justification (High Quality Examples)
        justification = self._compose_justification(status, intent, company, area, risk_reason)
        
        return {
            "status": status,
            "product_area": area,
            "response": response,
            "justification": justification,
            "request_type": intent,
            "confidence": round(confidence, 2),
            "company": company,
            "hit_count": len(hits)
        }
        
    def _compose_response(self, status, intent, company, area, hits):
        if intent == REQ_INVALID:
            return "This request appears to be outside the supported scope of our triage system."
            
        # Use v3 templates first for better intelligence
        if company in RESPONSE_TEMPLATES and area in RESPONSE_TEMPLATES[company]:
            return RESPONSE_TEMPLATES[company][area]
            
        # If escalated, use area-specific handoff
        if status == STATUS_ESCALATED:
            return f"Thank you for contacting support. This request requires specialist review because it involves {area.replace('_', ' ')}."
            
        # Grounded response from retrieval if similarity is high
        if hits and hits[0]["score"] > 0.5:
            if hits[0]["meta"].get("response"):
                # Avoid the "delete conversation" instructions for irrelevant Claude rows
                if "delete conversation" in hits[0]["meta"]["response"].lower() and area != "privacy":
                    pass # Fall through to template
                else:
                    return hits[0]["meta"]["response"]
            
        # Fallback to general company template
        if company in RESPONSE_TEMPLATES:
            return RESPONSE_TEMPLATES[company].get("general_support", f"A {company} specialist will review your {area} request.")
            
        return f"Please review your {company} {area.replace('_', ' ')} settings or contact our support team."

    def _compose_justification(self, status, intent, company, area, risk_reason):
        if intent == REQ_INVALID:
            return "Detected malformed or irrelevant request. Marked invalid."
            
        if status == STATUS_ESCALATED:
            if risk_reason:
                return f"Detected {risk_reason} indicators. Escalated for specialist review."
            return f"Detected complex {company} {area} issue requiring manual handling."
            
        # V3 examples logic
        if area == "workspace_access":
            return "Detected admin-controlled workspace access issue. Escalated for specialist review."
        if area == "assessments":
            return "Detected candidate assessment submission failure. Routed to assessments support."
        if area == "merchant_disputes":
            return "Detected merchant dispute involving product fulfillment. Escalated for dispute handling."
            
        return f"Detected {company} {area} context. Categorized as {intent} and processed."

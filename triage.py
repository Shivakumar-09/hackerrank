import pandas as pd
from rules import (
    infer_company, check_escalation, check_invalid, get_response, 
    map_product_area, map_request_type
)
from retrieval import TicketRetriever

class TriageEngine:
    def __init__(self):
        self.retriever = TicketRetriever()
        
    def process_ticket(self, ticket_id, subject, issue, company=None):
        combined_text = str(subject) + " " + str(issue)
        
        # 1. Infer Company
        inferred_company = company
        if pd.isna(company) or not company or str(company).strip() == "":
            inferred_company = infer_company(combined_text)
            if not inferred_company:
                inferred_company = "Unknown"
                
        # 2. Check Invalid
        is_invalid = check_invalid(combined_text)
        
        # 3. Check Escalation
        is_escalated, escalation_reason = check_escalation(combined_text)
        
        # 4. Retrieve Similar Tickets
        similar_tickets = self.retriever.retrieve_similar(subject, issue, top_n=3)
        
        # 5. Predict Labels via Weighted Voting
        area_scores, type_scores = {}, {}
        for t in similar_tickets:
            w = t['similarity']
            area = map_product_area(t['product_area'])
            rtype = map_request_type(t['request_type'])
            area_scores[area] = area_scores.get(area, 0) + w
            type_scores[rtype] = type_scores.get(rtype, 0) + w
            
        def get_top(scores_dict, default):
            if not scores_dict: return default
            return max(scores_dict.items(), key=lambda x: x[1])[0]
            
        pred_area = get_top(area_scores, "general_support")
        pred_type = get_top(type_scores, "product_issue")
        
        # Override for invalid
        if is_invalid:
            pred_type = "invalid"
            
        # Determine Status
        status = "escalated" if is_escalated else "replied"
        
        # Calculate Confidence
        base_confidence = 0.5
        if similar_tickets:
            base_confidence = min(0.95, base_confidence + similar_tickets[0]['similarity'])
        if is_escalated:
            base_confidence = 0.99
            pred_area = map_product_area(escalation_reason) if escalation_reason else "fraud_security"
            
        # Determine Justification
        if is_invalid:
            justification = "Detected malformed irrelevant request. Marked invalid."
        elif is_escalated:
            justification = f"Detected {escalation_reason} indicators and high risk. Escalated for specialist review."
        else:
            justification = f"Detected {inferred_company} {pred_type} issue with low risk. Replied using {inferred_company} support pattern."
            
        # Generate Response
        if is_escalated or is_invalid or not similar_tickets or not similar_tickets[0].get('response'):
            response = get_response(inferred_company, status, is_invalid)
        else:
            response = similar_tickets[0]['response']
            
        return {
            "ticket_id": ticket_id,
            "company": inferred_company,
            "status": status,
            "product_area": pred_area,
            "request_type": pred_type,
            "confidence": round(base_confidence, 2),
            "response": response,
            "justification": justification,
            "similar_tickets_count": len(similar_tickets)
        }

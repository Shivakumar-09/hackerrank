import pandas as pd
from rules import (
    infer_company, check_escalation, detect_request_type, 
    get_polished_response, map_product_area
)
from retrieval import TicketRetriever

class TriageEngine:
    def __init__(self):
        self.retriever = TicketRetriever()
        
    def process_ticket(self, ticket_id, subject, issue, company=None):
        combined_text = (str(subject) + " " + str(issue)).strip()
        
        # 1. Improved Company Inference (No more "Unknown" if possible)
        inferred_company = company
        if pd.isna(company) or not company or str(company).lower() == "unknown":
            inferred_company = infer_company(combined_text)
        
        # 2. Request Type Detection
        request_type = detect_request_type(combined_text)
        
        # 3. Escalation Check
        is_escalated, escalation_reason = check_escalation(combined_text)
        status = "escalated" if is_escalated else "replied"
        
        # 4. Retrieval Hints
        similar_tickets = self.retriever.retrieve_similar(subject, issue, top_n=3)
        
        # 5. Product Area Classification with Restricted Mappings
        # Use retrieval majority vote mapped to approved categories
        retrieval_areas = [map_product_area(t['product_area']) for t in similar_tickets]
        
        if retrieval_areas:
            product_area = max(set(retrieval_areas), key=retrieval_areas.count)
        else:
            # Fallback to direct keyword mapping of the issue text
            product_area = map_product_area(combined_text)
            
        # 6. Calibrated Confidence Scoring (Moderately Raised)
        # Base confidence starts higher
        confidence = 0.65 
        
        if company and str(company).lower() != "unknown":
            confidence += 0.1
            
        if similar_tickets:
            # Boost based on top similarity score (up to +0.3)
            confidence += (similar_tickets[0]['similarity'] * 0.3)
            
        if is_escalated:
            confidence = max(confidence, 0.95)
            
        if request_type == "invalid":
            confidence = 0.98
            
        confidence = min(round(confidence, 2), 0.99)
        
        # 7. Justification Generation
        if request_type == "invalid":
            justification = "Detected malformed or irrelevant request content. Marked as invalid."
        elif is_escalated:
            justification = f"Detected {escalation_reason} indicators and high-risk context. Escalated for specialist review."
        else:
            justification = f"Detected {inferred_company} {product_area} context. Categorized as {request_type} and processed with high confidence."

        # 8. Final Response
        response = get_polished_response(inferred_company, status, request_type)
        
        return {
            "ticket_id": ticket_id,
            "company": inferred_company,
            "status": status,
            "product_area": product_area,
            "request_type": request_type,
            "confidence": confidence,
            "response": response,
            "justification": justification,
            "similar_tickets_count": len(similar_tickets)
        }

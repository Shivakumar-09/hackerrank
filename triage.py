import pandas as pd
from rules import (
    infer_company, check_escalation, detect_request_type, 
    get_polished_response, get_product_area_from_keywords
)
from retrieval import TicketRetriever

class TriageEngine:
    def __init__(self):
        self.retriever = TicketRetriever()
        
    def process_ticket(self, ticket_id, subject, issue, company=None):
        combined_text = (str(subject) + " " + str(issue)).strip()
        
        # 1. Company Inference
        inferred_company = company
        company_source = "provided"
        if pd.isna(company) or not company or str(company).lower() == "unknown":
            inferred_company = infer_company(combined_text)
            company_source = "inferred"
            if not inferred_company:
                inferred_company = "Unknown"
        
        # 2. Request Type Detection
        request_type = detect_request_type(combined_text)
        
        # 3. Escalation Check
        is_escalated, escalation_reason = check_escalation(combined_text)
        status = "escalated" if is_escalated else "replied"
        
        # 4. Retrieval Hints
        similar_tickets = self.retriever.retrieve_similar(subject, issue, top_n=3)
        
        # 5. Product Area Classification (Hybrid)
        keyword_area = get_product_area_from_keywords(combined_text)
        
        # Vote from retrieval
        retrieval_areas = [t['product_area'] for t in similar_tickets]
        if retrieval_areas:
            # Majority vote or fallback to keywords
            most_common_retrieval = max(set(retrieval_areas), key=retrieval_areas.count)
            # If keyword area is 'general_support' but retrieval has a specific area, trust retrieval
            if keyword_area == "general_support":
                product_area = most_common_retrieval
            else:
                product_area = keyword_area # Favor keyword precision if found
        else:
            product_area = keyword_area
            
        # 6. Confidence Scoring
        confidence = 0.5
        if company_source == "provided":
            confidence += 0.1
        if similar_tickets:
            # Boost based on top similarity score
            confidence += (similar_tickets[0]['similarity'] * 0.4)
        if is_escalated:
            confidence = max(confidence, 0.9) # High confidence for explicit risk
        if request_type == "invalid":
            confidence = 0.95
            
        confidence = min(round(confidence, 2), 0.99)
        
        # 7. Justification Generation
        if request_type == "invalid":
            justification = "Detected malformed or irrelevant request content. Marked as invalid."
        elif is_escalated:
            justification = f"Detected {escalation_reason} indicators and high-risk context. Escalated for specialist review."
        else:
            justification = f"Detected {inferred_company} {product_area} context with {request_type} characteristics. Replied using standard guidance."

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

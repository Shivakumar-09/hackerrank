import pandas as pd
from rules import infer_company, check_escalation, check_toxicity, get_response
from retrieval import TicketRetriever

class TriageEngine:
    def __init__(self):
        self.retriever = TicketRetriever()
        
    def process_ticket(self, ticket_id, subject, issue, company=None):
        combined_text = str(subject) + " " + str(issue)
        
        # 1. Infer Company if None
        inferred_company = company
        if pd.isna(company) or not company or str(company).strip() == "":
            inferred_company = infer_company(combined_text)
            if not inferred_company:
                inferred_company = "Unknown"
        
        # 2. Check Escalation & Toxicity
        is_escalated, escalation_reason = check_escalation(combined_text)
        if not is_escalated:
            is_toxic, tox_reason = check_toxicity(combined_text)
            if is_toxic:
                is_escalated = True
                escalation_reason = tox_reason
        
        # 3. Retrieve Similar Tickets
        similar_tickets = self.retriever.retrieve_similar(subject, issue, top_n=3)
        
        # 4. Predict Labels via Majority Voting / Weighted Voting
        status_scores = {}
        area_scores = {}
        type_scores = {}
        
        for t in similar_tickets:
            w = t['similarity']
            status_scores[t['status']] = status_scores.get(t['status'], 0) + w
            area_scores[t['product_area']] = area_scores.get(t['product_area'], 0) + w
            type_scores[t['request_type']] = type_scores.get(t['request_type'], 0) + w
            
        def get_top(scores_dict, default):
            if not scores_dict:
                return default
            return max(scores_dict.items(), key=lambda x: x[1])[0]
            
        pred_status = get_top(status_scores, "Open")
        pred_area = get_top(area_scores, "General")
        pred_type = get_top(type_scores, "Support")
        
        # 5. Confidence Calculation
        base_confidence = 0.5
        if similar_tickets:
            base_confidence = min(0.95, base_confidence + similar_tickets[0]['similarity'])
            
        if is_escalated:
            pred_status = "Escalated"
            pred_type = "High-Risk"
            base_confidence = 0.99  # High confidence due to strict rule match
            
        # 6. Justification Quality
        if is_escalated:
            justification = f"Detected high-risk keywords ({escalation_reason}). Escalated for manual review."
        else:
            justification = f"Analyzed {inferred_company} issue. Confidence {base_confidence:.2f} based on semantic similarity."
            if inferred_company in ["Visa", "HackerRank", "Claude"]:
                 justification = f"Detected {inferred_company} issue with low risk. Replied using {inferred_company} guidance."
                 
        # 7. Responses
        if is_escalated:
            response = get_response(inferred_company, True)
        elif similar_tickets and similar_tickets[0].get('response'):
            response = similar_tickets[0]['response']
        else:
            # Unsupported or no relevant corpus found -> Escalate
            is_escalated = True
            pred_status = "Escalated"
            justification = "Escalated: No highly relevant documentation found in corpus."
            response = get_response(inferred_company, True)
        
        return {
            "ticket_id": ticket_id,
            "company": inferred_company,
            "status": pred_status,
            "product_area": pred_area,
            "request_type": pred_type,
            "confidence": round(base_confidence, 2),
            "escalated": is_escalated,
            "response": response,
            "justification": justification,
            "similar_tickets_count": len(similar_tickets)
        }

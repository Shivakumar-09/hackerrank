import pandas as pd
import os

def load_input_data(file_path="support_tickets.csv"):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    
    # Fallback simulated tests (tests fraud, compiler issue, cancel billing, nonsense input, hacked account)
    data = [
        {"ticket_id": 1, "Subject": "Payment fraud issue", "Issue": "I see an unauthorized charge on my Visa card.", "Company": "Visa"},
        {"ticket_id": 2, "Subject": "Compiler broken", "Issue": "The python compiler is not working for my HackerRank assessment.", "Company": "HackerRank"},
        {"ticket_id": 3, "Subject": "Cancel billing", "Issue": "I want to cancel my Claude subscription.", "Company": "Claude"},
        {"ticket_id": 4, "Subject": "asdfghj", "Issue": "qwerty", "Company": None},
        {"ticket_id": 5, "Subject": "Account hacked", "Issue": "Someone stole my password and hacked my account.", "Company": None}
    ]
    return pd.DataFrame(data)

def save_output_data(results, file_path="output.csv"):
    df = pd.DataFrame(results)
    # Reorder columns to ensure mandatory ones exist
    columns_order = ["ticket_id", "company", "status", "product_area", "request_type", "confidence", "response", "justification"]
    columns_order = [c for c in columns_order if c in df.columns]
    df = df[columns_order]
    df.to_csv(file_path, index=False, encoding="utf-8")

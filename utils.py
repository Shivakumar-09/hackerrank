import pandas as pd
import os

def load_input_data(file_path="input.csv"):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        # Generate some mock data if no input is provided
        data = [
            {"ticket_id": 1, "subject": "I cannot access my assessment", "issue": "The compiler is throwing a weird error.", "company": None},
            {"ticket_id": 2, "subject": "Unauthorized charge", "issue": "I see a duplicate charge on my card.", "company": "Visa"},
            {"ticket_id": 3, "subject": "Upgrade subscription", "issue": "I want to change my AI chat model subscription.", "company": "Claude"},
            {"ticket_id": 4, "subject": "Login failed", "issue": "I am locked out of my account.", "company": None},
            {"ticket_id": 5, "subject": "Payment dispute", "issue": "This is a fraud transaction, refund immediately.", "company": "Visa"},
        ]
        return pd.DataFrame(data)

def save_output_data(results, file_path="output.csv"):
    df = pd.DataFrame(results)
    df.to_csv(file_path, index=False)

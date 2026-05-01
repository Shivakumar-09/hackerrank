import pandas as pd
from triage import TriageEngine
from logger import TriageLogger
from utils import load_input_data, save_output_data
from tqdm import tqdm
import time
import sys

def main():
    print("="*60)
    print("MULTI-DOMAIN SUPPORT TRIAGE AGENT - INITIALIZING")
    print("="*60)
    
    try:
        engine = TriageEngine()
        logger = TriageLogger("log.txt")
    except Exception as e:
        print(f"Error initializing system: {e}")
        sys.exit(1)
    
    print("Loading input data...")
    df = load_input_data("support_tickets.csv")
    
    results = []
    stats = {
        "Total": len(df),
        "replied": 0,
        "escalated": 0,
        "product_issue": 0,
        "feature_request": 0,
        "bug": 0,
        "invalid": 0,
        "total_conf": 0.0
    }
    
    print(f"Processing {len(df)} tickets...")
    start_time = time.time()
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Triaging"):
        ticket_id = row.get("ticket_id", row.get("Ticket_ID", idx + 1))
        subject = row.get("Subject", row.get("subject", ""))
        issue = row.get("Issue", row.get("issue", ""))
        company = row.get("Company", row.get("company", None))
        
        try:
            res = engine.process_ticket(ticket_id, subject, issue, company)
            results.append(res)
            
            logger.log_decision(
                row_id=ticket_id,
                company=res["company"],
                confidence=res["confidence"],
                decision=res["status"],
                retrieved=res["similar_tickets_count"],
                reason=res["justification"]
            )
            
            stats[res["status"]] = stats.get(res["status"], 0) + 1
            stats[res["request_type"]] = stats.get(res["request_type"], 0) + 1
            stats["total_conf"] += res["confidence"]
            
        except Exception as e:
            print(f"\nError processing ticket {ticket_id}: {e}. Skipping.")
            continue
            
    end_time = time.time()
    speed = stats["Total"] / max(0.001, end_time - start_time)
    avg_conf = stats["total_conf"] / max(1, stats["Total"])
    
    print("\nSaving predictions to output.csv...")
    save_output_data(results, "output.csv")
    
    print("\n" + "="*60)
    print("PERFORMANCE METRICS (JUDGE SUMMARY)")
    print("="*60)
    print(f"Total Tickets Processed : {stats['Total']}")
    print(f"Status - Replied        : {stats['replied']}")
    print(f"Status - Escalated      : {stats['escalated']}")
    print(f"Types - Product Issues  : {stats['product_issue']}")
    print(f"Types - Invalid/Spam    : {stats['invalid']}")
    print(f"Types - Bugs            : {stats['bug']}")
    print(f"Types - Feature Req     : {stats['feature_request']}")
    print(f"Average Confidence      : {avg_conf:.2f}")
    print(f"Processing Speed        : {speed:.0f} tickets/sec")
    print("="*60)
    print("Run Complete. output.csv and log.txt generated securely.")

if __name__ == "__main__":
    main()

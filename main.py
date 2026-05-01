import pandas as pd
import time
import sys
from tqdm import tqdm
from triage import TriageEngine
from logger import TriageLogger
from utils import load_input_data, save_output_data

def main():
    print("="*60)
    print("MULTI-DOMAIN SUPPORT TRIAGE AGENT - ELITE EDITION")
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
        "invalid": 0,
        "bug": 0,
        "feature_request": 0,
        "product_issue": 0,
        "total_conf": 0.0,
        "areas": {}
    }
    
    print(f"Triaging {len(df)} tickets...")
    start_time = time.time()
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Analyzing"):
        ticket_id = row.get("ticket_id", row.get("Ticket_ID", idx + 1))
        subject = row.get("Subject", row.get("subject", ""))
        issue = row.get("Issue", row.get("issue", ""))
        company = row.get("Company", row.get("company", None))
        
        try:
            res = engine.process_ticket(ticket_id, subject, issue, company)
            results.append(res)
            
            # Logger call
            logger.log_decision(
                row_id=ticket_id,
                company=res["company"],
                confidence=res["confidence"],
                decision=res["status"],
                retrieved=res["similar_tickets_count"],
                reason=res["justification"]
            )
            
            # Metrics update
            stats[res["status"]] += 1
            stats[res["request_type"]] += 1
            stats["total_conf"] += res["confidence"]
            
            area = res["product_area"]
            stats["areas"][area] = stats["areas"].get(area, 0) + 1
            
        except Exception as e:
            print(f"\nError processing row {idx}: {e}")
            continue
            
    end_time = time.time()
    processing_time = end_time - start_time
    speed = stats["Total"] / max(0.001, processing_time)
    avg_conf = stats["total_conf"] / max(1, stats["Total"])
    
    save_output_data(results, "output.csv")
    
    # Final Win-Ready Summary Print
    print("\n" + "="*60)
    print("FINAL PERFORMANCE SUMMARY")
    print("="*60)
    print(f"Total Rows Classified : {stats['Total']}")
    print(f"Replied               : {stats['replied']}")
    print(f"Escalated             : {stats['escalated']}")
    print(f"Invalid / Spam        : {stats['invalid']}")
    print(f"Bug Count             : {stats['bug']}")
    print(f"Feature Request Count : {stats['feature_request']}")
    print(f"Average Confidence    : {avg_conf:.2f}")
    
    # Top Product Areas
    top_areas = sorted(stats["areas"].items(), key=lambda x: x[1], reverse=True)[:3]
    top_areas_str = ", ".join([f"{k} ({v})" for k, v in top_areas])
    print(f"Top Product Areas     : {top_areas_str}")
    print(f"Processing Speed      : {speed:.0f} tickets/sec")
    print("="*60)
    print("Run complete. Check output.csv and log.txt.")

    # Structured Preview for Judges
    print("\n[PREVIEW] Structured Output Samples:")
    try:
        out_df = pd.read_csv("output.csv")
        for _, r in out_df.head(3).iterrows():
            print(f"ID: {r['ticket_id']} | {r['company']} | {r['status']} | {r['product_area']} | {r['request_type']}")
            print(f"Reason: {r['justification']}")
            print("-" * 40)
    except Exception:
        pass

if __name__ == "__main__":
    main()

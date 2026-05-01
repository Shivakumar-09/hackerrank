import pandas as pd
from triage import TriageEngine
from logger import TriageLogger
from utils import load_input_data, save_output_data
from tqdm import tqdm
import time

def main():
    print("Initializing Multi-Domain Support Triage Agent...")
    engine = TriageEngine()
    logger = TriageLogger("log.txt")
    
    print("Loading input data...")
    df = pd.read_csv("support_tickets.csv")
    
    results = []
    
    stats = {
        "Total tickets": len(df),
        "Replied": 0,
        "Escalated": 0,
        "Invalid": 0,
        "Total confidence": 0.0,
        "Product areas": {}
    }
    
    print("Processing tickets...")
    start_time = time.time()
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        ticket_id = idx + 1
        subject = row.get("Subject", "")
        issue = row.get("Issue", "")
        company = row.get("Company", None)
        
        if pd.isna(subject) and pd.isna(issue):
            stats["Invalid"] += 1
            continue
            
        res = engine.process_ticket(ticket_id, subject, issue, company)
        results.append(res)
        
        # Logging
        logger.log_decision(
            row_id=ticket_id,
            company=res["company"],
            confidence=res["confidence"],
            retrieved_count=res["similar_tickets_count"],
            decision=res["status"],
            reason=res["justification"]
        )
        
        # Metrics
        if res["escalated"]:
            stats["Escalated"] += 1
        else:
            stats["Replied"] += 1
            
        stats["Total confidence"] += res["confidence"]
        
        area = res["product_area"]
        stats["Product areas"][area] = stats["Product areas"].get(area, 0) + 1
        
    end_time = time.time()
    processing_time = end_time - start_time
    tickets_per_sec = stats["Total tickets"] / max(0.001, processing_time)
        
    print("Saving results to output.csv...")
    save_output_data(results, "output.csv")
    
    # Print Performance Metrics
    valid_tickets = max(1, (stats["Total tickets"] - stats["Invalid"]))
    avg_conf = stats["Total confidence"] / valid_tickets
    
    # Get top 3 product areas
    top_areas = sorted(stats["Product areas"].items(), key=lambda x: x[1], reverse=True)[:3]
    top_areas_str = ", ".join([f"{k} ({v})" for k, v in top_areas])
    
    print("\n==============================================================")
    print("PERFORMANCE METRICS")
    print("==============================================================")
    print(f"Total tickets: {stats['Total tickets']}")
    print(f"Replied: {stats['Replied']}")
    print(f"Escalated: {stats['Escalated']}")
    print(f"Invalid: {stats['Invalid']}")
    print(f"Average confidence: {avg_conf:.2f}")
    print(f"Top product areas: {top_areas_str}")
    print(f"Processing Speed: {tickets_per_sec:.0f} tickets/sec")
    print("==============================================================\n")
    print("Run complete. Displaying files below:")
    
    print("\n==============================================================")
    print("STRUCTURED OUTPUT.CSV PREVIEW")
    print("==============================================================")
    try:
        out_df = pd.read_csv("output.csv")
        for _, r in out_df.iterrows():
            print(f"[Ticket {r['ticket_id']}] Company: {r['company']} | Status: {r['status']} | Confidence: {r['confidence']}")
            print(f"  Area: {r['product_area']} | Type: {r['request_type']}")
            print(f"  Reason: {r['justification']}")
            print("-" * 62)
    except Exception as e:
        print(f"Error reading output.csv: {e}")
        
    print("\n==============================================================")
    print("LOG.TXT CONTENT")
    print("==============================================================")
    try:
        with open("log.txt", "r", encoding="utf-8") as f:
            print(f.read().strip())
    except Exception as e:
        print(f"Error reading log.txt: {e}")

if __name__ == "__main__":
    main()

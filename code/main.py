import pandas as pd
from tqdm import tqdm
import sys
import traceback
from pathlib import Path

# Absolute Path Setup based on Repo Root
CODE_DIR = Path(__file__).resolve().parent
REPO_ROOT = CODE_DIR.parent
SUPPORT_DIR = REPO_ROOT / "support_tickets"
INPUT_CSV = SUPPORT_DIR / "support_tickets.csv"
OUTPUT_CSV = SUPPORT_DIR / "output.csv"

# Add code dir to sys.path
sys.path.append(str(CODE_DIR))

try:
    from triage import TriageEngine
    from logger import TriageLogger
    from config import LOG_FILE
    from utils import load_csv
except ImportError as e:
    print(f"CRITICAL IMPORT ERROR: {e}")
    sys.exit(1)

def main():
    logger = TriageLogger()
    logger.log("Started agent - Final Path Validation Run")
    
    print("="*60)
    print("MULTI-DOMAIN SUPPORT TRIAGE AGENT - FINAL SUBMISSION")
    print("="*60)
    
    # 1. Validate Input
    if not INPUT_CSV.exists():
        print(f"CRITICAL ERROR: Input file not found at {INPUT_CSV}")
        return

    # 2. Build Engine
    print("Building corpus index...")
    try:
        engine = TriageEngine()
        doc_count = sum(len(v) for v in engine.retriever.corpora.values())
        logger.log(f"Indexed {doc_count} corpus docs")
    except Exception as e:
        print(f"FAILED TO INITIALIZE ENGINE: {e}")
        traceback.print_exc()
        return
    
    # 3. Load Input
    print(f"Loading {INPUT_CSV.name}...")
    df = pd.read_csv(INPUT_CSV, encoding="utf-8")
    
    results = []
    stats = {
        "Total": len(df),
        "replied": 0,
        "escalated": 0,
        "invalid": 0,
        "total_conf": 0.0,
    }
    
    # 4. Processing Loop
    print(f"Processing {len(df)} rows...")
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Triaging"):
        try:
            res = engine.process(row)
            
            # Collect results for CSV
            results.append({
                "status": res["status"],
                "product_area": res["product_area"],
                "response": res["response"],
                "justification": res["justification"],
                "request_type": res["request_type"]
            })
            
            # Log to log.txt
            logger.log_decision(idx + 1, res["status"], res["product_area"], res["confidence"])
            
            # Stats
            stats[res["status"]] += 1
            if res["request_type"] == "invalid":
                stats["invalid"] += 1
            stats["total_conf"] += res["confidence"]
            
        except Exception as e:
            logger.log(f"Error at row {idx + 1}: {e}")
            continue

    # 5. Save Output CSV (FIXED SYSTEM)
    print("\nSaving output.csv...")
    try:
        # Ensure folder exists
        SUPPORT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Create DataFrame
        out_df = pd.DataFrame(results)
        
        # Force exact column order as per official requirements
        out_df = out_df[
            [
                "status",
                "product_area",
                "response",
                "justification",
                "request_type"
            ]
        ]
        
        # Write to CSV
        out_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
        
        # Immediate Validation
        if OUTPUT_CSV.exists():
            print(f"SUCCESS: Saved predictions to: {OUTPUT_CSV.as_posix()}")
            print(f"Rows written: {len(out_df)}")
            logger.log(f"Saved output.csv with {len(out_df)} rows")
        else:
            print(f"ERROR: output.csv not found at {OUTPUT_CSV} after save attempt.")
            
    except Exception as e:
        print(f"CRITICAL ERROR SAVING CSV: {e}")
        traceback.print_exc()
        logger.log(f"CSV Save Failed: {e}")

    # 6. Final Summary
    avg_conf = stats["total_conf"] / max(1, stats["Total"])
    print("\n" + "="*50)
    print("FINAL SUMMARY")
    print("="*50)
    print(f"Total Rows: {stats['Total']}")
    print(f"Replied: {stats['replied']}")
    print(f"Escalated: {stats['escalated']}")
    print(f"Saved output: {OUTPUT_CSV.as_posix()}")
    print(f"Saved log: {LOG_FILE.as_posix()}")
    print("="*50)
    
    logger.log("Run completed successfully")

if __name__ == "__main__":
    main()

import logging
from pathlib import Path
from config import LOG_FILE

class TriageLogger:
    def __init__(self):
        # Path is handled in config.py directory creation
        self.logger = logging.getLogger("TriageLogger")
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            try:
                # Ensure UTF-8 encoding as requested
                handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
                formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
            except Exception as e:
                print(f"CRITICAL ERROR: Could not initialize log file at {LOG_FILE}: {e}")
            
    def log(self, message):
        """Log a general event message."""
        self.logger.info(message)

    def log_decision(self, ticket_id, status, area, confidence):
        """Log a row-specific decision."""
        self.log(f"Row {ticket_id} => {status} | {area} | confidence {confidence:.2f}")

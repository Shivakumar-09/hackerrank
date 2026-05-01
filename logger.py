import logging

class TriageLogger:
    def __init__(self, log_file="log.txt"):
        self.logger = logging.getLogger("TriageLogger")
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
            
        file_handler = logging.FileHandler(log_file, mode='w')
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        
    def log_decision(self, row_id, company, confidence, retrieved_count, decision, reason):
        # Format: timestamp | row id | company | confidence | retrieved similar rows | decision | reason
        log_msg = f"RowID: {row_id} | Company: {company} | Confidence: {confidence:.2f} | Retrieved: {retrieved_count} | Decision: {decision} | Reason: {reason}"
        self.logger.info(log_msg)

import logging

class TriageLogger:
    def __init__(self, log_file="log.txt"):
        self.logger = logging.getLogger("TriageLogger")
        self.logger.setLevel(logging.INFO)
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        file_handler = logging.FileHandler(log_file, mode='w', encoding="utf-8")
        formatter = logging.Formatter('%(asctime)s | %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
    def log_decision(self, row_id, company, confidence, decision, retrieved, reason):
        log_msg = f"row_id: {row_id} | company: {company} | confidence: {confidence:.2f} | decision: {decision} | retrieval_matches: {retrieved} | reason: {reason}"
        self.logger.info(log_msg)

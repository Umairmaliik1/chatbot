#!/usr/bin/env python3
"""
Kommo CRM Integration Logging Configuration
This file configures enhanced logging for Kommo CRM integration activities
"""

import logging
import logging.handlers
import os
from datetime import datetime

def setup_kommo_logging():
    """Setup enhanced logging for Kommo CRM integration"""
    
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Create a dedicated logger for Kommo CRM
    kommo_logger = logging.getLogger("kommo_crm")
    kommo_logger.setLevel(logging.DEBUG)
    
    # Prevent duplicate handlers
    if kommo_logger.handlers:
        return kommo_logger
    
    # Create formatter for Kommo logs
    kommo_formatter = logging.Formatter(
        fmt='%(asctime)s | KOMO_CRM | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler for Kommo logs (INFO and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(kommo_formatter)
    kommo_logger.addHandler(console_handler)
    
    # File handler for all Kommo logs (DEBUG and above)
    kommo_log_file = os.path.join(logs_dir, f"kommo_crm_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.handlers.RotatingFileHandler(
        kommo_log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(kommo_formatter)
    kommo_logger.addHandler(file_handler)
    
    # Error file handler for errors only
    kommo_error_file = os.path.join(logs_dir, f"kommo_crm_errors_{datetime.now().strftime('%Y%m%d')}.log")
    error_handler = logging.handlers.RotatingFileHandler(
        kommo_error_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(kommo_formatter)
    kommo_logger.addHandler(error_handler)
    
    # Webhook activity file handler
    kommo_webhook_file = os.path.join(logs_dir, f"kommo_webhooks_{datetime.now().strftime('%Y%m%d')}.log")
    webhook_handler = logging.handlers.RotatingFileHandler(
        kommo_webhook_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    webhook_handler.setLevel(logging.INFO)
    webhook_handler.setFormatter(kommo_formatter)
    kommo_logger.addHandler(webhook_handler)
    
    kommo_logger.info("Kommo CRM logging configured successfully")
    kommo_logger.info(f"Log files location: {logs_dir}/")
    
    return kommo_logger

def get_kommo_logger():
    """Get the Kommo CRM logger instance"""
    return logging.getLogger("kommo_crm")

if __name__ == "__main__":
    # Test the logging setup
    logger = setup_kommo_logging()
    logger.info("Testing Kommo CRM logging")
    logger.warning("This is a test warning")
    logger.error("This is a test error")
    logger.debug("This is a test debug message")
    print("Logging test completed. Check the logs/ directory for log files.")

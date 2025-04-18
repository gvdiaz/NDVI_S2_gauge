
import logging
# import sys
from datetime import datetime
from pathlib import Path  # For directory handling

def configure_logging():
    """Set up logging configuration relative to project root"""
    # Get the directory where this script lives
    script_dir = Path(__file__).parent.parent
    
    # Option 1: Logs in project root/logs/
    logs_dir = script_dir / "logs"
    
    # Option 2: If you want logs in a different relative path
    # logs_dir = script_dir.parent / "var" / "logs"  # Goes up one level then into var/logs
    
    # Create directory if it doesn't exist (with parents if needed)
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Create log file path
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = logs_dir / f"error_log_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(sys.stdout)
        ]
    )



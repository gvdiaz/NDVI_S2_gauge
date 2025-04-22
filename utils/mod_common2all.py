
import logging
import sys
from datetime import datetime
from pathlib import Path  # For directory handling

# Package for config timezone
import pytz

def configure_logging(folder_path):
    """Set up logging configuration relative to project root"""
    # Get the directory where this script lives
    if folder_path:
        # Cuidado con ingresar rutas que no están mapeadas en SO nativo.
        script_dir = folder_path
    elif None:
        # Sino se guarda en esta carpeta.
        script_dir = Path(__file__).parent
    
    # Option 1: Logs in project root/logs/
    logs_dir = script_dir / "logs"
    
    # Option 2: If you want logs in a different relative path
    # logs_dir = script_dir.parent / "var" / "logs"  # Goes up one level then into var/logs
    
    # Create directory if it doesn't exist (with parents if needed)
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Create log file path
    buenos_aires_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    timestamp = datetime.now(buenos_aires_tz).strftime("%Y-%m-%d_%H-%M-%S")
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



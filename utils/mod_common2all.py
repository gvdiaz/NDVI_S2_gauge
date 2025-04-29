
import logging
import sys
from datetime import datetime
from pathlib import Path  # For directory handling

# Package for config timezone
import pytz

def configure_logging(folder_path = None, proj_name = None):
    """Set up logging configuration relative to project root"""
    # Get the directory where this script lives
    if folder_path != None:
        # Cuidado con ingresar rutas que no están mapeadas en SO nativo.
        script_dir = Path(folder_path)
    else:
        # Sino se guarda en esta carpeta.
        script_dir = Path(__file__).parent
    
    # Option 1: Logs in project root/logs/
    # logs_dir = script_dir / "logs"
    logs_dir = script_dir 
    
    # Option 2: If you want logs in a different relative path
    # logs_dir = script_dir.parent / "var" / "logs"  # Goes up one level then into var/logs
    
    # Create directory if it doesn't exist (with parents if needed)
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Create log file path
    buenos_aires_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    timestamp = datetime.now(buenos_aires_tz).strftime("%Y-%m-%d_%H-%M-%S")
    if proj_name == None:
        log_filename = logs_dir / f"error_log_{timestamp}.log"
    else:
        log_filename = logs_dir / f"error_log_{proj_name}_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return log_filename


from pathlib import Path
import logging
from venv import logger


logging.basicConfig(
    level="INFO", 
     format="%(asctime)s - %(levelname)s - %(message)s"
    )
logging.info("Starting payment file validation.")
# logging.warning("Skipping invalid record")
# logging.error("Error processing payment record")

logging.path = Path(__file__).parent / "logs" / "payment_validation.log"


def validate_payments(file_path: str) -> None:

    """
    Validates the payments in the given file.

    Args:
        file_path (str): The path to the file containing payment data.  
    """
    # Check if the file exists
    if not Path(file_path).exists():
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    
    # Check if the file is empty    
    if Path(file_path).stat().st_size == 0:
        raise ValueError(f"The file '{file_path}' is empty.")

    logger.info(f"File '{file_path}' is valid.")

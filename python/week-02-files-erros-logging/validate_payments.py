from pathlib import Path
import csv

Project_dir = Path(__file__).resolve().parent.parent
print(f"Project_dir: {Project_dir}")

# def validate_payments(file_path: csv) -> None:

#     """
#     Validates the payments in the given file.

#     Args:
#         file_path (str): The path to the file containing payment data.  
#     """
#     # # Check if the file exists
#     # if not Path(file_path).exists():
#     #     raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    
#     # # Check if the file is empty    
#     # if Path(file_path).stat().st_size == 0:
#     #     raise ValueError(f"The file '{file_path}' is empty.")

#     dict_file = file_path.dictRead()  # Assuming dictRead is a method that reads the file into a dictionary
#     for key, value in dict_file.items():
#         print(f"Validating payment record: {key} - {value}")
#         # Validate each payment record (for example, check if it has the correct fields)
#         if not all(field in value for field in ["id", "amount", "status"]):
#             raise ValueError(f"Invalid payment record: '{key} - {value}'")


# validate_payments('./data/payments.csv')
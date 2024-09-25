import functools
import logging

# Configure the logger to write to a file
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),  # Log to a file
                        # logging.StreamHandler()  # Log to the console well
                    ])

logger = logging.getLogger(__name__)

def log_decorator(func):
    """
    Decorator that logs the execution of the function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        logger.info(f"Executing {func_name} with args: {args} and kwargs: {kwargs}")
        try:
            # Execute the function
            result = func(*args, **kwargs)
            # Log the successful execution
            logger.info(f"{func_name} executed successfully.")
            return result
        except Exception as e:
            # Log any exception raised during execution
            logger.error(f"Error executing {func_name}: {e}", exc_info=True)
            raise e
    return wrapper






def read_log_file():
    """
    Function to read and display the content of the log file 'app.log'.
    """
    try:
        with open("app.log", "r") as log_file:
            content = log_file.read()
            if content:
                print("----- Log File Content -----")
                print(content)
            else:
                print("Log file is empty.")
    except FileNotFoundError:
        print("Log file not found. Please ensure 'app.log' exists.")

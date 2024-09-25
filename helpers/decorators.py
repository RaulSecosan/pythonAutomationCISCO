import functools

def log_decorator(func):
    """
    Decorator that logs the execution of the function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the function name and its arguments
        func_name = func.__name__
        # print(f"Executing {func_name} with args: {args} and kwargs: {kwargs}")
        print(f"Executing {func_name}...")
        try:
            # Execute the function
            result = func(*args, **kwargs)
            # Log the successful execution
            print(f"{func_name} executed successfully.")
            return result
        except Exception as e:
            # Log any failure during execution
            print(f"Error executing {func_name}: {e}")
            raise e
    return wrapper
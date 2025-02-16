def handle_b1_error():
    """
    Handles the error case for task B0, where data outside the `/data` directory is requested.
    Outputs a message indicating that accessing data outside `/data` is not possible.
    """
    error_message = "That's not possible. Data outside /data cannot be accessed or exfiltrated."
    print(error_message)
    return error_message


def handle_b2_error():
    """
    Handles the error case for task B1, where data deletion is requested.
    Outputs a message indicating that data deletion is not allowed.
    """
    error_message = "That's not possible. Data is never deleted anywhere on the file system."
    print(error_message)
    return error_message
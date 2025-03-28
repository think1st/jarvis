import socket

def is_online(host="8.8.8.8", port=53, timeout=3):
    """
    Returns True if the system has internet access.
    Default host is Google's DNS (8.8.8.8).
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False

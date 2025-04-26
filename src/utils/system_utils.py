import platform

def is_macos() -> bool:
    """
    Check if the current system is macOS.
    
    Returns:
        bool: True if running on macOS, False otherwise
    """
    return platform.system() == 'Darwin'

def is_windows() -> bool:
    """
    Check if the current system is Windows.
    
    Returns:
        bool: True if running on Windows, False otherwise
    """
    return platform.system() == 'Windows'

def get_os_name() -> str:
    """
    Get the name of the current operating system.
    
    Returns:
        str: The name of the operating system (e.g., 'Darwin' for macOS, 'Windows' for Windows)
    """
    return platform.system() 
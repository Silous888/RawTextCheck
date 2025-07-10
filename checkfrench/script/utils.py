"""
File        : utils.py
Author      : Silous
Created on  : 2025-04-18
Description : Utility functions for various operations in the application.
"""


# == Imports ==================================================================

import re


# == Functions ================================================================

def sanitize_folder_name(name: str) -> str:
    """Sanitize a folder name by removing or replacing invalid characters.
    Args:
        name (str): The folder name to sanitize.
    Returns:
        str: The sanitized folder name.
    """
    # Replace forbidden characters with underscore
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    # Remove ASCII control characters
    name = ''.join(c for c in name if ord(c) >= 32)
    # Trim whitespace from the beginning and end
    name = name.strip()
    # Limit length to a safe maximum (255 characters)
    return name[:255]

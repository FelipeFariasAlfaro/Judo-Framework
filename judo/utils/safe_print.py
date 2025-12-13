"""
Safe printing utility for handling Unicode characters on different platforms
"""

import sys


def safe_print(message: str, fallback_message: str = None):
    """
    Safely print a message, handling Unicode encoding issues
    
    Args:
        message: The message to print (may contain Unicode characters)
        fallback_message: Alternative message if Unicode fails (optional)
    """
    try:
        print(message)
    except UnicodeEncodeError:
        # Fallback for systems that can't handle Unicode (like Windows cmd with cp1252)
        if fallback_message:
            print(fallback_message)
        else:
            # Remove Unicode characters and try again
            ascii_message = message.encode('ascii', 'ignore').decode('ascii')
            print(ascii_message)


def safe_emoji_print(emoji: str, text: str):
    """
    Print text with emoji, falling back to text-only on encoding issues
    
    Args:
        emoji: The emoji character
        text: The text message
    """
    try:
        print(f"{emoji} {text}")
    except UnicodeEncodeError:
        print(text)
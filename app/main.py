"""
Small hello-world module for LOG430 lab.

This module exposes a single function `hello` and prints the greeting when
executed as a script.
"""

def hello() -> str:
    """Return greeting message."""
    return "Hello, World!"


if __name__ == "__main__":
    # Display the message when the file is run directly
    print(hello())

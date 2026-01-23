#!/usr/bin/env python3
"""
Entry point for the Todo Console Application
Initialize TodoList instance, start CLI loop, handle graceful shutdown
"""

import sys
import os
# Add the src directory to the path so imports work properly
sys.path.insert(0, os.path.dirname(__file__))
from todo.cli import TodoCLI


def main():
    """Main entry point for the application"""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()
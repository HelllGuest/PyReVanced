#!/usr/bin/env python3
"""
PyReVanced - Main Entry Point

A comprehensive Python GUI wrapper for the ReVanced CLI tool that provides an easy-to-use
interface for patching APK files with ReVanced patches.

Author: Anoop Kumar
License: MIT
Version: 1.0
"""

import sys
import tkinter as tk
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.revanced_gui import ReVancedGUI


def main():
    """Main entry point for the PyReVanced application."""
    # Create root window
    root = tk.Tk()
    
    # Create application instance
    app = ReVancedGUI(root)
    
    if app:
        # Handle application close
        def on_closing():
            app.cleanup()
            root.quit()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Start the main event loop
        try:
            root.mainloop()
        except KeyboardInterrupt:
            print("\nApplication interrupted by user")
            app.cleanup()
        except Exception as e:
            print(f"Unexpected error: {e}")
            app.cleanup()
            raise


if __name__ == "__main__":
    main()
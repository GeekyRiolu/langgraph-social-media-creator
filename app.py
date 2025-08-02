#!/usr/bin/env python3
"""
Social Media Content Creator - Deployment Entry Point
"""

# Import the main application
from chat_ui import demo

if __name__ == "__main__":
    # Launch the application for deployment
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    )

#!/usr/bin/env python3
"""
Social Media Content Creator - Deployment Entry Point
"""

import os
import sys

def main():
    """Main entry point for deployment."""
    try:
        # Import the main application
        from chat_ui import demo

        # Get port from environment variable (for cloud deployment)
        port = int(os.environ.get("PORT", 7860))

        print("🚀 Starting Social Media Content Creator...")
        print(f"📱 Server will be available on port {port}")

        # Launch the application for deployment
        demo.launch(
            server_name="0.0.0.0",
            server_port=port,
            share=True,
            show_error=True,
            show_api=False,  # Disable API docs to avoid schema issues
            quiet=True,      # Reduce verbose output
            favicon_path=None,
            root_path=os.environ.get("GRADIO_ROOT_PATH", "")
        )

    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

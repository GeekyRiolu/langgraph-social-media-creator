#!/usr/bin/env python3
"""
Launcher script for the Social Media Content Creator Chat UI.
This script checks dependencies and starts the Gradio interface.
"""

import sys
import subprocess
import importlib.util

def check_package(package_name):
    """Check if a package is installed."""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_package(package_name):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🚀 Starting Social Media Content Creator Chat UI...")
    print("=" * 50)
    
    # Check for required packages
    required_packages = {
        "gradio": "gradio>=4.0.0",
        "langgraph": "langgraph>=0.0.15",
        "pandas": "pandas>=2.0.0"
    }
    
    missing_packages = []
    for package, requirement in required_packages.items():
        if not check_package(package):
            missing_packages.append(requirement)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        
        print("\n🔧 Installing missing packages...")
        for package in missing_packages:
            print(f"Installing {package}...")
            if install_package(package):
                print(f"✅ {package} installed successfully")
            else:
                print(f"❌ Failed to install {package}")
                print("Please install manually using: pip install -r requirements.txt")
                return
    
    print("✅ All dependencies are ready!")
    print("\n🌐 Starting Gradio Chat UI...")
    print("📱 The interface will open in your browser automatically")
    print("🔗 If it doesn't open, go to: http://localhost:7860")
    print("\n💡 Tips:")
    print("   - Set your brand theme in the sidebar")
    print("   - Type 'generate' to create content plans")
    print("   - Type 'help' for assistance")
    print("   - Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Import and run the chat UI
        from chat_ui import demo
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True,
            inbrowser=True  # Automatically open browser
        )
    except ImportError as e:
        print(f"❌ Error importing chat_ui: {e}")
        print("Make sure chat_ui.py is in the same directory")
    except Exception as e:
        print(f"❌ Error starting chat UI: {e}")
        print("Please check the error message above and try again")

if __name__ == "__main__":
    main()

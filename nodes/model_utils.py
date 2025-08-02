import os
import sys
from typing import Optional, Tuple
from langchain_community.llms import LlamaCpp

# Check if huggingface_hub is installed
try:
    from huggingface_hub import hf_hub_download
    HUGGINGFACE_HUB_AVAILABLE = True
except ImportError:
    HUGGINGFACE_HUB_AVAILABLE = False

# TinyLlama model information
TINYLLAMA_REPO_ID = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"
TINYLLAMA_FILENAME = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"

def get_models_dir() -> str:
    """Get the path to the models directory."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_dir = os.path.join(base_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    return models_dir

def download_model(repo_id: str, filename: str) -> Optional[str]:
    """Download a model from Hugging Face Hub."""
    if not HUGGINGFACE_HUB_AVAILABLE:
        print("\nhuggingface_hub is not installed. To enable automatic model downloading, run:")
        print("pip install huggingface_hub")
        return None
    
    models_dir = get_models_dir()
    model_path = os.path.join(models_dir, filename)
    
    # Check if model already exists
    if os.path.exists(model_path):
        print(f"Model already exists at {model_path}")
        return model_path
    
    try:
        print(f"\nDownloading {filename} from {repo_id}...")
        print("This may take a while depending on your internet connection.")
        
        # Download the model
        downloaded_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=models_dir,
            local_dir_use_symlinks=False
        )
        
        print(f"Model downloaded successfully to {downloaded_path}")
        return downloaded_path
    except Exception as e:
        print(f"Error downloading model: {e}")
        return None

def get_llm(temperature: float = 0.7) -> Optional[LlamaCpp]:
    """Initialize the LLM with appropriate settings.

    Args:
        temperature: The temperature setting for generation (0.0-1.0)
    """
    # Use TinyLlama model
    repo_id = TINYLLAMA_REPO_ID
    filename = TINYLLAMA_FILENAME
    
    models_dir = get_models_dir()
    model_path = os.path.join(models_dir, filename)
    
    # Check if model exists, if not try to download it
    if not os.path.exists(model_path):
        if HUGGINGFACE_HUB_AVAILABLE:
            print(f"Model not found at {model_path}. Attempting to download...")
            model_path = download_model(repo_id, filename)
            if model_path is None:
                return None
        else:
            print(f"\nModel not found at {model_path}")
            print("To use the LLM functionality, you have two options:")
            print("\n1. Install huggingface_hub for automatic downloads:")
            print("   pip install huggingface_hub")
            print("\n2. Manually download the model:")
            print(f"   a. Visit https://huggingface.co/{repo_id}/")
            print(f"   b. Download the '{filename}' file")
            print(f"   c. Place it in the '{models_dir}' directory\n")
            print("Using rule-based fallback for generation...")
            return None
    
    try:
        # Print the model usage message when we're actually going to use it
        print("\nUsing TinyLlama model for generation")

        return LlamaCpp(
            model_path=model_path,
            temperature=temperature,
            max_tokens=2048,
            top_p=1,
            verbose=False,
        )
    except Exception as e:
        print(f"Error loading LlamaCpp model: {e}")
        print("Using rule-based fallback for generation...")
        return None
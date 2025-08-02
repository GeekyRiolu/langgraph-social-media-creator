from typing import Dict
import pandas as pd

def formatter_node(state: Dict) -> Dict:
    """Format the content into a structured DataFrame."""
    # Extract content from state
    content_list = state["content"]
    
    # Convert to DataFrame
    df = pd.DataFrame(content_list)
    
    # Ensure columns are in the correct order
    df = df[["day", "topic", "caption", "hashtags"]]
    
    # Store the DataFrame in the state
    state["formatted_content"] = df
    
    return state
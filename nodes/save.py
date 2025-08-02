from typing import Dict
import os

def save_node(state: Dict) -> Dict:
    """Save the formatted content to a CSV file."""
    # Extract the DataFrame and output path from state
    df = state["formatted_content"]
    output_path = state["output_path"]
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    
    # Update the state with the saved path
    state["output_path"] = os.path.abspath(output_path)
    
    return state
import argparse
import os
from typing import Dict, List, Optional, TypedDict

import pandas as pd
from langgraph.graph import END, START, StateGraph

# Import our custom nodes
from nodes.day_planner import day_planner_node
from nodes.content_generator import content_generator_node
from nodes.formatter import formatter_node
from nodes.save import save_node

# Define the state type
class State(TypedDict):
    """The state of the workflow."""
    brand_theme: str
    duration: int
    topics: Optional[List[str]]
    content: Optional[List[Dict]]
    formatted_content: Optional[pd.DataFrame]
    output_path: str
    use_model: bool
    randomness: str

def build_graph() -> StateGraph:
    """Build the LangGraph workflow."""
    # Initialize the graph
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("day_planner", day_planner_node)
    workflow.add_node("content_generator", content_generator_node)
    workflow.add_node("formatter", formatter_node)
    workflow.add_node("save", save_node)
    
    # Define the edges
    workflow.add_edge(START, "day_planner")
    workflow.add_edge("day_planner", "content_generator")
    workflow.add_edge("content_generator", "formatter")
    workflow.add_edge("formatter", "save")
    workflow.add_edge("save", END)
    
    # Compile the graph
    return workflow.compile()

def get_user_input():
    """Get user input for theme and duration."""
    print("\n===== Social Media Content Creator =====\n")
    
    # Get theme from user
    theme = input("Enter your content theme (e.g., 'Fitness for Busy Professionals'): ")
    if not theme.strip():
        theme = "Fitness for Busy Professionals"  # Default theme
        print(f"Using default theme: '{theme}'")
    
    # Get duration from user with validation
    while True:
        duration_input = input("Enter number of days for your content plan (7, 15, 30, etc.): ")
        try:
            duration = int(duration_input)
            if duration > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get generation method preference
    while True:
        generation_method = input("Choose generation method (model/rule-based) [model]: ").lower()
        if not generation_method or generation_method in ["model", "rule-based", "rule"]:
            if not generation_method or generation_method == "model":
                use_model = True
                print("Using model-based generation (will fall back to rule-based if model is unavailable)")
            else:
                use_model = False
                print("Using rule-based generation")
            break
        else:
            print("Please enter 'model' or 'rule-based'")
    
    # Get randomness level
    while True:
        randomness = input("Set randomness level (low/medium/high) [medium]: ").lower()
        if not randomness or randomness in ["low", "medium", "high"]:
            if not randomness:
                randomness = "medium"
            print(f"Using {randomness} randomness level")
            break
        else:
            print("Please enter 'low', 'medium', or 'high'")
    
    # Get output file path
    output = input("Enter output file name (default: content_calendar.csv): ")
    if not output.strip():
        output = "content_calendar.csv"
    
    return theme, duration, output, use_model, randomness

def main():
    # Check if command line arguments are provided
    parser = argparse.ArgumentParser(description="Generate a social media content calendar")
    parser.add_argument("--theme", type=str, help="The brand theme for content generation")
    parser.add_argument("--duration", type=int, help="Number of days for content plan")
    parser.add_argument("--output", type=str, help="Output file path")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--use-model", action="store_true", help="Use model-based generation (default)")
    parser.add_argument("--rule-based", action="store_true", help="Use rule-based generation")
    parser.add_argument("--randomness", type=str, choices=["low", "medium", "high"], default="medium", 
                        help="Set randomness level for generation (default: medium)")
    args = parser.parse_args()
    
    # Determine if we should use interactive mode
    interactive_mode = args.interactive or (args.theme is None and args.duration is None)
    
    if interactive_mode:
        # Get user input interactively
        theme, duration, output, use_model, randomness = get_user_input()
    else:
        # Use command line arguments or defaults
        theme = args.theme or "Fitness for Busy Professionals"
        duration = args.duration or 30
        output = args.output or "content_calendar.csv"
        # Determine generation method (rule-based flag takes precedence if both are specified)
        use_model = not args.rule_based if args.rule_based else args.use_model
        randomness = args.randomness
    
    # Build the graph
    graph = build_graph()
    
    # Initialize the state
    initial_state = {
        "brand_theme": theme,
        "duration": duration,
        "output_path": output,
        "use_model": use_model,
        "randomness": randomness,
        "topics": None,
        "content": None,
        "formatted_content": None
    }
    
    # Run the graph
    print(f"\nGenerating {duration}-day content plan for theme: '{theme}'...")
    print(f"Using {'model-based' if use_model else 'rule-based'} generation with {randomness} randomness")
    final_state = graph.invoke(initial_state)
    
    print(f"Content plan saved to {final_state['output_path']}")

if __name__ == "__main__":
    main()
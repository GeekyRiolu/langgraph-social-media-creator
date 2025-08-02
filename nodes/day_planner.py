from typing import Dict, List
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import LlamaCpp

# Initialize the LLM
def get_llm():
    """Initialize the LLM with appropriate settings."""
    # Check if models directory exists, create if not
    models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, "mistral-7b-instruct-v0.2.Q4_K_M.gguf")
    
    if not os.path.exists(model_path):
        print(f"\nModel not found at {model_path}")
        print("To use the LLM functionality, please download the Mistral model:")
        print("1. Visit https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/")
        print("2. Download the 'mistral-7b-instruct-v0.2.Q4_K_M.gguf' file")
        print(f"3. Place it in the '{models_dir}' directory\n")
        print("Using rule-based fallback for topic generation...")
        return None
    
    try:
        return LlamaCpp(
            model_path=model_path,
            temperature=0.7,
            max_tokens=2048,
            top_p=1,
            verbose=False,
        )
    except Exception as e:
        print(f"Error loading LlamaCpp model: {e}")
        print("Using rule-based fallback for topic generation...")
        return None

# Define the prompt template
day_planner_prompt = ChatPromptTemplate.from_template(
    """You are a social media content strategist. 
    Generate {duration} unique and engaging topic ideas for a social media content calendar 
    based on the theme: '{brand_theme}'.
    
    Each topic should be concise (5-10 words) and directly related to the theme.
    Ensure topics are varied and cover different aspects of the theme.
    
    Format your response as a numbered list with one topic per line.
    Do not include any explanations or additional text.
    """
)

def generate_rule_based_topics(brand_theme: str, duration: int) -> List[str]:
    """Generate topics using rule-based approach when LLM is not available."""
    base_topics = [
        "Introduction to {}",
        "Benefits of {}",
        "Quick Tips for {}",
        "Common Myths about {}",
        "How to Start with {}",
        "Success Stories with {}",
        "Challenges of {}",
        "Tools for {}",
        "Best Practices for {}",
        "Future of {}",
        "{} for Beginners",
        "Advanced {} Techniques",
        "Q&A about {}",
        "Comparing {} Approaches",
        "Daily {} Habits",
        "{} Inspiration",
        "Weekend {} Challenge",
        "Transforming Your Life with {}",
        "{} Community Spotlight",
        "Resources for {}",
        "Overcoming {} Obstacles",
        "Measuring {} Progress",
        "Integrating {} into Daily Life",
        "Seasonal {} Tips",
        "{} Motivation Monday",
        "Behind the Scenes of {}",
        "{} Transformation Tuesday",
        "{} Wisdom Wednesday",
        "{} Throwback Thursday",
        "{} Feature Friday",
    ]
    
    # Generate topics by formatting with the brand theme
    topics = [topic.format(brand_theme) for topic in base_topics[:duration]]
    
    # If we need more topics than our templates, add numbered variations
    while len(topics) < duration:
        index = len(topics) - len(base_topics) + 1
        template = base_topics[len(topics) % len(base_topics)]
        topics.append(f"{template.format(brand_theme)} - Part {index}")
    
    return topics

def day_planner_node(state: Dict) -> Dict:
    """Generate topic ideas for each day based on the brand theme."""
    # Extract parameters from state
    brand_theme = state["brand_theme"]
    duration = state["duration"]
    use_model = state.get("use_model", True)  # Default to True if not specified
    
    # Try to use LLM for topic generation if requested
    llm = get_llm() if use_model else None
    topics = []
    
    if llm:
        try:
            # Generate the prompt
            prompt = day_planner_prompt.format(brand_theme=brand_theme, duration=duration)
            
            # Get response from LLM
            response = llm.invoke(prompt)
            
            # Parse the response into a list of topics
            for line in response.strip().split("\n"):
                # Remove numbering and whitespace
                cleaned_line = line.strip()
                if cleaned_line:
                    # Extract just the topic text (remove numbering like "1. ")
                    if ". " in cleaned_line and cleaned_line[0].isdigit():
                        topic = cleaned_line.split(". ", 1)[1]
                    else:
                        topic = cleaned_line
                    topics.append(topic)
        except Exception as e:
            print(f"Error using LLM for topic generation: {e}")
            print("Falling back to rule-based topic generation...")
            topics = []
    
    # If LLM failed or is not available or not requested, use rule-based approach
    if not topics:
        topics = generate_rule_based_topics(brand_theme, duration)
    
    # Ensure we have exactly the requested number of topics
    topics = topics[:duration]
    
    # If we still don't have enough topics, generate some generic ones
    while len(topics) < duration:
        topics.append(f"Day {len(topics) + 1} - {brand_theme} Tips")
    
    # Update the state with the topics
    state["topics"] = topics
    return state
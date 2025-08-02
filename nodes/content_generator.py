from typing import Dict, List
import os
import random
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import LlamaCpp

# Import the model utilities
from nodes.model_utils import get_llm

# Define the prompt template
content_generator_prompt = ChatPromptTemplate.from_template(
    """You are a social media content creator for a brand with the theme: '{brand_theme}'.
    
    Create engaging social media content for the topic: '{topic}'.
    
    Your response should include:
    1. A short caption (1-2 sentences)
    2. 3-5 relevant hashtags
    
    Format your response exactly like this:
    Caption: [Your caption here]
    Hashtags: [hashtag1] [hashtag2] [hashtag3] [hashtag4] [hashtag5]
    
    Be concise, engaging, and on-brand.
    """
)

def generate_rule_based_content(brand_theme: str, topic: str, randomness: str = "medium") -> Dict:
    """Generate content using rule-based approach when LLM is not available."""
    # Template captions
    caption_templates = [
        "Ready to transform your {} journey? Today we're focusing on {}!",
        "Discover how {} can change your perspective on {}.",
        "Let's explore {} together and see how it impacts your {}.",
        "Today's {} tip: Make time for {} in your busy schedule.",
        "The secret to successful {} is understanding {}. Here's why!",
        "Have you incorporated {} into your {} routine yet? Here's how to start.",
        "Struggling with {}? Our {} approach might be just what you need.",
        "Your daily dose of {} inspiration: {} made simple.",
        "The most overlooked aspect of {} is {}. Let's change that!",
        "Small steps toward {} success: Focus on {} today.",
        # Additional templates for more variety
        "Breaking down {} concepts: {} explained simply.",
        "The {} revolution starts with {}. Are you ready?",
        "Mastering {} through the lens of {}. A fresh perspective!",
        "Why {} matters: The impact of {} on your daily life.",
        "From novice to expert: {} strategies for {}.",
        "The untold benefits of {} when approaching {}.",
        "Reimagining {} through innovative {} techniques.",
        "Behind every successful {} is a solid {}. Here's the proof.",
        "The {} advantage: Leveraging {} for maximum results.",
        "Transformative {} practices: {} edition."
    ]
    
    # Template hashtags for different themes with more variety
    hashtag_templates = {
        "fitness": [
            ["#FitnessJourney", "#HealthyLifestyle", "#WorkoutMotivation", "#FitnessTips", "#ActiveLifestyle"],
            ["#GetFit", "#FitnessGoals", "#TrainHard", "#HealthyBody", "#FitnessMotivation"],
            ["#WorkoutRoutine", "#StayActive", "#FitLife", "#StrengthTraining", "#MoveYourBody"],
            ["#FitnessCommunity", "#HealthyHabits", "#ExerciseDaily", "#FitnessJunkie", "#WorkoutWednesday"]
        ],
        "nutrition": [
            ["#HealthyEating", "#NutritionTips", "#CleanEating", "#MealPrep", "#BalancedDiet"],
            ["#EatWell", "#NutritionFacts", "#HealthyFood", "#FoodIsFuel", "#NutritiousFood"],
            ["#HealthyMeals", "#WholeFoods", "#NutritionGoals", "#EatHealthy", "#FoodForThought"],
            ["#MindfulEating", "#NutritionCoach", "#HealthyRecipes", "#FuelYourBody", "#EatTheRainbow"]
        ],
        "wellness": [
            ["#SelfCare", "#WellnessJourney", "#MindBodyBalance", "#HealthyHabits", "#WellnessWednesday"],
            ["#MentalHealth", "#Mindfulness", "#WellnessLifestyle", "#SelfLove", "#HealthAndWellness"],
            ["#WellnessTips", "#HolisticHealth", "#WellBeing", "#MindfulLiving", "#BalancedLife"],
            ["#WellnessWarrior", "#SelfCareRoutine", "#MindBodySpirit", "#WellnessCoach", "#InnerPeace"]
        ],
        "business": [
            ["#BusinessTips", "#Entrepreneurship", "#Success", "#Leadership", "#BusinessGrowth"],
            ["#StartupLife", "#BusinessStrategy", "#EntrepreneurMindset", "#SmallBusiness", "#BusinessOwner"],
            ["#BusinessAdvice", "#GrowthMindset", "#BusinessCoach", "#MarketingStrategy", "#BusinessSuccess"],
            ["#NetworkingTips", "#BusinessDevelopment", "#InnovationStrategy", "#LeadershipSkills", "#BusinessInsights"]
        ],
        "technology": [
            ["#TechTips", "#Innovation", "#DigitalTransformation", "#FutureTech", "#TechnologyTrends"],
            ["#TechNews", "#DigitalInnovation", "#EmergingTech", "#TechSolutions", "#InnovationMindset"],
            ["#AITechnology", "#TechStartup", "#DigitalStrategy", "#TechForGood", "#InnovationLeadership"],
            ["#TechCommunity", "#DigitalDisruption", "#FutureTrends", "#TechInnovation", "#SmartTechnology"]
        ],
        "default": [
            ["#DailyTips", "#LifeHacks", "#Inspiration", "#Growth", "#Motivation"],
            ["#LifeTips", "#PersonalGrowth", "#DailyInspiration", "#PositiveVibes", "#SuccessMindset"],
            ["#GoodVibes", "#LifeLessons", "#MindsetMatters", "#DailyMotivation", "#InspirationDaily"],
            ["#LifeGoals", "#PositiveThinking", "#MindsetShift", "#GrowthMindset", "#DailyWisdom"]
        ]
    }
    
    # Set temperature based on randomness level
    if randomness == "low":
        # Less random - use first few templates
        caption_template = random.choice(caption_templates[:5])
        hashtag_set_index = 0
    elif randomness == "high":
        # More random - use all templates and add some variations
        caption_template = random.choice(caption_templates)
        # Sometimes add an emoji to the caption
        emojis = ["✨", "🔥", "💪", "🌟", "📈", "🚀", "💯", "🎯", "⚡", "🌈"]
        if random.random() > 0.5:
            caption_template = random.choice(emojis) + " " + caption_template
        hashtag_set_index = random.randint(0, 3)
    else:  # medium (default)
        caption_template = random.choice(caption_templates[:15])
        hashtag_set_index = random.randint(0, 2)
    
    # Format the caption
    words = brand_theme.split()
    theme_word = words[0].lower() if words else "lifestyle"
    caption = caption_template.format(theme_word, topic)
    
    # Select hashtags based on theme
    for theme_key in hashtag_templates.keys():
        if theme_key in brand_theme.lower():
            hashtag_set = hashtag_templates[theme_key]
            break
    else:
        hashtag_set = hashtag_templates["default"]
    
    # Get the hashtags from the selected set
    hashtags = hashtag_set[hashtag_set_index].copy()
    
    # Add a theme-specific hashtag
    theme_hashtag = "#" + ''.join(word.capitalize() for word in brand_theme.split())
    if theme_hashtag not in hashtags:
        hashtags[random.randint(0, len(hashtags)-1)] = theme_hashtag
    
    # For high randomness, shuffle the hashtags
    if randomness == "high":
        random.shuffle(hashtags)
    
    return {
        "caption": caption,
        "hashtags": " ".join(hashtags)
    }

def content_generator_node(state: Dict) -> Dict:
    """Generate content (caption and hashtags) for each topic."""
    # Extract parameters from state
    brand_theme = state["brand_theme"]
    topics = state["topics"]
    use_model = state.get("use_model", True)  # Default to True if not specified
    randomness = state.get("randomness", "medium")  # Default to medium if not specified
    
    # Set temperature based on randomness level
    if randomness == "low":
        temperature = 0.3
    elif randomness == "high":
        temperature = 1.0
    else:  # medium
        temperature = 0.7
    
    # Try to use LLM for content generation if requested
    llm = get_llm(use_tinyllama=True) if use_model else None
    content_list = []
    
    for day, topic in enumerate(topics, start=1):
        content_item = {
            "day": day,
            "topic": topic,
            "caption": "",
            "hashtags": ""
        }
        
        if llm:
            try:
                # Generate the prompt
                prompt = content_generator_prompt.format(brand_theme=brand_theme, topic=topic)
                
                # Get response from LLM with adjusted temperature
                response = llm.invoke(prompt, temperature=temperature)
                
                # Parse the response
                caption = ""
                hashtags = []
                
                for line in response.strip().split("\n"):
                    if line.startswith("Caption:"):
                        caption = line.replace("Caption:", "").strip()
                    elif line.startswith("Hashtags:"):
                        hashtag_text = line.replace("Hashtags:", "").strip()
                        # Extract hashtags (they might be space-separated or formatted as #tag)
                        hashtags = [tag.strip() for tag in hashtag_text.split() if tag.strip()]
                        # Ensure hashtags start with #
                        hashtags = [tag if tag.startswith("#") else f"#{tag}" for tag in hashtags]
                
                if caption and hashtags:
                    content_item["caption"] = caption
                    content_item["hashtags"] = " ".join(hashtags[:5])  # Limit to 5 hashtags
                else:
                    # Fallback if parsing failed
                    rule_based = generate_rule_based_content(brand_theme, topic, randomness)
                    content_item["caption"] = rule_based["caption"]
                    content_item["hashtags"] = rule_based["hashtags"]
                    
            except Exception as e:
                print(f"Error using LLM for content generation for topic '{topic}': {e}")
                print("Falling back to rule-based content generation...")
                rule_based = generate_rule_based_content(brand_theme, topic, randomness)
                content_item["caption"] = rule_based["caption"]
                content_item["hashtags"] = rule_based["hashtags"]
        else:
            # Use rule-based approach if LLM is not available or not requested
            rule_based = generate_rule_based_content(brand_theme, topic, randomness)
            content_item["caption"] = rule_based["caption"]
            content_item["hashtags"] = rule_based["hashtags"]
        
        content_list.append(content_item)
    
    # Update the state with the content
    state["content"] = content_list
    return state
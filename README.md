# LangGraph Social Media Content Creator

A LangGraph-based agent that generates a social media content calendar based on a theme.

## Features

- Generate a 30-day (or custom duration) social media content plan
- Create engaging topics, captions, and hashtags
- Save the plan as a CSV file
- Supports both LLM-based and rule-based content generation
- Automatic model downloading (with huggingface_hub installed)

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Model Options:**
   - **Automatic Download (Recommended)**: The system will automatically download TinyLlama (1.1B parameters, ~670MB) when first run if you have `huggingface_hub` installed.
   - **Manual Download**: Download [tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf](https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf) (~670MB) and place it in the `models` directory (will be created automatically if it doesn't exist)

## Usage

### Interactive Mode

Run the script without arguments to use interactive mode:

```bash
python main.py
```

You'll be prompted to enter:
- Content theme (e.g., "Fitness for Busy Professionals")
- Number of days for your content plan (7, 15, 30, etc.)
- Output file name (defaults to content_calendar.csv)

### Command Line Arguments

```bash
python main.py --theme "Healthy Cooking" --duration 15 --output meal_plan.csv --rule-based --randomness medium
```

Arguments:
- `--theme`: The brand theme for content generation
- `--duration`: Number of days for content plan (default: 30)
- `--output`: Output file path (default: content_calendar.csv)
- `--interactive`: Force interactive mode
- `--use-model`: Use model-based generation (default)
- `--rule-based`: Use rule-based generation (overrides `--use-model`)
- `--randomness`: Set randomness level for generation (low/medium/high, default: medium)

## Output Format

The generated CSV file contains the following columns:
- Day: The day number (1-30)
- Topic: The content topic for that day
- Caption: A 1-2 sentence caption for the post
- Hashtags: 3-5 relevant hashtags

## Project Structure

- `main.py`: Entry point and LangGraph workflow definition
- `nodes/`: Directory containing the workflow nodes
  - `day_planner.py`: Generates topic ideas
  - `content_generator.py`: Creates captions and hashtags
  - `formatter.py`: Formats content as a DataFrame
  - `save.py`: Saves the content to a CSV file
  - `model_utils.py`: Handles model downloading and initialization
- `models/`: Directory for storing LLM models (created automatically)
- `requirements.txt`: Project dependencies

## License

MIT License
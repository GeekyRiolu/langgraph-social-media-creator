import gradio as gr
import pandas as pd
from typing import Dict, List, Optional, TypedDict
from langgraph.graph import END, START, StateGraph

# Import our custom nodes
from nodes.day_planner import day_planner_node
from nodes.content_generator import content_generator_node
from nodes.formatter import formatter_node
from nodes.save import save_node

# Custom CSS for dark theme and modern styling
CUSTOM_CSS = """
/* Dark theme variables */
:root {
    --primary-color: #6366f1;
    --primary-hover: #5855eb;
    --secondary-color: #1f2937;
    --background-dark: #0f172a;
    --background-card: #1e293b;
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --border-color: #334155;
    --accent-color: #10b981;
    --warning-color: #f59e0b;
    --error-color: #ef4444;
    --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --gradient-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
    --shadow-md: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
}

/* Global dark theme */
.gradio-container {
    background: var(--background-dark) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Main container styling */
.main-container {
    background: var(--background-dark);
    min-height: 100vh;
    padding: 2rem;
}

/* Header styling */
.header-section {
    text-align: center;
    margin-bottom: 3rem;
    padding: 2rem;
    background: var(--gradient-primary);
    border-radius: 20px;
    box-shadow: var(--shadow-lg);
}

.header-section h1 {
    color: white !important;
    font-size: 3rem !important;
    font-weight: 800 !important;
    margin-bottom: 1rem !important;
    text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.header-section p {
    color: rgba(255, 255, 255, 0.9) !important;
    font-size: 1.2rem !important;
    font-weight: 400 !important;
    margin: 0 !important;
}

/* Card styling */
.settings-card, .chat-card {
    background: var(--background-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    box-shadow: var(--shadow-md) !important;
    backdrop-filter: blur(10px);
}

/* Settings panel */
.settings-card {
    background: linear-gradient(145deg, #1e293b, #334155) !important;
    min-width: 400px !important;
}

.settings-card h3 {
    color: var(--primary-color) !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    margin-bottom: 2rem !important;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Settings form elements spacing */
.settings-card .gradio-group {
    margin-bottom: 1.5rem !important;
}

.settings-card .gradio-textbox,
.settings-card .gradio-slider,
.settings-card .gradio-radio {
    margin-bottom: 1.5rem !important;
}

.settings-card label {
    font-size: 1rem !important;
    font-weight: 600 !important;
    margin-bottom: 0.5rem !important;
    color: var(--text-primary) !important;
}

/* Input styling */
.gradio-textbox, .gradio-slider, .gradio-radio {
    background: var(--background-dark) !important;
    border: 2px solid var(--border-color) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    transition: all 0.3s ease !important;
}

.gradio-textbox:focus, .gradio-slider:focus {
    border-color: var(--primary-color) !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
}

/* Button styling */
.gradio-button {
    background: var(--gradient-primary) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 0.75rem 1.5rem !important;
    transition: all 0.3s ease !important;
    box-shadow: var(--shadow-md) !important;
}

.gradio-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-lg) !important;
}

/* Chat interface */
.chat-card {
    height: 100%;
    max-width: none !important;
}

.gradio-chatbot {
    background: var(--background-dark) !important;
    border: 2px solid var(--border-color) !important;
    border-radius: 16px !important;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    width: 100% !important;
    max-width: none !important;
}

/* Message bubbles with reduced width */
.gradio-chatbot .message {
    background: var(--background-card) !important;
    border-radius: 12px !important;
    margin: 0.5rem !important;
    padding: 1rem !important;
    border: 1px solid var(--border-color) !important;
    max-width: 70% !important;
    word-wrap: break-word !important;
}

.gradio-chatbot .message.user {
    background: var(--gradient-primary) !important;
    color: white !important;
    margin-left: auto !important;
    margin-right: 1rem !important;
    max-width: 60% !important;
}

.gradio-chatbot .message.bot {
    background: var(--background-card) !important;
    color: var(--text-primary) !important;
    margin-left: 1rem !important;
    margin-right: auto !important;
    max-width: 75% !important;
}

/* Chat container styling */
.gradio-chatbot > div {
    width: 100% !important;
    max-width: none !important;
}

/* Message content styling */
.gradio-chatbot .message-content {
    width: 100% !important;
    overflow-wrap: break-word !important;
    word-break: break-word !important;
}

/* Download section styling */
.download-section .gradio-file {
    background: var(--background-card) !important;
    border: 2px dashed var(--border-color) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    padding: 1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: var(--shadow-md) !important;
}

.download-section .gradio-file:hover {
    border-color: var(--primary-color) !important;
    background: var(--background-dark) !important;
    cursor: pointer;
}


/* Quick start section */
.quick-start {
    background: linear-gradient(145deg, #0f172a, #1e293b) !important;
    border: 1px solid var(--primary-color) !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    margin-top: 2rem !important;
}

.quick-start h4 {
    color: var(--accent-color) !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    margin-bottom: 1rem !important;
}

.quick-start ol {
    color: var(--text-secondary) !important;
    padding-left: 1.5rem !important;
}

.quick-start li {
    margin-bottom: 0.5rem !important;
    line-height: 1.6 !important;
}

/* Status indicators */
.status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.875rem;
    font-weight: 500;
}

.status-success {
    background: rgba(16, 185, 129, 0.1);
    color: var(--accent-color);
    border: 1px solid var(--accent-color);
}

.status-warning {
    background: rgba(245, 158, 11, 0.1);
    color: var(--warning-color);
    border: 1px solid var(--warning-color);
}

.status-error {
    background: rgba(239, 68, 68, 0.1);
    color: var(--error-color);
    border: 1px solid var(--error-color);
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.fade-in {
    animation: fadeIn 0.6s ease-out;
}

.pulse {
    animation: pulse 2s infinite;
}

/* Layout improvements */
.gradio-container .gradio-row {
    width: 100% !important;
    max-width: none !important;
}

.gradio-container .gradio-column {
    width: 100% !important;
}

/* Chat interface width improvements */
.chat-card .gradio-chatbot {
    min-height: 600px !important;
    width: 100% !important;
}

/* Message bubble improvements */
.gradio-chatbot .message-wrap {
    width: 100% !important;
    display: flex !important;
}

.gradio-chatbot .message-wrap.user {
    justify-content: flex-end !important;
}

.gradio-chatbot .message-wrap.bot {
    justify-content: flex-start !important;
}

/* Responsive design */
@media (max-width: 768px) {
    .main-container {
        padding: 1rem;
    }

    .header-section h1 {
        font-size: 2rem !important;
    }

    .settings-card, .chat-card {
        padding: 1rem !important;
    }

    .gradio-chatbot .message {
        max-width: 85% !important;
    }

    .gradio-chatbot .message.user {
        max-width: 80% !important;
    }
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--background-dark);
}

::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--primary-color);
}

/* Avatar styling with white background - Multiple selectors for compatibility */
.gradio-chatbot .avatar,
.gradio-chatbot .avatar img,
.gradio-chatbot img[alt="avatar"],
.gradio-chatbot .message img,
.gradio-chatbot .user img,
.gradio-chatbot .bot img,
.gradio-chatbot [data-testid="avatar"],
.gradio-chatbot [class*="avatar"] img,
.gradio-chatbot [class*="Avatar"] img {
    background-color: white !important;
    border-radius: 50% !important;
    padding: 6px !important;
    border: 2px solid var(--border-color) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    width: 40px !important;
    height: 40px !important;
    min-width: 40px !important;
    min-height: 40px !important;
    max-width: 40px !important;
    max-height: 40px !important;
    object-fit: contain !important;
    display: block !important;
}

/* Force white background on all possible avatar containers */
.gradio-chatbot div[class*="avatar"],
.gradio-chatbot div[class*="Avatar"],
.gradio-chatbot .message > div:first-child,
.gradio-chatbot .user > div:first-child,
.gradio-chatbot .bot > div:first-child {
    background-color: white !important;
    border-radius: 50% !important;
    padding: 6px !important;
    border: 2px solid var(--border-color) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    width: 52px !important;
    height: 52px !important;
    min-width: 52px !important;
    min-height: 52px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* Ensure SVG content fits properly */
.gradio-chatbot .avatar svg,
.gradio-chatbot img[alt="avatar"] svg,
.gradio-chatbot .message img svg {
    width: 28px !important;
    height: 28px !important;
    fill: currentColor !important;
}

/* User avatar specific styling */
.gradio-chatbot .message.user .avatar,
.gradio-chatbot .message.user .avatar img,
.gradio-chatbot .user .avatar,
.gradio-chatbot .user img {
    background-color: white !important;
    border-color: var(--primary-color) !important;
}

/* Bot avatar specific styling */
.gradio-chatbot .message.bot .avatar,
.gradio-chatbot .message.bot .avatar img,
.gradio-chatbot .bot .avatar,
.gradio-chatbot .bot img {
    background-color: white !important;
    border-color: var(--accent-color) !important;
}

/* Additional aggressive targeting for Gradio's avatar system */
.gradio-chatbot img[src*="male-icon.svg"],
.gradio-chatbot img[src*="chatbot-icon.svg"] {
    background-color: white !important;
    border-radius: 50% !important;
    padding: 6px !important;
    border: 2px solid var(--primary-color) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    width: 40px !important;
    height: 40px !important;
}

/* Force styling on all images in chatbot */
.gradio-chatbot img {
    background-color: white !important;
    border-radius: 50% !important;
    padding: 6px !important;
    border: 2px solid var(--border-color) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    width: 40px !important;
    height: 40px !important;
    object-fit: contain !important;
}

/* Override any default Gradio avatar styling */
.gradio-container .gradio-chatbot img {
    background: white !important;
    border-radius: 50% !important;
    padding: 6px !important;
}

"""

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

def generate_content_plan(theme: str, duration: int, generation_method: str, randomness: str, history, user_message: str):
    """Generate content plan and return formatted response."""
    try:
        # Validate inputs
        if not theme.strip():
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": "Please provide a valid brand theme."})
            return history

        if duration < 1 or duration > 365:
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": "Duration must be between 1 and 365 days."})
            return history
        
        # Determine generation method
        use_model = generation_method == "Model-based (TinyLlama)"
        
        # Build the graph
        graph = build_graph()
        
        # Initialize the state
        initial_state = {
            "brand_theme": theme,
            "duration": duration,
            "output_path": "temp_content_calendar.csv",
            "use_model": use_model,
            "randomness": randomness.lower(),
            "topics": None,
            "content": None,
            "formatted_content": None
        }
        
        # Add user message and status message
        history.append({"role": "user", "content": user_message})
        status_msg = f"🚀 Generating {duration}-day content plan for '{theme}' using {generation_method.lower()} with {randomness.lower()} randomness..."
        history.append({"role": "assistant", "content": status_msg})
        
        # Run the graph
        final_state = graph.invoke(initial_state)
        
        # Format the response
        df = final_state['formatted_content']

        # Create a clean, markdown-formatted summary
        summary = f"""
## ✅ Content Plan Generated Successfully!

**🎨 Theme:** {theme}
**📅 Duration:** {duration} days
**🤖 Method:** {generation_method}
**🎲 Creativity:** {randomness}

---

### 📝 Sample Content Preview

"""

        # Add first 3 entries as examples with clean formatting
        for i in range(min(3, len(df))):
            row = df.iloc[i]
            summary += f"""
**📅 Day {row['day']}: {row['topic']}**

💬 *{row['caption']}*

🏷️ `{row['hashtags']}`

---
"""

        if len(df) > 3:
            summary += f"\n✨ **... and {len(df) - 3} more days of amazing content!**\n\n"

        # Save to file for download
        output_filename = f"{theme.replace(' ', '_').lower()}_content_plan.csv"
        df.to_csv(output_filename, index=False)

        # Add download section
        summary += f"""
### 📁 Download Your Content Plan

Your content plan has been saved as **`{output_filename}`**

🎉 **Ready to boost your social media presence!**
"""

        history.append({"role": "assistant", "content": summary})

        # Return both history and the file path for download
        return history, output_filename

    except Exception as e:
        error_msg = f"❌ **Error:** {str(e)}\n\nPlease try again with different parameters."
        history.append({"role": "assistant", "content": error_msg})
        return history

def chat_interface(message, history, theme, duration, generation_method, randomness):
    """Main chat interface function."""
    if not message.strip():
        return history, "", None

    # Check if user is asking to generate content
    if any(keyword in message.lower() for keyword in ["generate", "create", "make", "plan", "content"]):
        if not theme.strip():
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": "Please enter a brand theme first using the sidebar options."})
            return history, "", None

        updated_history, download_file = generate_content_plan(theme, duration, generation_method, randomness, history, message)
        return updated_history, "", download_file

    # Handle general questions about the tool
    elif any(keyword in message.lower() for keyword in ["help", "how", "what", "?"]):
        help_response = """
## 🤖 Social Media Content Creator Help

### 📋 How to Use:

1. **Enter your brand theme** in the sidebar (e.g., "Healthy Cooking", "Travel Photography")
2. **Set the number of days** for your content plan (1-365)
3. **Choose generation method:**
   - **Rule-based:** Fast, no model download required
   - **Model-based:** Uses TinyLlama AI model for more creative content
4. **Set creativity level** (Low/Medium/High)
5. **Type "generate"** or "create content plan" to start

---

### 🎯 Example Themes:
- Fitness for Busy Professionals
- Sustainable Living Tips
- Small Business Marketing
- Photography Techniques
- Healthy Recipe Ideas

### 📦 What You'll Get:
- Daily content topics
- Engaging captions (1-2 sentences)
- Relevant hashtags (3-5 per post)
- Downloadable CSV file

---

### 🚀 Ready to start?
Just say **"generate"** when you're ready!
"""
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": help_response})
        return history, "", None

    else:
        # General conversation
        response = f"I'm here to help you create social media content plans! Set your brand theme in the sidebar and say 'generate' to create your content plan. Type 'help' for more information."
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})
        return history, "", None

# Create the modern Gradio interface with dark theme
with gr.Blocks(
    title="🎯 Social Media Content Creator - AI Powered",
    theme=gr.themes.Base(),
    css=CUSTOM_CSS,
    head="""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    """
) as demo:

    # Header section
    with gr.Row(elem_classes="header-section fade-in"):
        gr.HTML("""
        <div style="text-align: center;">
            <h1>🎯 Social Media Content Creator</h1>
            <p>Generate engaging social media content plans for your brand using AI or rule-based generation</p>
        </div>
        """)

    # Main content area
    with gr.Row(elem_classes="main-container"):
        # Settings sidebar
        with gr.Column(scale=2, elem_classes="settings-card fade-in", min_width=400):
            gr.HTML("""
            <h3>⚙️ Settings</h3>
            """)

            theme_input = gr.Textbox(
                label="🎨 Brand Theme",
                placeholder="e.g., Healthy Cooking, Travel Photography, Fitness Tips",
                value="Fitness for Busy Professionals",
                elem_classes="modern-input",
                info="Define your brand's focus area for targeted content"
            )

            duration_input = gr.Slider(
                label="📅 Duration (days)",
                minimum=1,
                maximum=365,
                value=30,
                step=1,
                elem_classes="modern-slider",
                info="How many days of content to generate"
            )

            generation_method = gr.Radio(
                label="🤖 Generation Method",
                choices=["Rule-based (Fast)", "Model-based (TinyLlama)"],
                value="Rule-based (Fast)",
                elem_classes="modern-radio",
                info="Choose between fast rule-based or AI-powered generation"
            )

            randomness_level = gr.Radio(
                label="🎲 Creativity Level",
                choices=["Low", "Medium", "High"],
                value="Medium",
                elem_classes="modern-radio",
                info="Control the variety and creativity of generated content"
            )

            # Status indicator
            status_display = gr.HTML("""
            <div class="status-indicator status-success">
                <span>✅</span> Ready to generate content
            </div>
            """)

        # Chat interface
        with gr.Column(scale=4, elem_classes="chat-card fade-in"):
            gr.HTML("""
            <h3>💬 Content Generation Chat</h3>
            """)

            chatbot = gr.Chatbot(
                height=600,
                placeholder="👋 Welcome!Set your brand theme in the sidebar and type 'generate' to create your content plan.",
                type="messages",
                elem_classes="modern-chatbot",
                avatar_images=("male-icon.svg", "chatbot-icon.svg"),
                show_copy_button=True
            )

            with gr.Row():
                msg = gr.Textbox(
                    label="",
                    placeholder="💬 Choose the prompt and press enter...",
                    container=False,
                    scale=4,
                    elem_classes="modern-input"
                )

                send_btn = gr.Button(
                    "Send 🚀",
                    variant="primary",
                    scale=1,
                    elem_classes="modern-button"
                )

            # Download section
            with gr.Row():
                download_file = gr.File(
                    label="📁 Download Your Content Plan",
                    visible=False,
                    elem_classes="download-section"
                )

            # Example prompts
            with gr.Row():
                gr.Examples(
                    examples=[
                        ["generate"],
                        ["create content plan"],
                        ["help"],
                        ["what can you do?"],
                        ["show me examples"]
                    ],
                    inputs=msg,
                    label="💡 Try these prompts:"
                )
    
    # Handle message submission
    def handle_message_submit(message, history, theme, duration, gen_method, randomness):
        """Handle message submission with loading state."""
        updated_history, cleared_msg, file_path = chat_interface(message, history, theme, duration, gen_method, randomness)

        # Show download file if content was generated
        if file_path:
            return updated_history, cleared_msg, gr.File(value=file_path, visible=True)
        else:
            return updated_history, cleared_msg, gr.File(visible=False)

    # Event handlers
    msg.submit(
        handle_message_submit,
        inputs=[msg, chatbot, theme_input, duration_input, generation_method, randomness_level],
        outputs=[chatbot, msg, download_file],
        show_progress=True
    )

    send_btn.click(
        handle_message_submit,
        inputs=[msg, chatbot, theme_input, duration_input, generation_method, randomness_level],
        outputs=[chatbot, msg, download_file],
        show_progress=True
    )

    # Update status when settings change
    def update_status(theme, duration, method, randomness):
        if theme.strip():
            method_emoji = "⚡" if "Rule-based" in method else "🤖"
            randomness_emoji = {"Low": "🔒", "Medium": "⚖️", "High": "🎲"}.get(randomness, "⚖️")
            return f"""
            <div class="status-indicator status-success">
                <span>✅</span> Ready to generate {duration} days of content for "{theme}" using {method_emoji} {method.split()[0]} with {randomness_emoji} {randomness} creativity
            </div>
            """
        else:
            return """
            <div class="status-indicator status-warning">
                <span>⚠️</span> Please set a brand theme to continue
            </div>
            """

    # Update status when inputs change
    for input_component in [theme_input, duration_input, generation_method, randomness_level]:
        input_component.change(
            update_status,
            inputs=[theme_input, duration_input, generation_method, randomness_level],
            outputs=[status_display]
        )

if __name__ == "__main__":
    print("🚀 Starting Social Media Content Creator...")
    print("🎯 Modern Dark Theme UI Loaded")
    print("📱 Access the app at: http://localhost:7860")

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True,
        show_api=False,  # Disable API docs to avoid schema issues
        quiet=True       # Reduce verbose output
    )

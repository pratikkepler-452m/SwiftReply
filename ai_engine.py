import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini AI
api_key = os.getenv("GEMINI_API_KEY")
if api_key and api_key != "YOUR_GEMINI_API_KEY_HERE":
    genai.configure(api_key=api_key)

def get_system_prompt(business_info: dict) -> str:
    """Generates the system prompt using the provided business configuration."""
    base_prompt = (
        "You are Swift Reply AI, a professional AI assistant for startups and small businesses. "
        "You help customers professionally and clearly. "
        "You answer using the business information provided. "
        "You are concise, intelligent, persuasive, and friendly. "
        "Always maintain a professional business tone. "
        "If information is unavailable, politely say so. "
        "If the user shows interest in the services, suggest that they provide their contact information to get in touch with our team.\n\n"
    )
    
    business_context = f"""
    --- BUSINESS INFORMATION ---
    Business Name: {business_info.get('name', 'N/A')}
    Industry: {business_info.get('industry', 'N/A')}
    Services: {business_info.get('services', 'N/A')}
    Company Description: {business_info.get('description', 'N/A')}
    FAQ Information: {business_info.get('faq', 'N/A')}
    Tone Style: {business_info.get('tone', 'Professional and Friendly')}
    --- END OF BUSINESS INFORMATION ---
    """
    
    return base_prompt + business_context

def create_chat_session(business_info: dict):
    """Initializes and returns a new Gemini chat session."""
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
         raise ValueError("GEMINI_API_KEY is missing. Please add it to the .env file.")
         
    system_instruction = get_system_prompt(business_info)
    
    # We use gemini-pro which is 100% supported in all regions and API key tiers.
    # We inject the system prompt directly into the starting history since gemini-pro doesn't natively support the system_instruction parameter.
    model = genai.GenerativeModel(model_name="gemini-pro")
    
    initial_history = [
        {"role": "user", "parts": [system_instruction + "\n\nDo you understand these instructions?"]},
        {"role": "model", "parts": ["Yes, I perfectly understand. I will act strictly as the Swift Reply AI assistant according to these instructions."]}
    ]
    
    return model.start_chat(history=initial_history)

def generate_response(chat_session, user_message: str) -> str:
    """Generates a response from the chat session."""
    try:
        response = chat_session.send_message(user_message)
        return response.text
    except Exception as e:
        return f"Error communicating with AI: {str(e)}"

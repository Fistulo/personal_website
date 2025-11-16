import os
from anthropic import AsyncAnthropic, APIError
import logging

logger = logging.getLogger(__name__)

# Load your personal info
with open("data/about_me.txt", "r") as f:
    ABOUT_ME = f.read()

client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

async def answer_question(question: str) -> str:
    """Answer questions about you using Claude."""
    
    try:
        message = await client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=300,
            system=f"""You are a helpful assistant answering questions about me. 
            Here's what you know:

            {ABOUT_ME}

            Guidelines:
            - Answer concisely and naturally
            - If you don't know something, say so
            - Be friendly and professional
            - Answer as if you were me responding""",
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        
        return message.content[0].text
        
    except APIError as e:
        logger.error(f"Anthropic API error: {e}")
        return "Sorry, I'm having trouble answering right now. Please try again later."
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return "An unexpected error occurred. Please try again."

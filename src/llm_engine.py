# Import Google's Gemini client
from google import genai

# Import our Gemini configuration
from src.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)


# Create the Gemini client
gemini_client = genai.Client(
    api_key=GEMINI_API_KEY
)


# Send a prompt to Gemini and return the generated answer
def generate_answer(prompt):

    # Try to communicate with Gemini
    try:

        # Use the Gemini Interactions API
        interaction = gemini_client.interactions.create(
            model=GEMINI_MODEL,
            input=prompt
        )

        # Return Gemini's generated text
        return interaction.output_text

    # Handle API errors
    except Exception as error:

        # Convert the error into text
        error_message = str(error)

        # Handle quota or rate-limit errors
        if (
            "429" in error_message
            or "quota" in error_message.lower()
        ):

            # Return a friendly message instead of crashing
            return (
                "⚠️ Gemini API quota has temporarily been reached. "
                "The SQL and RAG systems are working correctly, "
                "but Gemini's natural-language generation is "
                "currently unavailable. Please try again after "
                "the quota resets."
            )

        # Handle all other Gemini errors
        return (
            "⚠️ Gemini could not generate an answer right now. "
            "Please try again later."
        )

from app.llm.llm_interface import GeminiLLMProvider


def main():

    try:
        provider = GeminiLLMProvider()

        print("Connecting to Gemini AI...")

        response = provider.generate_response(
            "Reply with exactly: Hello, Gemini is working!"
        )

        print("\nGemini Response:")
        print(response)

        print("\nGemini API connection successful!")

    except Exception as error:
        print("\nGemini API connection failed.")
        print("Error:", error)


if __name__ == "__main__":
    main()

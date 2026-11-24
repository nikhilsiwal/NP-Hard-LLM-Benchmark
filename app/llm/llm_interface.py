
import os
import requests

from abc import ABC, abstractmethod
from dotenv import load_dotenv


load_dotenv()


class LLMProvider(ABC):

    @abstractmethod
    def generate_response(self, prompt):
        pass


class MockLLMProvider(LLMProvider):

    def generate_response(self, prompt):

        if not prompt:
            raise ValueError("Prompt cannot be empty")

        return '{"solution": [1, 0, 1, 0]}'


class GeminiLLMProvider(LLMProvider):

    def __init__(self, api_key=None, model="gemini-3.5-flash"):

        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Check your .env file."
            )

        self.model = model

        self.url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            f"models/{self.model}:generateContent"
        )

    def generate_response(self, prompt):

        if not prompt:
            raise ValueError("Prompt cannot be empty")

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }

        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        try:
            response = requests.post(
                self.url,
                headers=headers,
                json=data,
                timeout=120
            )

            response.raise_for_status()

        except requests.exceptions.Timeout:
            raise TimeoutError(
                "Gemini API took more than 120 seconds to respond."
            )

        result = response.json()

        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]

        except (KeyError, IndexError, TypeError):
            raise ValueError(
                "Invalid response received from Gemini API"
            )


if __name__ == "__main__":

    provider = MockLLMProvider()

    print(provider.generate_response("Test prompt"))




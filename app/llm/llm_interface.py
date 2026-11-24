
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

        self.prompt_tokens = None
        self.completion_tokens = None
        self.total_tokens = None

    def generate_response(self, prompt):

        if not prompt:
            raise ValueError("Prompt cannot be empty")

        self.prompt_tokens = None
        self.completion_tokens = None
        self.total_tokens = None

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
            response_text = (
                result["candidates"][0]["content"]["parts"][0]["text"]
            )

        except (KeyError, IndexError, TypeError):
            raise ValueError(
                "Invalid response received from Gemini API"
            )

        usage = result.get("usageMetadata", {})

        self.prompt_tokens = usage.get("promptTokenCount")
        self.completion_tokens = usage.get("candidatesTokenCount")
        self.total_tokens = usage.get("totalTokenCount")

        if self.total_tokens is None:
            if (
                self.prompt_tokens is not None
                and self.completion_tokens is not None
            ):
                self.total_tokens = (
                    self.prompt_tokens + self.completion_tokens
                )

        return response_text


class GroqLLMProvider(LLMProvider):

    def __init__(
        self,
        api_key=None,
        model="openai/gpt-oss-120b"
    ):

        self.api_key = api_key or os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise ValueError(
                "Groq API key not found. Check your .env file."
            )

        self.model = model

        self.url = (
            "https://api.groq.com/openai/v1/chat/completions"
        )

        self.prompt_tokens = None
        self.completion_tokens = None
        self.total_tokens = None

    def generate_response(self, prompt):

        if not prompt:
            raise ValueError("Prompt cannot be empty")

        self.prompt_tokens = None
        self.completion_tokens = None
        self.total_tokens = None

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_completion_tokens": 8192,
            "reasoning_effort": "low"
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
                "Groq API took more than 120 seconds to respond."
            )

        result = response.json()

        try:
            choice = result["choices"][0]
            message = choice["message"]
            response_text = message.get("content")

        except (KeyError, IndexError, TypeError):
            raise ValueError(
                "Invalid response received from Groq API"
            )

        usage = result.get("usage", {})

        self.prompt_tokens = usage.get("prompt_tokens")
        self.completion_tokens = usage.get("completion_tokens")
        self.total_tokens = usage.get("total_tokens")

        if self.total_tokens is None:
            if (
                self.prompt_tokens is not None
                and self.completion_tokens is not None
            ):
                self.total_tokens = (
                    self.prompt_tokens + self.completion_tokens
                )

        if not response_text or not response_text.strip():
            finish_reason = choice.get("finish_reason")

            raise ValueError(
                f"Groq returned an empty response. "
                f"Finish reason: {finish_reason}"
            )

        return response_text


if __name__ == "__main__":

    provider = MockLLMProvider()

    print(provider.generate_response("Test prompt"))



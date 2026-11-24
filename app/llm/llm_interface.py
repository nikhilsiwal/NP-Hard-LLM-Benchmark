
from abc import ABC, abstractmethod


class LLMProvider(ABC):

    @abstractmethod
    def generate_response(self, prompt):
        pass


class MockLLMProvider(LLMProvider):

    def generate_response(self, prompt):

        if not prompt:
            raise ValueError("Prompt cannot be empty")

        return '{"solution": [1, 0, 1, 0]}'


if __name__ == "__main__":

    provider = MockLLMProvider()

    sample_prompt = "Solve the Subset Sum Problem."

    response = provider.generate_response(sample_prompt)

    print("Prompt:", sample_prompt)
    print("LLM Response:", response)

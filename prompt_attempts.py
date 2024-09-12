from openai import OpenAI

from src.constants import OPENROUTER_API_URL, HERMES_405B
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.factories.concrete_llm_content_factory import ConcreteLlmContentFactory
from src.prompting.open_ai_llm_client import OpenAiLlmClient


def main():
    filesystem_manager = FilesystemManager()

    # gets API Key from environment variable OPENAI_API_KEY
    client = OpenAI(
        base_url=OPENROUTER_API_URL,
        api_key=filesystem_manager.load_secret_key(),
    )

    messages = [{"role": "user", "content": "Screwed up content"},
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "I'm going to see if the context changes or not"},
                {"role": "system", "content": "You are the same helpful assistant."},
                {"role": "user", "content": "Has the context changed?"},
                {"role": "system", "content": "The system context has changed once again!"},
                {"role": "user", "content": "Aw crap, the system role has changed so many times! Is this even legal?"}]

    content = ConcreteLlmContentFactory(model=HERMES_405B, messages=messages,
                                        llm_client=OpenAiLlmClient(client)).generate_content().get()

    print(content)


if __name__ == "__main__":
    main()

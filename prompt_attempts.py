from openai import OpenAI

from src.constants import OPENROUTER_API_URL, HERMES_405B
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.factories.concrete_ai_completion_factory import ConcreteAiCompletionFactory
from src.prompting.factories.open_ai_llm_content_factory import OpenAiLlmContentFactory


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

    content = OpenAiLlmContentFactory(client, model=HERMES_405B, messages=messages,
                                      ai_completion_factory=ConcreteAiCompletionFactory(
                                          client)).generate_content().get()

    print(content)


if __name__ == "__main__":
    main()

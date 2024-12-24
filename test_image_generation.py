import sys
from pathlib import Path

from src.augmentation.augment_text import augment_text
from src.filesystem.file_operations import write_binary_file
from src.images.factories.openai_generated_image_factory import (
    OpenAIGeneratedImageFactory,
)
from src.interfaces.console_interface_manager import ConsoleInterfaceManager
from src.prompting.factories.openai_llm_client_factory import OpenAILlmClientFactory
from src.requests.factories.ConcreteUrlContentFactory import ConcreteUrlContentFactory


def main():
    interface_manager = ConsoleInterfaceManager()
    original_prompt = "Create a close-up portrait, as it could appear in a painting or a photo ID, of the following: "
    input_text = interface_manager.prompt_for_input(
        "Enter your notion of what the portrait should show: "
    )
    prompt = original_prompt + input_text

    generated_image_product = OpenAIGeneratedImageFactory(
        OpenAILlmClientFactory().create_llm_client()
    ).generate_image(prompt)

    while not generated_image_product.is_valid():
        print(f"Was unable to generate image: {generated_image_product.get_error()}")

        [augmented_text, _] = augment_text(input_text, 0.01, 1, True, True, True)

        print(f"New text: {augmented_text}")

        input_text = augmented_text

        prompt = original_prompt + input_text

        generated_image_product = OpenAIGeneratedImageFactory(
            OpenAILlmClientFactory().create_llm_client()
        ).generate_image(prompt)

    url_content_product = ConcreteUrlContentFactory().get_url(
        generated_image_product.get()
    )

    if not url_content_product.is_valid():
        print(
            f"Was unable to get the content of the url: {url_content_product.get_error()}"
        )
        sys.exit()

    image_name = interface_manager.prompt_for_input(
        "What should be the name of the image?: "
    )

    write_binary_file(Path(f"data/images/{image_name}.png"), url_content_product.get())


if __name__ == "__main__":
    main()

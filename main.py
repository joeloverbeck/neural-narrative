import json
import sys

from openai import OpenAI

from files import read_file
from parsing import parse_tool_response
from tools import generate_tool_prompt


def main():
    # Function to load the content of GPT_SECRET_KEY.txt

    # Specify the path to the file
    file_path = 'GPT_SECRET_KEY.txt'

    # Load the secret key
    try:
        # Attempt to load the secret key
        secret_key = read_file(file_path)
    except FileNotFoundError:
        sys.exit(f"Error: File '{file_path}'not found. Please check the file path.")
    except Exception as e:
        sys.exit(f"An unexpected error occurred: {str(e)}")

    # Load the JSON file
    with open('character_generator_tool.json', 'r') as file:
        character_generator_tool = json.load(file)

    tool_prompt = generate_tool_prompt(character_generator_tool)

    character_generation_instructions = read_file('character_generation_instructions.txt')

    # gets API Key from environment variable OPENAI_API_KEY
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=secret_key,
    )

    completion = client.chat.completions.create(
        model="nousresearch/hermes-3-llama-3.1-405b",
        messages=[
            {
                "role": "system",
                "content": character_generation_instructions + "\n\n" + tool_prompt,
            },
            {
                "role": "user",
                "content": "Create the bio for a character based in the post-apocalypse. Make it quite extreme.",
            },
        ],
        temperature=1.0,
        top_p=1.0,
    )

    if completion.choices and completion.choices[0] and completion.choices[0].message:
        print(parse_tool_response(completion.choices[0].message.content))
    else:
        print("The LLM didn't return a valid message.")
        print(completion)


if __name__ == "__main__":
    main()

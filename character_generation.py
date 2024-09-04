from src.characters import generate_character, store_generated_character
from src.parsing import extract_character_from_tool_response


def main():
    # Loop until a valid playthrough name is provided
    while True:
        playthrough_name = input("Enter your playthrough name: ")
        if playthrough_name:
            break  # Exit the loop if the input is not empty
        else:
            print("Playthrough name cannot be empty. Please try again.")

    # Loop until a valid character description is provided
    while True:
        user_input = input("What kind of character would you like to generate? ")
        if user_input:
            break  # Exit the loop if the input is not empty
        else:
            print("Character description cannot be empty. Please try again.")

    # Print the final input for further processing or feedback
    print(f"Playthrough Name: {playthrough_name}")
    print(f"Character Description: {user_input}")

    parsed_tool_response = generate_character(user_input)

    # Extract character data using the function provided
    character_data = extract_character_from_tool_response(parsed_tool_response)

    store_generated_character(playthrough_name, character_data)


if __name__ == "__main__":
    main()

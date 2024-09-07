import sys

from src.playthroughs import create_playthrough
from src.prompting.prompting import prompt_for_input


def main():
    try:
        # Ask the user for the name of the playthrough
        playthrough_name = prompt_for_input("Enter the name of your playthrough: ")

        # Call the create_playthrough function
        playthrough_path = create_playthrough(playthrough_name)

        # Confirm that the playthrough has been successfully created
        print(f"Playthrough '{playthrough_name}' created successfully at {playthrough_path}.")

    except Exception as e:
        # Print the exception message and exit the program
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

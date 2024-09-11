import sys

from src.commands.create_playthrough_command import CreatePlaythroughCommand
from src.prompting.prompting import prompt_for_input


def main():
    try:
        # Ask the user for the name of the playthrough
        playthrough_name = prompt_for_input("Enter the name of your playthrough: ")

        # Ask the user for the name of the world template
        world_template = prompt_for_input("Enter the name of the world (from those in the template): ")

        # Call the create_playthrough function
        CreatePlaythroughCommand(playthrough_name, world_template).execute()
        
    except Exception as e:
        # Print the exception message and exit the program
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

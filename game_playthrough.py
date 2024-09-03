import os


def create_game_playthrough_folder(playthrough_name):
    """
    Creates a folder with the name of the game session if it doesn't exist.
    """
    if not os.path.exists(playthrough_name):
        os.mkdir(playthrough_name)

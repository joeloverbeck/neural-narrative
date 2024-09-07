from termcolor import colored

from src.abstracts.observer import Observer


class ConsoleDialogueObserver(Observer):
    def update(self, message: dict) -> None:
        if message["narration_text"]:
            print(colored(f"{message['narration_text']}", "light_blue") + colored(f"\n{message['name']}: ",
                                                                                  "red") + colored(
                f"{message['speech']}", "light_grey"))
        else:
            print(colored(f"\n{message['name']}: ", "red") + colored(f"{message['speech']}", "light_grey"))

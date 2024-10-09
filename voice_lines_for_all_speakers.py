from src.services.voices_services import VoicesServices


def main():
    available_speakers = [
        "mq101prewarsoldier02",
        "azura",
        "npcmskinnymalone",
        "npcmzeke",
        "npcfmrsable",
        "malecoward",
        "brainfrog",
        "npcmdutchman",
        "npcftraderrylee",
        "holotapeinstitutevoicemale02",
        "elanadarkfirevoice",
        "radiofatfahey",
        "announcer_elevatorvoice",
        "npcfcurie",
        "frea",
        "npcmvaulttecrep",
        "synthgen1male03",
        "femalevampire",
        "npcmdoccrocker",
        "sheogorath",
        "npcfroslynchambers",
        "npcmproctorquinlan",
        "ancano",
        "synthgen3male01",
    ]

    for available_speaker in available_speakers:
        file_path = VoicesServices.generate_voice_line(
            "test",
            "Stop right there! Before you proceed any further, think carefully about the choice you're about to make.",
            available_speaker,
        )
        print(f"Generated voiceline for '{file_path}'")


if __name__ == "__main__":
    main()

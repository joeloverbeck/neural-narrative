import inspect
import re
from enum import Enum
from typing import Dict, List


class VoiceGenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class VoiceAgeEnum(str, Enum):
    CHILDLIKE = "CHILDLIKE"
    TEENAGE = "TEENAGE"
    YOUNG_ADULT_ADULT = "YOUNG ADULT/ADULT"
    MIDDLE_AGED = "MIDDLE-AGED"
    ELDERLY = "ELDERLY"


class VoiceEmotionEnum(str, Enum):
    CALM = "CALM"
    HAPPY_JOYFUL = "HAPPY/JOYFUL"
    SAD_MELANCHOLIC = "SAD/MELANCHOLIC"
    ANGRY_AGGRESSIVE = "ANGRY/AGGRESSIVE"
    ANXIOUS_FRIGHTENED = "ANXIOUS/FRIGHTENED"
    CONFIDENT_DETERMINED = "CONFIDENT/DETERMINED"
    SERIOUS_FIRM = "SERIOUS/FIRM"
    HOPEFUL = "HOPEFUL"
    SURPRISED = "SURPRISED"
    PLAYFUL = "PLAYFUL"
    EXCITED = "EXCITED"


class VoiceTempoEnum(str, Enum):
    FAST = "FAST"
    SLOW = "SLOW"
    MODERATE = "MODERATE"


class VoiceVolumeEnum(str, Enum):
    WHISPERING = "WHISPERING"
    SOFT_SPOKEN_QUIET = "SOFT-SPOKEN/QUIET"
    NORMAL_VOLUME = "NORMAL VOLUME"
    LOUD = "LOUD"


class VoiceTextureEnum(str, Enum):
    GRAVELLY_RASPY = "GRAVELLY/RASPY"
    SMOOTH = "SMOOTH"
    NASAL = "NASAL"
    CRISP = "CRISP"
    MUFFLED = "MUFFLED"
    WHISPERY_AIRY = "WHISPERY/AIRY"
    METALLIC_MECHANICAL = "METALLIC/MECHANICAL"
    GUTTURAL = "GUTTURAL"


class VoiceToneEnum(str, Enum):
    WARM = "WARM"
    NEUTRAL = "NEUTRAL"
    COLD = "COLD"
    AUTHORITATIVE = "AUTHORITATIVE"


class VoiceStyleEnum(str, Enum):
    FORMAL = "FORMAL"
    CASUAL = "CASUAL"
    INTENSE_DRAMATIC = "INTENSE/DRAMATIC"
    MONOTONE = "MONOTONE"
    DRAWLING = "DRAWLING"
    FLIRTATIOUS = "FLIRTATIOUS"
    HUMOROUS_SARCASTIC = "HUMOROUS/SARCASTIC"
    MELODIC = "MELODIC"


class VoicePersonalityEnum(str, Enum):
    INNOCENT_NAIVE = "INNOCENT/NAIVE"
    YOUTHFUL = "YOUTHFUL"
    ENERGETIC = "ENERGETIC"
    PASSIONATE = "PASSIONATE"
    ADVENTUROUS_DRIVEN = "ADVENTUROUS/DRIVEN"
    OPTIMISTIC = "OPTIMISTIC"
    NOBLE = "NOBLE"
    SULTRY = "SULTRY"
    KIND = "KIND"
    CHARMING = "CHARMING/WITTY"
    WISE_PHILOSOPHICAL = "WISE/PHILOSOPHICAL"
    STOIC = "STOIC"
    ECCENTRIC = "ECCENTRIC"
    MYSTERIOUS = "MYSTERIOUS"
    SKEPTICAL = "SKEPTICAL"
    WORLD_WEARY = "WORLD-WEARY"
    CYNICAL_PESSIMISTIC = "CYNICAL/PESSIMISTIC"
    PARANOID = "PARANOID"
    CUNNING_DECEPTIVE = "CUNNING/DECEPTIVE"
    VILLAINOUS = "VILLAINOUS"


class VoiceSpecialEffectsEnum(str, Enum):
    NO_SPECIAL_EFFECTS = "NO SPECIAL EFFECTS"
    ROBOTIC_SYNTHESIZED = "ROBOTIC/SYNTHESIZED"
    ALIEN = "ALIEN"
    DEMON_LIKE = "DEMON-LIKE"
    MAGICAL = "MAGICAL"
    DISTORTED = "DISTORTED"
    GHOSTLY_ECHOED = "GHOSTLY/ECHOED"
    RETRO = "RETRO"


# Function to convert CamelCase to snake_case and remove 'Enum' suffix
def convert_enum_name(name: str) -> str:
    """
    Convert Enum class name from CamelCase to snake_case and remove 'Enum' suffix.

    Args:
        name (str): The Enum class name.

    Returns:
        str: The converted snake_case name without 'Enum'.
    """
    # Remove 'Enum' suffix if present
    if name.endswith("Enum"):
        name = name[:-4]

    # Insert underscore before capital letters that follow lowercase letters or numbers
    s1 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)

    # Convert the entire string to lowercase
    snake_case = s1.lower()

    return snake_case


# Get the current module
current_module = inspect.getmodule(inspect.currentframe())

# Collect all Enum subclasses in the current module
enum_classes = {
    name: cls
    for name, cls in current_module.__dict__.items()
    if inspect.isclass(cls) and issubclass(cls, Enum)
}

# Create the categories_tags dictionary with desired key formatting
voice_categories_tags: Dict[str, List[str]] = {
    convert_enum_name(name): [member.value for member in cls]
    for name, cls in enum_classes.items()
}

from collections import Counter

from src.base.constants import (
    VOICE_MODELS_FILE,
    VOICE_GENDERS,
    VOICE_AGES,
    VOICE_EMOTIONS,
    VOICE_TEMPOS,
    VOICE_VOLUMES,
    VOICE_TEXTURES,
    VOICE_TONES,
    VOICE_STYLES,
    VOICE_PERSONALITIES,
    VOICE_SPECIAL_EFFECTS,
)
from src.filesystem.filesystem_manager import FilesystemManager


def main():
    # Parse the JSON data
    voice_models = FilesystemManager().load_existing_or_new_json_file(VOICE_MODELS_FILE)

    # Initialize dictionaries to store used tags by category
    used_tags = {
        "genders": set(),
        "ages": set(),
        "emotions": set(),
        "tempos": set(),
        "volumes": set(),
        "textures": set(),
        "tones": set(),
        "styles": set(),
        "personalities": set(),
        "special_effects": set(),
    }

    # Initialize dictionaries to count tag usage
    tag_counts = {
        "genders": Counter(),
        "ages": Counter(),
        "emotions": Counter(),
        "tempos": Counter(),
        "volumes": Counter(),
        "textures": Counter(),
        "tones": Counter(),
        "styles": Counter(),
        "personalities": Counter(),
        "special_effects": Counter(),
    }

    # Mapping of attribute categories to their possible tags
    attribute_categories = {
        "genders": VOICE_GENDERS,
        "ages": VOICE_AGES,
        "emotions": VOICE_EMOTIONS,
        "tempos": VOICE_TEMPOS,
        "volumes": VOICE_VOLUMES,
        "textures": VOICE_TEXTURES,
        "tones": VOICE_TONES,
        "styles": VOICE_STYLES,
        "personalities": VOICE_PERSONALITIES,
        "special_effects": VOICE_SPECIAL_EFFECTS,
    }

    # === Performance Optimization: Reverse Lookup Dictionary ===

    # Create a reverse lookup dictionary mapping each attribute to its category
    attribute_to_category = {}
    for category, tags in attribute_categories.items():
        for tag in tags:
            attribute_to_category[tag] = category

    # Optimized function to determine the category of an attribute using reverse lookup
    def get_attribute_category(attribute):
        return attribute_to_category.get(attribute)

    # === End of Optimization ===

    # Iterate over voice models and collect used tags and count them
    for model, attributes in voice_models.items():
        for attribute in attributes:
            category = get_attribute_category(attribute)
            if category:
                used_tags[category].add(attribute)
                tag_counts[category][attribute] += 1

    # Find unused tags by comparing possible tags with used tags
    unused_tags = {
        category: set(tags) - used_tags[category]
        for category, tags in attribute_categories.items()
    }

    # Print unused tags by category
    print("=== Unused Voice Attributes ===")
    for category, unused in unused_tags.items():
        print(
            f"Unused {category.capitalize()}: {', '.join(sorted(unused)) if unused else 'None'}"
        )
    print()

    # === Validation Checks ===

    # Initialize a dictionary to store problems for each voice model
    problematic_models = {}

    for model, attributes in voice_models.items():
        # Initialize a dictionary to count tags per category for this model
        category_counts = {category: 0 for category in attribute_categories.keys()}
        # Initialize a dictionary to store tags per category
        tags_in_categories = {category: [] for category in attribute_categories.keys()}

        for attribute in attributes:
            category = get_attribute_category(attribute)
            if category:
                category_counts[category] += 1
                tags_in_categories[category].append(attribute)

        # Initialize a list to store problems for this model
        problems = []

        # Check for missing tags and multiple tags in a category
        for category, count in category_counts.items():
            if count == 0:
                problems.append(f"Missing tag from category '{category}'")
            elif count > 1:
                multiple_tags = ", ".join(tags_in_categories[category])
                problems.append(
                    f"Multiple tags in category '{category}': {multiple_tags}"
                )

        # If there are any problems, add them to the problematic_models dictionary
        if problems:
            problematic_models[model] = problems

    # Print problematic voice models
    if problematic_models:
        print("=== Voice Models with Attribute Issues ===")
        for model, issues in problematic_models.items():
            print(f"Voice Model: {model}")
            for issue in issues:
                print(f"  - {issue}")
            print()
    else:
        print("All voice models have exactly one tag per category.")

    # === Display Tag Usage Counts ===

    print("=== Tag Usage Counts by Category ===")
    for category, counter in tag_counts.items():
        print(f"\n{category.capitalize()}:")
        if counter:
            for tag, count in counter.most_common():
                print(f"  {tag}: {count}")
        else:
            print("  None")
    print()


if __name__ == "__main__":
    main()

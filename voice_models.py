from collections import Counter
from typing import Dict
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


def get_attribute_category(attribute, attribute_to_category: Dict[str, str]):
    return attribute_to_category.get(attribute)


def main():
    voice_models = FilesystemManager().load_existing_or_new_json_file(VOICE_MODELS_FILE)
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
    attribute_to_category = {}
    for category, tags in attribute_categories.items():
        for tag in tags:
            attribute_to_category[tag] = category
    for model, attributes in voice_models.items():
        for attribute in attributes:
            category = get_attribute_category(attribute, attribute_to_category)
            if category:
                used_tags[category].add(attribute)
                tag_counts[category][attribute] += 1
    unused_tags = {
        category: (set(tags) - used_tags[category])
        for category, tags in attribute_categories.items()
    }
    print("=== Unused Voice Attributes ===")
    for category, unused in unused_tags.items():
        print(
            f"Unused {category.capitalize()}: {', '.join(sorted(unused)) if unused else 'None'}"
        )
    print()
    problematic_models = {}
    for model, attributes in voice_models.items():
        category_counts = {category: (0) for category in attribute_categories.keys()}
        tags_in_categories = {category: [] for category in attribute_categories.keys()}
        for attribute in attributes:
            category = get_attribute_category(attribute, attribute_to_category)
            if category:
                category_counts[category] += 1
                tags_in_categories[category].append(attribute)
        problems = []
        for category, count in category_counts.items():
            if count == 0:
                problems.append(f"Missing tag from category '{category}'")
            elif count > 1:
                multiple_tags = ", ".join(tags_in_categories[category])
                problems.append(
                    f"Multiple tags in category '{category}': {multiple_tags}"
                )
        if problems:
            problematic_models[model] = problems
    if problematic_models:
        print("=== Voice Models with Attribute Issues ===")
        for model, issues in problematic_models.items():
            print(f"Voice Model: {model}")
            for issue in issues:
                print(f"  - {issue}")
            print()
    else:
        print("All voice models have exactly one tag per category.")
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

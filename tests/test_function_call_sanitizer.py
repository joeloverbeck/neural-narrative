import pytest

from src.prompting.function_call_sanitizer import FunctionCallSanitizer


@pytest.mark.parametrize(
    "response, expected_response",
    [
        (
            '    <function=test> {"arg": 1}  </function>  ',
            '<function=test>{"arg": 1}</function>',
        ),
        (
            """
    <function=test> {"arg": 1}
    </function>
    """,
            '<function=test>{"arg": 1}</function>',
        ),
        (
            '<function=test> {"arg": 1}}</function>',
            '<function=test>{"arg": 1}</function>',
        ),
    ],
)
def test_fix_tool_call(response, expected_response):
    provider = FunctionCallSanitizer(response)
    assert provider.sanitize() == expected_response


def test_sanitize_response():
    response = '<function=generate_region>{"name": "Nexoria", "description": "Nexoria is a region defined by its sprawling savannas and vast grasslands, interrupted by towering mountain ranges and deep, winding canyons. The climate is mostly warm and temperate, with mild winters and hot summers. The region is home to a diverse array of sentient species, including lion folk, elephant men, and giraffe people, among others. The cultural norms of Nexoria revolve around community and cooperation, with a strong emphasis on hospitality and mutual aid. Music and dance are integral to their way of life, with vibrant festivals held throughout the year to celebrate the changing seasons and the bounty of the land.The architecture of Nexoria is characterized by its use of natural materials, such as wood, stone, and thatch, with buildings designed to blend seamlessly into the surrounding landscape. Iconic structures include the Great Boma, a massive circular meeting hall where the region\'s leaders gather to discuss matters of importance, and the Tower of Winds, a soaring spire adorned with intricate carvings that whistles hauntingly in the breeze.Nexoria is governed by a council of elders, with representatives from each of the region\'s major clans."}</function>'
    expected_output = '<function=generate_region>{"name": "Nexoria", "description": "Nexoria is a region defined by its sprawling savannas and vast grasslands, interrupted by towering mountain ranges and deep, winding canyons. The climate is mostly warm and temperate, with mild winters and hot summers. The region is home to a diverse array of sentient species, including lion folk, elephant men, and giraffe people, among others. The cultural norms of Nexoria revolve around community and cooperation, with a strong emphasis on hospitality and mutual aid. Music and dance are integral to their way of life, with vibrant festivals held throughout the year to celebrate the changing seasons and the bounty of the land.\\nThe architecture of Nexoria is characterized by its use of natural materials, such as wood, stone, and thatch, with buildings designed to blend seamlessly into the surrounding landscape. Iconic structures include the Great Boma, a massive circular meeting hall where the region\'s leaders gather to discuss matters of importance, and the Tower of Winds, a soaring spire adorned with intricate carvings that whistles hauntingly in the breeze.\\nNexoria is governed by a council of elders, with representatives from each of the region\'s major clans."}</function>'
    parser = FunctionCallSanitizer(response)
    assert parser.sanitize() == expected_output


def test_no_fix_needed():
    response = '<function=generate_region>{"name": "Nexoria", "description": "This is correct."}</function>'
    expected_output = response
    parser = parser = FunctionCallSanitizer(response)
    assert parser.sanitize() == expected_output


import pytest
import re
import json


def test_function_call_sanitizer_handles_incorrect_closing_tag():
    function_call_input = '<function=generate_interesting_situations>{"interesting_situations": ["Audrey discovers that Alain\'s family emergency was a ruse and he is actually on a secret mission, putting her in a position to help him despite their complicated past.", "Alain returns home early and overhears the conversation between Audrey and Luc, leading to an emotional confrontation and difficult choices for all three characters.", "Luc, feeling threatened by Audrey\'s presence and her history with Alain, starts scheming to drive a wedge between them permanently.", "Audrey uncovers a hidden secret about Luc that could change everything, forcing her to decide whether to use this information to win back Alain or to do the right thing.", "An unexpected event forces Audrey, Alain, and Luc to work together, testing their loyalty and feelings for each other in a high-stakes situation."]}[/function]'
    sanitizer = FunctionCallSanitizer(function_call_input)
    sanitized_output = sanitizer.sanitize()
    function_call_pattern = re.compile("<function=(\\w+)>(\\{.*})</function>")
    match = function_call_pattern.match(sanitized_output)
    assert match is not None, "Sanitized output did not match expected pattern"
    function_name = match.group(1)
    json_data_str = match.group(2)
    assert function_name == "generate_interesting_situations"
    try:
        json_data = json.loads(json_data_str)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON data: {e}")
    assert "interesting_situations" in json_data
    assert isinstance(json_data["interesting_situations"], list)
    assert len(json_data["interesting_situations"]) > 0


def test_sanitize_replaces_self_closing_function_tag_at_end():
    input_function_call = '<function=generate_story_concepts>{"concepts": ["Story1", "Story2"]}<function/>'
    expected_output = '<function=generate_story_concepts>{"concepts": ["Story1", "Story2"]}</function>'
    sanitizer = FunctionCallSanitizer(input_function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_sanitize_does_not_replace_self_closing_function_tag_in_middle():
    input_function_call = '<function=generate_story_concepts><function/>{"concepts": ["Story1", "Story2"]}</function>'
    expected_output = input_function_call
    sanitizer = FunctionCallSanitizer(input_function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_sanitize_does_not_modify_correct_closing_tag():
    input_function_call = '<function=generate_story_concepts>{"concepts": ["Story1", "Story2"]}</function>'
    expected_output = input_function_call
    sanitizer = FunctionCallSanitizer(input_function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_sanitize_fixes_closing_tag_without_lt():
    input_function_call = (
        '<function=generate_story_concepts>{"concepts": ["Story1", "Story2"]}/function>'
    )
    expected_output = '<function=generate_story_concepts>{"concepts": ["Story1", "Story2"]}</function>'
    sanitizer = FunctionCallSanitizer(input_function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_sanitize_large_input_with_self_closing_tag_at_end():
    input_function_call = '<function=generate_story_concepts>{"concepts": ["In a world ravaged by a catastrophic virus, Mikel, a cunning survivor, discovers an ancient artifact in the Sepulchre of Forgotten Shadows that holds the key to humanity\'s survival. As he navigates the treacherous landscape of Iberia Mortis, Mikel must confront the infected, forge uneasy alliances, and decide between saving himself or sacrificing everything for the greater good. This thrilling post-apocalyptic adventure explores themes of redemption, sacrifice, and the indomitable human spirit.", "In the ruins of Donostia, Mikel stumbles upon a secret community hidden within the Sepulchre of Forgotten Shadows. As he delves deeper into this mysterious society, Mikel discovers an ancient ritual that could turn the tide against the infected. With time running out and the fate of humanity hanging in the balance, Mikel must decide whether to seize this dark power for himself or risk everything to protect the last remnants of civilization.", "When a devastating plague threatens to wipe out the few remaining survivors in Iberia Mortis, Mikel embarks on a perilous journey to find a cure. His search leads him to the Sepulchre of Forgotten Shadows, where he uncovers a long-forgotten prophecy about a chosen one who will rise from the ashes of humanity to defeat the infected. As Mikel struggles to accept his destiny, he must rally the people of Donostia and unite the warring factions of Iberia Mortis in a desperate final stand against the encroaching darkness.", "In a world where the lines between the living and the dead are blurred, Mikel discovers a hidden sanctuary within the Sepulchre of Forgotten Shadows. As he explores this haven from the horrors of Iberia Mortis, Mikel meets an enigmatic woman who shares his gift for manipulation and survival. Together, they form an unlikely alliance to uncover the truth behind the virus and investigate the dark secrets that haunt the Sepulchre\'s depths. This chilling post-apocalyptic thriller delves into themes of trust, betrayal, and the price of survival in a world gone mad.", "In the lawless ruins of Donostia, Mikel thrives as a charismatic leader of a band of survivors who have taken refuge in the Sepulchre of Forgotten Shadows. But when a mysterious stranger arrives bearing news of a cure for the virus, Mikel\'s leadership is challenged, and dark secrets from his past begin to surface. As tensions rise and the infected close in, Mikel must confront his own demons and decide whether to protect his newfound family or seize the opportunity to escape the horrors of Iberia Mortis once and for all. This gritty post-apocalyptic drama explores power dynamics, loyalty, and the struggle for identity in a world without rules."]}<function/>'
    expected_output = input_function_call.replace("<function/>", "</function>")
    sanitizer = FunctionCallSanitizer(input_function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output.endswith("</function>")
    assert "<function/>" not in sanitized_output


def test_incorrect_closing_tag_replaced():
    function_call = '<function=some_function>{"key": "value"}<function>'
    expected_output = '<function=some_function>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_correct_function_call_unchanged():
    function_call = '<function=some_function>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == function_call


def test_incorrect_closing_tag_square_brackets():
    function_call = '<function=some_function>{"key": "value"}[/function]'
    expected_output = '<function=some_function>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_extra_closing_braces_before_closing_tag():
    function_call = '<function=some_function>{"key": "value"}}}</function>'
    expected_output = '<function=some_function>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_single_quotes_replaced_with_double_quotes():
    function_call = "<function=some_function>{'key': 'value'}</function>"
    expected_output = '<function=some_function>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_self_closing_function_tag_at_end_replaced():
    function_call = '<function=some_function>{"key": "value"}<function />'
    expected_output = '<function=some_function>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_remove_extra_spaces_between_tags():
    function_call = '   <function=some_function>   {"key": "value"}   </function>   '
    expected_output = '<function=some_function>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_remove_line_breaks():
    function_call = '<function=some_function>\n{"key": "value"}\n</function>'
    expected_output = '<function=some_function>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_incorrect_closing_tag_with_extra_characters():
    function_call = '<function=some_function>{"key": "value"}some_extra_text</function>'
    expected_output = '<function=some_function>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_missing_opening_function_tag():
    function_call = '{"key": "value"}</function>'
    expected_output = '{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == function_call


def test_missing_closing_function_tag():
    function_call = '<function=some_function>{"key": "value"}'
    expected_output = '<function=some_function>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_fix_closing_function_tag_without_lt_or_slash():
    function_call = '<function=some_function>{"key": "value"}function>'
    expected_output = '<function=some_function>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_no_match_inside_function_name():
    function_call = '<function=some_function_name>{"key": "value"}<function>'
    expected_output = '<function=some_function_name>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_closing_tag_without_lt_or_slash():
    function_call = '<function=some_function>{"key": "value"}function>'
    expected_output = '<function=some_function>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_single_quoted_list_items():
    input_function_call = "<function=generate_story_concepts>{\"concepts\": [\"In a world where magic is a distant memory, Roran Wainwright stumbles upon an ancient artifact that grants him extraordinary powers. As he navigates the treacherous political landscape of Mythalia, Roran must confront the dark secrets of his past and decide whether to use his newfound abilities for personal gain or to protect the innocent. Along the way, he forges unlikely alliances and uncovers a sinister plot that threatens to plunge the world into chaos.\", 'When a series of mysterious disappearances rocks the coastal town of Siren\\'s Respite, Roran Wainwright finds himself at the center of a chilling mystery. As he delves deeper into the town\\'s dark underbelly, he discovers a hidden world of supernatural creatures and ancient evils lurking just beneath the surface. With the help of a motley crew of allies, including a battle-scarred dwarf and a disillusioned paladin, Roran must race against time to uncover the truth and save the town from an unspeakable fate.', \"In the aftermath of a devastating war, Roran Wainwright stumbles upon a secret society dedicated to the preservation of Mythalia's magical heritage. As he immerses himself in this hidden world, Roran discovers a talent for the arcane arts and sets out on a quest to restore magic to the land. But as he delves deeper into the mysteries of the past, Roran realizes that the price of power may be higher than he ever imagined, and that the key to saving the future may lie in the shadows of his own shattered heart.\", 'When a chance encounter with a mysterious stranger leaves Roran Wainwright in possession of a powerful artifact, he finds himself drawn into a centuries-old conflict between rival factions vying for control of Mythalia\\'s most precious resources. As he navigates the treacherous waters of this high-stakes game, Roran must decide where his loyalties lie and whether he is willing to sacrifice everything he holds dear in the pursuit of power and revenge.',\"In a world where the lines between magic and technology are blurring, Roran Wainwright stumbles upon a hidden workshop filled with wondrous inventions and arcane devices. As he delves deeper into the secrets of this forgotten place, Roran discovers a talent for tinkering and sets out to create something truly extraordinary. But as his creations begin to attract the attention of powerful forces, Roran must navigate a dangerous web of alliances and betrayals to protect his work and the people he loves. Along the way, he discovers that the true power of invention lies not in the devices themselves, but in the hearts and minds of those who create them.\"]}</function>"
    sanitizer = FunctionCallSanitizer(input_function_call)
    sanitized_output = sanitizer.sanitize()
    match = re.match("<function=([^\\s>]+)>(.*)</function>", sanitized_output)
    assert match is not None, "Sanitized output does not match expected format."
    json_content = match.group(2)
    function_name = match.group(1)
    data = json.loads(json_content)
    assert "concepts" in data, "'concepts' key not found in the data."
    assert isinstance(data["concepts"], list), "'concepts' is not a list."
    assert len(data["concepts"]) == 5, "Incorrect number of concepts."
    for concept in data["concepts"]:
        assert isinstance(concept, str), "Concept is not a string."
    assert function_name == "generate_story_concepts", "Function name is incorrect."


def test_mixed_quotes_and_escape_characters():
    input_function_call = "<function=echo_input>{'text': 'He said, \\'Hello, World!\\'', 'count': 1}</function>"
    sanitizer = FunctionCallSanitizer(input_function_call)
    sanitized_output = sanitizer.sanitize()
    match = re.match("<function=([^\\s>]+)>(.*)</function>", sanitized_output)
    assert match is not None, "Sanitized output does not match expected format."
    json_content = match.group(2)
    data = json.loads(json_content)
    assert data["text"] == "He said, 'Hello, World!'", "Incorrect 'text' value."
    assert data["count"] == 1, "Incorrect 'count' value."


def test_double_quoted_strings():
    input_function_call = (
        '<function=process>{"message": "All systems operational."}</function>'
    )
    sanitizer = FunctionCallSanitizer(input_function_call)
    sanitized_output = sanitizer.sanitize()
    match = re.match("<function=([^\\s>]+)>(.*)</function>", sanitized_output)
    assert match is not None, "Sanitized output does not match expected format."
    json_content = match.group(2)
    data = json.loads(json_content)
    assert data["message"] == "All systems operational.", "Incorrect 'message' value."


def test_empty_function_call():
    input_function_call = ""
    with pytest.raises(ValueError):
        FunctionCallSanitizer(input_function_call)


def test_sanitizer_removes_incorrect_function_closing_tag():
    function_call = '<function=generate_research_resolution>{"narrative": "In the dimly lit common room of the Haven of the Wayward, Roran Wainwright sat hunched over a worn, leather-bound tome, his brow furrowed in concentration. The flickering light of the Lumina Lilies cast an ethereal glow across the pages, illuminating the cryptic text that held the key to unlocking the secrets of this strange and wondrous place. Thogrim Ironfist, the battle-scarred dwarf, and Astera Lightbearer, the weary paladin, looked on with a mix of curiosity and concern. They had seen the toll that Roran\'s obsessive pursuit of knowledge had taken on him, the dark circles beneath his eyes and the gauntness of his features a testament to his single-minded determination. Despite their misgivings, they could not deny the importance of the task at hand. The secrets contained within the tome could hold the key to understanding the mysterious Lumina Lilies, the bioluminescent flora that had become a symbol of hope and resilience in this unforgiving world. As Roran pored over the ancient text, his mind raced with the possibilities. Could the Lumina Lilies hold the key to unlocking the secrets of the ancient ruins that dotted the landscape? Or perhaps they could provide a much-needed source of light and warmth in the darkest depths of the Whispering Grove? The answers lay within the pages before him, waiting to be deciphered. But as the hours turned to days and the days to weeks, the toll of Roran\'s relentless research began to show. His once-sparkling eyes grew dull and lifeless, his skin taking on a sickly pallor that spoke of countless sleepless nights. Thogrim and Astera watched with growing concern as their friend and companion seemed to waste away before their very eyes, consumed by his obsessive quest for knowledge.", "outcome": "After weeks of painstaking research, Roran finally unlocked the secrets of the Lumina Lilies. The ancient tome revealed that the bioluminescent flora was not only a source of light, but also a powerful healing agent, capable of curing even the most grievous of wounds. The discovery filled Roran with a sense of triumph and validation, his exhaustion giving way to a renewed sense of purpose. With this newfound knowledge, he knew that he could make a real difference in the lives of those around him.", "consequences": "The toll of Roran\'s relentless research was not limited to his physical well-being. His relationships with his companions suffered as well, as he became increasingly distant and withdrawn. Thogrim and Astera, once his closest allies, found themselves pushed away by his obsessive behavior. The once-close-knit group began to fracture, leaving Roran increasingly isolated in his pursuit of knowledge. In the end, the cost of his research was high, leaving him with a bitter-sweet victory that was tempered by the knowledge of all that he had sacrificed in its pursuit."}/function</function>'
    expected_output = function_call.replace("/function</function>", "</function>")
    sanitizer = FunctionCallSanitizer(function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_sanitizer_handles_multiple_incorrect_closing_tags():
    function_call = '<function=my_func>{"key": "value"}/function</function>'
    expected_output = '<function=my_func>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_sanitizer_adds_missing_closing_tag():
    function_call = '<function=my_func>{"key": "value"}'
    expected_output = '<function=my_func>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_sanitizer_does_not_alter_correct_function_call():
    function_call = '<function=my_func>{"key": "value"}</function>'
    expected_output = function_call
    sanitizer = FunctionCallSanitizer(function_call)
    sanitized_output = sanitizer.sanitize()
    assert sanitized_output == expected_output


def test_sanitize_replaces_start_tag_placeholder():
    input_str = '<{start_tag}=create_character_bio>{"key": "value"}</function>'
    expected_output = '<function=create_character_bio>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(input_str)
    assert sanitizer.sanitize() == expected_output


def test_sanitize_removes_end_tag_placeholder():
    input_str = '<function=create_character_bio>{"key": "value"}</end_tag></function>'
    expected_output = '<function=create_character_bio>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(input_str)
    assert sanitizer.sanitize() == expected_output


def test_sanitize_full_error_case():
    input_str = 'Here is the character bio you requested:<{start_tag}=create_character_bio>{"name": "Ezekiel Zephyr", "description": "An enigmatic...", "key": "value"}</end_tag></function>'
    expected_output = '<function=create_character_bio>{"name": "Ezekiel Zephyr", "description": "An enigmatic...", "key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(input_str)
    assert sanitizer.sanitize() == expected_output


def test_sanitize_handles_no_errors():
    input_str = '<function=create_character_bio>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(input_str)
    assert sanitizer.sanitize() == input_str


def test_sanitize_appends_missing_closing_tag():
    input_str = '<function=create_character_bio>{"key": "value"}'
    expected_output = '<function=create_character_bio>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(input_str)
    assert sanitizer.sanitize() == expected_output


def test_sanitize_handles_multiple_errors():
    input_str = (
        '<{start_tag}=create_character_bio>{"key": "value"}</end_tag></function>'
    )
    expected_output = '<function=create_character_bio>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(input_str)
    assert sanitizer.sanitize() == expected_output


def test_sanitize_with_extra_characters_after_json():
    input_str = (
        '<function=create_character_bio>{"key": "value"} some extra text</function>'
    )
    expected_output = '<function=create_character_bio>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(input_str)
    assert sanitizer.sanitize() == expected_output


def test_sanitize_with_incorrect_closing_tag():
    input_str = '<function=create_character_bio>{"key": "value"}[/function]'
    expected_output = '<function=create_character_bio>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(input_str)
    assert sanitizer.sanitize() == expected_output


def test_sanitize_with_missing_function_keyword_in_closing_tag():
    input_str = '<function=create_character_bio>{"key": "value"}<>'
    expected_output = '<function=create_character_bio>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(input_str)
    assert sanitizer.sanitize() == expected_output


def test_sanitize_with_self_closing_function_tag():
    input_str = '<function=create_character_bio>{"key": "value"}<function />'
    expected_output = '<function=create_character_bio>{"key": "value"}</function>'
    sanitizer = FunctionCallSanitizer(input_str)
    assert sanitizer.sanitize() == expected_output


def test_sanitize_missing_closing_function_tag():
    function_call = (
        "<function=generate_goals>{"
        '"goals": {"goal_1": "Test goal 1", "goal_2": "Test goal 2"}}'
    )

    sanitizer = FunctionCallSanitizer(function_call)
    sanitized_call = sanitizer.sanitize()

    expected_call = (
        "<function=generate_goals>{"
        '"goals": {"goal_1": "Test goal 1", "goal_2": "Test goal 2"}}'
        "</function>"
    )

    assert sanitized_call == expected_call

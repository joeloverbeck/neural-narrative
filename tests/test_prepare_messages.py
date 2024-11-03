# test_prepare_messages.py

import json

import pytest

from src.writers_room.utils import prepare_messages


@pytest.fixture
def basic_user_message():
    return {
        "role": "user",
        "content": "Hello, how are you?",
        "timestamp": "2024-04-27T12:34:56Z",
    }


@pytest.fixture
def basic_assistant_message():
    return {
        "role": "assistant",
        "content": "I'm fine, thank you!",
        "timestamp": "2024-04-27T12:35:00Z",
    }


@pytest.fixture
def tool_message():
    return {
        "role": "tool",
        "content": "Tool response",
        "timestamp": "2024-04-27T12:35:05Z",
    }


@pytest.fixture
def message_with_tool_calls():
    return {
        "role": "assistant",
        "content": "Here is the result.",
        "tool_calls": [
            {
                "function": {
                    "name": "calculate_sum",
                    "arguments": json.dumps({"a": 5, "b": 10}),
                }
            },
            {
                "function": {
                    "name": "fetch_data",
                    "arguments": json.dumps({"endpoint": "users"}),
                }
            },
        ],
        "timestamp": "2024-04-27T12:36:00Z",
    }


def test_prepare_messages_empty():
    messages = []
    expected = []
    assert prepare_messages(messages) == expected


def test_prepare_messages_single_user_message(basic_user_message):
    messages = [basic_user_message]
    expected = [
        {
            "message_text": "Hello, how are you?",
            "message_type": "user",
            "sender": "You",
            "tool_calls": "",
            "timestamp": "2024-04-27T12:34:56Z",
        }
    ]
    assert prepare_messages(messages) == expected


def test_prepare_messages_single_user_message_no_content():
    messages = [
        {
            "role": "user",
            "timestamp": "2024-04-27T12:34:56Z",
        }
    ]
    expected = [
        {
            "message_text": "No content",
            "message_type": "user",
            "sender": "You",
            "tool_calls": "",
            "timestamp": "2024-04-27T12:34:56Z",
        }
    ]
    assert prepare_messages(messages) == expected


def test_prepare_messages_single_assistant_message(basic_assistant_message):
    messages = [basic_assistant_message]
    expected = [
        {
            "message_text": "I'm fine, thank you!",
            "message_type": "assistant",
            "sender": "Assistant",
            "tool_calls": "",
            "timestamp": "2024-04-27T12:35:00Z",
        }
    ]
    assert prepare_messages(messages) == expected


def test_prepare_messages_single_assistant_message_no_content():
    messages = [
        {
            "role": "assistant",
            "timestamp": "2024-04-27T12:35:00Z",
        }
    ]
    expected = [
        {
            "message_text": "No content",
            "message_type": "assistant",
            "sender": "Assistant",
            "tool_calls": "",
            "timestamp": "2024-04-27T12:35:00Z",
        }
    ]
    assert prepare_messages(messages) == expected


def test_prepare_messages_single_tool_message(tool_message):
    messages = [tool_message]
    expected = []  # Tool messages are skipped
    assert prepare_messages(messages) == expected


def test_prepare_messages_mixed_messages(
    basic_user_message, basic_assistant_message, tool_message
):
    messages = [basic_user_message, basic_assistant_message, tool_message]
    expected = [
        {
            "message_text": "Hello, how are you?",
            "message_type": "user",
            "sender": "You",
            "tool_calls": "",
            "timestamp": "2024-04-27T12:34:56Z",
        },
        {
            "message_text": "I'm fine, thank you!",
            "message_type": "assistant",
            "sender": "Assistant",
            "tool_calls": "",
            "timestamp": "2024-04-27T12:35:00Z",
        },
    ]
    assert prepare_messages(messages) == expected


def test_prepare_messages_message_with_tool_calls(message_with_tool_calls):
    messages = [message_with_tool_calls]
    expected_tool_calls = (
        'calculate_sum ("a"= 5, "b"= 10)\nfetch_data ("endpoint"= "users")'
    )
    expected = [
        {
            "message_text": "Here is the result.",
            "message_type": "assistant",
            "sender": "Assistant",
            "tool_calls": expected_tool_calls,
            "timestamp": "2024-04-27T12:36:00Z",
        }
    ]
    assert prepare_messages(messages) == expected


def test_prepare_messages_message_with_empty_tool_calls(basic_assistant_message):
    messages = [basic_assistant_message]
    expected = [
        {
            "message_text": "I'm fine, thank you!",
            "message_type": "assistant",
            "sender": "Assistant",
            "tool_calls": "",
            "timestamp": "2024-04-27T12:35:00Z",
        }
    ]
    assert prepare_messages(messages) == expected


def test_prepare_messages_multiple_tool_calls(message_with_tool_calls):
    messages = [message_with_tool_calls, message_with_tool_calls]
    expected_tool_calls = (
        'calculate_sum ("a"= 5, "b"= 10)\nfetch_data ("endpoint"= "users")'
    )
    expected = [
        {
            "message_text": "Here is the result.",
            "message_type": "assistant",
            "sender": "Assistant",
            "tool_calls": expected_tool_calls,
            "timestamp": "2024-04-27T12:36:00Z",
        },
        {
            "message_text": "Here is the result.",
            "message_type": "assistant",
            "sender": "Assistant",
            "tool_calls": expected_tool_calls,
            "timestamp": "2024-04-27T12:36:00Z",
        },
    ]
    assert prepare_messages(messages) == expected


def test_prepare_messages_message_with_missing_role():
    messages = [
        {
            "content": "Missing role field.",
            "sender": "CustomSender",
            "timestamp": "2024-04-27T12:37:00Z",
        }
    ]
    expected = [
        {
            "message_text": "Missing role field.",
            "message_type": "CustomSender",
            "sender": "CustomSender",
            "tool_calls": "",
            "timestamp": "2024-04-27T12:37:00Z",
        }
    ]
    assert prepare_messages(messages) == expected


def test_prepare_messages_message_with_missing_sender():
    messages = [
        {
            "role": "assistant",
            "content": "Missing sender field.",
            "timestamp": "2024-04-27T12:38:00Z",
        }
    ]
    expected = [
        {
            "message_text": "Missing sender field.",
            "message_type": "assistant",
            "sender": "Assistant",
            "tool_calls": "",
            "timestamp": "2024-04-27T12:38:00Z",
        }
    ]
    assert prepare_messages(messages) == expected


def test_prepare_messages_message_with_missing_timestamp():
    messages = [
        {
            "role": "user",
            "content": "No timestamp here.",
        }
    ]
    expected = [
        {
            "message_text": "No timestamp here.",
            "message_type": "user",
            "sender": "You",
            "tool_calls": "",
            "timestamp": None,
        }
    ]
    assert prepare_messages(messages) == expected


def test_prepare_messages_tool_calls_with_invalid_json():
    messages = [
        {
            "role": "assistant",
            "content": "Invalid tool calls.",
            "tool_calls": [
                {
                    "function": {
                        "name": "invalid_function",
                        "arguments": "{invalid_json}",
                    }
                }
            ],
            "timestamp": "2024-04-27T12:39:00Z",
        }
    ]
    # Since json.loads will fail, prepare_tool_calls_text will raise an error.
    with pytest.raises(json.JSONDecodeError):
        prepare_messages(messages)


def test_prepare_messages_tool_calls_missing_function_field():
    messages = [
        {
            "role": "assistant",
            "content": "Tool call missing function.",
            "tool_calls": [
                {
                    # Missing 'function' key
                }
            ],
            "timestamp": "2024-04-27T12:40:00Z",
        }
    ]
    # Accessing tool_call["function"] will raise a KeyError
    with pytest.raises(KeyError):
        prepare_messages(messages)


def test_prepare_messages_tool_calls_missing_name():
    messages = [
        {
            "role": "assistant",
            "content": "Tool call missing name.",
            "tool_calls": [
                {
                    "function": {
                        # Missing 'name'
                        "arguments": json.dumps({"key": "value"}),
                    }
                }
            ],
            "timestamp": "2024-04-27T12:41:00Z",
        }
    ]
    # 'name' is missing; depending on implementation, it might set name to None or raise an error
    with pytest.raises(KeyError):
        prepare_messages(messages)


def test_prepare_messages_tool_calls_missing_arguments():
    messages = [
        {
            "role": "assistant",
            "content": "Tool call missing arguments.",
            "tool_calls": [
                {
                    "function": {
                        "name": "some_function",
                        # Missing 'arguments'
                    }
                }
            ],
            "timestamp": "2024-04-27T12:42:00Z",
        }
    ]
    with pytest.raises(KeyError):
        prepare_messages(messages)


def test_prepare_messages_non_dict_message():
    messages = [
        "This is not a dict",
    ]
    with pytest.raises(AttributeError):
        prepare_messages(messages)


def test_prepare_messages_tool_calls_with_extra_fields(message_with_tool_calls):
    # Add extra fields in tool_calls
    messages = [
        {
            **message_with_tool_calls,
            "tool_calls": [
                {
                    "function": {
                        "name": "calculate_sum",
                        "arguments": json.dumps({"a": 5, "b": 10}),
                        "extra": "field",
                    },
                    "extra_tool_info": "info",
                }
            ],
        }
    ]
    expected_tool_calls = 'calculate_sum ("a"= 5, "b"= 10)'
    expected = [
        {
            "message_text": "Here is the result.",
            "message_type": "assistant",
            "sender": "Assistant",
            "tool_calls": expected_tool_calls,
            "timestamp": "2024-04-27T12:36:00Z",
        }
    ]
    assert prepare_messages(messages) == expected


def test_prepare_messages_multiple_messages_various_cases():
    messages = [
        {
            "role": "user",
            "content": "User message 1",
            "timestamp": "2024-04-27T12:43:00Z",
        },
        {
            "role": "tool",
            "content": "Tool response",
            "timestamp": "2024-04-27T12:43:05Z",
        },
        {
            "role": "assistant",
            "content": "Assistant message with tool calls.",
            "tool_calls": [
                {
                    "function": {
                        "name": "do_something",
                        "arguments": json.dumps({"param": "value"}),
                    }
                }
            ],
            "timestamp": "2024-04-27T12:43:10Z",
        },
        {
            "content": "Message without role.",
            "sender": "CustomSender",
            "timestamp": "2024-04-27T12:43:15Z",
        },
        {
            "role": "assistant",
            "content": "",
            "timestamp": "2024-04-27T12:43:20Z",
        },
    ]
    expected_tool_calls = 'do_something ("param"= "value")'
    expected = [
        {
            "message_text": "User message 1",
            "message_type": "user",
            "sender": "You",
            "tool_calls": "",
            "timestamp": "2024-04-27T12:43:00Z",
        },
        {
            "message_text": "Assistant message with tool calls.",
            "message_type": "assistant",
            "sender": "Assistant",
            "tool_calls": expected_tool_calls,
            "timestamp": "2024-04-27T12:43:10Z",
        },
        {
            "message_text": "Message without role.",
            "message_type": "CustomSender",
            "sender": "CustomSender",
            "tool_calls": "",
            "timestamp": "2024-04-27T12:43:15Z",
        },
        {
            "message_text": "No content",
            "message_type": "assistant",
            "sender": "Assistant",
            "tool_calls": "",
            "timestamp": "2024-04-27T12:43:20Z",
        },
    ]
    assert prepare_messages(messages) == expected

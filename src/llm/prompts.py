import os
import re
import json
import random
import logging
from typing import List, Tuple

# Load prompts configuration
prompts_config_chat_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../data/prompts_config_chat.json'))

with open(prompts_config_chat_path, 'r') as file:
    prompts_config_chat = json.load(file)

with open(prompts_config_chat_path.replace('chat', 'dalle3'), 'r') as file:
    prompts_config_image = json.load(file)


def prepare_prompt_for_text_model(category: str = None) -> Tuple[List[str], str]:
    """
    Prepares and formats a prompt based on the given category and variable.

    Args:
        category (str, optional): The category of prompts to choose from. If None, a random category is selected.

    Returns:
        list: A list of formatted messages for the prompt.

    Raises:
        Exception: If an error occurs during the prompt preparation.
    """
    try:
        if not category:
            category = random.choice(list(prompts_config_chat.keys()))

        prompt_config = random.choice(prompts_config_chat[category])
        messages = prompt_config['messages']

        # if 'input_variables' in prompt_config:
        input_variables = {
            var_name: random.choice(values)
            for var_name, values in prompt_config['input_variables'].items()
        }

        for message in messages:
            message['content'] = message['content'].format(
                **input_variables)

        var = next(iter(input_variables.values()))

        return messages, var
    except Exception as e:
        logging.error(
            f"An unexpected error occurred during prompt preparation for chat: {e}")
        raise


def prepare_prompt_for_image_model(chosen_var: str = None) -> List[str]:
    """
    Prepares and formats a prompt based on the given category and variable.
    This prompt is to be used by a Image Generation model (such as Dalle 3).

    Args:
        chosen_var (str, optional): A specific variable to use in the prompt. If None, a random variable is chosen.

    Returns:
        list: A list of formatted messages for the prompt.

    Raises:
        Exception: If an error occurs during the prompt preparation.
    """
    try:
        prompt_config = random.choice(prompts_config_image)
        message = prompt_config['message']

        if 'input_variables' in prompt_config:
            input_variables = {
                var_name: (random.choice(values)
                           if not chosen_var else chosen_var)
                for var_name, values in prompt_config['input_variables'].items()
            }

            message = message.format(**input_variables)

        return message
    except Exception as e:
        logging.error(
            f"An unexpected error occurred during prompt preparation for image: {e}")
        raise


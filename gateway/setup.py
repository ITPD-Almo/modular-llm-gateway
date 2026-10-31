"""Guided setup for users who should never need to edit a credential file."""

import getpass
import warnings

from .credentials import Credentials, save_credentials
from .deepseek import ERROR_MESSAGES, ProviderError, available_models


def run_setup() -> None:
    print("Connect your DeepSeek account\nCreate a key at https://platform.deepseek.com if you do not have one.")
    print("Paste it below. Input is hidden. Ctrl+C cancels without changing your saved settings.")
    print("The connection check lists available models; it does not generate a paid chat response.")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", getpass.GetPassWarning)
            key = getpass.getpass("DeepSeek API key (hidden): ").strip()
    except getpass.GetPassWarning:
        raise ValueError("Hidden input is unavailable. Run llmgw setup in an interactive terminal.") from None
    candidate = Credentials(key)
    print("Checking your key with DeepSeek...")
    try:
        models = available_models(candidate)
    except ProviderError as error:
        raise ValueError(ERROR_MESSAGES.get(error.reason, ERROR_MESSAGES["unavailable"])) from None
    print("Connected. Choose a model:")
    for index, model in enumerate(models, 1):
        print(f"  {index}. {model}" + (" (default)" if index == 1 else ""))
    answer = input("Model number [1]: ").strip() or "1"
    if not answer.isdecimal() or not 1 <= int(answer) <= len(models):
        raise ValueError("Invalid model choice. Nothing was saved; run llmgw setup again.")
    selected = Credentials(key, models[int(answer) - 1])
    save_credentials(selected)
    print(f"Saved privately for your user. Model: {selected.model}")
    print("The key is stored in a permission-protected local file, not encrypted.")
    print("Ready: llmgw serve\nThen use llmgw chat in another terminal. Real chats use your DeepSeek balance.")
    print("Use llmgw logout to remove the saved key. Restart any running gateway after changing settings.")

import asyncio

import litellm
from litellm.integrations.custom_logger import CustomLogger
from litellm.llms.custom_llm import CustomLLM


class FakeProvider(CustomLLM):
    """Same behaviour as gateway.main.fake_provider: echo the last message."""

    def _reply(self, messages, model):
        prompt = messages[-1]["content"] if messages else ""
        return litellm.completion(model=model, messages=messages, mock_response=f"fake: {prompt}")

    def completion(self, model, messages, *args, **kwargs):
        return self._reply(messages, "gpt-3.5-turbo")

    async def acompletion(self, model, messages, *args, **kwargs):
        return self._reply(messages, "gpt-3.5-turbo")


fake_provider = FakeProvider()


def _record(data, name, stage, change):
    data.setdefault("metadata", {}).setdefault("plugin_changes", []).append(
        {"plugin": name, "stage": stage, "change": change}
    )


class MetadataHook(CustomLogger):
    async def async_pre_call_hook(self, user_api_key_dict, cache, data, call_type):
        data.setdefault("metadata", {})["gateway"] = "modular"
        _record(data, "metadata", "request", "added metadata.gateway=modular")
        return data

    async def async_post_call_success_hook(self, data, user_api_key_dict, response):
        _record(data, "metadata", "response", "recorded metadata transformation")
        return response


class UppercaseHook(CustomLogger):
    async def async_pre_call_hook(self, user_api_key_dict, cache, data, call_type):
        for m in data.get("messages", []):
            if isinstance(m.get("content"), str):
                m["content"] = m["content"].upper()
        _record(data, "uppercase", "request", "uppercased message content")
        return data

    async def async_post_call_success_hook(self, data, user_api_key_dict, response):
        _record(data, "uppercase", "response", "recorded uppercase transformation")
        return response


class TraceHook(CustomLogger):
    """Not a plugin: copies the recorded changes into the response so the caller sees them."""

    async def async_post_call_success_hook(self, data, user_api_key_dict, response):
        changes = data.get("metadata", {}).get("plugin_changes", [])
        response._hidden_params.setdefault("additional_headers", {})["x-plugin-trace"] = ",".join(
            c["plugin"] for c in changes if c["stage"] == "request"
        )
        setattr(response, "plugin_changes", changes)
        return response


class FailingHook(CustomLogger):
    async def async_pre_call_hook(self, user_api_key_dict, cache, data, call_type):
        raise RuntimeError("boom")


class HangingHook(CustomLogger):
    async def async_pre_call_hook(self, user_api_key_dict, cache, data, call_type):
        await asyncio.sleep(3600)
        return data


metadata = MetadataHook()
uppercase = UppercaseHook()
trace = TraceHook()
failing = FailingHook()
hanging = HangingHook()

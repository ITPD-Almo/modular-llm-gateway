# Plugins

The gateway loads plugins from the JSON file named by `GATEWAY_CONFIG` (default: `config/plugins.json`). Each entry is a Python import path ending in a class name. The class is instantiated once at startup.

Each plugin receives a request dictionary in `process_request(request)` and must return a request dictionary. The gateway calls plugins in the exact order listed in the configuration. The returned request is sent to the fake provider. The provider response dictionary is then passed through every plugin's `process_response(response)` in that same order. A plugin may add, remove, or transform fields, and should preserve fields it does not own.

The example metadata plugin adds `metadata.gateway` and a `plugin_trace` entry. The uppercase plugin changes each text message to uppercase and adds its own trace entry. The trace in the curl example makes ordering visible.

Configuration, import, and class-construction errors stop startup with a clear error. An exception while processing a request returns HTTP 500 with a `plugin failure` detail; the provider is not called after the failing stage.

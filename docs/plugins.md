# Plugins

The gateway loads plugins from the JSON file named by `GATEWAY_CONFIG` (default: `config/plugins.json`). Each entry is a Python import path ending in a class name. The class is instantiated once at startup.

Each plugin receives a request dictionary in `process_request(request)` and must return a request dictionary. The gateway calls plugins in the exact order listed in the configuration. The returned request is sent to the fake provider. The provider response dictionary is then passed through every plugin's `process_response(response)` in that same order. A plugin may add, remove, or transform fields, and should preserve fields it does not own.

The example metadata plugin adds `metadata.gateway` and a `plugin_trace` entry. The uppercase plugin changes each text message to uppercase and adds its own trace entry. The response also contains `plugin_changes`, with the plugin name, stage, and human-readable change for every transformation. The trace and change list in the curl example make ordering and effects visible.

Configuration, import, and class-construction errors stop startup with a clear error. An exception while processing a request returns HTTP 500 naming the failing plugin; the provider is not called after the failing stage. Provider errors are returned separately as HTTP 502.

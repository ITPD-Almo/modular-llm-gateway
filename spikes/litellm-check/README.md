# LiteLLM plugin workflow spike

Disposable. Not for `main`.

Rebuilds the v0.1.0 two-plugin workflow (metadata, then uppercase, fake echo provider) as LiteLLM Proxy 1.106.2 callbacks, to check whether an existing gateway supports the same workflow with acceptable effort ([ASM-02](../../docs/assumptions.md#asm-02)).

- `hooks.py`: the fake provider, the two plugins, a trace hook that copies `plugin_changes` into the response, and a failing and a hanging plugin.
- `config-*.yaml`: the default order, reversed, metadata only, with a failing plugin, and with a hanging plugin.
- `run.sh <config-name>`: starts the proxy, sends the setup guide's request twice, and stops it.
- `results.txt`: the run on 2026-10-22.

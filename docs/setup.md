# Setup and run

This recipe requires Python 3.12. From a clean clone:

```console
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# POSIX shells: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
Copy-Item .env.example .env  # PowerShell; use `cp .env.example .env` on POSIX
```

Start the gateway with the example configuration:

```console
python -m uvicorn gateway.main:app --reload
```

Send a request in another terminal:

```console
curl -X POST http://127.0.0.1:8000/v1/chat/completions -H "Content-Type: application/json" -d '{"model":"fake","messages":[{"role":"user","content":"hello"}]}'
```

The response contains `fake: HELLO`, `provider: fake`, and `plugin_trace: ["metadata", "uppercase"]`, showing both configured effects and their order. Run the tests with `python -m pytest`.

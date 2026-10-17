# Setup and run

This recipe requires Python 3.12. From a clean clone:

```sh
git clone --recurse-submodules https://github.com/ITPD-Almo/modular-llm-gateway.git
cd modular-llm-gateway
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
cp .env.example .env
```

On Windows PowerShell, use:

```powershell
git clone --recurse-submodules https://github.com/ITPD-Almo/modular-llm-gateway.git
Set-Location modular-llm-gateway
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
Copy-Item .env.example .env
```

Start the gateway with the example configuration:

```console
python -m uvicorn gateway.main:create_app --factory --env-file .env --reload
```

Send a request in another terminal:

```console
curl -X POST http://127.0.0.1:8000/v1/chat/completions -H "Content-Type: application/json" -d '{"model":"fake","messages":[{"role":"user","content":"hello"}]}'
```

The response contains `fake: HELLO`, `provider: fake`, and `plugin_trace: ["metadata", "uppercase"]`, showing both configured effects and their order. Run the tests with `python -m pytest`. Run the repository checks with `npx markdownlint-cli2 "**/*.md"` and `npx lychee "**/*.md"` (the same checks run in CI).

# v0.1.0 hanging-plugin check

Disposable. Not for `main`.

Measures how v0.1.0 behaves when a plugin hangs: one hung request, then 45 concurrent hung requests followed by `/health` and a healthy request.

- `hang_plugin.py`: a request hook that sleeps `HANG_SECONDS` (default 60) when the message is exactly `hang`.
- `hanging.json`: metadata, the hanging plugin, then uppercase.
- `run.sh <checkout>`: run against a checkout of `v0.1.0` (`6bd7eef`) that has `.venv` with `pip install -e ".[test]"`. It starts uvicorn on ports 8765 and 8766, uses curl limits of 10 seconds, counts server threads from `/proc`, and kills each server afterwards.
- `results.txt`: the run on 2026-10-25 (Linux, Python 3.12.3, FastAPI 0.162.0, Uvicorn 0.54.0).

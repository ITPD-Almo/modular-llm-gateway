"""Allow `python -m gateway` alongside the installed llmgw command."""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())

"""Private per-user provider profile, outside any project or plugin configuration."""

from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import stat
import tempfile


@dataclass(frozen=True)
class Credentials:
    api_key: str = field(repr=False)
    model: str = "deepseek-flash"

    def __post_init__(self) -> None:
        if not 8 <= len(self.api_key) <= 512 or not all(33 <= ord(c) <= 126 for c in self.api_key):
            raise ValueError("The API key must be nonempty ASCII text without spaces or newlines")
        if not self.model or len(self.model) > 128 or not all(c.isascii() and (c.isalnum() or c in "._-") for c in self.model):
            raise ValueError("Invalid model identifier")


def profile_directory() -> Path:
    base = Path(os.getenv("XDG_CONFIG_HOME", str(Path.home() / ".config"))).expanduser()
    if not base.is_absolute():
        raise ValueError("XDG_CONFIG_HOME must be an absolute path")
    return base / "llmgw"


def _check(path: Path, directory: bool = False) -> None:
    info = path.lstat()
    correct_type = stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)
    if not correct_type or info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077:
        raise ValueError("Provider profile must be owned by you with private permissions; run llmgw setup")


def load_credentials() -> Credentials | None:
    directory = profile_directory()
    if not directory.exists() and not directory.is_symlink():
        return None
    _check(directory, directory=True)
    path = directory / "provider.json"
    if not path.exists() and not path.is_symlink():
        return None
    _check(path)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, encoding="utf-8") as source:
        info = os.fstat(source.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
            raise ValueError("Unsafe provider profile permissions")
        try:
            data = json.loads(source.read(4096))
            return Credentials(api_key=data["api_key"], model=data["model"])
        except (ValueError, KeyError, TypeError):
            raise ValueError("Provider profile is invalid; run llmgw setup again") from None


def save_credentials(credentials: Credentials) -> None:
    directory = profile_directory()
    directory.mkdir(parents=True, mode=0o700, exist_ok=True)
    _check(directory, directory=True)
    path = directory / "provider.json"
    if path.exists() or path.is_symlink():
        _check(path)
    fd, temporary = tempfile.mkstemp(prefix=".provider-", dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as destination:
            json.dump({"provider": "deepseek", "model": credentials.model, "api_key": credentials.api_key}, destination)
            destination.write("\n")
            destination.flush()
            os.fsync(destination.fileno())
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def remove_credentials() -> bool:
    directory = profile_directory()
    if not directory.exists() and not directory.is_symlink():
        return False
    _check(directory, directory=True)
    path = directory / "provider.json"
    if not path.exists() and not path.is_symlink():
        return False
    _check(path)
    path.unlink()
    return True

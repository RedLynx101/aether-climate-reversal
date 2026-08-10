"""Security boundaries shared by AETHER publication tooling."""

from __future__ import annotations

import ctypes
import os
from pathlib import Path


def resolve_within(base: Path, candidate: str | Path, allowed_root: Path) -> Path:
    """Resolve a contributor-controlled path inside an explicit trusted root.

    Parent-directory segments are allowed only when the final path remains inside
    ``allowed_root``. Absolute and drive-qualified inputs are rejected before any
    filesystem access occurs.
    """

    candidate_path = Path(candidate)
    if candidate_path.is_absolute() or candidate_path.drive:
        raise ValueError(f"Absolute paths are not allowed: {candidate}")

    trusted_root = allowed_root.resolve()
    resolved = (base.resolve() / candidate_path).resolve()
    try:
        resolved.relative_to(trusted_root)
    except ValueError as exc:
        raise ValueError(f"Path escapes the approved root: {candidate}") from exc
    return resolved


def trusted_windows_powershell() -> Path:
    """Return the system PowerShell executable without ambient PATH lookup."""

    if os.name != "nt":
        raise OSError("The Word-to-PDF PowerShell fallback is available only on Windows.")

    buffer = ctypes.create_unicode_buffer(32_768)
    length = ctypes.windll.kernel32.GetSystemDirectoryW(buffer, len(buffer))
    if length == 0 or length >= len(buffer):
        raise OSError("Windows did not return a valid system directory.")

    executable = Path(buffer.value) / "WindowsPowerShell" / "v1.0" / "powershell.exe"
    if not executable.is_file():
        raise FileNotFoundError(f"Trusted PowerShell executable was not found: {executable}")
    return executable.resolve()

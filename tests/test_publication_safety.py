from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from publication_safety import resolve_within, trusted_windows_powershell


class ResolveWithinTests(unittest.TestCase):
    def test_accepts_a_parent_reference_that_stays_in_the_repository(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            paper = root / "manuscript" / "paper"
            figure = root / "analysis" / "figures" / "figure.png"
            paper.mkdir(parents=True)
            figure.parent.mkdir(parents=True)
            figure.write_bytes(b"png")

            resolved = resolve_within(
                paper,
                "../../analysis/figures/figure.png",
                root,
            )

            self.assertEqual(resolved, figure)

    def test_rejects_parent_traversal_outside_the_approved_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            figures = root / "analysis" / "figures"
            figures.mkdir(parents=True)

            with self.assertRaisesRegex(ValueError, "escapes the approved root"):
                resolve_within(figures, "../../../outside.png", figures)

    def test_rejects_absolute_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            root.mkdir(exist_ok=True)

            with self.assertRaisesRegex(ValueError, "Absolute paths are not allowed"):
                resolve_within(root, root / "private.png", root)


class TrustedPowerShellTests(unittest.TestCase):
    @unittest.skipUnless(os.name == "nt", "Windows-specific system API")
    def test_returns_the_system_executable_by_absolute_path(self) -> None:
        executable = trusted_windows_powershell()

        self.assertTrue(executable.is_absolute())
        self.assertEqual(executable.name.lower(), "powershell.exe")
        self.assertNotEqual(executable.parent, Path.cwd())


if __name__ == "__main__":
    unittest.main()

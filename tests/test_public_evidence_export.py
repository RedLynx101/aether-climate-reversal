from __future__ import annotations

import importlib.util
import io
import sys
import unittest
from pathlib import Path

from PIL import Image, PngImagePlugin


ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "scripts" / "export_public_evidence.py"


def load_exporter():
    spec = importlib.util.spec_from_file_location("aether_public_evidence_export", EXPORTER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {EXPORTER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def png_bytes(pixel: tuple[int, int, int, int], *, compress_level: int, comment: str) -> bytes:
    image = Image.new("RGBA", (2, 2), pixel)
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("comment", comment)
    output = io.BytesIO()
    image.save(output, format="PNG", pnginfo=metadata, compress_level=compress_level)
    return output.getvalue()


class PublicEvidenceExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.exporter = load_exporter()

    def test_png_metadata_and_compression_differences_are_pixel_equivalent(self) -> None:
        existing = png_bytes((12, 34, 56, 255), compress_level=0, comment="linux encoder")
        generated = png_bytes((12, 34, 56, 255), compress_level=9, comment="windows encoder")
        self.assertNotEqual(existing, generated)
        self.assertTrue(self.exporter.artifacts_match("analysis/figures/example.png", existing, generated))

    def test_changed_png_pixel_is_rejected_without_tolerance(self) -> None:
        existing = png_bytes((12, 34, 56, 255), compress_level=6, comment="same metadata")
        with Image.open(io.BytesIO(existing)) as changed:
            changed.putpixel((1, 1), (12, 34, 57, 255))
            output = io.BytesIO()
            changed.save(output, format="PNG")
            generated = output.getvalue()
        self.assertFalse(self.exporter.artifacts_match("analysis/figures/example.png", existing, generated))

    def test_malformed_png_is_rejected(self) -> None:
        valid = png_bytes((12, 34, 56, 255), compress_level=6, comment="valid")
        self.assertFalse(self.exporter.artifacts_match("analysis/figures/example.png", b"not a png", valid))
        self.assertFalse(self.exporter.artifacts_match("analysis/figures/example.png", valid, b"not a png"))

    def test_json_requires_exact_bytes(self) -> None:
        existing = b'{"case":"ordinary","value":1}\n'
        generated = b'{"case":"ordinary","value":2}\n'
        self.assertFalse(self.exporter.artifacts_match("website/app/evidence.generated.json", existing, generated))

    def test_json_allows_only_git_line_ending_normalization(self) -> None:
        lf = b'{\n  "value": 1\n}\n'
        crlf = lf.replace(b'\n', b'\r\n')
        self.assertTrue(self.exporter.artifacts_match("website/app/evidence.generated.json", crlf, lf))
        self.assertFalse(self.exporter.artifacts_match("website/app/evidence.generated.json", b'{"value":1}\n', lf))


if __name__ == "__main__":
    unittest.main()

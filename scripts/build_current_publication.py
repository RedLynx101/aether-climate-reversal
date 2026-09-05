"""Build the current, portable PDF publication from the canonical Markdown.

Run with ``uv run --group publication python scripts/build_current_publication.py``.
The --check mode validates checked-in PDFs against their source manifest without
rewriting artifacts. No Microsoft Word installation or network is required.
"""
from __future__ import annotations

import argparse
import hashlib
from html import escape
import json
from pathlib import Path
import re

from markdown_it import MarkdownIt
import matplotlib
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable, Image, KeepTogether, ListFlowable, ListItem, Paragraph,
    SimpleDocTemplate, Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.46"
PUBLICATION_DATE = "September 2026"
DEST = ROOT / "manuscript/submission"
WEB = ROOT / "website/public/papers"
MANIFEST = DEST / "current-publication.json"
DOCUMENTS = [
    ("manuscript/paper/aether_scientific_paper.md", "AETHER_v0.46_working_paper.pdf", "Working paper"),
    ("manuscript/paper/technical_supplement.md", "AETHER_v0.46_technical_supplement.pdf", "Technical supplement"),
]
INK = colors.HexColor("#153e32")
MUTED = colors.HexColor("#4a6259")
PAGE_WIDTH, PAGE_HEIGHT = letter
CONTENT_WIDTH = PAGE_WIDTH - 108
MD = MarkdownIt("commonmark").enable("table")


def sha(path: Path) -> str:
    content = path.read_bytes()
    if path.suffix.lower() in {".md", ".py"}:
        content = content.replace(b"\r\n", b"\n")
    return hashlib.sha256(content).hexdigest()


def register_fonts() -> None:
    folder = Path(matplotlib.get_data_path()) / "fonts/ttf"
    for family, base in [("Body", "DejaVuSerif"), ("Head", "DejaVuSans")]:
        variants = {"": "", "-Bold": "-Bold", "-Italic": "-Italic" if family == "Body" else "-Oblique", "-BoldItalic": "-BoldItalic" if family == "Body" else "-BoldOblique"}
        for name, suffix in variants.items():
            pdfmetrics.registerFont(TTFont(family + name, str(folder / (base + suffix + ".ttf"))))
        pdfmetrics.registerFontFamily(family, normal=family, bold=family+"-Bold", italic=family+"-Italic", boldItalic=family+"-BoldItalic")


def styles() -> dict[str, ParagraphStyle]:
    body = ParagraphStyle("body", fontName="Body", fontSize=10, leading=15,
                          textColor=INK, spaceAfter=9, allowWidows=0, allowOrphans=0,
                          splitLongWords=True)
    return {
        "body": body,
        "h1": ParagraphStyle("title", parent=body, fontName="Head-Bold", fontSize=24, leading=30, spaceBefore=8, spaceAfter=16, keepWithNext=True),
        "h2": ParagraphStyle("h2", parent=body, fontName="Head-Bold", fontSize=15, leading=20, spaceBefore=18, spaceAfter=9, keepWithNext=True),
        "h3": ParagraphStyle("h3", parent=body, fontName="Head-Bold", fontSize=11.5, leading=16, spaceBefore=12, spaceAfter=7, keepWithNext=True),
        "h4": ParagraphStyle("h4", parent=body, fontName="Head-Bold", fontSize=10, leading=14, spaceBefore=10, spaceAfter=6, keepWithNext=True),
        "cell": ParagraphStyle("cell", parent=body, fontName="Head", fontSize=8.2, leading=11.7, spaceAfter=0),
        "cellhead": ParagraphStyle("cellhead", parent=body, fontName="Head-Bold", fontSize=8.2, leading=11.7, spaceAfter=0),
        "caption": ParagraphStyle("caption", parent=body, fontName="Head", fontSize=8.2, leading=11.5, textColor=MUTED, spaceBefore=5, spaceAfter=13),
        "code": ParagraphStyle("code", parent=body, fontName="Head", fontSize=8, leading=12, backColor=colors.HexColor("#edf3ef"), borderPadding=8),
    }


def safe_url(value: str, parent: Path) -> str:
    if value.startswith(("https://", "http://", "mailto:")):
        return escape(value, quote=True)
    # Repository-relative document links stay useful in downloaded PDFs.
    if not value.startswith(("#", "/")) and ":" not in value:
        target = (parent / value).resolve()
        if target.is_relative_to(ROOT):
            return escape("https://github.com/RedLynx101/aether-climate-reversal/blob/main/" + target.relative_to(ROOT).as_posix(), quote=True)
    return ""


def inline(token, parent: Path) -> str:
    output = []
    link_stack = []
    for child in token.children or []:
        kind = child.type
        if kind in {"text", "code_inline"}:
            value = escape(child.content)
            output.append(f'<font name="Head">{value}</font>' if kind == "code_inline" else value)
        elif kind in {"softbreak", "hardbreak"}:
            output.append(" " if kind == "softbreak" else "<br/>")
        elif kind in {"strong_open", "strong_close", "em_open", "em_close"}:
            output.append({"strong_open":"<b>", "strong_close":"</b>", "em_open":"<i>", "em_close":"</i>"}[kind])
        elif kind == "link_open":
            url = safe_url(child.attrGet("href") or "", parent)
            link_stack.append(bool(url))
            if url:
                output.append(f'<a href="{url}" color="#226c58">')
        elif kind == "link_close":
            if link_stack.pop():
                output.append("</a>")
        elif kind == "image":
            output.append(escape(child.content))
        else:
            # HTML is not a publication escape hatch; retain readable text only.
            output.append(escape(child.content))
    return "".join(output)


def contained_image(source: str, parent: Path) -> Path:
    path = (parent / source).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        raise ValueError(f"Image is missing or outside the repository: {source}")
    return path


def make_story(source: Path, label: str) -> tuple[list, list[str]]:
    text = source.read_text(encoding="utf-8-sig")
    if re.search(r"\[@[a-zA-Z_]", text):
        raise ValueError("Readable current publication must not contain raw citation keys")
    ss = styles()
    tokens = MD.parse(text)
    story: list = []
    assets: list[str] = []
    index = 0
    list_depth = 0
    while index < len(tokens):
        token = tokens[index]
        if token.type == "heading_open":
            style = ss.get(token.tag, ss["h4"])
            story.append(Paragraph(inline(tokens[index+1], source.parent), style))
            index += 3
            if token.tag == "h1":
                story.extend([Paragraph(f"Noah Hicks | {label} v{VERSION} | {PUBLICATION_DATE}", ss["caption"]),
                              HRFlowable(width="100%", thickness=.7, color=INK), Spacer(1,12)])
            continue
        if token.type == "table_open":
            rows, row, cell, head = [], [], [], False
            index += 1
            while tokens[index].type != "table_close":
                item = tokens[index]
                if item.type == "thead_open": head = True
                elif item.type == "thead_close": head = False
                elif item.type == "tr_open": row = []
                elif item.type == "inline": row.append(Paragraph(inline(item, source.parent), ss["cellhead" if head else "cell"]))
                elif item.type == "tr_close": rows.append(row)
                index += 1
            if rows:
                columns = len(rows[0])
                if columns > 6:
                    raise ValueError("Current-paper tables must have at most six readable columns")
                widths = [CONTENT_WIDTH / columns] * columns
                table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT", splitByRow=1)
                table.setStyle(TableStyle([
                    ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#e4eee7")),
                    ("LINEBELOW",(0,0),(-1,0),.8,INK),
                    ("LINEBELOW",(0,1),(-1,-1),.25,colors.HexColor("#cbd7cd")),
                    ("VALIGN",(0,0),(-1,-1),"TOP"),
                    ("TOPPADDING",(0,0),(-1,-1),8),
                    ("BOTTOMPADDING",(0,0),(-1,-1),8),
                    ("LEFTPADDING",(0,0),(-1,-1),7),
                    ("RIGHTPADDING",(0,0),(-1,-1),7),
                ]))
                story.extend([table, Spacer(1,12)])
        elif token.type == "paragraph_open":
            content = tokens[index+1]
            images = [c for c in content.children or [] if c.type == "image"]
            if images:
                for image in images:
                    path = contained_image(image.attrGet("src") or "", source.parent)
                    assets.append(path.relative_to(ROOT).as_posix())
                    graphic = Image(str(path))
                    scale = min(CONTENT_WIDTH / graphic.imageWidth, 330 / graphic.imageHeight)
                    graphic.drawWidth = graphic.imageWidth * scale
                    graphic.drawHeight = graphic.imageHeight * scale
                    graphic.hAlign = "CENTER"
                    story.append(KeepTogether([graphic, Paragraph(escape(image.content), ss["caption"])]))
            else:
                prefix = "• " if list_depth else ""
                story.append(Paragraph(prefix + inline(content, source.parent), ss["body"]))
            index += 3
            continue
        elif token.type in {"bullet_list_open", "ordered_list_open"}:
            list_depth += 1
        elif token.type in {"bullet_list_close", "ordered_list_close"}:
            list_depth -= 1
        elif token.type in {"fence", "code_block"}:
            story.append(Paragraph(escape(token.content).replace("\n","<br/>"), ss["code"]))
        elif token.type == "hr":
            story.append(HRFlowable(width="100%", thickness=.4, color=MUTED))
        index += 1
    return story, assets


def page_furniture(canvas, document) -> None:
    canvas.saveState()
    canvas.setFont("Head", 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawString(54, PAGE_HEIGHT-32, f"AETHER | v{VERSION} | Conditional research")
    canvas.drawRightString(PAGE_WIDTH-54, 30, str(document.page))
    canvas.drawString(54, 30, "Noah Hicks | aetherclimate.com")
    canvas.restoreState()


def build() -> None:
    register_fonts()
    DEST.mkdir(parents=True, exist_ok=True)
    WEB.mkdir(parents=True, exist_ok=True)
    entries = []
    for relative, filename, label in DOCUMENTS:
        source, output = ROOT/relative, DEST/filename
        story, assets = make_story(source, label)
        document = SimpleDocTemplate(str(output), pagesize=letter,
            leftMargin=54, rightMargin=54, topMargin=52, bottomMargin=49,
            title=f"AETHER: {label} v{VERSION}", author="Noah Hicks",
            subject="Conditional carbon-infrastructure research; not externally peer reviewed",
            invariant=1, pageCompression=1)
        document.build(story, onFirstPage=page_furniture, onLaterPages=page_furniture)
        (WEB/filename).write_bytes(output.read_bytes())
        entries.append({"source":relative, "source_sha256":sha(source),
                        "pdf":output.relative_to(ROOT).as_posix(), "pdf_sha256":sha(output),
                        "web_pdf":(WEB/filename).relative_to(ROOT).as_posix(),
                        "pages":len(PdfReader(output).pages),
                        "assets":{p:sha(ROOT/p) for p in assets}})
        print(f"Built {filename}: {entries[-1]['pages']} pages")
    manifest = {"version":VERSION, "builder_sha256":sha(Path(__file__)), "documents":entries}
    MANIFEST.write_text(json.dumps(manifest, indent=2)+"\n", encoding="utf-8")
    check()


def check() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["version"] != VERSION or manifest["builder_sha256"] != sha(Path(__file__)):
        raise ValueError("Publication manifest is stale; rebuild")
    for entry in manifest["documents"]:
        for field, hashfield in [("source","source_sha256"),("pdf","pdf_sha256")]:
            if sha(ROOT/entry[field]) != entry[hashfield]:
                raise ValueError(f"Publication drift: {entry[field]}")
        if sha(ROOT/entry["web_pdf"]) != entry["pdf_sha256"]:
            raise ValueError("Website PDF differs from research PDF")
        for path, digest in entry["assets"].items():
            if sha(ROOT/path) != digest:
                raise ValueError(f"Figure drift: {path}")
        pages = PdfReader(ROOT/entry["pdf"]).pages
        if len(pages) != entry["pages"] or not pages:
            raise ValueError("PDF page count invalid")
        for number,page in enumerate(pages,1):
            text = page.extract_text()
            if len(text.strip()) < 80 or "[@" in text or "\ufffd" in text:
                raise ValueError(f"Invalid/blank/unresolved PDF content on page {number}")
    print("Current publication source, assets, PDFs, website copies and text checks passed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    check() if args.check else build()

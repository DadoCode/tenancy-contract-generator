#!/usr/bin/env python3
"""
generate_contract.py — Fill a tenancy agreement template (.docx) with
contract-specific data from a JSON file.

Usage:
    python generate_contract.py data.json output.docx
    python generate_contract.py data.json output.docx --template custom_template.docx

The template must use {{PLACEHOLDER_NAME}} style placeholders (double curly
braces). This script replaces every placeholder found in data.json and
raises an error listing any placeholders in the template that were not
supplied, so missing fields are caught before a contract goes out.
"""

import json
import re
import shutil
import sys
import zipfile
import argparse
from pathlib import Path


PLACEHOLDER_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


def find_placeholders(xml_text: str) -> set:
    return set(PLACEHOLDER_RE.findall(xml_text))


def xml_escape(value: str) -> str:
    """Escape a value for safe insertion into WordprocessingML text."""
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def fill_template(template_path: Path, data: dict, output_path: Path) -> None:
    tmp_dir = output_path.parent / f".{output_path.stem}_build"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True)

    with zipfile.ZipFile(template_path, "r") as z:
        z.extractall(tmp_dir)

    doc_xml_path = tmp_dir / "word" / "document.xml"
    xml_text = doc_xml_path.read_text(encoding="utf-8")

    template_placeholders = find_placeholders(xml_text)
    data_keys = set(data.keys())

    missing = template_placeholders - data_keys
    if missing:
        raise ValueError(
            "Missing values for placeholders found in the template: "
            + ", ".join(sorted(missing))
        )

    unused = data_keys - template_placeholders
    if unused:
        print(
            "Note: these keys in your data were not found in the template "
            f"and were ignored: {', '.join(sorted(unused))}",
            file=sys.stderr,
        )

    for key in template_placeholders:
        placeholder = "{{%s}}" % key
        value = xml_escape(data[key])
        xml_text = xml_text.replace(placeholder, value)

    doc_xml_path.write_text(xml_text, encoding="utf-8")

    if output_path.exists():
        output_path.unlink()

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in tmp_dir.rglob("*"):
            if file.is_file():
                zf.write(file, file.relative_to(tmp_dir))

    shutil.rmtree(tmp_dir)


def main():
    parser = argparse.ArgumentParser(description="Generate a filled tenancy agreement.")
    parser.add_argument("data_json", help="Path to a JSON file with placeholder values")
    parser.add_argument("output_docx", help="Path to write the generated .docx")
    parser.add_argument(
        "--template",
        default=str(Path(__file__).parent / "tenancy_template.docx"),
        help="Path to the {{PLACEHOLDER}} template (default: tenancy_template.docx next to this script)",
    )
    args = parser.parse_args()

    with open(args.data_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    fill_template(Path(args.template), data, Path(args.output_docx))
    print(f"Contract written to {args.output_docx}")


if __name__ == "__main__":
    main()

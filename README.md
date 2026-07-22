# Tenancy Contract Generator

Automated document generation for residential tenancy agreements. Turns a
structured data file into a fully populated, ready-to-sign Word contract —
no manual copy-pasting, no risk of leaving a placeholder unfilled in a legal
document.

## What it does

Real estate agencies drafting tenancy agreements typically fill contracts by
hand: copying the landlord's details, tenant's details, rent terms, and
deposit scheme information into a Word template for every single tenancy.
This tool automates that process end-to-end.

- Takes a JSON file of contract-specific data (landlord, tenant, property,
  rent, deposit, and deposit scheme details)
- Fills a Word (`.docx`) template automatically
- **Fails loudly, not silently** — if any required field is missing, the
  script stops and tells you exactly which one, so a contract can never go
  out with a blank field
- Outputs a clean, ready-to-send `.docx`

## How it works

1. The tenancy template uses `{{PLACEHOLDER_NAME}}` style tags throughout
   (e.g. `{{LANDLORD_FULL_NAME}}`, `{{MONTHLY_RENT}}`, `{{DEPOSIT_SCHEME_NAME}}`)
2. `generate_contract.py` reads a JSON file of values and replaces every
   placeholder found in the template
3. It cross-checks the template against the data file before writing
   anything, so missing information is caught before a document is
   generated — not after

## Usage

```bash
python3 generate_contract.py your_data.json output.docx
```

See `example_data.json` for the full list of fields the template expects.

## Example

`example_data.json` → `generate_contract.py` → a complete, formatted tenancy
agreement with every field populated — landlord and tenant details, rent and
deposit terms, deposit scheme information, and correctly ordered tenant
signatures for joint tenancies.

## Tech

Pure Python standard library (`zipfile`, `re`, `json`) — no external
dependencies. Works directly on the `.docx` XML, so all original formatting,
fonts, and styling are preserved exactly.

---

*Built to eliminate manual data entry errors in a real estate agency's
contract workflow.*

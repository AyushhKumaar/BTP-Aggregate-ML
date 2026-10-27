"""
PDF Parser - Extract tables, equations, and key text from reference papers.
Uses PyMuPDF (fitz) for text extraction.
"""

import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)


def extract_pdf_text(pdf_path: Path) -> str:
    """Extract all text from a PDF file."""
    doc = fitz.open(str(pdf_path))
    text = ""
    for page_num, page in enumerate(doc, 1):
        text += f"\n\n{'='*60}\nPAGE {page_num}\n{'='*60}\n"
        text += page.get_text()
    doc.close()
    return text


def extract_tables_and_equations(text: str) -> dict:
    """Extract key sections from paper text."""
    sections = {
        'tables': [],
        'equations': [],
        'key_values': [],
    }

    lines = text.split('\n')
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()

        # Detect table references
        if 'table' in line_lower and any(c.isdigit() for c in line):
            context = '\n'.join(lines[max(0, i-2):min(len(lines), i+10)])
            sections['tables'].append(context)

        # Detect equations
        if any(sym in line for sym in ['=', 'σ', 'Φ', 'exp', 'ln']):
            if len(line.strip()) > 5 and not line.strip().startswith('http'):
                sections['equations'].append(line.strip())

        # Detect key numerical values
        if any(unit in line_lower for unit in ['mpa', 'gpa', 'g/cm', 'kn', 'mm']):
            sections['key_values'].append(line.strip())

    return sections


def main():
    project_root = Path(__file__).parent.parent
    pdf_dir = project_root
    docs_dir = project_root / 'docs'
    docs_dir.mkdir(exist_ok=True)

    output_path = docs_dir / 'extracted_papers_notes.md'

    pdfs = list(pdf_dir.glob('*.pdf'))
    if not pdfs:
        print("No PDF files found in project root.")
        return

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Extracted Paper Notes\n\n")
        f.write("*Auto-generated from reference PDFs using PyMuPDF*\n\n")
        f.write("---\n\n")

        for pdf_path in pdfs:
            print(f"Processing: {pdf_path.name}")
            f.write(f"## {pdf_path.name}\n\n")

            try:
                text = extract_pdf_text(pdf_path)
                sections = extract_tables_and_equations(text)

                # Write summary
                f.write(f"**Total text length:** {len(text)} characters\n\n")

                # Tables
                f.write("### Tables Found\n\n")
                for i, table in enumerate(sections['tables'][:20], 1):
                    f.write(f"#### Table Reference {i}\n```\n{table}\n```\n\n")

                # Key equations
                f.write("### Key Equations\n\n")
                seen = set()
                for eq in sections['equations'][:30]:
                    if eq not in seen and len(eq) > 10:
                        f.write(f"- `{eq}`\n")
                        seen.add(eq)

                # Key values
                f.write("\n### Key Numerical Values\n\n")
                seen_vals = set()
                for val in sections['key_values'][:30]:
                    if val not in seen_vals and len(val) > 5:
                        f.write(f"- {val}\n")
                        seen_vals.add(val)

                f.write("\n---\n\n")

            except Exception as e:
                f.write(f"**Error processing:** {str(e)}\n\n")
                print(f"  Error: {e}")

    print(f"\nExtracted notes saved to: {output_path}")


if __name__ == '__main__':
    main()

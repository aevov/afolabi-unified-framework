import os
import markdown
import subprocess

# Define the order of documents for the encyclopedia
DOCS_ORDER = [
    "README.md",
    "AXIOMS.md",
    "WHITE_PAPER.md",
    "AFT_MATHEMATICAL_FOUNDATIONS.md",
    "AFT_UNIFICATION.md",
    "QFT_AUF_CORRESPONDENCE.md",
    "COSMOLOGICAL_IMPLICATIONS.md",
    "FRONTIER_IMPLICATIONS.md",
    "ANTIMATTER_APPLICATIONS.md",
    "papers/README.md",
    "papers/01_quantum_substrate_fallacy/paper.md",
    "papers/02_distributed_coherence/paper.md",
    "papers/03_beyond_dilution_refrigerator/paper.md",
    "papers/04_information_first_physics/paper.md",
    "papers/05_observer_hardware_equivalence/paper.md",
    "FALSIFIABILITY_CRITERIA.md",
    "PILOT_STUDY_PROTOCOL.md",
    "VALIDATION_REPORT.md",
    "ACADEMIC_CURRICULUM.md",
    "ACADEMIC_PROGRAM_PROPOSAL.md",
    "PITCH_DECK.md",
    "RESONANT_ECONOMY.md",
    "CIVILIZATIONAL_IMPLICATIONS.md",
    "AEVOV_LANG_SPEC.md",
    "API_SPECIFICATION.md",
    "FAQ_AND_CRITICS.md",
    "MASTER_INDEX.md"
]

# Base directory
BASE_DIR = "/home/baba/Desktop/complete quantum/cr8OS-complete-quantum/AUF"

CSS = """
body {
    font-family: 'Inter', Helvetica, Arial, sans-serif;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
    background: #ffffff;
}
h1, h2, h3, h4 {
    color: #004d40;
    margin-top: 2.5rem;
    page-break-after: avoid;
}
h1 {
    font-size: 3rem;
    border-bottom: 4px solid #004d40;
    padding-bottom: 1rem;
    text-align: center;
}
h2 {
    font-size: 2.2rem;
    border-bottom: 2px solid #e0f2f1;
    padding-bottom: 0.5rem;
}
.page-break {
    page-break-after: always;
}
code {
    background: #f4f4f4;
    padding: 0.2rem 0.4rem;
    border-radius: 4px;
    font-family: 'Courier New', Courier, monospace;
}
pre {
    background: #f4f4f4;
    padding: 1rem;
    border-radius: 8px;
    overflow-x: auto;
    border-left: 4px solid #004d40;
}
blockquote {
    border-left: 5px solid #00bfa5;
    margin: 1.5rem 0;
    padding: 1rem;
    background: #f9f9f9;
    font-style: italic;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 2rem 0;
}
th, td {
    padding: 12px;
    border: 1px solid #e0e0e0;
    text-align: left;
}
th {
    background: #004d40;
    color: white;
}
tr:nth-child(even) {
    background: #f5f5f5;
}
.title-page {
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    page-break-after: always;
}
.title-page h1 {
    font-size: 4rem;
    border: none;
}
.title-page .subtitle {
    font-size: 1.5rem;
    color: #666;
    margin-top: -1rem;
}
.footer {
    text-align: center;
    color: #999;
    font-size: 0.8rem;
    margin-top: 5rem;
}
"""

def generate_encyclopedia():
    full_markdown = ""
    
    # Title Page
    full_markdown += "<div class='title-page'>\n"
    full_markdown += "<h1>AUF ADMIN ENCYCLOPEDIA</h1>\n"
    full_markdown += "<div class='subtitle'>The Complete Knowledge Base of the Afolabi Unified Framework</div>\n"
    full_markdown += "<p><strong>CONFIDENTIAL | FOR ADMIN EYES ONLY</strong></p>\n"
    full_markdown += "<p>Version 2.0 | Compiled February 2026</p>\n"
    full_markdown += "</div>\n\n"

    collected_files = set()
    
    # 1. First, process files in the manually defined order
    for relative_path in DOCS_ORDER:
        file_path = os.path.join(BASE_DIR, relative_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                full_markdown += f"\n<div class='page-break'></div>\n\n"
                full_markdown += f"## {relative_path}\n"
                full_markdown += content
                collected_files.add(os.path.normpath(relative_path))
        else:
            print(f"Warning: File not found {file_path}")

    # 2. Then, recursively find all other .md files not yet collected
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                rel_path = os.path.normpath(os.path.relpath(full_path, BASE_DIR))
                
                if rel_path not in collected_files and file != "AUF_ENCYCLOPEDIA.md":
                    with open(full_path, 'r') as f:
                        content = f.read()
                        full_markdown += f"\n<div class='page-break'></div>\n\n"
                        full_markdown += f"## {rel_path}\n"
                        full_markdown += content
                        collected_files.add(rel_path)

    # Add footer
    full_markdown += "\n<div class='footer'>© 2026 cr8OS Foundation / Aevov Research | Private Documentation</div>\n"

    # Convert to HTML
    html_content = markdown.markdown(full_markdown, extensions=['extra', 'toc', 'tables', 'fenced_code'])
    
    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>AUF Admin Encyclopedia</title>
        <style>{CSS}</style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    html_file = os.path.join(BASE_DIR, "AUF_ENCYCLOPEDIA.html")
    with open(html_file, 'w') as f:
        f.write(full_html)
    
    print(f"Encyclopedia generated at {html_file}")
    
    # Convert to PDF using LibreOffice
    print("Converting to PDF...")
    try:
        subprocess.run([
            "libreoffice", "--headless", "--convert-to", "pdf", 
            "AUF_ENCYCLOPEDIA.html", "--outdir", BASE_DIR
        ], check=True)
        print("PDF conversion successful.")
    except Exception as e:
        print(f"PDF conversion failed: {e}")

if __name__ == "__main__":
    generate_encyclopedia()

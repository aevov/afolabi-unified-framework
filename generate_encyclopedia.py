import os
import markdown
import subprocess
import sys

# Base directory
BASE_DIR = "/home/baba/Desktop/complete quantum/cr8OS-complete-quantum/AUF"

# Define the order and filter for Public vs Admin
ADMIN_ONLY_DOCS = [
    "ACADEMIC_PROGRAM_PROPOSAL.md",
    "PITCH_DECK.md",
    "AFT_ACCESS_MODES.md",
    "API_SPECIFICATION.md",
    "HANDOVER_PROTOCOL.md",
    "CASE_STUDIES.md",
    "FMM_REPORT.md"
]

# Sensitive patterns that should never be in the public version
PUBLIC_BLACKLIST = ADMIN_ONLY_DOCS + [
    "generate_encyclopedia.py",
    "AUF_ENCYCLOPEDIA.pdf",
    "AUF_ADMIN_ENCYCLOPEDIA.pdf",
    "AUF_PUBLIC_ENCYCLOPEDIA.pdf"
]

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
    "RESONANT_ECONOMY.md",
    "CIVILIZATIONAL_IMPLICATIONS.md",
    "AEVOV_LANG_SPEC.md",
    "FAQ_AND_CRITICS.md",
    "MASTER_INDEX.md"
]

CSS = """
body {
    font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
}
h1, h2, h3, h4 { color: #004d40; margin-top: 2rem; }
.page-break { page-break-after: always; }
pre { background: #f4f4f4; padding: 1rem; border-left: 4px solid #004d40; }
blockquote { border-left: 5px solid #00bfa5; padding: 0.5rem 1rem; background: #f9f9f9; }
table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
th, td { padding: 10px; border: 1px solid #ddd; }
th { background: #004d40; color: white; }
.title-page { height: 90vh; display: flex; flex-direction: column; justify-content: center; text-align: center; }
"""

def generate_encyclopedia(is_public=False):
    mode_text = "PUBLIC EDITION" if is_public else "ADMIN ENCYCLOPEDIA"
    output_name = "AUF_PUBLIC_ENCYCLOPEDIA" if is_public else "AUF_ADMIN_ENCYCLOPEDIA"
    
    full_markdown = f"<div class='title-page'>\n<h1>AUF {mode_text}</h1>\n"
    full_markdown += "<p>Afolabi Unified Framework Knowledge Base</p>\n"
    if not is_public:
        full_markdown += "<p><strong>CONFIDENTIAL | TRADE SECRETS | FOR ADMIN EYES ONLY</strong></p>\n"
    full_markdown += f"<p>Version 2.0 | {mode_text}</p>\n</div>\n\n"

    collected_files = set()
    
    # 1. Process ordered docs
    for rel_path in DOCS_ORDER:
        if is_public and any(p in rel_path for p in PUBLIC_BLACKLIST):
            continue
            
        file_path = os.path.join(BASE_DIR, rel_path)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                full_markdown += f"\n<div class='page-break'></div>\n## {rel_path}\n"
                full_markdown += f.read()
                collected_files.add(os.path.normpath(rel_path))

    # 2. Process remaining
    if not is_public:
        for root, _, files in os.walk(BASE_DIR):
            for file in files:
                if file.endswith(".md"):
                    rel_path = os.path.normpath(os.path.relpath(os.path.join(root, file), BASE_DIR))
                    if rel_path not in collected_files and not any(p in rel_path for p in PUBLIC_BLACKLIST):
                        with open(os.path.join(root, file), 'r') as f:
                            full_markdown += f"\n<div class='page-break'></div>\n## {rel_path}\n"
                            full_markdown += f.read()
                            collected_files.add(rel_path)

    html_file = os.path.join(BASE_DIR, f"{output_name}.html")
    with open(html_file, 'w') as f:
        f.write(f"<html><head><style>{CSS}</style></head><body>{markdown.markdown(full_markdown, extensions=['extra', 'tables', 'fenced_code'])}</body></html>")
    
    subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", html_file, "--outdir", BASE_DIR])
    os.remove(html_file)
    print(f"Generated {output_name}.pdf")

if __name__ == "__main__":
    is_pub = "--public" in sys.argv
    generate_encyclopedia(is_public=is_pub)
    if not is_pub:
        # Also always generate public if we ran as admin
        generate_encyclopedia(is_public=True)

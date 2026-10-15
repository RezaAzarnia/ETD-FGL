#!/usr/bin/env python3
"""reproduce_all_artifacts.py

Master reproduction orchestrator for the ETD-FGL publication package.
Executes the consolidation, figure generation, table generation, and manuscript assembly pipelines.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    project_dir = Path(__file__).resolve().parent.parent.parent.parent
    scripts = [
        ("Consolidation and Provenance", "extract_and_consolidate_results.py"),
        ("Publication Figures (PDF/SVG/PNG)", "generate_publication_figures.py"),
        ("Publication Tables (CSV/TeX/MD)", "build_publication_tables.py"),
        ("Manuscript Content and Reviews", "build_manuscript_sections.py"),
        ("Package Validation Suite", "paper_artifacts/ETDFGL_Publication_Results_v1/validation/validate_publication_package.py"),
    ]

    print("================================================================================")
    print("ETD-FGL Master Publication Results Reproduction Pipeline")
    print("================================================================================")

    for desc, script_rel in scripts:
        script_path = project_dir / script_rel
        print(f"\n--> Running step: {desc} ({script_rel})...")
        cmd = [sys.executable, str(script_path)]
        res = subprocess.run(cmd, cwd=project_dir)
        if res.returncode != 0:
            print(f"FAILED step: {desc} with exit code {res.returncode}")
            sys.exit(res.returncode)
        print(f"PASSED step: {desc}")

    print("\n================================================================================")
    print("Reproduction Pipeline Finished Successfully! All Artifacts Verified.")
    print("================================================================================")


if __name__ == "__main__":
    main()

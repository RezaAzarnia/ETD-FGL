#!/usr/bin/env bash
# ETD-FGL Artifact Reproduction Script (Bash)
set -e
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
cd "$PROJECT_ROOT"
python extract_and_consolidate_results.py
python generate_publication_figures.py
python build_publication_tables.py
python build_manuscript_sections.py
python paper_artifacts/ETDFGL_Publication_Results_v1/validation/validate_publication_package.py
echo "ETD-FGL reproduction completed successfully."

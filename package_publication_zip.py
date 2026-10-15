#!/usr/bin/env python3
"""package_publication_zip.py

Creates the unified distribution ZIP archive:
paper_artifacts/ETDFGL_Publication_Results_v1.zip
"""

import shutil
from pathlib import Path


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    artifacts_dir = project_dir / "paper_artifacts"
    target_dir = artifacts_dir / "ETDFGL_Publication_Results_v1"
    zip_stem = artifacts_dir / "ETDFGL_Publication_Results_v1"

    print(f"Creating ZIP archive from: {target_dir}")
    shutil.make_archive(
        base_name=str(zip_stem),
        format="zip",
        root_dir=str(artifacts_dir),
        base_dir="ETDFGL_Publication_Results_v1",
    )
    zip_path = artifacts_dir / "ETDFGL_Publication_Results_v1.zip"
    print(f"Zip created successfully: {zip_path} (Size: {zip_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()

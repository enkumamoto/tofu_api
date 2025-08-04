from pathlib import Path


def list_modules(base_path: Path):
    return [
        f.name for f in base_path.iterdir()
        if f.is_dir()
        and (f / "Makefile").exists()
        and f.name != "terraform-api"
    ]

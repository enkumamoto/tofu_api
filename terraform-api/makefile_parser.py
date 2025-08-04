import re
from pathlib import Path


def parse_makefile(makefile_path: Path):
    if not makefile_path.exists():
        return []

    targets = []
    with makefile_path.open() as f:
        for line in f:
            match = re.match(r"^([a-zA-Z0-9_-]+):", line)
            if match:
                target = match.group(1)
                if not target.startswith("."):
                    targets.append(target)
    return targets

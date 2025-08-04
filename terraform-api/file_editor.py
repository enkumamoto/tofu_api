from pathlib import Path


def list_editable_files(module_path: str):
    valid_extensions = [".tf", ".tfvars", ".tfbackend"]
    return [str(f.name) for f in Path(module_path).iterdir() if f.suffix in valid_extensions]


def read_file_content(file_path: Path):
    return file_path.read_text()


def write_file_content(file_path: Path, content: str):
    file_path.write_text(content)

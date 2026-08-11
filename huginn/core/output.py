from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def prepare_output_dir(domain):
    target_dir = PROJECT_ROOT / "output" / domain
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir

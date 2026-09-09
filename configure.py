import os
import subprocess
import sys
from pathlib import Path

VENV_DIR = Path(".venv")


def venv_python() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def main() -> None:
    if not VENV_DIR.exists():
        run(sys.executable, "-m", "venv", str(VENV_DIR))

    python = str(venv_python())

    run(python, "-m", "pip", "install", "--upgrade", "pip")
    run(python, "-m", "pip", "install", "-e", ".[dev]")
    run(python, "-m", "pre_commit", "install")
    run(python, "-m", "pre_commit", "run", "--all-files")

    print("\nProjeto configurado com sucesso!")


if __name__ == "__main__":
    main()

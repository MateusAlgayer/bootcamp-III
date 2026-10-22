import os
import subprocess
import sys
from pathlib import Path

VENV_DIR = Path(".venv")


def venv_bin_dir() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts"
    return VENV_DIR / "bin"


def venv_python() -> Path:
    if os.name == "nt":
        return venv_bin_dir() / "python.exe"
    return venv_bin_dir() / "python"


def venv_env() -> dict[str, str]:
    """Ambiente com o .venv à frente do PATH (equivale a ativar o venv).

    Necessário porque hooks do pre-commit com ``language: system`` resolvem
    ``python`` pelo PATH; sem isso o interpretador global é usado.
    """
    env = os.environ.copy()
    bin_dir = str(venv_bin_dir().resolve())
    env["PATH"] = bin_dir + os.pathsep + env.get("PATH", "")
    env["VIRTUAL_ENV"] = str(VENV_DIR.resolve())
    return env


def run(*args: str, env: dict[str, str] | None = None) -> None:
    subprocess.run(args, check=True, env=env)


def main() -> None:
    if not VENV_DIR.exists():
        run(sys.executable, "-m", "venv", str(VENV_DIR))

    python = str(venv_python())
    env = venv_env()

    run(python, "-m", "pip", "install", "--upgrade", "pip", env=env)
    run(python, "-m", "pip", "install", "-e", ".[dev]", env=env)
    run(python, "-m", "pre_commit", "install", env=env)
    run(python, "-m", "pre_commit", "run", "--all-files", env=env)

    print("\nProjeto configurado com sucesso!")


if __name__ == "__main__":
    main()

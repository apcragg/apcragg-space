#!/usr/bin/python3

import argparse
import filecmp
import logging
import pathlib
import platform
import shlex
import shutil
import socket
import coloredlogs
import subprocess
from typing import Callable, Iterable, Sequence, Union

REPO_ROOT = pathlib.Path(__file__).resolve().parent
HOME_DIR = pathlib.Path.home()
VENV = "venv"
VENV_DIR = REPO_ROOT / VENV
VENV_PYTHON = VENV_DIR / "bin/python3"
VENV_PROMPT = "apcragg-space"
PY_REQUIREMENTS = REPO_ROOT / "requirements.txt"
PY_REQUIREMENTS_DEV = REPO_ROOT / "requirements-dev.txt"
BOOTSTRAP_ARTIFACTS_FOLDER = VENV_DIR / "bootstrap_artifacts"
REQUIREMENTS_FILES = ["requirements.txt", "requirements-dev.txt"]
BOOTSTRAP_ARTIFACT_FILE_NAMES = REQUIREMENTS_FILES + ["setup.py", "bootstrap.py"]

# Nice colors
coloredlogs.DEFAULT_FIELD_STYLES["levelname"] = {  # type: ignore
    "color": 8,
    "bold": True,
}
coloredlogs.install(fmt="%(asctime)s [%(filename)s] [%(levelname)s] %(message)s")


def log_banner(
    msg: str,
    logger: Callable = logging.info,
    line_ch: str = "-",
    split_lines: bool = True,
) -> None:
    """Pretty prints a message in banner"""
    logger(line_ch * 60)
    if split_lines:
        lines = msg.split("\n")
        for line in lines:
            logger(line)
    else:
        logger(msg)
    logger(line_ch * 60)


def printable_cmd(cmd: Sequence[Union[str, pathlib.Path]]) -> str:
    """Forms printable string from command."""
    return " ".join([shlex.quote(str(x)) for x in cmd])


def copy_definition_files() -> None:
    """Copy bootstrap dependency definition files to venv."""
    log_banner("Caching bootstrap state...")
    BOOTSTRAP_ARTIFACTS_FOLDER.mkdir(parents=True, exist_ok=True)
    for file_name in BOOTSTRAP_ARTIFACT_FILE_NAMES:
        source_file_path = REPO_ROOT / file_name
        destination_path = BOOTSTRAP_ARTIFACTS_FOLDER / file_name
        logging.info(f"Copying {source_file_path} to {destination_path}")
        shutil.copy(source_file_path, destination_path)


def compare_artifact_files(files: Iterable[str]) -> bool:
    """Compares files to stored artifacts and returns False if they aren't equal"""
    for file_name in files:
        source_file_path = REPO_ROOT / file_name
        if source_file_path.exists():
            artifact_path = BOOTSTRAP_ARTIFACTS_FOLDER / file_name
            logging.info(f"Checking {artifact_path} vs {source_file_path}")
            if not artifact_path.exists():
                logging.info(f"{artifact_path} did not exist")
                return False
            if not filecmp.cmp(source_file_path, artifact_path, shallow=False):
                logging.info(f"{artifact_path} did not match {source_file_path}")
                return False

    return True


def check_bootstrap_state() -> bool:
    """Checks if repo was bootstrapped with latest Python dependencies."""

    # Check venv exists
    if not VENV_DIR.exists():
        logging.info(f"Virtual environment not found at {VENV_DIR}")
        return False

    if not BOOTSTRAP_ARTIFACTS_FOLDER.exists():
        logging.info(
            "Bootstrap artifact folder not found " f"at {BOOTSTRAP_ARTIFACTS_FOLDER}"
        )
        return False

    # Check setup and requirements artifacts are correct
    return compare_artifact_files(BOOTSTRAP_ARTIFACT_FILE_NAMES)


def run_shell_command(
    cmd: Sequence[Union[str, pathlib.Path]],
    *,
    suppress_info: bool = False,
    raise_err: bool = False,
    cwd: Union[str, pathlib.Path] = REPO_ROOT,
    **spr_kwargs,
) -> int:
    """Runs shell command, returns returncode."""
    cmd = [str(c) for c in cmd]
    echo_msg = f"Sending command: {printable_cmd(cmd)}"
    logging.info(echo_msg)

    result = subprocess.run(cmd, check=raise_err, cwd=str(cwd), **spr_kwargs)
    rc = result.returncode
    if not suppress_info:
        if rc:
            logging.info(
                f"Received non-zero return code ({rc}) from " f"{printable_cmd(cmd)}"
            )
    return rc


def install_py_deps() -> None:
    log_banner("Installing Python Dependenceis")
    logging.info(f"Creating venv in '{VENV_DIR}'")
    init_venv_cmd = [
        "python3",
        "-m",
        VENV,
        VENV_DIR,
        # Change the display name of the venv in the terminal
        # NOTE: The venv is still located in a venv/ directory
        "--prompt",
        VENV_PROMPT,
    ]

    subprocess.run(init_venv_cmd)

    logging.info("Installing python development requirements")
    status = run_shell_command(
        [VENV_PYTHON, "-m", "pip", "install", "-r", PY_REQUIREMENTS_DEV], cwd=VENV_DIR
    )

    if status:
        log_banner(
            "Failed to install python development requirements", logging.critical, "@"
        )
        exit(status)

    logging.info("Installing python requirements")
    status = run_shell_command(
        [VENV_PYTHON, "-m", "pip", "install", "-r", PY_REQUIREMENTS], cwd=VENV_DIR
    )
    print(status)
    if status:
        log_banner("Failed to install python requirements", logging.critical, "@")
        exit(status)

        logging.info("Succesfully installed all python requirements")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        "--update_cache",
        action="store_true",
        help="Update Bootstrap Artifact cache without running install script",
    )
    parser.add_argument(
        "-f",
        "--full",
        "--force",
        action="store_true",
        help="Run full update script regardless of cache state",
    )
    args = parser.parse_args()
    update_cache = args.update_cache
    full = args.full

    logging.basicConfig(
        level=logging.info,
        format="[BOOTSTRAP] [{levelname}] {message}",
        style="{",
    )

    log_banner("Running bootstrap.py")

    os_name = platform.system()
    if not os_name:
        os_name = "unknown"
    hostname = socket.gethostname()
    logging.info(f"OS Platform: {os_name}")
    logging.info(f"Hostname: {hostname}")

    log_banner("Checking bootstrap cache state")
    if check_bootstrap_state() and not full:
        log_banner(
            """Bootstrap script has been run with the latest python dependencies.\n"""
            """                        You are up-to-date!"""
        )
        exit(0)

    if not update_cache:
        # Clear out old way of doing bootstrap
        if VENV_DIR.exists() and not VENV_DIR.is_symlink():
            log_banner("Clearing old venv")
            shutil.rmtree(VENV_DIR)

        install_py_deps()
    else:
        log_banner("Updating bootstrap artifact acache without running install script")

    # Update bootstrap cache
    copy_definition_files()
    assert check_bootstrap_state(), "Error caching bootstrap state"

    log_banner("Done!")
